"""Drop a reflexive compound analysis only when its nonreflexive twin exists."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path


def analysis_key(record, strip_reflexive=False):
    word = record['word']
    if strip_reflexive:
        if not word.endswith('ся'):
            return None
        word = word[:-2]
    parents = []
    for parent in record['parents']:
        value = parent['word']
        if strip_reflexive and parent.get('role') == 'head':
            if not value.endswith('ся'):
                return None
            value = value[:-2]
        parents.append((parent.get('role', ''), value, parent['pos'],
                        parent.get('form', ''), parent.get('hom_index', 0)))
    return (word, record['rule'], record.get('hom_index', 0), tuple(sorted(parents)))


def partition_reflexive(rows):
    keys = {analysis_key(r) for r in rows}
    kept, removed = [], []
    for record in rows:
        twin = analysis_key(record, strip_reflexive=True)
        if twin is not None and twin in keys:
            removed.append({'category': 'reflexive_twin',
                            'reason': 'Есть тот же разбор без -ся у результата и глагольной основы.',
                            'nonreflexive_word': record['word'][:-2], 'record': record})
        else:
            kept.append(record)
    return kept, removed


def filter_reflexive(path):
    path = Path(path)
    raw = path.read_bytes()
    report_path = path.with_suffix('.reflexive_stats.json')
    if report_path.exists():
        previous = json.loads(report_path.read_text())
        if previous['output_sha256'] == hashlib.sha256(raw).hexdigest():
            return previous
    rows = [json.loads(line) for line in raw.decode().splitlines() if line.strip()]
    kept, removed = partition_reflexive(rows)
    temporary = path.with_suffix('.jsonl.tmp')
    temporary.write_text(''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in kept))
    report = {'policy': 'same rule, modifier lemma/POS/form and head without -ся',
              'before_relations': len(rows), 'after_relations': len(kept),
              'removed_relations': len(removed),
              'after_unique_words': len({r['word'] for r in kept}),
              'input_sha256': hashlib.sha256(raw).hexdigest(),
              'output_sha256': hashlib.sha256(temporary.read_bytes()).hexdigest()}
    path.with_suffix('.reflexive_rejected.jsonl').write_text(''.join(
        json.dumps(r, ensure_ascii=False) + '\n' for r in removed))
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    temporary.replace(path)
    manifest_path = path.with_suffix('.manifest.json')
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text())
        manifest.update(sha256=report['output_sha256'], reflexive_filter=report,
                        rules_after_reflexive_filter=dict(sorted(Counter(
                            r['rule'] for r in kept).items())))
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    print('Reflexive twins: %d -> %d relations; %d removed' % (
        len(rows), len(kept), len(removed)), flush=True)
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', default='data/derived/verb_compound.jsonl')
    filter_reflexive(parser.parse_args().input)
