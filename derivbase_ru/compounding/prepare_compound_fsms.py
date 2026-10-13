from tqdm import tqdm
from typing import Dict, List

from derivbase_ru.derivation import Derivation
from derivbase_ru.compounding.compound_analyzer import CompoundAnalyzer
from derivbase_ru.compounding.prepare_fsms import prepare_fsms


def prepare_compound_fsms(
        derivator: Derivation,
        wordlist: Dict[str, List[str]],
        load: bool = True,
        save: bool = True
) -> Dict[str, CompoundAnalyzer]:
    head_parts, mod_parts, head_rare, mod_rare = prepare_fsms(
        derivator, wordlist,
        load=load, save=save
    )

    cas = dict()
    for rule in tqdm(derivator.rules_compound):
        if rule.after_merge_rule_ids:
            # not implemented yet
            continue
        head_rules, mod_rules = rule.simple_rule_ids[:2]
        pos_m = rule.poss_m[0]
        print(rule.name, head_rules, mod_rules)

        if head_rules:
            head_rule = derivator.rules_dict[head_rules[0]]
            head_rule_name = head_rule.name
        else:
            head_rule_name = rule.pos_b
        head_part = head_parts[head_rule_name]

        if mod_rules:
            mod_rule = derivator.rules_dict[mod_rules[0]]
            mod_rule_name = mod_rule.name
        elif pos_m == '*':
            mod_rule_name = rule.name
        else:
            mod_rule_name = pos_m
        mod_part = mod_parts[mod_rule_name]

        print(head_part.name, mod_part.name, rule.order)
        if rule.order == [0, 1]:
            ca = CompoundAnalyzer(rule.name, rule.pos_a, head_part, mod_part)
        else:
            ca = CompoundAnalyzer(rule.name, rule.pos_a, mod_part, head_part)
        cas[rule.name] = ca
    return cas  # , derivator, head_parts, mod_parts, head_rare, mod_rare


def analyze_word(cas: Dict[str, CompoundAnalyzer], word: str, pos: str):
    analyzes = []
    for rule_name, ca in cas.items():
        if ca.pos != pos:
            continue
        analyzes.extend(ca.analyze(word, pos))
    return analyzes


# derivator = Derivation(use_guesser=True)
#
# wordlist = dict()
# wordlist["adv"] = ["сидя"]
# wordlist["adj"] = ["сладкий", "недельный"]
# wordlist["noun"] = ["монета", "неделя"]
# wordlist["num"] = ["один", "два"]
# wordlist["verb"] = ["ходить", "идти"]
# cas = prepare_compound_fsms(derivator, wordlist, load=False, save=False)
# print(analyze_word(cas, "полусладкий", "adj"))
# print(analyze_word(cas, "мимоходом", "adv"))
# print(analyze_word(cas, "двухнедельный", "adj"))
