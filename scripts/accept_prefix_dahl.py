"""Record the user's acceptance of prefix candidates supported only by Dahl tokens."""
import hashlib
import json
from pathlib import Path


def accept_dahl(dataset):
    dataset = Path(dataset)
    rows = [json.loads(line) for line in dataset.read_text().splitlines() if line.strip()]
    accepted = []
    for record in rows:
        if record.get('lexical_evidence') != ['dahl_token']:
            continue
        record.update(review_status='user_accept', acceptance={
            'reviewer': 'user', 'basis': 'accept_all_dahl_token_candidates',
            'reason': 'Пользователь явно принял все doubtful из Даля.',
        })
        accepted.append(record)
    for path, records in [(dataset, rows),
                          (dataset.with_suffix('.doubtful.jsonl'), accepted)]:
        temporary = path.with_name(path.name + '.tmp')
        temporary.write_text(''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in records))
        temporary.replace(path)
    manifest_path = dataset.with_suffix('.manifest.json')
    manifest = json.loads(manifest_path.read_text())
    manifest['dahl_user_acceptance'] = {'accepted_relations': len(accepted),
                                       'basis': 'explicit_user_instruction'}
    for name in ('candidates', 'doubtful'):
        path = Path(manifest['outputs'][name]['path'])
        manifest['outputs'][name]['sha256'] = hashlib.sha256(path.read_bytes()).hexdigest()
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    return len(accepted)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', default='data/derived/verb_pfx.jsonl')
    print('Accepted Dahl token candidates:', accept_dahl(parser.parse_args().input))
