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


def test_user_overrides_and_parent_correction_keep_original_review(tmp_path):
    dataset, review, rows, decisions = fixture(tmp_path)
    rows[2]['parents'][1].update(word='мед', id='мед|noun',
                              morphology_evidence=[{'lemma': 'мёд', 'genitive': 'мёда'}])
    decisions[2]['relation_key'] = relation_key(rows[2])
    snapshot = tmp_path / 'original.jsonl'
    snapshot.write_text(''.join(json.dumps(r) + '\n' for r in rows))
    metadata = json.loads(review.with_suffix('.meta.json').read_text())
    metadata['input_sha256'] = hashlib.sha256(snapshot.read_bytes()).hexdigest()
    review.with_suffix('.meta.json').write_text(json.dumps(metadata))
    review.write_text(''.join(json.dumps(r) + '\n' for r in decisions))
    original_review = review.read_bytes()
    review.with_suffix('.overrides.json').write_text(json.dumps({
        'input_sha256': metadata['input_sha256'], 'overrides': [{
            'relation_key': decisions[2]['relation_key'], 'verdict': 'accept',
            'basis': 'explicit_correction', 'reason': 'User requested honey',
            'modifier_correction': {'from': 'мед', 'to': 'мёд', 'pos': 'noun'}}]}))
    report = apply_review(dataset, review, snapshot)
    assert report['verdicts'] == {'accept': 2, 'reject': 1, 'uncertain': 0}
    corrected = json.loads(dataset.read_text().splitlines()[1])
    assert corrected['parents'][1]['word'] == 'мёд'
    assert corrected['parents'][1]['id'] == 'мёд|noun'
    assert corrected['review_status'] == 'user_accept'
    assert corrected['semantic_review']['previous_llm_verdict'] == 'uncertain'
    assert corrected['verified'] is False
    assert review.read_bytes() == original_review
    assert dataset.with_suffix('.semantic_input.jsonl').read_bytes() == snapshot.read_bytes()


def test_user_override_cannot_silently_accept_rejected_relation(tmp_path):
    dataset, review, _, decisions = fixture(tmp_path)
    metadata = json.loads(review.with_suffix('.meta.json').read_text())
    review.with_suffix('.overrides.json').write_text(json.dumps({
        'input_sha256': metadata['input_sha256'], 'overrides': [{
            'relation_key': decisions[1]['relation_key'], 'verdict': 'accept',
            'basis': 'shared_component', 'reason': 'Invalid scope expansion'}]}))
    before = dataset.read_bytes()
    with pytest.raises(ValueError):
        apply_review(dataset, review)
    assert dataset.read_bytes() == before
