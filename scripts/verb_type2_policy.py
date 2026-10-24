#!/usr/bin/env python3
"""Apply the user's explicit -ировать(ся)/-овать(ся) => type 2 policy."""
import argparse
import gzip
import hashlib
import json
from pathlib import Path
import re


def type2_ending(word):
    word = re.sub('[\u0300\u0301]', '', word.lower())
    if word.endswith('ся'):
        word = word[:-2]
    return word.endswith(('ировать', 'овать'))


def apply_type2(mapping, words=()):
    output = {word: list(types) for word, types in mapping.items()}
    changes = []
    for word in sorted(set(mapping) | set(words)):
        if type2_ending(word) and output.get(word) != ['2']:
            changes.append({'word': word, 'before': output.get(word, []), 'after': ['2']})
            output[word] = ['2']
    return output, changes


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--types', type=Path, default=Path('data/verb_inflect_types.json'))
    parser.add_argument('--dictionary', type=Path, default=Path('data/wiktionary/parsed_ru.jsonl.gz'))
    parser.add_argument('--report', type=Path, default=Path('docs/verb_type2_policy_2026.json'))
    args = parser.parse_args()
    if len({p.resolve() for p in (args.types, args.dictionary, args.report)}) != 3:
        parser.error('Input and report paths must be distinct')
    before = args.types.read_bytes()
    mapping = json.loads(before)
    words = set()
    with gzip.open(args.dictionary, 'rt', encoding='utf-8') as stream:
        for line in stream:
            record = json.loads(line)
            word = record.get('title', '')
            if ' ' not in word and any(e.get('pos') == 'гл' for e in record.get('entries', [])):
                words.add(word)
    output, changes = apply_type2(mapping, words)
    serialized = json.dumps(output, ensure_ascii=False).encode('utf-8')
    summary = {'basis': 'explicit_user_suffix_policy', 'changed': len(changes),
               'new_assignments': sum(not r['before'] for r in changes),
               'matched': sum(type2_ending(w) for w in output),
               'before_multitype': sum(len(t) > 1 for t in mapping.values()),
               'after_multitype': sum(len(t) > 1 for t in output.values()),
               'before_sha256': hashlib.sha256(before).hexdigest(),
               'after_sha256': hashlib.sha256(serialized).hexdigest(), 'changes': changes}
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    args.types.write_bytes(serialized)
    print(json.dumps({k: v for k, v in summary.items() if k != 'changes'}, ensure_ascii=False))


if __name__ == '__main__':
    main()
