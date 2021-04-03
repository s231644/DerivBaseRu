import json
from itertools import product
from lark.tree import pydot__tree_to_png
from collections import defaultdict

from src.loading_rules_to_tree import *
from src.functions import *


class SubRule:
    def __init__(self, tags_b: Dict[str, str], raw_rules: str):
        self.tags_b = dict()
        for tag in tags_b:
            possible_values = tags_b[tag].split(',')
            self.tags_b[tag] = possible_values
        self.logical_form, self.operators = normalize_raw_text(raw_rules)
        self.tree = short_parser.parse(self.logical_form)

    def plot_tree(self, filename: str = 'tree'):
        pydot__tree_to_png(self.tree, filename + ".png")

    def compute_tree(self, tree, cur_results: List[str]) -> List[str]:
        if hasattr(tree.children[0], 'value'):
            command = self.operators[int(tree.children[0].value)]
            new_results = []
            for word in cur_results:
                new_results += eval(command)
        elif tree.children[0].data == 'or':
            new_results = []
            for child in tree.children[0].children:
                new_results += self.compute_tree(child, cur_results)
        elif tree.children[0].data == 'and':
            new_results = self.compute_tree(tree.children[0].children[0], cur_results)
            new_results = self.compute_tree(tree.children[0].children[1], new_results)
        else:
            new_results = []
        return new_results

    def check(self, **kwargs) -> bool:
        for tag in self.tags_b:
            if kwargs.get(tag) is not None and not (set(kwargs[tag]) & set(self.tags_b[tag])):
                return False
        return True

    def apply(self, word_b: str, **kwargs) -> Set[str]:
        if not self.check(**kwargs):
            return set()
        try:
            return set(self.compute_tree(self.tree, [word_b]))
        except:
            return set()


class WholeRule:
    def __init__(self, name: str, short_id: str, pos_b: str, pos_a: str, info: str = '', only_complex: bool = False, rare: List[str] = [], subrules: List[SubRule] = None):
        self.name = name
        self.short_id = short_id
        self.info = info
        self.pos_a = pos_a
        self.pos_b = pos_b
        self.only_complex = only_complex
        self.rare = list(map(lambda x: x.split(';'), rare))
        self.subrules = subrules if subrules is not None else []

        self.rare_straight = defaultdict(set)
        self.rare_inversed = defaultdict(set)
        for s, i in self.rare:
            self.rare_straight[s].add(i)
            self.rare_inversed[i].add(s)

    def __repr__(self):
        return f'{self.name}\t({self.short_id})'

    def check(self, pos_b: str = None, pos_a: str = None):
        return self.pos_b == pos_b and self.pos_a == pos_a

    def apply(self, word_b: str, **kwargs) -> Set[str]:
        results = set()
        for subrule in self.subrules:
            results |= subrule.apply(word_b, **kwargs)

        if kwargs.get('use_rare'):
            results |= self.rare_straight[word_b]
        return results

    def apply_with_tags(self, word_b: str, pos_b: str = None, pos_a: str = None, **kwargs) -> Set[str]:
        if not self.check(pos_b, pos_a):
            return set()
        return self.apply(word_b, **kwargs)


class ComplexRule(WholeRule):
    def __init__(self, name: str, pos_b: str, pos_a: str, info: str = '', only_complex: bool = False, rare: List[str] = [], simple_rule_ids: List[str] = None):
        WholeRule.__init__(self, name, '-', pos_b, pos_a, info, only_complex, rare, None)
        self.simple_rule_ids = simple_rule_ids if simple_rule_ids is not None else []
        self.simple_rules = []  # need to get WholeRule_s by their ids later in Derivation class

    def apply(self, word: str, **kwargs):
        cur_results = {word}
        for simple_rule in self.simple_rules:
            new_results = set()
            for word in cur_results:
                new_results |= simple_rule.apply(word)
            cur_results = new_results
        return cur_results

    def apply_with_tags(self, word_b: str, pos_b: str = None, pos_a: str = None, **kwargs):
        if not self.check(pos_b, pos_a):
            return set()
        # TODO: make possible inner tag analysis by Guesser
        cur_results = {word_b}
        for simple_rule in self.simple_rules:
            new_results = set()
            for word in cur_results:
                new_results |= simple_rule.apply(word, **kwargs)
            kwargs = dict()
            cur_results = new_results
        return cur_results


class CompoundRule(WholeRule):
    def __init__(self, name: str, pos_b: str, pos_a: str, info: str = '', only_complex: bool = False, rare: List[str] = [], 
        compound_rules: Dict = None):
        WholeRule.__init__(self, name, '-', pos_b, pos_a, info, only_complex, rare, None)
        self.n_modifiers = len(compound_rules.get('modifiers') or [])
        self.poss_m = [rule.get('pos_m') for rule in compound_rules.get('modifiers')]
        self.simple_rule_ids = [compound_rules.get('head')] + [rule.get('complex') for rule in compound_rules.get('modifiers')]
        self.simple_rules = []  # need to get WholeRule_s by their ids later in Derivation class
        # a 2D list: 0 --- head, 1 --- first modifier, ...
        self.order = compound_rules.get('order')
        self.before_merge_rule_ids = compound_rules.get('before_merge') 
        self.after_merge_rule_ids = compound_rules.get('after_merge')
        self.before_merge_rules = [] 
        self.after_merge_rules = []


    def check(self, pos_b: str = None, poss_m: List[str] = [], pos_a: str = None):
        return self.pos_b == pos_b and self.pos_a == pos_a and self.poss_m == poss_m

    def apply(self, word_b: str, words_m: List[str], **kwargs):
        results = []

        for i, word_ in enumerate([word_b] + words_m):
            cur_results = {word_}
            for simple_rule in self.simple_rules[i]:
                new_results = set()
                for word in cur_results:
                    new_results |= simple_rule.apply(word)
                cur_results = new_results
            results.append(cur_results)
        permuted_results = [list(results[i]) for i in self.order]
        results = set(map(lambda x: ''.join(x), product(*permuted_results)))
        new_results = set()
        for simple_rule in self.after_merge_rules:
            new_results = set()
            for word in results:
                new_results |= simple_rule.apply(word)
            results = new_results
        return results

    def apply_with_tags(self, word_b: str, pos_b: str = None, pos_a: str = None, words_m: List[str] = [], poss_m: List[str] = [], tags_dict: List[Dict] = [], **kwargs):
        if not self.check(pos_b, poss_m, pos_a):
            return set()
        # TODO: make possible inner tag analysis by Guesser
        results = []

        for i, word_ in enumerate([word_b] + words_m):
            cur_results = {word_}
            step = 0
            for simple_rule in self.simple_rules[i]:
                new_results = set()
                for word in cur_results:
                    if not step:
                        new_results |= simple_rule.apply(word, **tags_dict[i], **kwargs)
                    else:
                        new_results |= simple_rule.apply(word, **kwargs)
                step += 1
                cur_results = new_results
            results.append(cur_results)
        permuted_results = [results[i] for i in self.order]
        results = set(map(lambda x: ''.join(x), product(*permuted_results)))
        new_results = set()
        for simple_rule in self.after_merge_rules:
            new_results = set()
            for word in results:
                new_results |= simple_rule.apply(word)
            results = new_results
        return results


def load_rules_from_json(json_file, tag_type='b', rule_type='simple'):
    rules = []
    with open(json_file, encoding='utf-8') as data_file:
        try:
            data = json.loads(data_file.read())
        except:
            raise AssertionError('error loading file', json_file)
        for json_rule in data['data']:
            try:
                if rule_type == 'simple':
                    subrules = [SubRule(tags_b=case[f'tags_{tag_type}'], raw_rules=case['rules']) for case in json_rule.get('cases')]
                    rules.append(WholeRule(name=json_rule.get('rule_id'), short_id=json_rule.get('short_id'),
                        pos_b=json_rule.get('pos_b'), pos_a=json_rule.get('pos_a'), info=json_rule.get('info'), 
                        only_complex=json_rule.get('only_complex') is not None,
                        rare=json_rule.get('rare') or [], subrules=subrules))
                elif rule_type == 'complex':
                    rules.append(ComplexRule(name=json_rule.get('rule_id'), 
                        pos_b=json_rule.get('pos_b'), pos_a=json_rule.get('pos_a'), info=json_rule.get('info'), 
                        only_complex=False,
                        rare=json_rule.get('rare') or [], simple_rule_ids=json_rule.get('complex')))
                elif rule_type == 'compound':
                    rules.append(CompoundRule(name=json_rule.get('rule_id'),
                        pos_b=json_rule.get('pos_b'), pos_a=json_rule.get('pos_a'), info=json_rule.get('info'),
                        only_complex=False,
                        rare=json_rule.get('rare') or [], compound_rules=json_rule.get('compound_rules')))
            except:
                print("ERROR reading a rule!", json_rule.get('rule_id'))

    return rules
