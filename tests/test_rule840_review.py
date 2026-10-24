import copy
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from review_rule840 import partition, POLICY, ROOT


def test_complete_review_covers_every_relation_and_preserves_source():
    records = [json.loads(l) for l in (ROOT / 'data/derived/verb_sfx.remaining.jsonl').read_text().splitlines()]
    original = copy.deepcopy(records)
    decisions = json.loads(POLICY.read_text())['decisions']
    groups = partition(records, decisions)
    assert {k: len(v) for k,v in groups.items()} == {'accepted': 159, 'rejected': 23, 'pending': 26}
    assert records == original
    by_pair = {(r['parents'][0]['word'], r['word']): status for status,rows in groups.items() for r in rows}
    assert by_pair['отговеть', 'отгануть'] == 'rejected'
    assert by_pair['учать', 'учануть'] == 'accepted'
    assert by_pair['учить', 'учануть'] == 'rejected'
    assert by_pair['ласкать', 'ласкануть'] == 'pending'
    assert by_pair['держать', 'дергануть'] == 'rejected'
    assert by_pair['дёргать', 'дёргануть'] == 'accepted'
    assert all(r['verified'] for r in groups['accepted'])
    try:
        partition(records, decisions[:-1])
    except ValueError:
        pass
    else:
        raise AssertionError('Missing review accepted')
