"""Apply a complete, snapshot-bound LLM review; preserve all three partitions."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path


def relation_key(record):
    parents = sorted((p.get('role', ''), p['word'], p['pos'], p.get('form', ''),
                      p.get('hom_index', 0)) for p in record['parents'])
    return json.dumps([record['word'], record['rule'], record.get('hom_index', 0), parents],
                      ensure_ascii=False, separators=(',', ':'))


def apply_review(dataset, review_path, source_path=None):
    dataset, review_path = Path(dataset), Path(review_path)
    raw = Path(source_path).read_bytes() if source_path else dataset.read_bytes()
    metadata = json.loads(review_path.with_suffix('.meta.json').read_text())
    if (metadata.get('review_sha256') is not None
            and hashlib.sha256(review_path.read_bytes()).hexdigest() != metadata['review_sha256']):
        raise ValueError('Review differs from its recorded checksum')
    if hashlib.sha256(raw).hexdigest() != metadata['input_sha256']:
        raise ValueError('Dataset differs from the reviewed snapshot')
    rows = [json.loads(l) for l in raw.decode().splitlines() if l.strip()]
    decisions = [json.loads(l) for l in review_path.read_text().splitlines() if l.strip()]
    keys = [relation_key(r) for r in rows]
    reviews = {r['relation_key']: r for r in decisions}
    if (len(keys) != len(set(keys)) or len(reviews) != len(decisions)
            or set(keys) != set(reviews)):
        raise ValueError('Review must cover each relation exactly once')
    if any(r['verdict'] not in {'accept', 'reject', 'uncertain'} or not r.get('reason')
           for r in decisions):
        raise ValueError('Missing verdict or reason')
    overrides_path = review_path.with_suffix('.overrides.json')
    overrides = {}
    if overrides_path.exists():
        data = json.loads(overrides_path.read_text())
        if data['input_sha256'] != metadata['input_sha256']:
            raise ValueError('Overrides refer to a different snapshot')
        overrides = {r['relation_key']: r for r in data['overrides']}
        if len(overrides) != len(data['overrides']) or not set(overrides) <= set(reviews):
            raise ValueError('Duplicate or unknown override relation')
        for key, override in overrides.items():
            if (reviews[key]['verdict'] != 'uncertain' or override['verdict'] != 'accept'
                    or not override.get('reason') or not override.get('basis')):
                raise ValueError('Only explicit acceptance of uncertain relations is supported')
    parts = {s: [] for s in ('accept', 'reject', 'uncertain')}
    for key, record in zip(keys, rows):
        review = reviews[key]
        override = overrides.get(key)
        if override:
            review = dict(review, verdict='accept', reason=override['reason'],
                          confidence='user_decision', reviewer='user')
            correction = override.get('modifier_correction')
            if correction:
                matches = [p for p in record['parents']
                           if p.get('role') == 'modifier'
                           and p['word'] == correction['from'] and p['pos'] == correction['pos']]
                if len(matches) != 1:
                    raise ValueError('Modifier correction does not match its relation')
                modifier = matches[0]
                if not any(e.get('lemma') == correction['to']
                           for e in modifier.get('morphology_evidence', [])):
                    raise ValueError('Corrected lemma is not supported by morphology evidence')
                modifier['word'] = correction['to']
                modifier['id'] = correction['to'] + '|' + correction['pos']
        record['semantic_review'] = {
            k: review[k] for k in ('verdict', 'reason', 'confidence', 'reviewer')}
        # An LLM judgement is not independent verification of derivational origin.
        record['verified'] = False
        record['review_status'] = 'llm_' + review['verdict']
        if override:
            record['review_status'] = 'user_accept'
            record['semantic_review'].update(previous_llm_verdict='uncertain',
                                              acceptance_basis=override['basis'])
            if correction:
                record['semantic_review']['modifier_correction'] = correction
        parts[review['verdict']].append(record)
    final_keys = [relation_key(r) for partition in parts.values() for r in partition]
    if len(final_keys) != len(set(final_keys)):
        raise ValueError('Corrections produced duplicate relations')
    dataset.with_suffix('.semantic_input.jsonl').write_bytes(raw)
    for status, suffix in [('reject', '.semantic_rejected.jsonl'),
                           ('uncertain', '.semantic_pending.jsonl')]:
        dataset.with_suffix(suffix).write_text(''.join(
            json.dumps(r, ensure_ascii=False) + '\n' for r in parts[status]))
    temporary = dataset.with_suffix('.jsonl.tmp')
    temporary.write_text(''.join(json.dumps(r, ensure_ascii=False) + '\n'
                                 for r in parts['accept']))
    report = {
        'reviewer': metadata['reviewer'], 'date': metadata['date'],
        'review_file': str(review_path),
        'review_sha256': hashlib.sha256(review_path.read_bytes()).hexdigest(),
        'input_sha256': metadata['input_sha256'],
        'output_sha256': hashlib.sha256(temporary.read_bytes()).hexdigest(),
        'input_relations': len(rows),
        'verdicts': {s: len(records) for s, records in parts.items()},
        'unique_words': {s: len({r['word'] for r in records})
                         for s, records in parts.items()},
        'scope': 'LLM semantic assessment, not independent proof of immediate derivation',
    }
    if overrides:
        report.update(user_overrides=len(overrides),
                      override_bases=dict(Counter(o['basis'] for o in overrides.values())),
                      overrides_sha256=hashlib.sha256(overrides_path.read_bytes()).hexdigest(),
                      scope='LLM assessment with explicit user decisions; verified remains false')
    temporary.replace(dataset)
    manifest_path = dataset.with_suffix('.manifest.json')
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text())
        manifest.update(sha256=report['output_sha256'], semantic_review=report,
                        rules_after_semantic_review=dict(sorted(Counter(
                            r['rule'] for r in parts['accept']).items())))
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    dataset.with_suffix('.semantic_stats.json').write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', default='data/derived/verb_compound.jsonl')
    parser.add_argument('--review', default='data/verb_compound_semantic_review.jsonl')
    parser.add_argument('--snapshot', default=None,
                        help='read the original snapshot while writing partitions to --input')
    args = parser.parse_args()
    print(json.dumps(apply_review(args.input, args.review, args.snapshot), ensure_ascii=False, indent=2))
