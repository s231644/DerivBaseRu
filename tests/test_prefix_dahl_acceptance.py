import hashlib
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from accept_prefix_dahl import accept_dahl


def test_acceptance_changes_only_token_only_candidates_and_refreshes_hashes(tmp_path):
    dataset = tmp_path / 'verb_pfx.jsonl'
    doubtful = dataset.with_suffix('.doubtful.jsonl')
    rows = [{'word': str(i), 'lexical_evidence': evidence, 'review_status': 'pending',
             'verified': False, 'lexeme_verified': False}
            for i, evidence in enumerate([['dahl_token'], ['dahl_head'],
                                           ['wiktionary_verb', 'dahl_token']])]
    dataset.write_text(''.join(json.dumps(r) + '\n' for r in rows))
    dataset.with_suffix('.manifest.json').write_text(json.dumps({'outputs': {
        'candidates': {'path': str(dataset)}, 'doubtful': {'path': str(doubtful)}}}))
    assert accept_dahl(dataset) == 1
    changed = [json.loads(l) for l in dataset.read_text().splitlines()]
    assert changed[0]['review_status'] == 'user_accept'
    assert changed[0]['acceptance']['reviewer'] == 'user'
    assert changed[0]['lexeme_verified'] is False
    assert changed[1:] == rows[1:]
    assert [json.loads(l) for l in doubtful.read_text().splitlines()] == changed[:1]
    manifest = json.loads(dataset.with_suffix('.manifest.json').read_text())
    assert manifest['outputs']['candidates']['sha256'] == hashlib.sha256(dataset.read_bytes()).hexdigest()
    before = dataset.read_bytes()
    assert accept_dahl(dataset) == 1
    assert dataset.read_bytes() == before
