#!/usr/bin/env python3
"""Apply the versioned LLM review of non-reflexive verb types; no derivation generation."""
import argparse
from collections import Counter
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / 'data/reviews/verb_inflect_nonreflexive_2026.json'


def apply_review(mapping, policy=POLICY):
    rows = json.loads(Path(policy).read_text(encoding='utf-8'))['rows']
    output = {w: list(t) for w, t in mapping.items()}
    seen = set()
    for row in rows:
        word = row['word']
        if word in seen or word.endswith(('ся', 'сь')) or not row['types']:
            raise ValueError('Invalid non-reflexive review: ' + word)
        seen.add(word)
        if row['status'] not in {'resolved', 'retained_variants', 'pending'}:
            raise ValueError('Unknown review status: ' + row['status'])
        if row['status'] != 'pending':
            output[word] = sorted(set(row['types']))
    return output, sorted(rows, key=lambda r: r['word'])


def write_report(rows, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', encoding='utf-8', newline='') as stream:
        writer = csv.writer(stream, delimiter='\t', lineterminator='\n')
        writer.writerow(['word', 'before', 'inflect_types', 'status', 'accented_variants', 'reason'])
        for r in rows:
            forms = '; '.join(v['infinitive'] +
                              (' → ' + v['per1_sg'] if v.get('per1_sg') else '') +
                              ' [' + v['inflect_type'] + ']' +
                              (' — ' + v['meaning'] if v.get('meaning') else '')
                              for v in r['variants']) or '-'
            writer.writerow([r['word'], ', '.join(r['before']), ', '.join(r['types']),
                             r['status'], forms, r['reason']])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--types', type=Path, default=ROOT / 'data/verb_inflect_types.json')
    parser.add_argument('--policy', type=Path, default=POLICY)
    parser.add_argument('--report', type=Path, default=ROOT / 'docs/verb_inflect_nonreflexive_review_2026.tsv')
    parser.add_argument('--summary', type=Path, default=ROOT / 'docs/verb_inflect_llm_review_2026.json')
    args = parser.parse_args()
    if len({p.resolve() for p in (args.types, args.policy, args.report, args.summary)}) != 4:
        parser.error('Paths must differ')
    original = args.types.read_bytes()
    mapping = json.loads(original)
    output, rows = apply_review(mapping, args.policy)
    # Separate lexical keys stay unaccented; stress belongs to individual
    # homograph/paradigm records in the policy and the human-readable report.
    args.types.write_text(json.dumps(output, ensure_ascii=False), encoding='utf-8')
    write_report(rows, args.report)
    summary = {'reviewer': 'LLM', 'reviewed_nonreflexive': len(rows),
               'statuses': dict(Counter(r['status'] for r in rows)),
               'changed_assignments': sum(set(mapping.get(w, [])) != set(t) for w, t in output.items()),
               'multitype_before': sum(len(t) > 1 for t in mapping.values()),
               'multitype_after': sum(len(t) > 1 for t in output.values()),
               'before_sha256': hashlib.sha256(original).hexdigest(),
               'after_sha256': hashlib.sha256(args.types.read_bytes()).hexdigest(),
               'policy_sha256': hashlib.sha256(args.policy.read_bytes()).hexdigest()}
    args.summary.parent.mkdir(parents=True, exist_ok=True)
    args.summary.write_text(json.dumps(summary, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
