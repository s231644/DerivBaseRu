#!/usr/bin/env python3
"""Export the current reviewed verb list; never run derivation generation."""
import argparse
from collections import Counter
import csv
import gzip
import hashlib
import json
from pathlib import Path

from verb_registry import ROOT, DEFAULT_REGISTRY


def load_json(path):
    return json.loads(path.read_text(encoding='utf-8'))


def reflexive_variant(variant, postfix):
    result = dict(variant)
    if result.get('meaning'):
        result['base_meaning'] = result.pop('meaning')
    result['infinitive'] += postfix
    if result.get('per1_sg'):
        result['per1_sg'] += 'сь' if result['per1_sg'][-1] in 'аеёиоуыэюя' else 'ся'
    result['basis'] = 'inherited_from_nonreflexive_paradigm'
    return result


def records(mapping):
    reviews = ROOT / 'docs'
    policy_path = ROOT / 'data/reviews/verb_inflect_nonreflexive_2026.json'
    llm = {r['word']: r for r in load_json(policy_path)['rows']}
    inherited = {r['word']: r for r in load_json(reviews / 'verb_reflexive_type_inheritance_2026.json')['rows']}
    refinements = {r['word']: r for r in load_json(reviews / 'verb_inflect_type_refinement_2026.json')['changes']}
    roots = {r['word']: r for r in load_json(reviews / 'verb_type_root_audit_2026.json')['records'] if r['changed']}
    explicit = set()
    base_inventory = {}
    excluded = {line.split('#', 1)[0].strip() for line in (ROOT / 'data/pseudo_lemmas.txt').read_text().splitlines()}
    with (ROOT / 'data/verbs_roots.csv').open(encoding='utf-8') as stream:
        for r in csv.DictReader(stream, delimiter='\t'):
            if r['inflect_type'].strip():
                word = r['lemma'].strip()
                explicit.add(word)
                item = base_inventory.setdefault(word, {'types': set(), 'real': False})
                item['types'].update(t.strip() for t in r['inflect_type'].split(',') if t.strip())
                item['real'] |= r.get('real') == '1'
    from verb_type2_policy import type2_ending
    result = []
    for word, types in sorted(mapping.items(), key=lambda pair: (pair[0].replace('ё', 'е'), pair[0])):
        row = {'schema': 1, 'word': word, 'pos': 'verb', 'inflect_type': types,
               'reflexive': word.endswith(('ся', 'сь')), 'generation_excluded': word in excluded,
               'review_status': 'automatic',
               'ambiguity': 'unresolved' if len(types) > 1 else 'none',
               'type_sources': ['automatic'], 'variants': [], 'notes': []}
        if word in explicit:
            row['review_status'] = 'explicit_csv'
            row['type_sources'] = ['data/verbs_roots.csv']
            row['base_inventory_types'] = sorted(base_inventory[word]['types'])
            row['base_real'] = base_inventory[word]['real']
            if set(types) != base_inventory[word]['types']:
                row['notes'].append('CSV содержит омонимичные основы разных типов; плоское назначение сохранено, все типы основ перечислены в base_inventory_types.')
        for ledger, source in [(refinements, 'dictionary_refinement'), (roots, 'root_prefix_constraint')]:
            if word in ledger and set(ledger[word]['after']) == set(types):
                row['type_sources'].append(source)
        if type2_ending(word) and types == ['2']:
            row['review_status'] = 'explicit_user_rule'
            row['type_sources'].append('user_type2_ovat_irovat')
        if word in llm:
            decision = llm[word]
            row['review_status'] = decision['status']
            row['type_sources'].append('data/reviews/verb_inflect_nonreflexive_2026.json')
            if set(decision['types']) != set(types):
                raise ValueError('Stale LLM decision for ' + word)
            row['variants'] = decision['variants']
            row['notes'].append(decision['reason'])
            if decision['status'] == 'retained_variants':
                row['ambiguity'] = 'confirmed_variants'
        if word in inherited:
            transfer = inherited[word]
            if transfer['status'] == 'missing_base':
                row['review_status'] = 'pending_missing_base'
                row['notes'].append('Невозвратной основы нет в справочнике: ' + transfer['base'])
            else:
                base = transfer['base']
                if base not in mapping or set(mapping[base]) != set(types):
                    raise ValueError('Stale inheritance for ' + word)
                row['inherited_from'] = base
                row['review_status'] = 'inherited'
                row['type_sources'].append('user_reflexive_inheritance')
                base_review = llm.get(base)
                if base_review:
                    row['base_review_status'] = base_review['status']
                    row['variants'] = [reflexive_variant(v, word[-2:]) for v in base_review['variants']]
                    if base_review['status'] == 'retained_variants':
                        row['ambiguity'] = 'confirmed_variants'
        row['needs_review'] = row['ambiguity'] == 'unresolved'
        result.append(row)
    return result


def export_registry(types_path=ROOT / 'data/verb_inflect_types.json',
                    output=DEFAULT_REGISTRY, table=ROOT / 'data/verbs_registry.tsv',
                    manifest=ROOT / 'docs/verb_registry_2026.json'):
    mapping = load_json(Path(types_path))
    rows = records(mapping)
    payload = ''.join(json.dumps(r, ensure_ascii=False, separators=(',', ':'))+'\n' for r in rows).encode('utf-8')
    for p in (output, table, manifest):
        Path(p).parent.mkdir(parents=True, exist_ok=True)
    Path(output).write_bytes(gzip.compress(payload, mtime=0))
    with Path(table).open('w', encoding='utf-8', newline='') as stream:
        writer = csv.writer(stream, delimiter='\t', lineterminator='\n')
        writer.writerow(['word', 'inflect_types', 'review_status', 'ambiguity', 'inherited_from',
                         'accented_paradigms', 'type_sources', 'generation_excluded', 'base_inventory_types', 'notes'])
        for r in rows:
            variants = '; '.join(v['infinitive'] + (' → '+v['per1_sg'] if v.get('per1_sg') else '')+
                                 ' ['+v['inflect_type']+']'+(' — '+v['meaning'] if v.get('meaning') else '')
                                 for v in r['variants']) or '-'
            writer.writerow([r['word'], ', '.join(r['inflect_type']), r['review_status'], r['ambiguity'],
                             r.get('inherited_from', '-'), variants, ', '.join(r['type_sources']),
                             int(r['generation_excluded']), ', '.join(r.get('base_inventory_types', [])) or '-',
                             '; '.join(r['notes']) or '-'])
    sources = [Path(types_path), ROOT / 'data/reviews/verb_inflect_nonreflexive_2026.json',
               ROOT / 'data/verbs_roots.csv', ROOT / 'data/pseudo_lemmas.txt',
               ROOT / 'docs/verb_reflexive_type_inheritance_2026.json',
               ROOT / 'docs/verb_inflect_type_refinement_2026.json', ROOT / 'docs/verb_type_root_audit_2026.json']
    relative = lambda p: str(Path(p).resolve().relative_to(ROOT)) if Path(p).resolve().is_relative_to(ROOT) else str(p)
    summary = {'schema': 1, 'verbs': len(rows), 'multitype': sum(len(r['inflect_type']) > 1 for r in rows),
               'ambiguity': dict(Counter(r['ambiguity'] for r in rows)),
               'generation_excluded': sum(r['generation_excluded'] for r in rows),
               'review_status': dict(Counter(r['review_status'] for r in rows)),
               'inputs': {relative(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},
               'outputs': {relative(p): hashlib.sha256(Path(p).read_bytes()).hexdigest() for p in (output, table)}}
    Path(manifest).write_text(json.dumps(summary, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    return summary


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--types', type=Path, default=ROOT / 'data/verb_inflect_types.json')
    parser.add_argument('--out', type=Path, default=DEFAULT_REGISTRY)
    parser.add_argument('--table', type=Path, default=ROOT / 'data/verbs_registry.tsv')
    parser.add_argument('--manifest', type=Path, default=ROOT / 'docs/verb_registry_2026.json')
    args = parser.parse_args()
    paths = (args.types, args.out, args.table, args.manifest)
    if len({p.resolve() for p in paths}) != 4:
        parser.error('Input and output paths must differ')
    print(json.dumps(export_registry(*paths), ensure_ascii=False, indent=2))
