"""Strict, reproducible first review of verb suffix candidates.

Review rule846–850 and rule842; trust regular rule930 as requested.
Unconfirmed rule842 pairs are quarantined, never called incorrect merely
because a dictionary lacks an aspect correspondence. Raw generation is retained.
"""
import argparse
from collections import Counter, defaultdict
import gzip
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
RULES = ROOT / 'derivbase_ru/rules/rus/verb/simple/verb=verb+sfx.json'
POLICY = ROOT / 'data/reviews/verb_sfx_policy.json'

from verb_suffix_type_review import (RARE_DECISIONS, TYPE7_DECISIONS, rare_decisions,
                                     type7_decisions, strong_signature, group_pending)


def normalize(text):
    return re.sub('[\u0301\u0300\u00b4]', '', text.lower()).replace('ё', 'е')


def correspondences(dictionary):
    """Only the explicit correspondence field; not synonyms or related words."""
    result = defaultdict(set)
    with gzip.open(dictionary, 'rt', encoding='utf-8') as stream:
        for line in stream:
            page = json.loads(line)
            for entry in page.get('entries', []):
                if entry.get('lang') != 'ru' or entry.get('pos') != 'гл':
                    continue
                text = entry.get('inflection', {}).get('params', {}).get('соотв', '')
                # [[lemma|accented display]]: use the lemma, not the display.
                text = re.sub(r'\[\[([^]|#]+)(?:#[^]|]*)?(?:\|[^]]*)?\]\]', r'\1', text)
                result[normalize(page['title'])].update(re.findall('[а-яё-]+', normalize(text)))
    return result


def key(record):
    return (record['rule'].split('(')[0], record['parents'][0]['word'], record['word'])


def classify(record, links, explicit, policy):
    rule, parent, word = key(record)
    latest = policy.get('_type7_decisions', {}).get((rule, parent, word))
    if latest:
        return latest['status'], 'explicit_type7plus_review', latest['reason']
    for status in ('rejected', 'pending', 'accepted'):
        for decision in policy.get(status, []):
            if (rule, parent, word) == (decision['rule'], decision['parent'], decision['word']):
                return status, 'manual_semantics', decision['reason']
    manual = policy.get('_rare_decisions', {}).get((rule, parent, word))
    if manual:
        return manual['status'], 'explicit_rare_type_review', manual['reason']
    if rule == 'rule930':
        return 'accepted', 'regular_rule_user', 'Регулярное присоединение -ся/-сь; проверка не требуется по указанию пользователя.'
    if rule in {'rule846', 'rule847', 'rule848', 'rule849', 'rule850'}:
        if (parent, word) in explicit[rule]:
            return 'accepted', 'explicit_rule_pair', 'Проверенная явно заданная пара непродуктивного типа.'
        if (rule == 'rule846' and parent in policy['accepted_rule846_generated']
                and parent.endswith('лечь') and word == parent[:-4] + 'ложить'):
            return 'accepted', 'manual_causative', 'Проверенное каузативное соответствие -лечь → -ложить.'
        return 'pending', 'unconfirmed_nonproductive_pair', 'Нет проверенной пары непродуктивного типа.'
    if rule == 'rule842':
        if (parent, word) in explicit[rule]:
            return 'accepted', 'explicit_rule_pair', 'Явное исключение, заданное в правиле.'
        a, b = normalize(parent), normalize(word)
        evidence = []
        if b in links.get(a, set()):
            evidence.append(parent + ':соотв→' + word)
        if a in links.get(b, set()):
            evidence.append(word + ':соотв→' + parent)
        if evidence:
            return 'accepted', 'wiktionary_correspondence', '; '.join(evidence)
        signature = strong_signature(record)
        if signature:
            return signature
        return 'pending', 'missing_pair_evidence', 'Нет явного соответствия в соотв; требуется отдельная семантическая проверка.'
    return 'untouched', '', ''


def review(output, dictionary):
    output = Path(output)
    raw = output.with_suffix('.raw.jsonl.gz')
    rules = json.loads(RULES.read_text())['data']
    explicit = {r['rule_id'].split('(')[0]: {tuple(pair.split(';')) for pair in r.get('rare', [])}
                for r in rules}
    policy = json.loads(POLICY.read_text())
    policy['_rare_decisions'] = rare_decisions()
    policy['_type7_decisions'] = type7_decisions()
    links = correspondences(dictionary)
    paths = {'main': output, 'pending': output.with_suffix('.semantic_pending.jsonl'),
             'rejected': output.with_suffix('.semantic_rejected.jsonl'),
             'doubtful': output.with_suffix('.doubtful.jsonl')}
    temporary = {name: path.with_name(path.name + '.tmp') for name, path in paths.items()}
    handles = {name: path.open('w', encoding='utf-8') for name, path in temporary.items()}
    counts = defaultdict(Counter)
    methods = defaultdict(Counter)
    try:
        with gzip.open(raw, 'rt', encoding='utf-8') as stream:
            for line in stream:
                record = json.loads(line)
                if not record.get('lexical_evidence'):
                    continue
                status, method, reason = classify(record, links, explicit, policy)
                counts[key(record)[0]][status] += 1
                methods[method or 'untouched'][status] += 1
                if status != 'untouched':
                    record.update(verified=status == 'accepted', review_status=status,
                                  review_method=method, review_reason=reason)
                target = {'accepted': 'main', 'untouched': 'main'}.get(status, status)
                serialized = json.dumps(record, ensure_ascii=False) + '\n'
                handles[target].write(serialized)
                # Doubtful remains a lexical subset of the current main file.
                if target == 'main' and record.get('review_status') != 'accepted' and record['lexical_evidence'] == ['dahl_token']:
                    handles['doubtful'].write(serialized)
    finally:
        for handle in handles.values():
            handle.close()
    for name, path in paths.items():
        temporary[name].replace(path)
    grouped = group_pending(output)
    files = {'raw': raw, 'dictionary': Path(dictionary), 'rules': RULES, 'policy': POLICY, 'review_script': Path(__file__), 'type_review_script': ROOT / 'scripts/verb_suffix_type_review.py',
             'rare_decisions': RARE_DECISIONS, 'type7_decisions': TYPE7_DECISIONS, **paths}
    report = {'scope': 'rule930 regular; rule846–850 reviewed; rule842 dictionary evidence, explicit rare-type/type7+ decisions and conservative signatures; rule836/840 untouched',
              'methods': {method: dict(values) for method, values in sorted(methods.items())},
              'pending_type_groups': len(grouped['groups']),
              'rules': {rule: dict(values) for rule, values in sorted(counts.items())},
              'files': {name: {'path': str(path), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}
                        for name, path in files.items()}}
    output.with_suffix('.semantic_review.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(report['rules'], ensure_ascii=False, indent=2))
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', default=str(ROOT / 'data/derived/verb_sfx.jsonl'))
    parser.add_argument('--dict', default=str(ROOT / 'data/wiktionary/parsed_ru.jsonl.gz'))
    args = parser.parse_args()
    review(args.out, args.dict)
