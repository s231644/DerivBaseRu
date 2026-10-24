#!/usr/bin/env python3
"""Prioritize existing rule836 candidates using transparent, non-destructive signals."""
import argparse
from collections import Counter, defaultdict
import csv
import gzip
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def norm(word):
    return re.sub('[\u0300\u0301]', '', word.lower()).replace('ё', 'е')


def nonreflexive(word):
    return re.sub(r'(ся|сь)$', '', norm(word))


def conservative_stems(word, types):
    """Diagnostic intact stems; NOT an exhaustive list of legitimate alternations."""
    word = nonreflexive(word)
    stems = set()
    for value in types:
        if value == '2':
            endings = ('ировать', 'овать', 'евать')
        elif value in {'1', '4', '4щ', '4*', '5', '5щ', '6', '6щ'}:
            endings = ('ать', 'ять', 'еть', 'ить')
        elif value.startswith('7'):
            for ending in ('ти', 'ть'):
                if word.endswith(ending):
                    stem = word[:-len(ending)]
                    replacement = {'7т': 'т', '7д': 'д', '7б': 'б', '7ст': 'ст'}.get(value)
                    stems.add(stem[:-1] + replacement if replacement and stem.endswith('с') else stem)
            continue
        elif value.startswith('10'):
            if word.endswith('оть'):
                stem = word[:-3]
                if value == '10ел' and stem.endswith('ол'):
                    stem = stem[:-2] + 'ел'
                stems.add(stem)
                if stem.endswith('л'):
                    stems.add(stem + 'ь')
            continue
        elif value in {'11', '12у', '15'}:
            endings = ('ть',)
        else:
            continue
        for ending in endings:
            if word.endswith(ending):
                stems.add(word[:-len(ending)])
    return stems


def dictionary_signals(path, wanted):
    links, definitions = defaultdict(set), defaultdict(list)
    with gzip.open(path, 'rt', encoding='utf-8') as stream:
        for line in stream:
            page = json.loads(line)
            title = norm(page.get('title', ''))
            if title not in wanted:
                continue
            for entry in page.get('entries', []):
                if entry.get('pos') != 'гл' or entry.get('lang') != 'ru':
                    continue
                params = (entry.get('inflection') or {}).get('params', {})
                text = params.get('соотв', '')
                text = re.sub(r'\[\[([^]|#]+)(?:#[^]|]*)?(?:\|[^]]*)?\]\]', r'\1', text)
                links[title].update(re.findall('[а-яё-]+', norm(text)))
                definitions[title].extend(entry.get('senses') or [])
    return links, definitions


def analyze(records, links, definitions):
    selected = [r for r in records if r['rule'].startswith('rule836(')]
    parents = defaultdict(set)
    for r in selected:
        parents[r['word']].add(r['parents'][0]['word'])
    result = []
    for r in selected:
        source, target = r['parents'][0]['word'], r['word']
        a, b = norm(source), norm(target)
        base = nonreflexive(target)
        expected = conservative_stems(source, r['parents'][0].get('inflect_type') or [])
        shape = 'intact_stem' if base.endswith('нуть') and base[:-4] in expected else 'extra_stem_change'
        paired = b in links.get(a, set()) or a in links.get(b, set())
        glosses = definitions.get(b, [])
        gloss = norm(' '.join(glosses))
        # These are search cues, not proofs of semantic equivalence.
        event_cue = bool(re.search(r'однократ|один раз|одним |резк|сильно|быстро', gloss))
        state_cue = bool(re.search(r'\bстать\b|становиться|постепенно|утратить', gloss))
        parent_mention = any(a in re.findall('[а-яё-]+', norm(g)) for g in glosses)
        token_only = r.get('lexical_evidence') == ['dahl_token']
        flags = []
        if paired: flags.append('dictionary_correspondence')
        if parent_mention: flags.append('parent_in_definition')
        if event_cue: flags.append('event_gloss_cue')
        if state_cue: flags.append('state_gloss_cue')
        if shape != 'intact_stem': flags.append(shape)
        if token_only: flags.append('dahl_token_only')
        if len(parents[target]) > 1: flags.append('competing_parents')
        priority = ('dictionary_supported' if paired else
                    'risky_stem_change' if shape != 'intact_stem' else
                    'weak_lexeme_evidence' if token_only else 'semantic_review')
        result.append({'parent': source, 'word': target, 'decision': 'review', 'priority': priority,
                       'stem_shape': shape, 'source_stems': sorted(expected),
                       'flags': flags, 'target_parent_count': len(parents[target]),
                       'target_parents': sorted(parents[target]), 'target_definitions': glosses})
    rank = {'risky_stem_change': 0, 'weak_lexeme_evidence': 1, 'semantic_review': 2, 'dictionary_supported': 3}
    result.sort(key=lambda r: (rank[r['priority']], -r['target_parent_count'], r['word'], r['parent']))
    return result, parents


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, default=ROOT / 'data/derived/verb_sfx.remaining.jsonl')
    parser.add_argument('--dictionary', type=Path, default=ROOT / 'data/wiktionary/parsed_ru.jsonl.gz')
    parser.add_argument('--output', type=Path, default=ROOT / 'data/derived/verb_sfx.rule836.audit.jsonl')
    args = parser.parse_args()
    if len({p.resolve() for p in (args.input, args.dictionary, args.output)}) != 3:
        parser.error('Input and output paths must differ')
    records = [json.loads(l) for l in args.input.read_text().splitlines() if l.strip()]
    selected = [r for r in records if r['rule'].startswith('rule836(')]
    wanted = {norm(r['word']) for r in selected} | {norm(r['parents'][0]['word']) for r in selected}
    links, definitions = dictionary_signals(args.dictionary, wanted)
    rows, parents = analyze(records, links, definitions)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(''.join(json.dumps(r, ensure_ascii=False)+'\n' for r in rows), encoding='utf-8')
    table = ROOT / 'docs/verb_rule836_filter_audit_2026.tsv'
    with table.open('w', encoding='utf-8', newline='') as stream:
        writer = csv.writer(stream, delimiter='\t', lineterminator='\n')
        writer.writerow(['priority', 'parent', 'word', 'stem_shape', 'flags', 'target_parent_count', 'competing_parents'])
        for r in rows:
            writer.writerow([r['priority'], r['parent'], r['word'], r['stem_shape'], ','.join(r['flags']) or '-',
                             r['target_parent_count'], ','.join(r['target_parents'])])
    summary = {'scope': 'Existing rule836 relations only; priority signals, no automatic verdicts',
               'relations': len(rows), 'targets': len(parents),
               'targets_with_competing_parents': sum(len(v) > 1 for v in parents.values()),
               'priorities': dict(Counter(r['priority'] for r in rows)),
               'flags': dict(Counter(f for r in rows for f in r['flags'])),
               'input_sha256': hashlib.sha256(args.input.read_bytes()).hexdigest(),
               'dictionary_sha256': hashlib.sha256(args.dictionary.read_bytes()).hexdigest(),
               'largest_groups': [{'target': w, 'parents': sorted(p)} for w,p in
                                  sorted(parents.items(), key=lambda item: (-len(item[1]), item[0]))[:30]]}
    (ROOT / 'docs/verb_rule836_filter_audit_2026.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({k:v for k,v in summary.items() if k != 'largest_groups'}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
