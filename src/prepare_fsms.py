import pandas as pd
import warnings
from tqdm import tqdm
from collections import defaultdict
from typing import List, Optional, Dict

from src.fsm_part import DerivedFSM


def build_fsm(
        wordlist: Dict[str, List[str]],
        rule_name: str,
        pos_b: str,
        pos_a: Optional[str],
        rule_id: Optional[str],
        rare_dict: dict,
        load: bool = True,
        save: bool = True
) -> DerivedFSM:
    if load:
        try:
            fsm = DerivedFSM.load(rule_name.replace('/', '_') + ".pickle")
            return fsm
        except FileNotFoundError:
            warnings.warn("File does not exist!")
    fsm = DerivedFSM(
        rule_name, pos_b, pos_a, rule_id, wordlist.get(pos_b, [])
    )
    for lemma, pos, form in rare_dict.get(rule_name, []):
        fsm.add_word(form, lemma, pos)
    if save:
        fsm.save()
    return fsm


def prepare_fsms(wordlist: Dict[str, List[str]], load: bool = True, save: bool = True):
    derivator = DerivedFSM.derivator

    # loading rare forms
    mod_rare = defaultdict(list)
    head_rare = defaultdict(list)

    rare_star = pd.read_csv('../src/rules/compounds_rare_star.csv', sep=";")
    for i in range(len(rare_star)):
        d = dict(rare_star.iloc[i])
        if d["index"] == 0:
            head_rare[d["with_rule_id"]].append((d["lemma"], d["pos"], d["form"]))
        else:
            mod_rare[d["with_rule_id"]].append((d["lemma"], d["pos"], d["form"]))

    # processing normal words
    head_parts = defaultdict(DerivedFSM)
    mod_parts = defaultdict(DerivedFSM)

    for rule in tqdm(derivator.rules_compound):
        if rule.after_merge_rule_ids:
            # not implemented yet
            continue
        head_rules, mod_rules = rule.simple_rule_ids[:2]
        pos_m = rule.poss_m[0]

        # filling in the head FSM
        if head_rules:
            # e.g. suffix
            head_rule = derivator.rules_dict[head_rules[0]]
            head_rule_name = head_rule.name
            head_rule_id = head_rule_name
            pos_b, pos_a = head_rule.pos_b, head_rule.pos_a
        else:
            # no changes, e. g. "rule550([adj + ITFX] + noun -> noun)"
            head_rule_name = rule.pos_b
            head_rule_id = None
            pos_b, pos_a = rule.pos_b, rule.pos_b

        if head_rule_name not in head_parts:
            head_parts[head_rule_name] = build_fsm(
                wordlist, head_rule_name, pos_b, pos_a, head_rule_id, head_rare,
                load=load, save=save
            )
        # filling in the modifier FSM
        if mod_rules:
            # interfix
            mod_rule = derivator.rules_dict[mod_rules[0]]
            mod_rule_name = mod_rule.name
            mod_rule_id = mod_rule_name
            pos_b, pos_a = mod_rule.pos_b, mod_rule.pos_b
        elif pos_m == '*':
            # star
            mod_rule_name = rule.name
            mod_rule_id = None
            pos_b, pos_a = "*", "*"
        else:
            # adv, noun, etc.
            mod_rule_name = pos_m
            mod_rule_id = None
            pos_b, pos_a = pos_m, pos_m
        mod_parts[mod_rule_name] = build_fsm(
            wordlist, mod_rule_name, pos_b, pos_a, mod_rule_id, mod_rare,
            load=load, save=save
        )
    return derivator, head_parts, mod_parts, head_rare, mod_rare
