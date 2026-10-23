"""Compare indexed compound search with exhaustive engine generation."""
import json
from pathlib import Path
import subprocess
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from run_pipeline import Derivation, apply_compound_rule
import pymorphy3
import pytest
from compound_morphology import checked_modifier_forms


@pytest.fixture(scope='module')
def morphology():
    return pymorphy3.MorphAnalyzer()


@pytest.fixture(scope='module')
def interfix_chain():
    return next(r.simple_rules[1] for r in
                Derivation(lang='rus').loaded_rules['compound']
                if r.name == 'rule961([noun + ITFX] + verb -> verb)')


@pytest.mark.parametrize('word,genitive,valid,invalid', [
    ('ложь', 'лжи', 'лже', 'ложе'),
    ('кровь', 'крови', 'крово', 'крво'),
    ('сон', 'сна', 'сно', 'соно'),
    ('камень', 'камня', 'камне', 'каменьо'),
    ('пора', 'поры', 'поро', 'про'),
    ('перо', 'пера', 'перо', 'про'),
])
def test_genitive_licenses_stem(word, genitive, valid, invalid,
                               morphology, interfix_chain):
    forms, reason = checked_modifier_forms(word, 'noun', interfix_chain, morphology)
    assert reason is None
    assert valid in forms
    assert any(e['genitive'] == genitive for e in forms[valid])
    assert invalid not in forms


@pytest.mark.parametrize('word', ['пери', 'пальто', 'такси', 'кино'])
def test_indeclinable_modifiers_excluded(word, morphology, interfix_chain):
    forms, reason = checked_modifier_forms(word, 'noun', interfix_chain, morphology)
    assert forms == {}
    assert reason == 'indeclinable'


def test_explicit_exception_keeps_genitive_evidence(morphology, interfix_chain):
    forms, _ = checked_modifier_forms('судно', 'noun', interfix_chain, morphology)
    assert forms['судо']
    assert all(e['rule_exception'] for e in forms['судо'])


def test_fleeting_vowel_does_not_insert_soft_sign(morphology, interfix_chain):
    forms, _ = checked_modifier_forms('ложь', 'noun', interfix_chain, morphology)
    assert 'лже' in forms
    assert 'льже' not in forms


def test_predicted_lemma_is_not_dictionary_evidence(morphology, interfix_chain):
    forms, reason = checked_modifier_forms(
        'абракадабровщина', 'noun', interfix_chain, morphology)
    assert not forms
    assert reason == 'no_known_lemma'


def test_indexed_compounds_match_exhaustive_search(tmp_path):
    words = {
        'noun': ['вода', 'пар'],
        'adj': ['красный', 'синий'],
        'verb': ['носить', 'ходить', 'водоносить', 'пароходить',
                 'красноносить', 'синоходить', 'самоносить', 'полуходить'],
    }
    tags = {'noun': 'сущ', 'adj': 'прил', 'verb': 'гл'}
    dictionary, output = tmp_path / 'dict.jsonl', tmp_path / 'out.jsonl'
    dictionary.write_text(''.join(
        json.dumps({'title': word, 'entries': [{'pos': tags[pos]}]}) + '\n'
        for pos, bucket in words.items() for word in bucket))
    root = Path(__file__).resolve().parents[1]
    subprocess.run([sys.executable, str(root / 'scripts/rebuild_verb_compounds.py'),
                    '--dict', str(dictionary), '--out', str(output)],
                   cwd=root, check=True)
    records = [json.loads(line) for line in output.read_text().splitlines()]
    actual = {(r['word'], r['rule'], tuple(p['word'] for p in r['parents']))
              for r in records}
    expected = set()
    for rule in Derivation(lang='rus').loaded_rules['compound']:
        if rule.pos_a != 'verb':
            continue
        for head in words['verb']:
            for modifier in words[rule.poss_m[0]]:
                if head == modifier:
                    continue
                for word in apply_compound_rule(rule, head, modifier, True):
                    if word in words['verb']:
                        expected.add((word, rule.name, (head, modifier)))
    assert actual == expected
    assert len(actual) == len(records) == 4
    assert all(not r['verified'] and r['review_status'] == 'pending'
               for r in records)
