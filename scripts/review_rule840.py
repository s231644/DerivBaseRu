#!/usr/bin/env python3
"""Apply the complete, versioned LLM review to the existing rule840 snapshot."""
import argparse
from collections import Counter
import copy
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / 'data/reviews/verb_rule840_semantic_2026.json'


def key(record):
    return record['parents'][0]['word'], record['word'], record['rule']


def partition(records, decisions):
    selected = [r for r in records if r['rule'].startswith('rule840(')]
    lookup = {(d['parent'], d['word'], d['rule']): d for d in decisions}
    if len(lookup) != len(decisions) or len({key(r) for r in selected}) != len(selected):
        raise ValueError('Duplicate relation/review key')
    if set(lookup) != {key(r) for r in selected}:
        raise ValueError('Review must cover exactly every rule840 relation in the input')
    groups = {status: [] for status in ('accepted', 'rejected', 'pending')}
    for record in sorted(selected, key=key):
        decision = lookup[key(record)]
        status = decision['status']
        if status not in groups or not decision.get('reason'):
            raise ValueError('Invalid review decision')
        updated = copy.deepcopy(record)
        updated.update(verified=status == 'accepted', review_status=status,
                       semantic_review={'reviewer': 'LLM', 'reason': decision['reason'],
                                        'sources': decision['sources']})
        groups[status].append(updated)
    return groups


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, default=ROOT / 'data/derived/verb_sfx.remaining.jsonl')
    parser.add_argument('--policy', type=Path, default=POLICY)
    args = parser.parse_args()
    policy = json.loads(args.policy.read_text())
    digest = hashlib.sha256(args.input.read_bytes()).hexdigest()
    if digest != policy['input_sha256']:
        parser.error('Input snapshot changed; review coverage and meanings must be checked again')
    groups = partition([json.loads(l) for l in args.input.read_text().splitlines() if l.strip()], policy['decisions'])
    outputs = {}
    for status, records in groups.items():
        path = args.input.parent / ('verb_sfx.rule840.' + status + '.jsonl')
        path.write_text(''.join(json.dumps(r, ensure_ascii=False)+'\n' for r in records), encoding='utf-8')
        outputs[status] = {'path': str(path.relative_to(ROOT)), 'rows': len(records),
                           'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}
    table = ROOT / 'docs/verb_rule840_semantic_review_2026.tsv'
    with table.open('w', encoding='utf-8', newline='') as stream:
        writer = csv.writer(stream, delimiter='\t', lineterminator='\n')
        writer.writerow(['parent', 'word', 'decision', 'reason'])
        for d in sorted(policy['decisions'], key=lambda d: (d['word'], d['parent'])):
            writer.writerow([d['parent'], d['word'], d['status'], d['reason']])
    report = {'scope': '208 rule840 relations only; source candidates and other rules unchanged',
              'input_sha256': digest, 'policy_sha256': hashlib.sha256(args.policy.read_bytes()).hexdigest(),
              'counts': dict(Counter(d['status'] for d in policy['decisions'])), 'outputs': outputs}
    (ROOT / 'docs/verb_rule840_semantic_review_2026.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(report['counts'], ensure_ascii=False))


if __name__ == '__main__':
    main()
