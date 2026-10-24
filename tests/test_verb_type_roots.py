from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from audit_verb_type_roots import decomposition, families, refine_by_roots

ROOTS = Path(__file__).resolve().parents[1] / 'data/verbs_roots.csv'


def test_prefixes_boundaries_reflexives_and_irregular_iti():
    assert decomposition('недоперелиться', {'лить'})['prefixes'] == ['недо', 'пере']
    assert decomposition('изъять', {'ять'})['prefixes'] == ['из']
    assert decomposition('подъехать', {'ехать'})['prefixes'] == ['под']
    assert decomposition('разойтись', {'идти'})['root'] == 'идти'
    assert decomposition('подзанять', {'ять'})['prefixes'] == ['под', 'за']
    assert decomposition('апрувить', {'вить'}) is None
    assert decomposition('свежить', {'жить'}) is None


def test_inventory_preserves_homonyms_and_pseudo_roots():
    roots, _ = families(ROOTS)
    assert 'жать' in roots['14м'] and 'жать' in roots['14н']
    assert 'чать' in roots['14н']
    assert decomposition('начать', roots['14н']) is not None


def test_narrowing_does_not_invent_types_or_remove_unknown_subtypes():
    mapping = {'барыжить': ['16', '4'], 'бурдеть': ['1', '15'],
               'воскипеть': ['12петь', '5'], 'пожать': ['14м', '14н'],
               'ввестись': ['7д', '7с'], 'сговнять': ['14ним', '1'],
               'ошибочный': ['15'], 'жать': ['14н']}
    output, audit = refine_by_roots(mapping, ROOTS)
    assert output['барыжить'] == ['4']
    assert output['бурдеть'] == ['1']
    assert output['воскипеть'] == ['5']
    assert output['ввестись'] == ['7д']
    assert output['пожать'] == ['14м', '14н']
    assert output['сговнять'] == ['1', '14ним']
    assert output['ошибочный'] == ['15']
    assert output['жать'] == ['14н']
    assert mapping['барыжить'] == ['16', '4']
    again, _ = refine_by_roots(output, ROOTS)
    assert again == output
    missing = next(r for r in audit if r['word'] == 'сговнять')
    assert missing['unavailable_inventory'] == ['14ним']
