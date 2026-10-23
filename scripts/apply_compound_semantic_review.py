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


def apply_review(dataset, review_path):
    dataset, review_path = Path(dataset), Path(review_path)
    raw = dataset.read_bytes()
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
    parts = {s: [] for s in ('accept', 'reject', 'uncertain')}
    for key, record in zip(keys, rows):
        review = reviews[key]
        record['semantic_review'] = {
            k: review[k] for k in ('verdict', 'reason', 'confidence', 'reviewer')}
        # An LLM judgement is not independent verification of derivational origin.
        record['verified'] = False
        record['review_status'] = 'llm_' + review['verdict']
        parts[review['verdict']].append(record)
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
    args = parser.parse_args()
    print(json.dumps(apply_review(args.input, args.review), ensure_ascii=False, indent=2))
