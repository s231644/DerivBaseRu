from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from rebuild_verb_prefixes import Derivation, generate, verb_rules
from rebuild_verb_suffixes import RULES


def test_all_suffix_file_rules_including_rare_only_and_postfix_are_selected():
    rules, skipped = verb_rules(Derivation(lang='rus'), RULES, {'SFX', 'PTFX'})
    assert len(rules) == 9
    assert not skipped
    assert any(r.name == 'rule930(verb + ся -> verb)' and r.info == 'PTFX' for r in rules)
    for rule in rules:
        if not rule.subrules:
            assert rule.rare_straight
            source = next(iter(rule.rare_straight))
            assert rule.rare_straight[source] <= generate(rule, source, None)


def test_suffix_generation_respects_type_and_keeps_reflexive_rule():
    engine = Derivation(lang='rus')
    rule = engine.rules_dict['rule930(verb + ся -> verb)']
    assert 'мыться' in generate(rule, 'мыть', ['12ы'])
    assert not generate(rule, 'мыть', None)
    rule = engine.rules_dict['rule842(verb + ива(ть)/ва(ть)/а3(ть) -> verb)']
    assert 'сжигать' in generate(rule, 'сжечь', ['8г'])


def test_select_remaining_rules_and_reject_unknown_selectors():
    engine = Derivation(lang='rus')
    rules, skipped = verb_rules(engine, RULES, {'SFX', 'PTFX'}, ['rule836', 'rule840'])
    assert {r.name.split('(', 1)[0] for r in rules} == {'rule836', 'rule840'}
    assert not skipped
    try:
        verb_rules(engine, RULES, {'SFX', 'PTFX'}, ['rule836', 'rule999999'])
    except ValueError as error:
        assert 'rule999999' in str(error)
    else:
        raise AssertionError('Unknown selector must not trigger partial generation')
