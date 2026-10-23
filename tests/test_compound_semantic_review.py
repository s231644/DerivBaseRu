import hashlib
import json
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from apply_compound_semantic_review import apply_review, relation_key


def fixture(tmp_path):
    rows = [{'word': w, 'rule': 'rule961', 'verified': False,
             'parents': [{'word': 'водить', 'role': 'head', 'pos': 'verb'},
                         {'word': m, 'role': 'modifier', 'pos': 'noun', 'form': f}]}
            for w, m, f in [('руководить', 'рука', 'руко'),
                            ('руководить', 'другое', 'друго'),
                            ('неясный', 'неясное', 'неясно')]]
    dataset = tmp_path / 'verbs.jsonl'
    dataset.write_text(''.join(json.dumps(r) + '\n' for r in rows))
    review = tmp_path / 'review.jsonl'
    decisions = [{'relation_key': relation_key(r), 'verdict': v,
                  'reason': 'Explicit LLM judgement', 'confidence': 'medium',
                  'reviewer': 'test reviewer'}
                 for r, v in zip(rows, ['accept', 'reject', 'uncertain'])]
    review.write_text(''.join(json.dumps(r) + '\n' for r in decisions))
    review.with_suffix('.meta.json').write_text(json.dumps({
        'input_sha256': hashlib.sha256(dataset.read_bytes()).hexdigest(),
        'reviewer': 'test reviewer', 'date': '2026-10-24'}))
    return dataset, review, rows, decisions


def test_review_partitions_relations_not_words(tmp_path):
    dataset, review, rows, _ = fixture(tmp_path)
    original = dataset.read_bytes()
    report = apply_review(dataset, review)
    assert report['verdicts'] == {'accept': 1, 'reject': 1, 'uncertain': 1}
    kept = json.loads(dataset.read_text())
    assert kept['word'] == 'руководить'
    assert kept['verified'] is False
    assert kept['review_status'] == 'llm_accept'
    rejected = json.loads(dataset.with_suffix('.semantic_rejected.jsonl').read_text())
    assert rejected['word'] == kept['word']
    assert relation_key(kept) != relation_key(rejected)
    assert json.loads(dataset.with_suffix('.semantic_pending.jsonl').read_text())['word'] == 'неясный'
    assert dataset.with_suffix('.semantic_input.jsonl').read_bytes() == original


@pytest.mark.parametrize('failure', ['snapshot', 'missing', 'duplicate', 'invalid'])
def test_incomplete_or_stale_review_cannot_change_dataset(tmp_path, failure):
    dataset, review, _, decisions = fixture(tmp_path)
    if failure == 'snapshot':
        dataset.write_text(dataset.read_text() + '\n')
    elif failure == 'missing':
        decisions.pop()
    elif failure == 'duplicate':
        decisions.append(decisions[0])
    else:
        decisions[0]['verdict'] = 'maybe'
    review.write_text(''.join(json.dumps(r) + '\n' for r in decisions))
    before = dataset.read_bytes()
    with pytest.raises(ValueError):
        apply_review(dataset, review)
    assert dataset.read_bytes() == before
