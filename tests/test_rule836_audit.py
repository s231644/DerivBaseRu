from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from audit_rule836 import analyze, conservative_stems


def record(source, target, types, evidence=('wiktionary_verb',)):
    return {'word': target, 'rule': 'rule836(verb + ну2(ть) -> verb)',
            'parents': [{'word': source, 'inflect_type': types}], 'lexical_evidence': list(evidence)}


def test_stem_change_is_a_signal_not_a_rejection():
    assert 'плет' in conservative_stems('плести', ['7т'])
    assert 'греб' in conservative_stems('грести', ['7б'])
    assert 'коль' in conservative_stems('колоть', ['10ол'])
    rows, _ = analyze([record('дёргать', 'дёрнуть', ['1'])], {}, {})
    assert rows[0]['stem_shape'] == 'extra_stem_change'
    assert rows[0]['decision'] == 'review'  # legitimate -г- loss must not be rejected


def test_identical_stems_do_not_prove_semantics_and_dictionary_support_is_specific():
    records = [record('копать', 'копнуть', ['1']), record('копить', 'копнуть', ['4']),
               record('коптить', 'копнуть', ['4'])]
    rows, parents = analyze(records, {'копнуть': {'копать'}}, {'копнуть': ['Однократно копнуть землю.']})
    by_parent = {r['parent']: r for r in rows}
    assert by_parent['копать']['priority'] == 'dictionary_supported'
    assert by_parent['копить']['stem_shape'] == 'intact_stem'
    assert by_parent['копить']['priority'] == 'semantic_review'
    assert by_parent['коптить']['priority'] == 'risky_stem_change'
    assert all(r['decision'] == 'review' for r in rows)
    assert parents['копнуть'] == {'копать', 'копить', 'коптить'}


def test_reflexives_are_preserved_and_no_missing_dictionary_is_a_verdict():
    records = [record('толкать', 'толкнуть', ['1']), record('толкаться', 'толкнуться', ['1'], ('dahl_token',))]
    rows, _ = analyze(records, {}, {})
    assert len(rows) == 2
    assert {r['word'] for r in rows} == {'толкнуть', 'толкнуться'}
    assert all(r['decision'] == 'review' for r in rows)
    assert next(r for r in rows if r['word'] == 'толкнуться')['priority'] == 'weak_lexeme_evidence'
