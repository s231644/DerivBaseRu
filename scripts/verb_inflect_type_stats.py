#!/usr/bin/env python3
"""Describe stored automatic verb types separately from explicit CSV overrides."""
import argparse
from collections import Counter, defaultdict
import csv
import hashlib
import json
from pathlib import Path


def describe(mapping):
    histogram = Counter(len(types) for types in mapping.values())
    multi = sum(count for size, count in histogram.items() if size > 1)
    return {'verbs': len(mapping), 'multiple_types': multi,
            'multiple_percent': round(100 * multi / len(mapping), 4) if mapping else 0,
            'type_count_histogram': dict(sorted(histogram.items()))}


def collect(types_path, overrides_path, remaining_path=None):
    mapping = {word: tuple(sorted(set(types)))
               for word, types in json.loads(types_path.read_text()).items()}
    # Match the builder's override policy, including last-row-wins semantics.
    overrides = {}
    with overrides_path.open(encoding='utf-8') as stream:
        for row in csv.DictReader(stream, delimiter='\t'):
            word, value = (row.get('lemma') or '').strip(), (row.get('inflect_type') or '').strip()
            if word and value:
                overrides[word] = tuple(sorted({t.strip() for t in value.split(',') if t.strip()}))
    explicit = {w: t for w, t in mapping.items() if w in overrides}
    automatic = {w: t for w, t in mapping.items() if w not in overrides}
    combinations = defaultdict(list)
    for word, types in automatic.items():
        if len(types) > 1:
            combinations[types].append(word)
    groups = [{'types': list(types), 'verbs': len(words), 'examples': sorted(words)[:10]}
              for types, words in combinations.items()]
    groups.sort(key=lambda group: (-group['verbs'], group['types']))
    summary = {'schema': 1, 'scope': 'Stored final assignments; CSV overrides excluded from automatic group',
               'all': describe(mapping), 'automatic': describe(automatic),
               'csv_overrides': describe(explicit),
               'override_mismatches': sorted(w for w, t in explicit.items() if t != overrides[w]),
               'automatic_multitype_combinations': groups,
               'inputs': {}}
    inputs = {'types': types_path, 'csv_overrides': overrides_path}
    remaining_words = set()
    if remaining_path is not None:
        inputs['remaining_candidates'] = remaining_path
        parents_by_rule = defaultdict(set)
        counts_by_rule = defaultdict(Counter)
        for line in remaining_path.open(encoding='utf-8'):
            if not line.strip():
                continue
            record = json.loads(line)
            parents = {p['word'] for p in record.get('parents', []) if p.get('role') == 'head'}
            remaining_words.update(parents)
            rule = record['rule'].split('(', 1)[0]
            parents_by_rule[rule].update(parents)
            counts_by_rule[rule]['relations'] += 1
            if any(len(automatic.get(w, ())) > 1 for w in parents):
                counts_by_rule[rule]['relations_with_automatic_multitype_parent'] += 1
        def subset(words):
            return describe({w: automatic[w] for w in words if w in automatic})
        summary['remaining_candidates'] = {
            'unique_parent_words': len(remaining_words),
            'automatic_parents': subset(remaining_words),
            'by_rule': {rule: {'unique_parent_words': len(parents_by_rule[rule]),
                               'automatic_parents': subset(parents_by_rule[rule]),
                               **dict(counts_by_rule[rule])}
                        for rule in sorted(parents_by_rule)}}
    for name, path in inputs.items():
        summary['inputs'][name] = {'path': str(path),
                                  'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}
    rows = [(word, list(types), word in remaining_words)
            for word, types in sorted(automatic.items()) if len(types) > 1]
    return summary, rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--types', type=Path, default=Path('data/verb_inflect_types.json'))
    parser.add_argument('--overrides', type=Path, default=Path('data/verbs_roots.csv'))
    parser.add_argument('--remaining', type=Path,
                        help='optionally include parent statistics for a candidate JSONL')
    parser.add_argument('--summary', type=Path, default=Path('docs/verb_inflect_type_stats_2026.json'))
    parser.add_argument('--words', type=Path, default=Path('docs/verb_inflect_multitype_2026.tsv'))
    args = parser.parse_args()
    inputs = [args.types, args.overrides] + ([args.remaining] if args.remaining else [])
    if (args.summary.resolve() == args.words.resolve() or
            {p.resolve() for p in inputs} & {args.summary.resolve(), args.words.resolve()}):
        parser.error('Output paths must differ from each other and all inputs')
    summary, rows = collect(args.types, args.overrides, args.remaining)
    for path in (args.summary, args.words):
        path.parent.mkdir(parents=True, exist_ok=True)
    args.summary.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    with args.words.open('w', encoding='utf-8', newline='') as stream:
        writer = csv.writer(stream, delimiter='\t', lineterminator='\n')
        writer.writerow(['word', 'type_count', 'inflect_types', 'parent_in_remaining_candidates'])
        for word, types, in_remaining in rows:
            writer.writerow([word, len(types), ', '.join(types), int(in_remaining) if args.remaining else '-'])
    print(json.dumps({key: summary[key] for key in ('all', 'automatic', 'csv_overrides')},
                     ensure_ascii=False, indent=2))
    if args.remaining:
        print(json.dumps(summary['remaining_candidates'], ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
