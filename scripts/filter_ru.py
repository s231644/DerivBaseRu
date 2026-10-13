"""Keep only Russian (lang="ru") entries from a parsed ru.wiktionary JSONL.

Usage:
  python scripts/filter_ru.py data/wiktionary/parsed.jsonl data/wiktionary/parsed_ru.jsonl
"""
from __future__ import annotations

import argparse
import json


def filter_ru(in_path: str, out_path: str, lang: str = "ru") -> tuple:
    total = kept = 0
    with open(in_path, encoding="utf-8") as fi, open(out_path, "w", encoding="utf-8") as fo:
        for line in fi:
            total += 1
            try:
                rec = json.loads(line)
            except ValueError:
                continue
            entries = [e for e in (rec.get("entries") or []) if e.get("lang") == lang]
            if not entries:
                continue
            rec["entries"] = entries
            fo.write(json.dumps(rec, ensure_ascii=False) + chr(10))
            kept += 1
    return total, kept


def main(argv=None):
    ap = argparse.ArgumentParser(description="Filter parsed Wiktionary JSONL by language")
    ap.add_argument("in_path")
    ap.add_argument("out_path")
    ap.add_argument("--lang", default="ru")
    args = ap.parse_args(argv)
    total, kept = filter_ru(args.in_path, args.out_path, args.lang)
    print("total", total, "kept", kept)


if __name__ == "__main__":
    main()
