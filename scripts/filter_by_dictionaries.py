"""Filter derivation results by dictionaries, then merge subagent verdicts.

Reproducible pipeline used for the adverb analysis (see docs/analysis_log.md).

Этап 1 — просеять результаты правил по словарям:
  python scripts/filter_by_dictionaries.py filter \
      --rules-prefix rule982,rule977 --pos-a adv \
      --input data/derived/adv.jsonl.gz \
      --out data/derived/adv_g1.jsonl \
      --doubtful /tmp/g1_doubtful.jsonl

Этап 2 — после вердиктов субагентов собрать итог:
  python scripts/filter_by_dictionaries.py merge \
      --filtered data/derived/adv_g1.jsonl \
      --judged /tmp/g1_ok1.jsonl --judged /tmp/g1_ok2.jsonl \
      --final data/derived/adv_g1.final.jsonl

Словари: Викисловарь (parsed_ru.jsonl.gz, статья с нужной частью речи) и словарь Даля
(dahl.jsonl.gz: заголовок или токен толкования). Записи, подтверждённые только Далей,
пишутся в --doubtful и отдаются субагентам на проверку (политика: диалектное и устаревшее
подходит, отклоняется только очевидный мусор).
"""
from __future__ import annotations

import argparse
import gzip
import json
import os
import re
import sys

WIKTIONARY_POS = {
    "сущ": "noun", "прил": "adj", "прич": "adj", "гл": "verb",
    "деепр": "verb", "нар": "adv", "числ": "num",
}


def norm(text: str) -> str:
    text = text.lower()
    for ch in ("\u0301", "\u0300", "\u00b4"):
        text = text.replace(ch, "")
    # ё и е считаем одной буквой: правила дают «е», словарь часто «ё»
    return text.replace("ё", "е")


def load_wiktionary(path: str):
    known = set()
    with gzip.open(path, "rt", encoding="utf-8") as fh:
        for line in fh:
            rec = json.loads(line)
            title = (rec.get("title") or "").lower()
            for entry in rec.get("entries") or []:
                pos = WIKTIONARY_POS.get(entry.get("pos"))
                if pos:
                    known.add((title, pos))
    return known


def load_dahl(path: str):
    heads, tokens = set(), set()
    with gzip.open(path, "rt", encoding="utf-8") as fh:
        for line in fh:
            rec = json.loads(line)
            head = (rec.get("word") or "").strip().lower()
            if head:
                heads.add(head)
            text = rec.get("text") or ""
            if text:
                tokens.update(re.findall(r"[а-яё-]{2,}", norm(text)))
    return heads, tokens


def cmd_filter(args):
    prefixes = tuple(p.strip() for p in args.rules_prefix.split(",") if p.strip())
    known = load_wiktionary(args.wiktionary)
    heads, tokens = load_dahl(args.dahl)
    print("словари: викисловарь %d пар, даль %d заголовков / %d токенов"
          % (len(known), len(heads), len(tokens)), flush=True)
    kept = doubtful = total = 0
    out = open(args.out, "w", encoding="utf-8")
    doubt = open(args.doubtful, "w", encoding="utf-8") if args.doubtful else None
    opener = gzip.open if args.input.endswith(".gz") else open
    with opener(args.input, "rt", encoding="utf-8") as fh:
        for line in fh:
            rec = json.loads(line)
            if not rec["rule"].startswith(prefixes):
                continue
            total += 1
            word = rec["word"]
            nw = norm(word)
            by = []
            if (word.lower(), args.pos_a) in known:
                by.append("wiktionary")
            if nw in heads or nw in tokens:
                by.append("dahl")
            if not by:
                continue
            rec["verified"] = True
            rec["verified_by"] = by
            out.write(json.dumps(rec, ensure_ascii=False) + "\n")
            kept += 1
            if by == ["dahl"] and doubt is not None:
                doubt.write(json.dumps({
                    "word": word,
                    "parent": rec["parents"][0]["word"] if rec.get("parents") else "",
                    "rule": rec["rule"],
                }, ensure_ascii=False) + "\n")
                doubtful += 1
    out.close()
    if doubt is not None:
        doubt.close()
    print("правил по префиксам %s: рёбер %d, после фильтра %d, сомнительных (только Даль) %d"
          % (",".join(prefixes), total, kept, doubtful), flush=True)


def cmd_merge(args):
    rows = [json.loads(l) for l in open(args.filtered, encoding="utf-8")]
    by_key = {}
    for rec in rows:
        parent = rec["parents"][0]["word"] if rec.get("parents") else ""
        by_key[(rec["word"], parent, rec["rule"])] = rec
    approved = []
    seen = set()
    for path in args.judged:
        for line in open(path, encoding="utf-8"):
            verdict = json.loads(line)
            key = (verdict["word"], verdict.get("parent", ""), verdict["rule"])
            rec = by_key.get(key)
            if rec is None or key in seen:
                continue
            seen.add(key)
            rec = dict(rec)
            rec["verified_by"] = ["dahl"]
            rec["judged_by"] = "subagent"
            if verdict.get("reason"):
                rec["reason"] = verdict["reason"]
            approved.append(rec)
    base = [r for r in rows if r.get("verified_by") != ["dahl"]]
    final = base + approved
    with open(args.final, "w", encoding="utf-8") as fh:
        for rec in final:
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
    print("итог: %d (= %d по словарям + %d одобрено судьями из %d)"
          % (len(final), len(base), len(approved), len(rows) - len(base)), flush=True)


def cmd_clean(args):
    """Drop artefacts: capitalised Cyrillic entries and Latin-only words."""
    kept, dropped_cap, dropped_lat = 0, 0, 0
    with open(args.input, encoding="utf-8") as fi, \
         open(args.out, "w", encoding="utf-8") as fo:
        for line in fi:
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except ValueError:
                dropped_lat += 0  # битая строка: считаем отдельно ниже
                dropped_bad = getattr(cmd_clean, "_bad", 0) + 1
                cmd_clean._bad = dropped_bad
                continue
            word = rec.get("word", "")
            parents = [p.get("word", "") for p in rec.get("parents") or []]
            if word[:1].isupper() or any(p[:1].isupper() for p in parents):
                dropped_cap += 1
                continue
            if re.search(r"[A-Za-z]", word):
                dropped_lat += 1
                continue
            fo.write(json.dumps(rec, ensure_ascii=False) + "\n")
            kept += 1
    print("%s: осталось %d (отброшено заглавных %d, латиницы %d)"
          % (args.input, kept, dropped_cap, dropped_lat), flush=True)


def cmd_blacklist(args):
    """Убирает рёбра, перечисленные в blacklist (артефакт для воспроизводимости)."""
    bad = set()
    with open(args.blacklist, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            e = json.loads(line)
            bad.add((norm(e.get("child")), norm(e.get("parent", "")), e.get("rule")))
    rows = []
    with open(args.input, encoding="utf-8") as fi:
        for line in fi:
            line = line.strip()
            if line:
                rows.append(line)
    kept = dropped = 0
    with open(args.out, "w", encoding="utf-8") as fo:
        for line in fi:
            rec = json.loads(line)
            parent = rec["parents"][0]["word"] if rec.get("parents") else ""
            if (norm(rec.get("word")), norm(parent), rec.get("rule")) in bad:
                dropped += 1
                continue
            fo.write(json.dumps(rec, ensure_ascii=False) + "\n")
            kept += 1
    print("%s: осталось %d (снято blacklist: %d)" % (args.input, kept, dropped), flush=True)


def cmd_canonical(args):
    """Приводит написание к словарному (ё вместо е), если лексема есть в Викисловаре."""
    canon = {}
    with gzip.open(args.wiktionary, "rt", encoding="utf-8") as fh:
        for line in fh:
            rec = json.loads(line)
            title = rec.get("title") or ""
            if title:
                canon.setdefault(norm(title), title)
    kept = changed = 0
    with open(args.input, encoding="utf-8") as fi, open(args.out, "w", encoding="utf-8") as fo:
        for line in fi:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            word = rec.get("word")
            fixed = canon.get(norm(word))
            if fixed and fixed != word:
                rec["word"] = fixed
                rec["id"] = fixed + "|" + (rec.get("pos") or "")
                changed += 1
            for parent in rec.get("parents") or []:
                pf = canon.get(norm(parent.get("word")))
                if pf and pf != parent.get("word"):
                    parent["word"] = pf
                    parent["id"] = pf + "|" + (parent.get("pos") or "")
            fo.write(json.dumps(rec, ensure_ascii=False) + "\n")
            kept += 1
    print("%s: записей %d, исправлено написаний %d" % (args.input, kept, changed), flush=True)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="mode", required=True)
    f = sub.add_parser("filter")
    f.add_argument("--rules-prefix", required=True)
    f.add_argument("--pos-a", default="adv")
    f.add_argument("--input", default="data/derived/adv.jsonl.gz")
    f.add_argument("--out", required=True)
    f.add_argument("--doubtful", default=None)
    f.add_argument("--wiktionary", default="data/wiktionary/parsed_ru.jsonl.gz")
    f.add_argument("--dahl", default="data/dahl/dahl.jsonl.gz")
    f.set_defaults(func=cmd_filter)
    m = sub.add_parser("merge")
    m.add_argument("--filtered", required=True)
    m.add_argument("--judged", action="append", required=True)
    m.add_argument("--final", required=True)
    m.set_defaults(func=cmd_merge)
    b = sub.add_parser("blacklist")
    b.add_argument("--input", required=True)
    b.add_argument("--blacklist", required=True)
    b.add_argument("--out", required=True)
    b.set_defaults(func=cmd_blacklist)
    k = sub.add_parser("canonical")
    k.add_argument("--input", required=True)
    k.add_argument("--out", required=True)
    k.add_argument("--wiktionary", default="data/wiktionary/parsed_ru.jsonl.gz")
    k.set_defaults(func=cmd_canonical)
    c = sub.add_parser("clean")
    c.add_argument("--input", required=True)
    c.add_argument("--out", required=True)
    c.set_defaults(func=cmd_clean)
    args = ap.parse_args(argv)
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    args.func(args)


if __name__ == "__main__":
    main()
