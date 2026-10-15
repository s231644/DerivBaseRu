#!/usr/bin/env python
"""Слияние финальных датасетов деривации в один единый файл (graph_service).

Берёт финальные файлы отношений из data/derived (список — в graph_service/DATASETS.md),
выкидывает дубликаты записей и пишет один JSONL(.gz). Дальше для него
scripts/build_components.py считает компоненты связности всего графа разом.

Использование:
  .venv/bin/python scripts/build_unified.py \
      --out data/derived/unified.jsonl.gz [--input file1.jsonl --input file2.jsonl.gz]
  .venv/bin/python scripts/build_components.py \
      --input data/derived/unified.jsonl.gz --aggregate --out-dir data/derived
"""
import argparse, collections, gzip, json, os, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(REPO, 'data', 'derived')

# Финальные файлы из graph_service/DATASETS.md; порядок задаёт приоритет
# записи (первое вхождение побеждает при дубликатах).
DEFAULT_INPUTS = [
    'num.jsonl.gz',
    'verb_pfx.jsonl',
    'verb_sfx.jsonl',
    'verb_compound.jsonl',
    'adv.rare.verified.jsonl',
    'adv_pfx.final.clean.jsonl',
    'adv_sfx.clean.jsonl',
    'adv_g1.final.clean.jsonl',
    'adv_g2.final.clean.jsonl',
    'adv_g5.clean.jsonl',
    'adv_ymx.clean.jsonl',
]


def opener(path):
    return gzip.open(path, 'rt', encoding='utf-8') if path.endswith('.gz') else open(path, encoding='utf-8')


def edge_key(rec):
    """Ключ ребра: слово + правило + родители (компаунд несёт двух родителей)."""
    parents = tuple(sorted(p.get('id') or '' for p in (rec.get('parents') or [])))
    return (rec.get('id') or '', rec.get('rule') or '', parents)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--input', action='append', default=None,
                    help='входной файл (можно несколько; по умолчанию — финалы из DATASETS.md)')
    ap.add_argument('--out', default=os.path.join(DATA, 'unified.jsonl.gz'))
    args = ap.parse_args()

    names = args.input if args.input else DEFAULT_INPUTS
    paths = [n if os.path.isabs(n) else os.path.join(DATA, n) for n in names]

    seen = set()
    total = dup = bad = 0
    per_file = []
    write = gzip.open if args.out.endswith('.gz') else open
    with write(args.out, 'wt', encoding='utf-8') as out:
        for path in paths:
            if not os.path.exists(path):
                print('нет файла, пропускаю:', path, file=sys.stderr)
                continue
            kept = 0
            for line in opener(path):
                line = line.strip()
                if not line:
                    continue
                total += 1
                try:
                    rec = json.loads(line)
                except Exception:
                    bad += 1
                    continue
                if not rec.get('id') or not rec.get('parents'):
                    bad += 1
                    continue
                key = edge_key(rec)
                if key in seen:
                    dup += 1
                    continue
                seen.add(key)
                out.write(json.dumps(rec, ensure_ascii=False, sort_keys=True) + '\n')
                kept += 1
            per_file.append((os.path.basename(path), kept))
    for name, kept in per_file:
        print('%-32s +%d' % (name, kept))
    print('итого: прочитано %d, дубликатов %d, битых %d, уникальных рёбер %d -> %s'
          % (total, dup, bad, len(seen), args.out))


if __name__ == '__main__':
    main()
