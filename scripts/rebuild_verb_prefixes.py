"""Generate prefixal verb candidates with explicit inflection and lexical evidence."""
import argparse
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path
import re

from run_pipeline import Derivation, build_record, parent, read_dictionary, single_word

ROOT = Path(__file__).resolve().parents[1]
RULES = ROOT / 'derivbase_ru/rules/rus/verb/simple/verb=verb+pfx.json'


def normalize(word):
    return re.sub('[\u0301\u0300\u00b4]', '', word.lower()).replace('ё', 'е')


def lexical_evidence(word, wiki, heads, tokens):
    word = normalize(word)
    return [name for name, words in [('wiktionary_verb', wiki), ('dahl_head', heads),
                                     ('dahl_token', tokens)] if word in words]


def prefix_rules(engine, path=RULES):
    names = [r['rule_id'] for r in json.loads(Path(path).read_text())['data']]
    rules, skipped = [], []
    for name in names:
        rule = engine.rules_dict[name]
        if rule.pos_b != 'verb' or rule.pos_a != 'verb' or rule.info != 'PFX':
            raise ValueError('Non-prefix verb rule: ' + name)
        if rule.only_complex:
            skipped.append(name)
        else:
            rules.append(rule)
    return sorted(rules, key=lambda r: r.name), skipped


def generate(rule, word, types):
    # An absent type must not become the engine's unrestricted wildcard.
    return rule.apply(word, use_rare=True, form=['inf'], inflect_type=types or [])


def run(dictionary, dahl, inflect_types, output):
    buckets, known, pages = read_dictionary(str(dictionary))
    types = json.loads(Path(inflect_types).read_text())
    excluded = {line.split('#', 1)[0].strip()
                for line in (ROOT / 'data/pseudo_lemmas.txt').read_text().splitlines()}
    sources = sorted(w for w in buckets['verb'] if single_word(w) and w not in excluded)
    wiki = {normalize(w) for w in buckets['verb']}
    heads, tokens = set(), set()
    with gzip.open(dahl, 'rt') as stream:
        for line in stream:
            entry = json.loads(line)
            if entry.get('word'):
                heads.add(normalize(entry['word']))
            tokens.update(re.findall('[а-яё-]{2,}', normalize(entry.get('text') or '')))
    rules, skipped = prefix_rules(Derivation(lang='rus'))
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    paths = {'candidates': output,
             'raw': output.with_suffix('.raw.jsonl.gz'),
             'doubtful': output.with_suffix('.doubtful.jsonl')}
    temps = {key: path.with_name(path.name + '.tmp') for key, path in paths.items()}
    stats = {}
    print('Sources=%d with_types=%d rules=%d skipped_complex_only=%d' % (
        len(sources), sum(bool(types.get(w)) for w in sources), len(rules), len(skipped)), flush=True)
    with temps['candidates'].open('w') as out, temps['doubtful'].open('w') as doubtful, \
            gzip.open(temps['raw'], 'wt') as raw:
        for rule in rules:
            counts = Counter()
            for word in sources:
                for result in sorted(generate(rule, word, types.get(word))):
                    if result == word or not single_word(result) or result in excluded:
                        continue
                    base = parent(word, 'verb')
                    base['inflect_type'] = types.get(word, [])
                    record = build_record(result, 'verb', [base], rule,
                                          buckets['verb'].get(result), known, False,
                                          include_flags=False, kind='pfx')
                    evidence = lexical_evidence(result, wiki, heads, tokens)
                    record.update(verified=False, review_status='pending',
                                  lexeme_verified='wiktionary_verb' in evidence,
                                  lexical_evidence=evidence)
                    serialized = json.dumps(record, ensure_ascii=False) + '\n'
                    raw.write(serialized)
                    counts['generated'] += 1
                    if not evidence:
                        continue
                    out.write(serialized)
                    counts['candidates'] += 1
                    for source in evidence:
                        counts[source] += 1
                    if evidence == ['dahl_token']:
                        doubtful.write(serialized)
                        counts['doubtful_token_only'] += 1
            stats[rule.name] = dict(counts)
            print(rule.name, dict(counts), flush=True)
    for key, path in paths.items():
        temps[key].replace(path)
    totals = Counter()
    for counts in stats.values():
        totals.update(counts)
    inputs = {'dictionary': Path(dictionary), 'dahl': Path(dahl),
              'inflect_types': Path(inflect_types), 'rules': RULES,
              'pseudo_lemmas': ROOT / 'data/pseudo_lemmas.txt'}
    manifest = {'scope': 'Candidates, not semantically verified relations; raw includes unattested results.',
                'pages': pages, 'source_verbs': len(sources),
                'sources_with_types': sum(bool(types.get(w)) for w in sources),
                'rules': stats, 'skipped_complex_only': skipped,
                'totals': dict(totals),
                'inputs': {name: {'path': str(path), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}
                           for name, path in inputs.items()},
                'outputs': {name: {'path': str(path), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}
                            for name, path in paths.items()}}
    output.with_suffix('.manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    return manifest


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dict', default=str(ROOT / 'data/wiktionary/parsed_ru.jsonl.gz'))
    parser.add_argument('--dahl', default=str(ROOT / 'data/dahl/dahl.jsonl.gz'))
    parser.add_argument('--inflect-types', default=str(ROOT / 'data/verb_inflect_types.json'))
    parser.add_argument('--out', default=str(ROOT / 'data/derived/verb_pfx.jsonl'))
    parser.add_argument('--accept-dahl-token', action='store_true',
                        help='apply the user-authorized acceptance policy for Dahl-token candidates')
    args = parser.parse_args()
    run(args.dict, args.dahl, args.inflect_types, args.out)
    if args.accept_dahl_token:
        from accept_prefix_dahl import accept_dahl
        accept_dahl(args.out)
