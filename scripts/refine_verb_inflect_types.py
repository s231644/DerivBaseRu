#!/usr/bin/env python3
"""Resolve stored ambiguous verb types using attested paradigms, not prediction scores."""
import argparse
from collections import Counter
import csv
import gzip
import hashlib
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from derivbase_ru.guesser.ZaliznyakGuesser import ZaliznyakGuesser

PREFIXES = {'без', 'бес', 'в', 'во', 'вз', 'взо', 'воз', 'возо', 'вос', 'вы', 'до',
            'за', 'из', 'изо', 'ис', 'на', 'над', 'надо', 'недо', 'низ', 'нис', 'о',
            'об', 'обо', 'обез', 'обес', 'от', 'ото', 'пере', 'по', 'под', 'подо',
            'пре', 'пред', 'предо', 'при', 'про', 'раз', 'разо', 'рас', 'с', 'со', 'у',
            'полу', 'само'}
TYPE11_ROOTS = {'бить', 'вить', 'лить', 'пить', 'шить'}
BASIC = {'1', '2', '3', '4', '5', '6', '9', '11', '13', '15', '16'}


def norm(word):
    return re.sub('[\u0300\u0301]', '', word.lower()).replace('ё', 'е')


def prefixed_root(word, roots):
    word = re.sub('(ся|сь)$', '', norm(word))
    for root in roots:
        if not word.endswith(root):
            continue
        prefix = word[:-len(root)]
        reachable = {0}
        for index in range(len(prefix)):
            if index in reachable:
                for part in PREFIXES:
                    if prefix.startswith(part, index):
                        reachable.add(index + len(part))
        if len(prefix) in reachable:
            return True
    return False


def template_types(path):
    result = {}
    with gzip.open(path, 'rt', encoding='utf-8') as stream:
        for line in stream:
            record = json.loads(line)
            entries = [e for e in record.get('entries', []) if e.get('pos') == 'гл']
            if not entries:
                continue
            types, complete = set(), True
            for entry in entries:
                template = (entry.get('inflection') or {}).get('template', '')
                match = re.fullmatch(r'гл ru (\d+)[abcабвABC/0-9*°()\s-]*', template)
                if match:
                    types.add(match[1])
                else:
                    complete = False
            if complete:
                result[norm(record['title'])] = types
    return result


def main_type(value):
    match = re.match(r'\d+', value)
    return match[0] if match else value


def refine_mapping(mapping, dictionary, overrides, guesser=None):
    guesser = guesser or ZaliznyakGuesser(use_morph=True)
    explicit = set()
    with Path(overrides).open(encoding='utf-8') as stream:
        for row in csv.DictReader(stream, delimiter='\t'):
            if (row.get('inflect_type') or '').strip():
                explicit.add(row['lemma'].strip())
    templates = template_types(dictionary)
    output = {w: sorted(set(t)) for w, t in mapping.items()}
    audit = []
    for word, original in sorted(mapping.items()):
        old = set(original)
        if word in explicit or (len(old) < 2 and '11' not in old):
            continue
        parsed = [p for p in guesser.morph.parse(word)
                  if p.tag.POS == 'INFN' and norm(p.normal_form) == norm(word)]
        known = [p for p in parsed if p.is_known]
        evidence, attested = [], set()
        for p in known:
            one, three = p.inflect({'1per', 'sing'}), p.inflect({'3per', 'sing'})
            if not one or not three:
                continue
            variants = guesser.guess(word=word, pos='verb', per1=norm(one.word), per3=norm(three.word))
            found = {t for v in variants for t in v.get('inflect_type', [])}
            attested.update(found)
            evidence.append({'source': 'pymorphy3_known', 'per1': one.word, 'per3': three.word,
                             'types': sorted(found)})
        declared = templates.get(norm(word))
        new = set(old)
        if declared:
            # Keep subtype detail when available; only introduce an unambiguous
            # basic class when explicitly declared and absent in the old union.
            selected = {t for t in old | attested if main_type(t) in declared}
            missing = declared - {main_type(t) for t in selected}
            if missing <= BASIC:
                new = selected | missing
                evidence.append({'source': 'wiktionary_template', 'classes': sorted(declared)})
        elif attested:
            # Predictions from unknown-word analyzers are never used as proof.
            new = attested
        # Reject spurious closed-paradigm predictions only without an explicit
        # dictionary declaration of that class. Keep unresolved words nonempty.
        if '11' in new and not prefixed_root(word, TYPE11_ROOTS) and not (declared and '11' in declared):
            new.remove('11')
            evidence.append({'source': 'type11_root_prefix_guard'})
        if 'дать' in new and not prefixed_root(word, {'дать'}):
            new.remove('дать')
            evidence.append({'source': 'dat_root_prefix_guard'})
        if not new:
            new = old
            evidence.append({'source': 'unresolved_empty_result_preserved'})
        if new != old or len(old) > 1 or evidence:
            audit.append({'word': word, 'before': sorted(old), 'after': sorted(new),
                          'changed': new != old, 'evidence': evidence,
                          'pymorphy_known': bool(known),
                          'prediction_only': bool(parsed) and not known})
        output[word] = sorted(new)
    return output, audit


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--types', type=Path, default=ROOT / 'data/verb_inflect_types.json')
    parser.add_argument('--dictionary', type=Path, default=ROOT / 'data/wiktionary/parsed_ru.jsonl.gz')
    parser.add_argument('--overrides', type=Path, default=ROOT / 'data/verbs_roots.csv')
    parser.add_argument('--audit', type=Path, default=ROOT / 'data/derived/verb_inflect_type_refinement.jsonl')
    parser.add_argument('--summary', type=Path, default=ROOT / 'docs/verb_inflect_type_refinement_2026.json')
    args = parser.parse_args()
    paths = [args.types, args.dictionary, args.overrides, args.audit, args.summary]
    if len({p.resolve() for p in paths}) != len(paths):
        parser.error('Input and output paths must be distinct')
    before = args.types.read_bytes()
    mapping = json.loads(before)
    output, audit = refine_mapping(mapping, args.dictionary, args.overrides)
    args.types.write_text(json.dumps(output, ensure_ascii=False), encoding='utf-8')
    args.audit.parent.mkdir(parents=True, exist_ok=True)
    args.audit.write_text(''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in audit), encoding='utf-8')
    summary = {'before_sha256': hashlib.sha256(before).hexdigest(),
               'after_sha256': hashlib.sha256(args.types.read_bytes()).hexdigest(),
               'before_histogram': dict(sorted(Counter(len(set(t)) for t in mapping.values()).items())),
               'after_histogram': dict(sorted(Counter(len(t) for t in output.values()).items())),
               'changed': sum(r['changed'] for r in audit),
               'resolved_to_single': sum(r['changed'] and len(r['before']) > 1 and len(r['after']) == 1 for r in audit),
               'changes': [r for r in audit if r['changed']]}
    args.summary.parent.mkdir(parents=True, exist_ok=True)
    args.summary.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k: v for k, v in summary.items() if k != 'changes'}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
