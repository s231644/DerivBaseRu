from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from rebuild_verb_prefixes import Derivation, generate, lexical_evidence, prefix_rules


def test_prefix_rules_include_reclassified_components():
    rules, skipped = prefix_rules(Derivation(lang='rus'))
    names = {r.name for r in rules}
    assert 'rule961(полу + verb -> verb)' in names
    assert 'rule961(само + verb -> verb)' in names
    assert all(not r.only_complex for r in rules)
    assert 'rule882(обез + verb -> verb)' in skipped


def test_absent_inflection_type_is_not_wildcard():
    engine = Derivation(lang='rus')
    rule = engine.rules_dict['rule857(вы + verb -> verb)']
    assert generate(rule, 'красить', None) == set()
    assert 'выкрасить' in generate(rule, 'красить', ['4'])
    assert 'полусидеть' in generate(engine.rules_dict['rule961(полу + verb -> verb)'],
                                    'сидеть', None)


def test_lexical_evidence_distinguishes_token_and_head_and_normalizes_yo():
    assert lexical_evidence('МЁРЗНУТЬ', {'мерзнуть'}, set(), {'мерзнуть'}) == [
        'wiktionary_verb', 'dahl_token']
    assert lexical_evidence('слово', set(), set(), {'слово'}) == ['dahl_token']
    assert lexical_evidence('слово', set(), {'слово'}, set()) == ['dahl_head']
    assert lexical_evidence('новое', set(), set(), set()) == []
