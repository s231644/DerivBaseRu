import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from filter_reflexive_compounds import filter_reflexive, partition_reflexive


def row(word, head, modifier='рука', form='руко', rule='rule961'):
    return {'word': word, 'rule': rule, 'parents': [
        {'word': head, 'pos': 'verb', 'role': 'head'},
        {'word': modifier, 'pos': 'noun', 'role': 'modifier', 'form': form}]}


def test_only_matching_reflexive_analysis_is_removed():
    base = row('руководить', 'водить')
    reflexive = row('руководиться', 'водиться')
    other_modifier = row('руководиться', 'водиться', modifier='другой')
    other_rule = row('руководиться', 'водиться', rule='other')
    unpaired = row('рукополагаться', 'полагаться')
    rows = [base, reflexive, other_modifier, other_rule, unpaired]
    kept, rejected = partition_reflexive(rows)
    assert kept == [base, other_modifier, other_rule, unpaired]
    assert [r['record'] for r in rejected] == [reflexive]


def test_presence_of_word_alone_does_not_remove_analysis():
    rows = [row('руководить', 'водить'), row('руководиться', 'деться')]
    assert partition_reflexive(rows) == (rows, [])


def test_reflexive_audit_survives_repeat(tmp_path):
    path = tmp_path / 'verbs.jsonl'
    rows = [row('руководить', 'водить'), row('руководиться', 'водиться')]
    path.write_text(''.join(json.dumps(r) + '\n' for r in rows))
    report = filter_reflexive(path)
    assert report['removed_relations'] == 1
    assert filter_reflexive(path) == report
    assert json.loads(path.with_suffix('.reflexive_rejected.jsonl').read_text())['record'] == rows[1]
