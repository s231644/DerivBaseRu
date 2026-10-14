"""Group derivation edges by rule frequency and rewrite them sorted.

Records are grouped by their `rule`; groups are emitted in ASCENDING group size,
so rules that produce few edges come first and hyper-productive rules (where most
junk concentrates) come last. Inside a group records are sorted by
(word, parents, rule). Bucketing uses gzipped temp files, so the working set on
disk stays close to the output size.

Usage:
  python scripts/sort_edges.py data/derived/adv.jsonl.gz
  python scripts/sort_edges.py in.jsonl.gz --out out.jsonl.gz --drop-above 5000
"""
from __future__ import annotations

import argparse
import gzip
import json
import os
import shutil
import sys
import tempfile
from collections import Counter


def opener(path, mode):
    if path.endswith(".gz"):
        return gzip.open(path, mode, encoding="utf-8")
    return open(path, mode, encoding="utf-8")


def row_key(line):
    rec = json.loads(line)
    parents = rec.get("parents") or []
    words = "|".join(sorted((p.get("word") or "") for p in parents))
    return (rec.get("word") or "", words, rec.get("rule") or "")


def count_rules(in_path):
    counts = Counter()
    total = 0
    bad = 0
    with opener(in_path, "rt") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except ValueError:
                bad += 1
                continue
            counts[rec.get("rule") or ""] += 1
            total += 1
    return counts, total, bad


def sort_edges(in_path, out_path, report_path, drop_above):
    counts, total, bad = count_rules(in_path)
    order = sorted(counts, key=lambda r: (counts[r], r))
    keep = [r for r in order if drop_above is None or counts[r] <= drop_above]
    keep_set = set(keep)
    dropped = [r for r in order if r not in keep_set]
    print("rules=%d records=%d (drop_above=%s -> kept %d rules, dropped %d)"
          % (len(counts), total, drop_above, len(keep), len(dropped)), flush=True)

    tmpdir = tempfile.mkdtemp(prefix="sortedges-")
    buckets = {}
    written = 0
    try:
        with opener(in_path, "rt") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    rec = json.loads(line)
                except ValueError:
                    continue
                rule = rec.get("rule") or ""
                if rule not in keep_set:
                    continue
                h = buckets.get(rule)
                if h is None:
                    h = gzip.open(os.path.join(tmpdir, "%d.gz" % len(buckets)),
                                  "wt", encoding="utf-8")
                    buckets[rule] = h
                h.write(line + "\n")
        for h in buckets.values():
            h.close()

        with opener(out_path, "wt") as out:
            for rule in keep:
                h = buckets.get(rule)
                if h is None:
                    continue
                rows = []
                with gzip.open(h.name, "rt", encoding="utf-8") as bf:
                    for line in bf:
                        line = line.rstrip("\n")
                        if line:
                            rows.append((row_key(line), line))
                rows.sort(key=lambda t: t[0])
                for _, line in rows:
                    out.write(line + "\n")
                    written += 1
                rows = []
                print("  %-52s %8d" % (rule[:52], counts[rule]), flush=True)
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)

    report = {
        "input": in_path,
        "output": out_path,
        "records_in": total,
        "records_out": written,
        "unparsed": bad,
        "rules": len(counts),
        "rules_dropped": len(dropped),
        "drop_above": drop_above,
        "per_rule_ascending": [{"rule": r, "edges": counts[r]} for r in order],
    }
    if report_path:
        with open(report_path, "w", encoding="utf-8") as fh:
            json.dump(report, fh, ensure_ascii=False, indent=2)
    print("wrote %s (%d records)" % (out_path, written), flush=True)
    return report


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("input")
    ap.add_argument("--out", default=None)
    ap.add_argument("--report", default=None)
    ap.add_argument("--drop-above", type=int, default=None,
                    help="drop rules whose edge count exceeds this value")
    args = ap.parse_args(argv)
    if args.out is None:
        base = args.input[:-3] if args.input.endswith(".gz") else args.input
        root, ext = os.path.splitext(base)
        args.out = root + ".sorted" + ext + (".gz" if args.input.endswith(".gz") else "")
    if args.report is None:
        args.report = args.out + ".report.json"
    sort_edges(args.input, args.out, args.report, args.drop_above)


if __name__ == "__main__":
    main()
