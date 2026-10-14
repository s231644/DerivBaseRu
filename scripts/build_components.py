#!/usr/bin/env python
"""Pre-build connected components of the derivation graph so the viewer
does not compute them on the frontend at load time.

Usage:
  python scripts/build_components.py --input data/derived/verb_pfx.jsonl \
      [--input ...] --out-dir data/derived
Writes for each input <name>.components.json with:
  {nodes, edges, n_components, largest, id2c:{id->comp}, sizes:{comp->n}, reps:[...]}
"""
import argparse, gzip, json, os, sys
from collections import defaultdict

def opener(p):
    return gzip.open(p, 'rt', encoding='utf-8') if p.endswith('.gz') else open(p, encoding='utf-8')

class DSU:
    def __init__(self):
        self.p = {}
    def add(self, x):
        if x not in self.p: self.p[x] = x
    def find(self, x):
        self.add(x)
        r = x
        while self.p[r] != r:
            r = self.p[r]
        while self.p[x] != r:
            self.p[x], x = r, self.p[x]
        return r
    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.p[rb] = ra

def build(path):
    dsu = DSU(); words = {}; edges = 0
    for line in opener(path):
        line = line.strip()
        if not line: continue
        try: rec = json.loads(line)
        except Exception: continue
        i = rec.get('id')
        if not i: continue
        words.setdefault(i, rec.get('word') or i.split('|')[0])
        dsu.add(i)
        for p in (rec.get('parents') or []):
            pid = p.get('id')
            if not pid: continue
            words.setdefault(pid, p.get('word') or pid.split('|')[0])
            dsu.add(pid)
            dsu.union(pid, i)
            edges += 1
    comps = defaultdict(list)
    for n in dsu.p:
        comps[dsu.find(n)].append(n)
    order = sorted(comps.values(), key=len, reverse=True)
    id2c = {}; sizes = {}; reps = []
    for ci, members in enumerate(order):
        for n in members:
            id2c[n] = ci
        sizes[str(ci)] = len(members)
        reps.append({'comp': ci, 'size': len(members), 'words': sorted(words.get(m, m) for m in members)[:12]})
    return {'nodes': len(dsu.p), 'edges': edges, 'n_components': len(order),
            'largest': (len(order[0]) if order else 0), 'id2c': id2c, 'sizes': sizes, 'reps': reps[:200]}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--input', action='append', required=True)
    ap.add_argument('--out-dir', default='data/derived')
    args = ap.parse_args()
    os.makedirs(args.out_dir, exist_ok=True)
    for path in args.input:
        if not os.path.exists(path):
            print('skip (нет файла):', path); continue
        res = build(path)
        base = os.path.basename(path)
        for suf in ('.jsonl.gz', '.jsonl'):
            if base.endswith(suf): base = base[:-len(suf)]; break
        out = os.path.join(args.out_dir, base + '.components.json')
        with open(out, 'w', encoding='utf-8') as f:
            json.dump(res, f, ensure_ascii=False)
        print('%-32s nodes=%-8d edges=%-8d comps=%-8d largest=%d -> %s' % (
            os.path.basename(path), res['nodes'], res['edges'], res['n_components'], res['largest'], out))

if __name__ == '__main__':
    main()
