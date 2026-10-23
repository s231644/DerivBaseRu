"""Audit three-letter word prefixes and remove explicit false-analysis categories."""
import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path

CONFIG = Path(__file__).resolve().parents[1] / 'data/verb_compound_exclusions.json'


def exclusion(record, categories):
    modifiers = [p for p in record['parents'] if p.get('role') == 'modifier']
    for category in categories:
        if any(p['word'] == category['modifier'] and p['pos'] == category['pos']
               and p.get('form') in category['forms'] for p in modifiers):
            return category
    return None


def prefix_stats(rows):
    groups = defaultdict(list)
    for record in rows:
        groups[record['word'][:3]].append(record)
    return {
        prefix: {
            'relations': len(records),
            'unique_words': len({r['word'] for r in records}),
            'modifier_forms': dict(sorted(Counter(
                p['word'] + ' → ' + p['form']
                for r in records for p in r['parents']
                if p.get('role') == 'modifier').items())),
            'examples': sorted({r['word'] for r in records})[:8],
        }
        for prefix, records in sorted(groups.items(), key=lambda item: (-len(item[1]), item[0]))
    }


def filter_dataset(path, config=CONFIG):
    path = Path(path)
    config = Path(config)
    categories = json.loads(config.read_text())['categories']
    raw = path.read_bytes()
    stats_path = path.with_suffix('.prefix_stats.json')
    config_hash = hashlib.sha256(config.read_bytes()).hexdigest()
    if stats_path.exists():
        previous = json.loads(stats_path.read_text())
        if (previous['output_sha256'] == hashlib.sha256(raw).hexdigest()
                and previous['exclusions_sha256'] == config_hash):
            print('Compound categories: already filtered; original audit preserved', flush=True)
            return previous
    rows = [json.loads(line) for line in raw.decode().splitlines() if line.strip()]
    kept, rejected = [], []
    counts = Counter()
    for record in rows:
        category = exclusion(record, categories)
        if category:
            counts[category['id']] += 1
            rejected.append({'category': category['id'], 'reason': category['reason'],
                             'record': record})
        else:
            kept.append(record)
    before, after = prefix_stats(rows), prefix_stats(kept)
    report = {
        'grouping': 'first three Unicode letters of result word; counts are relations',
        'input_sha256': hashlib.sha256(raw).hexdigest(),
        'exclusions_sha256': config_hash,
        'before_relations': len(rows), 'after_relations': len(kept),
        'removed_relations': len(rejected),
        'after_unique_words': len({r['word'] for r in kept}),
        'categories': [dict(c, removed_relations=counts[c['id']]) for c in categories],
        'prefixes_before': before, 'prefixes_after': after,
    }
    temporary = path.with_suffix('.jsonl.tmp')
    temporary.write_text(''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in kept))
    report['output_sha256'] = hashlib.sha256(temporary.read_bytes()).hexdigest()
    path.with_suffix('.rejected.jsonl').write_text(''.join(
        json.dumps(r, ensure_ascii=False) + '\n' for r in rejected))
    stats_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    lines = ['prefix\tbefore_relations\tafter_relations\tremoved_relations']
    lines += ['\t'.join(map(str, (prefix, info['relations'],
                                 after.get(prefix, {}).get('relations', 0),
                                 info['relations'] - after.get(prefix, {}).get('relations', 0))))
              for prefix, info in before.items()]
    path.with_suffix('.prefix_stats.tsv').write_text('\n'.join(lines) + '\n')
    temporary.replace(path)
    manifest_path = path.with_suffix('.manifest.json')
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text())
        manifest['sha256'] = report['output_sha256']
        manifest['rules_after_category_filter'] = dict(sorted(Counter(
            r['rule'] for r in kept).items()))
        manifest['rule_counts_scope'] = 'rules[*].candidates are before category filtering'
        manifest['category_filter'] = {
            k: report[k] for k in ('input_sha256', 'exclusions_sha256',
                                  'before_relations', 'after_relations', 'removed_relations')}
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    print('Compound categories: %d -> %d relations; %d removed' % (
        len(rows), len(kept), len(rejected)), flush=True)
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', default='data/derived/verb_compound.jsonl')
    args = parser.parse_args()
    filter_dataset(args.input)
