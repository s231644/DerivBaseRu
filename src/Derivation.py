import os
from collections import defaultdict

from src.guesser.ZaliznyakGuesser import *
from src.DependencyDerivation import *


class Results:
    def __init__(self, words_a: Set[str] = {}, rule_id: str = None):
        self.data = defaultdict(set)
        self.derived = set()

        if rule_id is not None:
            self.data[rule_id] |= words_a
            self.derived |= words_a

    def __add__(self, other):
        if other is not None:
            for k in other.data:
                self.data[k] |= other.data[k]
            self.derived |= other.derived
        return self


class Derivation:
    def __init__(self, use_guesser: bool = False, **kwargs):
        self.use_guesser = use_guesser
        if self.use_guesser:
            self.tag_guesser = ZaliznyakGuesser(**kwargs)
        self.pos_all = ['noun', 'adj', 'verb', 'adv', 'num']
        self.rules = []
        self.rules_complex = []
        self.rules_dict = dict()

        # basic rules
        for pos in self.pos_all:
            rule_folder = os.path.join(os.path.dirname(__file__), 'rules', pos, 'simple')
            for rule_file in os.listdir(rule_folder):
                if not rule_file.endswith('.json'):
                    continue
                self.rules.extend(load_rules_from_json(os.path.join(rule_folder, rule_file), 'b', rule_type='simple'))

        for rule in self.rules:
            self.rules_dict[rule.name] = rule

        # complex rules
        for pos in self.pos_all:
            rule_folder = os.path.join(os.path.dirname(__file__), 'rules', pos, 'complex')
            if not os.path.exists(rule_folder):
                continue
            for rule_file in os.listdir(rule_folder):
                if not rule_file.endswith('.json'):
                    continue
                self.rules_complex.extend(load_rules_from_json(os.path.join(rule_folder, rule_file), 'b', rule_type='complex'))

        for rule in self.rules_complex:
            try:
                rule.simple_rules = [self.rules_dict[simple_rule_id] for simple_rule_id in rule.simple_rule_ids]
            except AttributeError:
                print("AttributeError:", rule.name)

        for rule in self.rules_complex:
            self.rules_dict[rule.name] = rule

        self.rules.extend(self.rules_complex)
        
        # TODO: compound rules
        self.rules_compound = []
        
        rule_folder = os.path.join(os.path.dirname(__file__), 'rules')
        self.rules_compound.extend(load_rules_from_json(os.path.join(rule_folder, 'compounds.json'), 'b', rule_type='compound'))
        for rule in self.rules_compound:
            try:
                for simple_rule_ids in rule.simple_rule_ids:
                    rule.simple_rules.append([self.rules_dict[simple_rule_id] for simple_rule_id in simple_rule_ids])
                rule.before_merge_rules = [self.rules_dict[simple_rule_id] for simple_rule_id in rule.before_merge_rule_ids]
                rule.after_merge_rules = [self.rules_dict[simple_rule_id] for simple_rule_id in rule.after_merge_rule_ids]
            except:
                print("Error:", rule.name)

    def _derive_with_rule(self, word_b: str, pos_b: str = None, pos_a: str = None, rule: WholeRule = None,
                          **kwargs) -> Results:
        results = []
        pos_b_all = [pos_b] if pos_b is not None else self.pos_all
        pos_a_all = [pos_a] if pos_a is not None else self.pos_all
        for pos_b_ in pos_b_all:
            for pos_a_ in pos_a_all:
                results.extend(rule.apply_with_tags(word_b, pos_b_, pos_a_, **kwargs))

        return Results(set(results), rule.name)

    def _derive(self, word_b: str, pos_b: str = None, pos_a: str = None, rule: WholeRule = None, **kwargs) -> Results:
        results = Results()
        if rule is not None:
            results += self._derive_with_rule(word_b, pos_b, pos_a, rule, **kwargs)
        else:
            for rule_ in self.rules:
                if (not rule_.only_complex) or kwargs.get('force_complex'):
                    results += self._derive_with_rule(word_b, pos_b, pos_a, rule_, **kwargs)
        return results

    def derive(self, word_b: str, pos_b: str = None, pos_a: str = None, rule_id: str = None, is_extended: bool = True,
               **kwargs):
        if self.use_guesser:
            tags_all = self.tag_guesser.guess(word=word_b, pos=pos_b, **kwargs)
        else:
            tags_all = [dict()]

        if not tags_all:
            tags_all = [dict()]

        rule = self.rules_dict.get(rule_id)

        results = Results()
        for tags in tags_all:
            tags.update(**kwargs)
            results += self._derive(word_b, pos_b, pos_a, rule, **tags)

        if is_extended:
            return {k: results.data[k] for k in results.data if results.data[k]}
        else:
            return results.derived

"""
evaluator = Derivation(use_guesser=True)
res = evaluator.derive('польза', pos_b='noun', is_extended=True)
#res = evaluator.derive('натянуть', pos_b='verb', is_extended=True)
print(res)
"""