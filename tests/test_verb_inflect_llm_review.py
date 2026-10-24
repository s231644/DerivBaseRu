import hashlib
import json
from pathlib import Path
import re
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from apply_verb_inflect_llm_review import apply_review, POLICY


def test_complete_nonreflexive_review_and_accented_variants():
    rows = json.loads(POLICY.read_text())['rows']
    assert len(rows) == len({r['word'] for r in rows}) == 285
    assert [r['word'] for r in rows] == sorted(r['word'] for r in rows)
    assert all(not r['word'].endswith(('ся', 'сь')) for r in rows)
    for r in rows:
        if r['status'] == 'retained_variants':
            assert set(v['inflect_type'] for v in r['variants']) == set(r['types'])
            for v in r['variants']:
                assert re.sub('[\u0301]', '', v['infinitive']) == r['word']
                assert '\u0301' in v['infinitive']
                assert '\u0301' in v['per1_sg'] or 'ё' in v['per1_sg']
    d = {r['word']: r for r in rows}
    assert [(v['inflect_type'], v['infinitive'], v['per1_sg']) for v in d['посыпать']['variants']] == [
        ('1', 'посыпа́ть', 'посыпа́ю'), ('6', 'посы́пать', 'посы́плю')]
    assert d['пожать']['types'] == ['14м', '14н']
    assert d['повыписать']['types'] == ['6']


def test_idempotence_pending_and_reflexive_preservation():
    rows = json.loads(POLICY.read_text())['rows']
    before = {r['word']: r['before'] for r in rows}
    before['посыпаться'] = ['1', '6']
    before['постороннее'] = ['1', '2']
    original = json.loads(json.dumps(before))
    after, _ = apply_review(before)
    assert before == original
    assert after['посыпаться'] == before['посыпаться']
    assert after['постороннее'] == before['постороннее']
    assert all(after[r['word']] == before[r['word']] for r in rows if r['status'] == 'pending')
    assert apply_review(after)[0] == after
