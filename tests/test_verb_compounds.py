"""Compare indexed compound search with exhaustive engine generation."""
import json
from pathlib import Path
import subprocess
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from run_pipeline import Derivation
import pymorphy3
import pytest
from compound_morphology import checked_modifier_forms, declension_tags


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


@pytest.mark.parametrize('word,pos,expected', [
    ('вода', 'noun', '1'), ('камень', 'noun', '2'),
    ('рука', 'noun', '3'), ('нож', 'noun', '4'),
    ('отец', 'noun', '5'), ('герой', 'noun', '6'),
    ('станция', 'noun', '7'), ('кровь', 'noun', '8'),
    ('время', 'noun', '8'), ('папа', 'noun', '1'),
    ('красный', 'adj', '1'), ('синий', 'adj', '2'),
    ('русский', 'adj', '3'), ('хороший', 'adj', '4'),
    ('куцый', 'adj', '5'),
])
def test_declension_type_matches_gender_and_pos(word, pos, expected, morphology):
    parses = [p for p in morphology.parse(word)
              if p.tag.POS == {'noun': 'NOUN', 'adj': 'ADJF'}[pos]
              and 'nomn' in p.tag and p.normal_form == word]
    contexts = [t for p in parses for t in declension_tags(word, pos, p)]
    assert contexts
    assert {v for t in contexts for v in t['inflect_type']} == {expected}


@pytest.mark.parametrize('word', ['Москва', 'Иван', 'Петров', 'Роман', 'иван'])
def test_proper_names_excluded(word, morphology, interfix_chain):
    forms, reason = checked_modifier_forms(word, 'noun', interfix_chain, morphology)
    assert not forms
    assert reason == 'proper_name'


def test_common_homonym_of_name_is_retained(morphology, interfix_chain):
    forms, reason = checked_modifier_forms('роман', 'noun', interfix_chain, morphology)
    assert reason is None
    assert forms['романо']
    assert all('Name' not in e['tag'] and 'Surn' not in e['tag']
               for e in forms['романо'])


def test_declension_does_not_allow_bare_stem(morphology, interfix_chain):
    forms, _ = checked_modifier_forms('раз', 'noun', interfix_chain, morphology)
    assert 'разо' in forms
    assert 'раз' not in forms


def test_indexed_compounds_respect_declension(tmp_path):
    words = {
        'noun': ['вода', 'пар'],
        'adj': ['красный', 'синий'],
        'verb': ['носить', 'ходить', 'водоносить', 'пароходить',
                 'красноносить', 'синоходить', 'синеходить',
                 'самоносить', 'полуходить'],
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
    expected = {
        ('водоносить', 'rule961([noun + ITFX] + verb -> verb)', ('носить', 'вода')),
        ('пароходить', 'rule961([noun + ITFX] + verb -> verb)', ('ходить', 'пар')),
        ('красноносить', 'rule961([adj + ITFX] + verb -> verb)', ('носить', 'красный')),
        ('синеходить', 'rule961([adj + ITFX] + verb -> verb)', ('ходить', 'синий')),
    }
    assert actual == expected
    assert len(actual) == len(records) == 4
    assert all(not r['verified'] and r['review_status'] == 'pending'
               for r in records)
    assert all(e['inflect_type'] and e['rule_tags']['gender']
               for r in records for p in r['parents'] if p['role'] == 'modifier'
               for e in p['morphology_evidence'])
