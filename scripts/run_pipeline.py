"""Run the DerivBaseRu derivation pipeline over a Wiktionary dictionary.

Pipeline (see docs/derivation_schema.md):
  1. read the dictionary (parsed ru.wiktionary JSONL) -> words grouped by POS;
  2. for each rule (optionally filtered by target POS `pos_a`);
  3. for each source word whose POS equals the rule's `pos_b`;
     apply the rule and record every derived form.

Results are written as one JSONL record per derivation edge (schema §3),
gzipped, with a sidecar meta.json header.

Usage:
  python scripts/run_pipeline.py --pos-a num        --out data/derived/num.jsonl.gz
  python scripts/run_pipeline.py --pos-a adv        --out data/derived/adv.jsonl.gz
  python scripts/run_pipeline.py --pos-a num,adv --limit 500
"""
from __future__ import annotations

import argparse
import gzip
import json
import os
import sys
import time
from collections import OrderedDict

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from derivbase_ru.cache import ResultCache
from derivbase_ru.derivation import Derivation

SCHEMA_VERSION = 1
STRESS = "\u0301\u00b4"

# Wiktionary POS template tags -> engine POS tags (Derivation.pos_all).
POS_MAP = {
    "сущ": "noun",
    "прил": "adj",
    "прич": "adj",
    "гл": "verb",
    "деепр": "verb",
    "нар": "adv",
    "числ": "num",
}

# rule.info -> schema `kind`
KIND_MAP = {
    "SFX": "sfx",
    "PFX": "pfx",
    "PFX_SFX": "pfx_sfx",
    "CONFIX": "pfx_sfx",
    "POSTFIX": "postfix",
    "INTERFIX": "interfix",
    "CONV": "conversion",
}


def has_stress(text: str) -> bool:
    return any(ch in text for ch in STRESS)


def read_dictionary(path: str):
    """Return (words_by_pos, known) from a parsed Wiktionary JSONL(.gz).

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
                positional = inflect.get("positional") or []
                accented = None
                for form in positional:
                    if form and has_stress(form):
                        accented = form
                        break
                bucket[word] = {
                    "accented": accented,
                    "inflect_type": None,
                }
    return words_by_pos, known, n


def rule_kind(info: str) -> str:
    for info_key, kind in KIND_MAP.items():
        if info_key in (info or "").upper():
            return kind
    return (info or "").lower() or "sfx"


def build_record(word_a, pos_a, word_b, pos_b, rule, meta_b, known, rare):
    entry_b = meta_b or {}
    is_real = (word_a, pos_a) in known
    return OrderedDict([
        ("schema", SCHEMA_VERSION),
        ("id", "%s|%s" % (word_a, pos_a)),
        ("word", word_a),
        ("pos", pos_a),
        ("lang", "rus"),
        ("accented", entry_b.get("accented") if is_real else None),
        ("hom_index", 0),
        ("rule", rule.name),
        ("kind", rule_kind(rule.info)),
        ("parents", [OrderedDict([
            ("id", "%s|%s" % (word_b, pos_b)),
            ("word", word_b),
            ("pos", pos_b),
            ("role", "head"),
            ("slot", 0),
        ])]),
        ("inflect_type", entry_b.get("inflect_type")),
        ("flags", OrderedDict([
            ("real", is_real),
            ("rare", bool(rare)),
            ("reconstructed", False),
            ("potential", not is_real),
        ])),
        ("source", "derivbase"),
    ])


def run(args) -> dict:
    t0 = time.time()
    print("reading dictionary: %s" % args.dict, flush=True)
    words_by_pos, known, n_pages = read_dictionary(args.dict)
    print("pages=%d words: %s" % (
        n_pages,
        ", ".join("%s=%d" % (p, len(w)) for p, w in words_by_pos.items()),
    ), flush=True)

    der = Derivation(lang=args.lang, cache=ResultCache(args.cache) if args.cache else None)
    wanted = set(a.strip() for a in args.pos_a.split(",") if a.strip())
    # The rule JSON files may list the same rule_id more than once (split
    # subrules). Merge such entries by name so no subrule is lost.
    by_name = OrderedDict()
    for r in der.loaded_rules["simple"] + der.loaded_rules["complex"]:
        if r.pos_a not in wanted:
            continue
        base = by_name.get(r.name)
        if base is None:
            by_name[r.name] = r
            continue
        base.subrules = list(base.subrules) + list(r.subrules)
        for s, i in r.rare:
            base.rare_straight[s].add(i)
            base.rare_inversed[i].add(s)
    rules = list(by_name.values())
    print("rules with pos_a in %s: %d" % (sorted(wanted), len(rules)), flush=True)

    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    opener = gzip.open if args.out.endswith(".gz") else open

    n_records = 0
    n_pairs = 0
    per_rule = OrderedDict()
    with opener(args.out, "wt", encoding="utf-8") as out:
        for rule in rules:
            source_words = sorted(words_by_pos.get(rule.pos_b, {}))
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
                    rare = word_b in rule.rare_inversed.get(word_a, set())
                    rec = build_record(
                        word_a, rule.pos_a, word_b, rule.pos_b,
                        rule, words_by_pos[rule.pos_a].get(word_a), known, rare,
                    )
                    out.write(json.dumps(rec, ensure_ascii=False) + "\n")
                    n_records += 1
                    emitted += 1
                n_pairs += 1
            per_rule[rule.name] = emitted
            print("rule %-55s words=%-6d edges=%d" % (
                rule.name[:55], len(source_words), emitted), flush=True)
            if der.cache is not None:
                der.cache.save()

    meta = OrderedDict([
        ("schema", SCHEMA_VERSION),
        ("lang", args.lang),
        ("pos_a", sorted(wanted)),
        ("generated_at", time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())),
        ("sources", [OrderedDict([("name", os.path.basename(args.dict)),
                                  ("pages", n_pages)])]),
        ("counts", OrderedDict([
            ("rules", len(rules)),
            ("source_words", n_pairs),
            ("edges", n_records),
        ])),
        ("per_rule", per_rule),
        ("seconds", round(time.time() - t0, 1)),
    ])
    meta_path = args.out + ".meta.json"
    with open(meta_path, "w", encoding="utf-8") as fh:
        json.dump(meta, fh, ensure_ascii=False, indent=2)
    print("wrote %s (%d edges) and %s" % (args.out, n_records, meta_path), flush=True)
    return meta


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dict", default="data/wiktionary/parsed_ru.jsonl.gz",
                    help="parsed Wiktionary dictionary (JSONL or JSONL.gz)")
    ap.add_argument("--out", default=None,
                    help="output JSONL(.gz); default data/derived/<pos_a>.jsonl.gz")
    ap.add_argument("--pos-a", default="num",
                    help="comma-separated target POS to run rules for")
    ap.add_argument("--lang", default="rus")
    ap.add_argument("--limit", type=int, default=0,
                    help="max source words per rule (0 = all)")
    ap.add_argument("--cache", default=None, help="result cache path")
    ap.add_argument("--no-rare", dest="use_rare", action="store_false",
                    help="do not use the rules' rare-form tables")
    args = ap.parse_args(argv)
    if args.out is None:
        args.out = "data/derived/%s.jsonl.gz" % args.pos_a.replace(",", "_")
    run(args)


if __name__ == "__main__":
    main()
