import os
import json
import pymorphy2
from itertools import chain as chain
from functools import reduce
from src.Rule import *
import warnings

"""
converter_of_verb_types = {'1а': '1', '1я': '1', '1е': '1',
                           '2о': '2', '2е*': '2', '2е': '2',
                           '5а': '5', '5я': '5', '5е': '5',
                           '5ща': '5щ', '5щя': '5щ', '5ще': '5щ',
                           '6а': '6', '6я': '6',
                           '6ща': '6щ', '6щя': '6щ',
                           }
"""
converter_of_verb_types = {
    '1а': '1', '1я': '1', '1е': '1',
    '2о': '2', '2е*': '2', '2е': '2',
    '4щ': '4', '4е': '4', '4*': '4',
    '5а': '5', '5я': '5', '5е': '5',
    '5ща': '5', '5щя': '5', '5ще': '5',
    '6а': '6', '6я': '6', '6е': '6',
    '6ща': '6', '6щя': '6'
}

order_of_verb_types = {
    '1': 1,
    '2': 1,
    '3': 1,
    '4щ': 1, '4': 2, '4*': 1,
    '5щ': 1, '5': 2,
    '6щ': 1, '6': 2,
    '7з': 1, '7б': 1, '7с': 1, '7д': 1, '7т': 1, '7ст': 1,
    '8г': 1, '8к': 1, '8*3': 1,
    '9': 1,
    '10ор': 1, '10ел': 1, '10ол': 1,
    '11': 1,
    '12ы': 1, '12у': 1, '12и': 1, '12греть': 1, '12брить': 1, '12петь': 1,
    '13': 1,
    '14н': 1, '14м': 1, '14ним': 1, '14ьм': 1, '14ым': 1, '14им': 1, '14йм': 1,
    '15': 2,
    '16': 1,
    'клясть': 1, 'есть': 1, 'дать': 1,'быть': 1, 'ехать': 1, 'идти': 1
}


class ZaliznyakGuesser:
    def __init__(self, use_morph=True):
        self.use_morph = use_morph
        if self.use_morph:
            self.morph = pymorphy2.MorphAnalyzer()
        self.pos_all = ['noun', 'adj', 'verb', 'adv']

        inflection_rules = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            'rules',
            'rules_inflection.json'
        )

        self.rules = load_rules_from_json(inflection_rules, 'a')

    def _find_possible_tags(self, word: str, pos: str, **kwargs) -> List[Dict[str, str]]:
        possible_variants = list()
        for rule in self.rules:
            if rule.pos_b != pos:
                continue
            for subrule in rule.subrules:
                if len(subrule.apply(word)) > 0:
                    possible_variants.append(subrule.tags_b)
        return possible_variants

    def _find_tags_verb(self, inf: str, per1: str, per3: str, **kwargs) -> List[Dict[str, str]]:
        possible_variants = []
        for verb_form, verb_tag in [(inf, 'inf'), (per1, 'per1'), (per3, 'per3')]:
            form_vars = self._find_possible_tags(verb_form, 'verb')
            possible_variants.append(
                set(chain.from_iterable([elem['inflect_type'] for elem in form_vars if verb_tag in elem['form']])))
        possible_variants = reduce(lambda x, y: x & y, possible_variants)
        possible_variants = list(set(map(lambda x: converter_of_verb_types.setdefault(x, x), possible_variants)))
        possible_variants.sort(key=lambda x: order_of_verb_types[x])
        return [{'inflect_type': [x] for x in possible_variants}]

    def _find_possible_tags_verb(self, word: str, per1: str = None, per3: str = None, **kwargs):
        if per1 and per3:
            return self._find_tags_verb(word, per1, per3, **kwargs)
        possible_variants = list()
        if not self.use_morph:
             warnings.warn(f'Morph is not defined! {word}', UserWarning)
        morph_word = self.morph.parse(word)
        for var in morph_word:
            if var.tag.POS in ['INFN']:
                try:
                    per1_ = var.inflect({'1per'}).word.replace('ё', 'е')
                    per3_ = var.inflect({'3per'}).word.replace('ё', 'е')
                    possible_variants.extend(self._find_tags_verb(word, per1_, per3_, **kwargs))
                except:
                    warnings.warn(f'Cannot inflect {word}!', UserWarning)
        return possible_variants

    def guess(self, word: str, pos: str = None, **kwargs) -> List[Dict[str, str]]:
        possible_variants = list()
        pos = [pos] if pos is not None else self.pos_all
        for pos_ in pos:
            if pos_ == 'verb':
                possible_variants.extend(self._find_possible_tags_verb(word, **kwargs))
            else:
                possible_variants.extend(self._find_possible_tags(word, pos_, **kwargs))
        return possible_variants
