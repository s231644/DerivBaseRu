#!/usr/bin/env python3
"""Constrain rare verb classes by the project's closed inventory of base verbs."""
import argparse
from collections import defaultdict, Counter
import csv
import hashlib
import json
from pathlib import Path
import re

from refine_verb_inflect_types import PREFIXES, norm


def families(path):
    roots = defaultdict(set)
    explicit = set()
    with Path(path).open(encoding='utf-8') as stream:
        for row in csv.DictReader(stream, delimiter='\t'):
            word = row['lemma'].strip()
            for value in row['inflect_type'].split(','):
                value = value.strip()
                if not value:
                    continue
                explicit.add(word)
                number = re.match(r'\d+', value)
                if not number or int(number[0]) >= 7:
                    roots[value].add(norm(word))
    # Union duplicate rows: жать belongs to both 14м and 14н. Pseudo-roots
    # (real=0) are intentional morphological bases and must also be included.
    return dict(roots), explicit


def decomposition(word, roots):
    word = re.sub(r'(ся|сь)$', '', norm(word))
    choices = []
    for root in sorted(roots):
        surfaces = {'идти': {'идти', 'йти'}, 'ять': {'ять', 'нять'}}.get(root, {root})
        for surface in surfaces:
            if not word.endswith(surface):
                continue
            prefix = word[:-len(surface)]
            # Boundary hard sign before a vowel is orthography, not an affix.
            if prefix.endswith('ъ') and surface.startswith(('е', 'ю', 'я')):
                prefix = prefix[:-1]
            paths = {0: []}
            for index in range(len(prefix)):
                if index not in paths:
                    continue
                for affix in sorted(PREFIXES, key=lambda a: (-len(a), a)):
                    if prefix.startswith(affix, index):
                        end = index + len(affix)
                        candidate = paths[index] + [affix]
                        if end not in paths or (len(candidate), candidate) < (len(paths[end]), paths[end]):
                            paths[end] = candidate
            if len(prefix) in paths:
                choices.append({'root': root, 'surface': surface, 'prefixes': paths[len(prefix)]})
    return min(choices, key=lambda c: (len(c['prefixes']), c['root'], c['prefixes'])) if choices else None


def refine_by_roots(mapping, inventory):
    roots, explicit = families(inventory)
    output = {w: sorted(set(t)) for w, t in mapping.items()}
    audit = []
    for word, types in sorted(output.items()):
        if word in explicit:
            continue
        unsupported, supported, unavailable = [], {}, []
        for value in types:
            number = re.match(r'\d+', value)
            if number and int(number[0]) < 7:
                continue
            if value not in roots:
                unavailable.append(value)
                continue
            analysis = decomposition(word, roots[value])
            if analysis is None:
                unsupported.append(value)
            else:
                supported[value] = analysis
        if not unsupported and not unavailable:
            continue
        remaining = [t for t in types if t not in unsupported]
        # Root inventory is a necessary constraint, not a way to invent a
        # productive class for a word whose only assignment is unsupported.
        changed = bool(unsupported and remaining)
        if changed:
            output[word] = remaining
        audit.append({'word': word, 'before': types, 'after': output[word],
                      'changed': changed, 'unsupported_types': unsupported,
                      'supported_rare_types': supported, 'unavailable_inventory': unavailable,
                      'status': 'narrowed' if changed else 'unresolved'})
    return output, audit


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--types', type=Path, default=Path('data/verb_inflect_types.json'))
    parser.add_argument('--roots', type=Path, default=Path('data/verbs_roots.csv'))
    parser.add_argument('--report', type=Path, default=Path('docs/verb_type_root_audit_2026.json'))
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    if len({p.resolve() for p in (args.types, args.roots, args.report)}) != 3:
        parser.error('Paths must be distinct')
    before = args.types.read_bytes()
    mapping = json.loads(before)
    output, audit = refine_by_roots(mapping, args.roots)
    serialized = json.dumps(output, ensure_ascii=False).encode('utf-8')
    report = {'applied': args.apply,
              'before_sha256': hashlib.sha256(before).hexdigest(),
              'proposed_sha256': hashlib.sha256(serialized).hexdigest(),
              'inventory_sha256': hashlib.sha256(args.roots.read_bytes()).hexdigest(), 'before_multitype': sum(len(set(t)) > 1 for t in mapping.values()),
              'after_multitype': sum(len(t) > 1 for t in output.values()),
              'changed': sum(r['changed'] for r in audit),
              'statuses': dict(Counter(r['status'] for r in audit)), 'records': audit}
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    if args.apply:
        args.types.write_bytes(serialized)
    print(json.dumps({k: v for k, v in report.items() if k != 'records'}, ensure_ascii=False))


if __name__ == '__main__':
    main()
