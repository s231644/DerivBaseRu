"""Проверка графа дериваций: компоненты связности с несколькими корнями.

Корень — узел без родителей (непроизводное слово). В компоненте связности должен быть
один корень; если корней два и более, значит какие-то рёбра склеили разные семьи.
Такие рёбра считаются лишними и записываются в blacklist (артефакт для воспроизводимости).

Использование:
  python scripts/validate_components.py report    --inputs a.jsonl,b.jsonl
  python scripts/validate_components.py blacklist --inputs a.jsonl,b.jsonl --out data/graph_blacklist.jsonl

Применение:
  python scripts/filter_by_dictionaries.py blacklist --input X.jsonl \
      --blacklist data/graph_blacklist.jsonl --out X.jsonl
"""
from __future__ import annotations

import argparse
import collections
import gzip
import json
import os
import sys


def open_text(path):
    """Читаем и plain, и .gz (числительные лежат в num.jsonl.gz)."""
    if path.endswith(".gz"):
        return gzip.open(path, "rt", encoding="utf-8")
    return open(path, encoding="utf-8")


def read_graph(paths):
    nodes, edges = set(), []
    for path in paths:
        if not os.path.exists(path):
            print("нет файла: %s" % path, file=sys.stderr)
            continue
        for line in open_text(path):
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            child = rec.get("id") or (rec["word"] + "|" + rec["pos"])
            nodes.add(child)
            for p in rec.get("parents") or []:
                pid = p.get("id") or (p["word"] + "|" + p["pos"])
                nodes.add(pid)
                edges.append({
                    "parent": pid,
                    "child": child,
                    "rule": rec.get("rule"),
                    "file": os.path.basename(path),
                    "verified_by": rec.get("verified_by"),
                })
    return nodes, edges


def components(nodes, edges, skip=()):
    adj = collections.defaultdict(set)
    for e in edges:
        if e in skip:
            continue
        adj[e["parent"]].add(e["child"])
        adj[e["child"]].add(e["parent"])
    seen, comps = set(), []
    for n in nodes:
        if n in seen:
            continue
        stack, comp = [n], set()
        while stack:
            x = stack.pop()
            if x in comp:
                continue
            comp.add(x)
            stack.extend(adj[x])
        seen |= comp
        comps.append(comp)
    return comps


# Дети всех рёбер. Ребро всегда соединяет узлы одной компоненты, поэтому
# глобальный предрасчёт эквивалентен покомпонентному проходу по всем рёбрам,
# но вместо O(компонент × рёбер) — O(рёбер).
_CHILD_HAS_PARENT: set[str] = set()


def roots_of(comp, edges, skip=()):
    has_parent = {e["child"] for e in edges if e not in skip} if skip else _CHILD_HAS_PARENT
    return sorted(x for x in comp if x not in has_parent)


def weakness(edge):
    """Чем больше — тем слабее подтверждение (такое ребро выкидываем первым)."""
    by = edge.get("verified_by") or []
    if by == ["dahl"]:
        return 3
    if "dahl" in by:
        return 2
    if by:
        return 1
    return 0


def reduce_component(comp, edges):
    """Минимальный набор рёбер, после удаления которых в каждой части один корень."""
    inside = [e for e in edges if e["parent"] in comp and e["child"] in comp]
    dropped = []
    while True:
        if len(roots_of(comp, edges, dropped)) <= 1:
            break
        best, best_key = None, None
        for e in inside:
            if e in dropped:
                continue
            rest = dropped + [e]
            parts = components(comp, inside, rest)
            if len(parts) < 2:
                continue
            if any(len(roots_of(p, edges, rest)) < 1 for p in parts):
                continue
            key = (weakness(e), e["rule"] or "", e["parent"])
            if best_key is None or key > best_key:
                best, best_key = e, key
        if best is None:
            break
        dropped.append(best)
    return dropped


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="mode", required=True)
    for mode in ("report", "blacklist"):
        p = sub.add_parser(mode)
        p.add_argument("--inputs", required=True, help="файлы через запятую")
        p.add_argument("--out", default=None)
    args = ap.parse_args(argv)
    paths = [x.strip() for x in args.inputs.split(",") if x.strip()]
    nodes, edges = read_graph(paths)
    _CHILD_HAS_PARENT.update(e["child"] for e in edges)
    comps = components(nodes, edges)
    multi = [c for c in comps if len(roots_of(c, edges)) >= 2]
    print("узлов %d, рёбер %d, компонент %d, с двумя и более корнями %d"
          % (len(nodes), len(edges), len(comps), len(multi)), flush=True)
    black = []
    for comp in multi:
        black.extend(reduce_component(comp, edges))
    print("лишних рёбер (blacklist): %d" % len(black), flush=True)
    if args.mode == "report" or not args.out:
        for e in black[:20]:
            print("   %s <- %s  [%s]" % (e["child"], e["parent"], e["rule"]))
        return
    with open(args.out, "w", encoding="utf-8") as fh:
        for e in black:
            fh.write(json.dumps({
                "child": e["child"], "parent": e["parent"], "rule": e["rule"],
                "verified_by": e.get("verified_by"), "file": e.get("file"),
            }, ensure_ascii=False) + "\n")
    print("blacklist записан: %s" % args.out, flush=True)


if __name__ == "__main__":
    main()

