"""Run the DerivBaseRu derivation pipeline over a Wiktionary dictionary.

Pipeline (see docs/derivation_schema.md):
  1. read the dictionary (parsed ru.wiktionary JSONL) -> words grouped by POS;
  2. for each rule (filtered by target POS pos_a and by complexity:
     simple / complex / compound);
  3. for each source word whose POS equals the rule pos_b
     (multi-word entries containing spaces are skipped):
       - simple/complex rules are applied to the word itself;
       - compound rules are applied for every candidate modifier word of the
         rule modifier POS (--modifier-limit bounds the candidates).
Results are written as one JSONL record per derivation edge (schema §3),
gzipped, with a sidecar meta.json header.

Usage:
  python scripts/run_pipeline.py --pos-a num
  python scripts/run_pipeline.py --pos-a num --complexities simple,complex
  python scripts/run_pipeline.py --pos-a adv --complexities compound
"""
from __future__ import annotations

import argparse
import gzip
import re
import json
import os
import sys
import time
from collections import OrderedDict
from itertools import product

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from derivbase_ru.cache import ResultCache
from derivbase_ru.derivation import Derivation, TagGuesserWrapper
from derivbase_ru.rule import CompoundRule

SCHEMA_VERSION = 1
COMPLEXITIES = ("simple", "complex", "compound")

# Temporarily omit the per-edge flags object from the output.
# Set back to True to restore it.
EMIT_FLAGS = False

STRESS = "\u0301\u00b4"

# Wiktionary POS template tags -> engine POS tags (Derivation.pos_all).
POS_MAP = {
    "сущ": "noun",
    "прил": "adj",
    "прич": "adj",
    "гл": "verb",
    # деепричастия (деепр) — не инфинитив, в корзину глаголов не берём
    "нар": "adv",
    "числ": "num",
}

# Lexemes tagged with another POS in Wiktionary but belonging to a
# derivation series; added to the bucket explicitly.
EXTRA_WORDS = {
    "num": ("один",),
}

# rule.info -> schema kind
KIND_MAP = {
    "SFX": "sfx",
    "PFX": "pfx",
    "PFX_SFX": "pfx_sfx",
    "CONFIX": "pfx_sfx",
    "POSTFIX": "postfix",
    "INTERFIX": "interfix",
    "CONV": "conversion",
    "COMPOUND": "compound",
}


def has_stress(text: str) -> bool:
    return any(ch in text for ch in STRESS)


POS_TOKENS = {"noun", "adj", "verb", "adv", "num", "part", "tgr", "*"}


def fixed_affix(name: str):
    """(affix, kind) для правила с фиксированным модификатором (pos_m="*").
    Префикс берётся из имени правила и НЕ становится узлом графа.
    rule1028(в + [пол] + noun + GEN -> adv) -> ("впол", "pfx")."""
    match = re.search(r"\(([^)]*)\)", name or "")
    if not match:
        return None, None
    body = match.group(1).split("->")[0]
    before, after, seen_head = [], [], False
    for part in [x.strip() for x in body.split("+")]:
        if part.startswith("[") and part.endswith("]"):
            (before if not seen_head else after).append(part[1:-1])
            continue
        if part in POS_TOKENS:
            seen_head = True
            continue
        if part:
            (before if not seen_head else after).append(part)
    if before:
        return "".join(before), "pfx"
    if after:
        return "".join(after), "sfx"
    return None, None


def fixed_modifiers(name: str):
    """Модификатор-префикс из имени правила: rule1026([полу] + adv -> adv) -> ['полу'].
    Варианты через слэш перечисляются: [мимо/само] -> ['мимо', 'само']."""
    match = re.search(r"\[([^\]]+)\]", name or "")
    if not match:
        return []
    return [part.strip() for part in match.group(1).split("/") if part.strip()]


def single_word(word: str) -> bool:
    return bool(word) and not any(c.isspace() for c in word)


def text_opener(path: str):
    if path.endswith(".gz"):
        return gzip.open(path, "rt", encoding="utf-8")
    return open(path, encoding="utf-8")


def add_extra_words(paths, words_by_pos, excluded=frozenset()):
    """Chain derivations: add (word, pos) pairs from other datasets as
    extra source words. They are NOT added to `known`, so anything derived
    from them stays potential unless the dictionary attests it."""
    added = 0
    for path in paths:
        for line in text_opener(path):
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except ValueError:
                continue
            word = rec.get("word")
            pos = rec.get("pos")
            if not word or pos not in words_by_pos:
                continue
            if word in excluded:
                continue
            if word in words_by_pos[pos]:
                continue
            words_by_pos[pos][word] = {
                "accented": rec.get("accented"),
                "inflect_type": rec.get("inflect_type"),
            }
            added += 1
    return added


def apply_compound_rule(rule, head: str, modifier: str, use_rare: bool):
    """Собирает compound-слово, применяя цепочки подправил к каждой части.

    Вызывается напрямую: Derivation.derive() не пробрасывает words_m/poss_m, а
    CompoundRule.apply_with_tags дублирует kwargs — из-за этого не работали
    rare-таблицы головы (rule986 у rule1027: мелькать -> мельком).
    """
    chains = list(getattr(rule, "simple_rules", []) or [])
    parts = []
    for index, word in enumerate([head, modifier]):
        chain = chains[index] if index < len(chains) else []
        current = {word}
        for subrule in chain:
            nxt = set()
            for w in current:
                nxt |= subrule.apply(w, use_rare=use_rare)
            current = nxt
        parts.append(current)
    order = getattr(rule, "order", None) or list(range(len(parts)))
    ordered = [parts[i] for i in order if i < len(parts)]
    separator = getattr(rule, "separator", "") or ""
    results = {separator.join(combo) for combo in product(*ordered)}
    for subrule in getattr(rule, "after_merge_rules", []) or []:
        nxt = set()
        for w in results:
            nxt |= subrule.apply(w, use_rare=use_rare)
        results = nxt
    return results


def read_dictionary(path: str):
    """Return (words_by_pos, known, n_pages) from a parsed Wiktionary JSONL(.gz).

    words_by_pos: {pos: {word: {"accented": str|None, "inflect_type": str|None}}}
    known:        set of (word, pos) attested in the dictionary
    """
    opener = gzip.open if path.endswith(".gz") else open
    words_by_pos = {pos: {} for pos in ("noun", "adj", "verb", "adv", "num")}
    known = set()
    n = 0
    with opener(path, "rt", encoding="utf-8") as fh:
        for line in fh:
            n += 1
            try:
                rec = json.loads(line)
            except ValueError:
                continue
            word = rec.get("title")
            if not word:
                continue
            for entry in rec.get("entries") or []:
                pos = POS_MAP.get(entry.get("pos"))
                if not pos:
                    continue
                known.add((word, pos))
                bucket = words_by_pos[pos]
                if word in bucket:
                    continue
                inflect = entry.get("inflection") or {}
                accented = None
                for form in inflect.get("positional") or []:
                    if form and has_stress(form):
                        accented = form
                        break
                bucket[word] = {"accented": accented, "inflect_type": None}
    for pos, extra in EXTRA_WORDS.items():
        for word in extra:
            known.add((word, pos))
            words_by_pos[pos].setdefault(
                word, {"accented": None, "inflect_type": None})
    return words_by_pos, known, n


def rule_kind(info: str) -> str:
    for info_key, kind in KIND_MAP.items():
        if info_key in (info or "").upper():
            return kind
    return (info or "").lower() or "sfx"


def parent(word: str, pos: str, role: str = "head", slot: int = 0) -> OrderedDict:
    return OrderedDict([
        ("id", "%s|%s" % (word, pos)),
        ("word", word),
        ("pos", pos),
        ("role", role),
        ("slot", slot),
    ])


def build_record(word_a, pos_a, parents, rule, meta_a, known, rare,
                 include_flags=True, kind=None, affix=None):
    entry_a = meta_a or {}
    is_real = (word_a, pos_a) in known
    rec = OrderedDict([
        ("schema", SCHEMA_VERSION),
        ("id", "%s|%s" % (word_a, pos_a)),
        ("word", word_a),
        ("pos", pos_a),
        ("lang", "rus"),
        ("accented", entry_a.get("accented") if is_real else None),
        ("hom_index", 0),
        ("rule", rule.name),
        ("kind", kind or rule_kind(rule.info)),
        ("parents", parents),
        ("inflect_type", entry_a.get("inflect_type")),
    ])
    if include_flags:
        rec["flags"] = OrderedDict([
            ("real", is_real),
            ("rare", bool(rare)),
            ("reconstructed", False),
            ("potential", not is_real),
        ])
    if affix:
        rec["affix"] = affix
    rec["source"] = "derivbase"
    return rec


def select_rules(der, wanted, complexities, force_complex):
    """Pick rules for the target POS and complexities, merging duplicate ids."""
    by_name = OrderedDict()
    skipped_complex = []
    for complexity in COMPLEXITIES:
        if complexity not in complexities:
            continue
        for r in der.loaded_rules[complexity]:
            if r.pos_a not in wanted:
                continue
            if getattr(r, "only_complex", False) and not force_complex:
                if r.name not in skipped_complex:
                    skipped_complex.append(r.name)
                continue
            base = by_name.get(r.name)
            if base is None:
                by_name[r.name] = r
                continue
            base.subrules = list(base.subrules) + list(r.subrules)
            for s, i in r.rare:
                base.rare_straight[s].add(i)
                base.rare_inversed[i].add(s)
    return list(by_name.values()), skipped_complex


def run(args) -> dict:
    t0 = time.time()
    print("reading dictionary: %s" % args.dict, flush=True)
    words_by_pos, known, n_pages = read_dictionary(args.dict)
    print("pages=%d words: %s" % (
        n_pages,
        ", ".join("%s=%d" % (p, len(w)) for p, w in words_by_pos.items()),
    ), flush=True)

    excluded = set()
    if args.exclude_words:
        excluded |= {w.strip() for w in args.exclude_words.split(",") if w.strip()}
    ex_path = args.exclude_file
    if ex_path is None:
        default_path = "data/pseudo_lemmas.txt"
        ex_path = default_path if os.path.exists(default_path) else ""
    if ex_path and os.path.exists(ex_path):
        with open(ex_path, encoding="utf-8") as fh:
            for line in fh:
                line = line.split("#", 1)[0].strip()
                if line:
                    excluded.add(line)
    if excluded:
        dropped = 0
        for pos_ in words_by_pos:
            for w in list(words_by_pos[pos_]):
                if w in excluded:
                    del words_by_pos[pos_][w]
                    dropped += 1
        print("excluded pseudo-lemmas: %d words dropped from sources" % dropped,
              flush=True)

    if args.extra_dataset:
        extra_paths = [s.strip() for s in args.extra_dataset.split(",") if s.strip()]
        n_extra = add_extra_words(extra_paths, words_by_pos, excluded)
        print("extra source words: %d (from %s)" % (n_extra, ", ".join(extra_paths)),
              flush=True)

    der = Derivation(
        lang=args.lang,
        guesser=TagGuesserWrapper(lang="rus") if args.guesser else None,
        cache=ResultCache(args.cache) if args.cache else None,
    )
    wanted = set(a.strip() for a in args.pos_a.split(",") if a.strip())
    complexities = set(a.strip() for a in args.complexities.split(",") if a.strip())
    rules, skipped_complex = select_rules(der, wanted, complexities, args.force_complex)
    if args.include_info:
        tokens = tuple(x.strip().upper() for x in args.include_info.split(",") if x.strip())
        rules = [r for r in rules
                 if any(t in (getattr(r, "info", "") or "").upper() for t in tokens)]
        print("include-info %s: правил %d" % (",".join(tokens), len(rules)), flush=True)
    if args.include_rules:
        good = tuple(x.strip() for x in args.include_rules.split(",") if x.strip())
        rules = [r for r in rules if r.name.startswith(good)]
        print("include-rules: правил %d" % len(rules), flush=True)
    if args.exclude_info:
        tokens = tuple(x.strip().upper() for x in args.exclude_info.split(",") if x.strip())
        rules = [r for r in rules
                 if not any(t in (getattr(r, "info", "") or "").upper() for t in tokens)]
        print("exclude-info %s: правил %d" % (",".join(tokens), len(rules)), flush=True)
    if args.exclude_rules:
        bad = tuple(x.strip() for x in args.exclude_rules.split(",") if x.strip())
        rules = [r for r in rules if not r.name.startswith(bad)]
    flat_rules = [r for r in rules if not isinstance(r, CompoundRule)]
    compound_rules = [r for r in rules if isinstance(r, CompoundRule)]
    print("complexities=%s pos_a=%s rules=%d (flat=%d, compound=%d, only_complex skipped=%d)" % (
        ",".join(sorted(complexities)), sorted(wanted), len(rules),
        len(flat_rules), len(compound_rules), len(skipped_complex)), flush=True)

    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    opener = gzip.open if args.out.endswith(".gz") else open

    n_records = 0
    n_pairs = 0
    per_rule = OrderedDict()
    with opener(args.out, "wt", encoding="utf-8") as out:
        for rule in flat_rules:
            source_words = sorted(
                w for w in words_by_pos.get(rule.pos_b, {}) if single_word(w)
            )
            if args.limit:
                source_words = source_words[:args.limit]
            emitted = 0
            for word_b in source_words:
                res = der.derive(
                    word_b=word_b,
                    pos_b=rule.pos_b,
                    pos_a=rule.pos_a,
                    rule_id=rule.name,
                    is_extended=True,
                    use_rare=args.use_rare,
                )
                for word_a in sorted(res):
                    if word_a == word_b:
                        continue
                    if args.real_only and (word_a, rule.pos_a) not in known:
                        continue
                    rare = word_b in rule.rare_inversed.get(word_a, set())
                    rec = build_record(
                        word_a, rule.pos_a, [parent(word_b, rule.pos_b)],
                        rule, words_by_pos[rule.pos_a].get(word_a), known, rare,
                        include_flags=EMIT_FLAGS,
                    )
                    out.write(json.dumps(rec, ensure_ascii=False) + "\n")
                    n_records += 1
                    emitted += 1
                n_pairs += 1
            per_rule[rule.name] = emitted
            print("rule %-50s words=%-6d edges=%d" % (
                rule.name[:50], len(source_words), emitted), flush=True)
            if der.cache is not None:
                der.cache.save()

        for rule in compound_rules:
            if len(rule.poss_m) != 1:
                print("rule %-50s SKIPPED (multi-modifier compound)" % rule.name[:50], flush=True)
                per_rule[rule.name] = 0
                continue
            modifier_pos = rule.poss_m[0]
            if modifier_pos == "*":
                # фиксированный префикс из имени правила ([полу], [мимо/само], [пол])
                modifiers = fixed_modifiers(rule.name)
            else:
                modifiers = sorted(
                    w for w in words_by_pos.get(modifier_pos, {}) if single_word(w)
                )[:args.modifier_limit]
            heads = sorted(
                w for w in words_by_pos.get(rule.pos_b, {}) if single_word(w)
            )
            if args.limit:
                heads = heads[:args.limit]
            order = rule.order or [0, 1]
            slot_head = order.index(0) if 0 in order else 0
            slot_mod = order.index(1) if 1 in order else 1
            emitted = 0
            for head in heads:
                for modifier in modifiers:
                    if modifier == head:
                        # a lexeme cannot be its own modifier
                        continue
                    res = apply_compound_rule(rule, head, modifier, args.use_rare)
                    for word_a in sorted(res):
                        if word_a in (head, modifier):
                            continue
                        if (args.compound_real_only or args.real_only) and (word_a, rule.pos_a) not in known:
                            continue
                        if modifier_pos == "*":
                            # Фиксированный префикс (полу-, впол-, мимо-): узел графа не создаётся,
                            # связь идёт от лексемы-основы (полусидя <- сидя <- сидеть).
                            affix, affix_kind = fixed_affix(rule.name)
                            parents_ = [parent(head, rule.pos_b, "head", 0)]
                            kind_ = affix_kind or "pfx"
                        else:
                            affix = None
                            parents_ = [parent(head, rule.pos_b, "head", slot_head),
                                        parent(modifier, modifier_pos, "modifier", slot_mod)]
                            kind_ = "compound"
                        rec = build_record(
                            word_a, rule.pos_a, parents_,
                            rule, words_by_pos[rule.pos_a].get(word_a), known, False,
                            include_flags=EMIT_FLAGS, kind=kind_, affix=affix,
                        )
                        out.write(json.dumps(rec, ensure_ascii=False) + "\n")
                        n_records += 1
                        emitted += 1
                    n_pairs += 1
            per_rule[rule.name] = emitted
            print("rule %-50s heads=%-5d mods=%-5d edges=%d" % (
                rule.name[:50], len(heads), len(modifiers), emitted), flush=True)
            if der.cache is not None:
                der.cache.save()

    meta = OrderedDict([
        ("schema", SCHEMA_VERSION),
        ("lang", args.lang),
        ("pos_a", sorted(wanted)),
        ("complexities", sorted(complexities)),
        ("generated_at", time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())),
        ("sources", [OrderedDict([("name", os.path.basename(args.dict)),
                                  ("pages", n_pages)])]),
        ("counts", OrderedDict([
            ("rules", len(rules)),
            ("source_words", n_pairs),
            ("edges", n_records),
        ])),
        ("per_rule", per_rule),
        ("skipped_only_complex", skipped_complex),
        ("seconds", round(time.time() - t0, 1)),
    ])
    meta_path = args.out + ".meta.json"
    with open(meta_path, "w", encoding="utf-8") as fh:
        json.dump(meta, fh, ensure_ascii=False, indent=2)
    print("wrote %s (%d edges) and %s" % (args.out, n_records, meta_path), flush=True)
    return meta


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dict", default="data/wiktionary/parsed_ru.jsonl.gz",
                    help="parsed Wiktionary dictionary (JSONL or JSONL.gz)")
    ap.add_argument("--out", default=None,
                    help="output JSONL(.gz); default data/derived/<pos_a>.jsonl.gz")
    ap.add_argument("--pos-a", default="num",
                    help="comma-separated target POS to run rules for")
    ap.add_argument("--complexities", default="simple,complex,compound",
                    help="rule groups to use: simple,complex,compound")
    ap.add_argument("--include-rules", default=None,
                    help="comma-separated rule-name prefixes to keep (exact startswith)")
    ap.add_argument("--exclude-info", default=None,
                    help="drop rules whose info contains any of these tokens")
    ap.add_argument("--include-info", default=None,
                    help="keep only rules whose info contains any of these tokens")
    ap.add_argument("--exclude-rules", default=None,
                    help="comma-separated rule-name prefixes to skip")
    ap.add_argument("--exclude-file", default=None,
                    help="file with source words to skip (default data/pseudo_lemmas.txt)")
    ap.add_argument("--exclude-words", default=None,
                    help="comma-separated source words to skip")
    ap.add_argument("--extra-dataset", default=None,
                    help="comma-separated JSONL datasets whose words are added as\n"
                         "extra source words, chaining derivations")
    ap.add_argument("--real-only", action="store_true",
                    help="keep only edges attested in the dictionary (all rules)")
    ap.add_argument("--compound-real-only", action="store_true",
                    help="keep only compound results attested in the dictionary")
    ap.add_argument("--modifier-limit", type=int, default=200,
                    help="max candidate modifier words per compound rule")
    ap.add_argument("--lang", default="rus")
    ap.add_argument("--limit", type=int, default=0,
                    help="max source words per rule (0 = all)")
    ap.add_argument("--cache", default=None, help="result cache path")
    ap.add_argument("--guesser", action="store_true",
                    help="use the Zaliznyak guesser for inflect_type tags (tags_b filtering)")
    ap.add_argument("--force-complex", action="store_true",
                    help="also apply rules flagged only_complex on their own")
    ap.add_argument("--no-rare", dest="use_rare", action="store_false",
                    help="do not use the rare-form tables")
    args = ap.parse_args(argv)
    if args.out is None:
        args.out = "data/derived/%s.jsonl.gz" % args.pos_a.replace(",", "_")
    run(args)


if __name__ == "__main__":
    main()


