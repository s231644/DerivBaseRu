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
    return text


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
    args = ap.parse_args(argv)
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    args.func(args)


if __name__ == "__main__":
    main()
