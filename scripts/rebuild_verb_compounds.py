"""Rebuild Wiktionary-attested rule961 candidates without a modifier limit.

Index every modifier's interfix forms, split attested verbs, then validate each
pair with the engine. Dictionary attestation does not verify derivation.
"""
import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
from importlib.metadata import version

import pymorphy3

from run_pipeline import (
    Derivation, apply_compound_rule, build_record, parent,
    read_dictionary, single_word,
)
from compound_morphology import INFLECTION_PATH, checked_modifier_forms
from filter_verb_compounds import filter_dataset


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dict', default='data/wiktionary/parsed_ru.jsonl.gz')
    parser.add_argument('--out', default='data/derived/verb_compound.jsonl')
    args = parser.parse_args()
    buckets, known, pages = read_dictionary(args.dict)
    excluded = {
        line.split('#', 1)[0].strip()
        for line in Path('data/pseudo_lemmas.txt').read_text().splitlines()
    }
    sources = {
        pos: {w for w in words if single_word(w) and w not in excluded}
        for pos, words in buckets.items()
    }
    rules = [r for r in Derivation(lang='rus').loaded_rules['compound']
             if r.pos_a == 'verb']
    morph = pymorphy3.MorphAnalyzer()
    output = Path(args.out)
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = output.with_suffix('.jsonl.tmp')
    stats = {}
    with temporary.open('w') as stream:
        for rule in sorted(rules, key=lambda r: r.name):
            # This indexed search is exact only for an unchanged verb head
            # and a single modifier before it, without post-merge operations.
            if (rule.poss_m not in [['noun'], ['adj']]
                    or list(rule.order) != [1, 0]
                    or rule.simple_rules[0]
                    or getattr(rule, 'after_merge_rules', [])
                    or getattr(rule, 'separator', '')):
                raise ValueError('Unsupported compound structure: ' + rule.name)
            pos = rule.poss_m[0]
            forms = defaultdict(set)
            proofs = {}
            rejected = Counter()
            types = Counter()
            for modifier in sorted(sources[pos]):
                current, reason = checked_modifier_forms(
                    modifier, pos, rule.simple_rules[1], morph)
                if reason:
                    rejected[reason] += 1
                types.update({t for evidence in current.values()
                              for e in evidence for t in e['inflect_type']})
                for form, evidence in current.items():
                    if form:
                        forms[form].add(modifier)
                        proofs[(form, modifier)] = evidence
            count = 0
            for word in sorted(buckets['verb']):
                if not single_word(word) or word in excluded:
                    continue
                for split in range(1, len(word)):
                    form, head = word[:split], word[split:]
                    if head not in sources['verb']:
                        continue
                    for modifier in sorted(forms.get(form, ())):
                        if modifier == head:
                            continue
                        inputs = {modifier} | {
                            e['stem'] for e in proofs[(form, modifier)]}
                        if not any(word in apply_compound_rule(rule, head, source, True)
                                   for source in inputs):
                            raise AssertionError((word, head, modifier))
                        parents = [parent(head, 'verb', 'head', 1),
                                   parent(modifier, pos, 'modifier', 0)]
                        parents[1]['form'] = form
                        parents[1]['morphology_evidence'] = proofs[(form, modifier)]
                        record = build_record(word, 'verb', parents, rule,
                                              buckets['verb'][word], known, False,
                                              include_flags=False, kind='compound')
                        record.update(verified=False, verified_by=['wiktionary'],
                                      review_status='pending',
                                      lexeme_verified=True)
                        stream.write(json.dumps(record, ensure_ascii=False) + '\n')
                        count += 1
            stats[rule.name] = {'modifiers': len(sources[pos]),
                                'modifier_forms': len(forms), 'candidates': count,
                                'modifier_declension_types': dict(sorted(types.items())),
                                'excluded_modifiers': dict(sorted(rejected.items()))}
            print(rule.name, stats[rule.name], flush=True)
    temporary.replace(output)
    manifest = {'dictionary': args.dict, 'pages': pages, 'rules': stats,
                'morphology_policy': 'known common declinable lemma; per-parse declension tags; genitive stem or explicit rule exception; explicit interfix',
                'declension_rules_sha256': hashlib.sha256(INFLECTION_PATH.read_bytes()).hexdigest(),
                'pymorphy3': version('pymorphy3'),
                'pymorphy3-dicts-ru': version('pymorphy3-dicts-ru'),
                'scope': 'Wiktionary verbs; semantic review pending; Dahl not included',
                'sha256': hashlib.sha256(output.read_bytes()).hexdigest()}
    output.with_suffix('.manifest.json').write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    filter_dataset(output)


if __name__ == '__main__':
    main()
