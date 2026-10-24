#!/usr/bin/env python3
"""Copy base verb types to remaining ambiguous reflexives, per user instruction."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path


def inherit_types(mapping):
    output = {word: list(types) for word, types in mapping.items()}
    rows = []
    for word, types in sorted(mapping.items()):
        if len(set(types)) < 2 or not word.endswith(('ся', 'сь')):
            continue
        base = word[:-2]
        inherited = mapping.get(base)
        status = 'missing_base' if not inherited else 'unchanged' if set(types) == set(inherited) else 'copied'
        if inherited:
            output[word] = sorted(set(inherited))
        rows.append({'word': word, 'base': base, 'before': types, 'after': output[word], 'status': status})
    return output, rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--types', type=Path, default=Path('data/verb_inflect_types.json'))
    parser.add_argument('--report', type=Path, default=Path('docs/verb_reflexive_type_inheritance_2026.json'))
    args = parser.parse_args()
    if args.types.resolve() == args.report.resolve():
        parser.error('Types and report paths must differ')
    before = args.types.read_bytes()
    mapping = json.loads(before)
    output, rows = inherit_types(mapping)
    serialized = json.dumps(output, ensure_ascii=False).encode('utf-8')
    report = {'basis': 'explicit_user_instruction_copy_nonreflexive_types',
              'reviewed': len(rows), 'statuses': dict(Counter(r['status'] for r in rows)),
              'resolved_to_single': sum(len(r['after']) == 1 for r in rows),
              'multitype_before': sum(len(set(t)) > 1 for t in mapping.values()),
              'multitype_after': sum(len(t) > 1 for t in output.values()),
              'before_sha256': hashlib.sha256(before).hexdigest(),
              'after_sha256': hashlib.sha256(serialized).hexdigest(), 'rows': rows}
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    args.types.write_bytes(serialized)
    print(json.dumps({k:v for k,v in report.items() if k != 'rows'}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
