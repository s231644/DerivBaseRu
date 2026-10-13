import os
import warnings

from collections import defaultdict
from typing import Set, Optional, List

from derivbase_ru.cache import ResultCache, rule_fingerprint
from derivbase_ru.rule import WholeRule
from derivbase_ru.rule_utils import load_rules_from_json


class Results:
    def __init__(
            self,
            words_a: Optional[Set[str]] = None,
            rule_id: Optional[str] = None
    ):
        self.data = defaultdict(set)
        self.derived = set()

        if rule_id is not None and words_a is not None:
            self.data[rule_id] |= words_a
            self.derived |= words_a

    def __add__(self, other):
        if other is not None:
            for k in other.data:
                self.data[k] |= other.data[k]
            self.derived |= other.derived
        return self


class TagGuesserWrapper:
    def __init__(self, lang: str = "rus", **kwargs):
        if lang == "rus":
            from derivbase_ru.guesser.ZaliznyakGuesser import ZaliznyakGuesser
            self.guesser = ZaliznyakGuesser(**kwargs)
            pass
        elif lang == "kaz":
            from derivbase_ru.guesser.kazakh_guesser import BarakhninGuesser
            self.guesser = BarakhninGuesser(**kwargs)
        else:
            raise ValueError(f"Unsupported language {lang}!")

    def guess(self, *args, **kwargs):
        return self.guesser.guess(*args, **kwargs)


class Derivation:
    pos_all = ['noun', 'adj', 'verb', 'adv', 'num']
    complexities = ['simple', 'complex', 'compound']

    def __init__(
            self,
            lang: str = "rus",
            guesser: Optional[TagGuesserWrapper] = None,
            cache: Optional[ResultCache] = None,
    ):
        self.lang = lang
        self.tag_guesser = guesser
        self.cache = cache

        self.rules_dict = dict()

        # load rules from files
        self.loaded_rules = {
            complexity: []
            for complexity in self.complexities
        }
        for complexity in self.complexities:
            for pos in self.pos_all:
                self._load_rules_from_file(pos, complexity)

        # initialize simple rules
        for rule in self.loaded_rules["simple"]:
            self.rules_dict[rule.name] = rule

        # initialize complex rules
        for rule in self.loaded_rules["complex"]:
            try:
                rule.simple_rules = [
                    self.rules_dict[simple_rule_id]
                    for simple_rule_id in rule.simple_rule_ids
                ]
            except Exception as e:
                warnings.warn(f"Could not load rule {rule.name}: {e}")
                continue
            self.rules_dict[rule.name] = rule

        for rule in self.loaded_rules["compound"]:
            try:
                for simple_rule_ids in rule.simple_rule_ids:
                    rule.simple_rules.append(
                        [
                            self.rules_dict[simple_rule_id]
                            for simple_rule_id in simple_rule_ids
                        ]
                    )
                rule.before_merge_rules = [
                    self.rules_dict[simple_rule_id]
                    for simple_rule_id in rule.before_merge_rule_ids
                ]
                rule.after_merge_rules = [
                    self.rules_dict[simple_rule_id]
                    for simple_rule_id in rule.after_merge_rule_ids
                ]
            except Exception as e:
                warnings.warn(f"Could not load rule {rule.name}: {e}")
                continue
            self.rules_dict[rule.name] = rule

    def _load_rules_from_file(self, pos: str, complexity: str):
        rule_folder = os.path.join(
            os.path.dirname(__file__),
            'rules', self.lang, pos, complexity
        )
        if not os.path.exists(rule_folder):
            # warnings.warn(
            #     f"Could not load {complexity} rules "
            #     f"for lang={self.lang} pos={pos}"
            # )
            return
        for rule_file in os.listdir(rule_folder):
            if not rule_file.endswith('.json'):
                continue
            new_rules = load_rules_from_json(
                os.path.join(rule_folder, rule_file),
                'b',
                rule_type=complexity,
                lang=self.lang
            )
            self.loaded_rules[complexity].extend(new_rules)

    def _derive_with_rule(
            self,
            rule: WholeRule,
            word_b: str,
            pos_b: Optional[str] = None,
            pos_a: Optional[str] = None,
            **kwargs
    ) -> Results:
        cache = getattr(self, "cache", None)
        key = None
        if cache is not None:
            fingerprint = rule.__dict__.get("_fingerprint")
            if fingerprint is None:
                fingerprint = rule_fingerprint(rule)
                rule.__dict__["_fingerprint"] = fingerprint
            key = cache.make_key(
                word_b, pos_b, pos_a, fingerprint,
                {"use_rare": bool(kwargs.get("use_rare"))},
            )
            cached = cache.get(key)
            if cached is not None:
                return Results(set(cached), rule.name)

        results = []
        pos_b_all = [pos_b] if pos_b is not None else self.pos_all
        pos_a_all = [pos_a] if pos_a is not None else self.pos_all
        for pos_b_ in pos_b_all:
            for pos_a_ in pos_a_all:
                results.extend(
                    rule.apply_with_tags(word_b, pos_b_, pos_a_, **kwargs)
                )

        derived = Results(set(results), rule.name)
        if cache is not None:
            cache.set(key, derived.derived)
        return derived

    def _derive(
            self,
            word_b: str,
            pos_b: str = None,
            pos_a: str = None,
            rule: Optional[WholeRule] = None,
            derive_simple: bool = True,
            derive_complex: bool = True,
            derive_compound: bool = True,
            tags_m: Optional[List[dict]] = None,
            **kwargs
    ) -> Results:
        results = Results()
        if rule is not None:
            results += self._derive_with_rule(
                rule, word_b, pos_b, pos_a, **kwargs
            )
        else:
            rules = []
            if derive_simple:
                rules.extend(self.loaded_rules["simple"])
            if derive_complex:
                rules.extend(self.loaded_rules["complex"])
            if derive_compound:
                rules.extend(self.loaded_rules["compound"])

            for rule_cls in rules:
                rule_ = self.rules_dict.get(rule_cls.name)
                if not rule_:
                    continue
                if (not rule_.only_complex) or kwargs.get('force_complex'):
                    results += self._derive_with_rule(
                        rule_, word_b, pos_b, pos_a,
                        tags_m=tags_m,
                        **kwargs
                    )
        return results

    def derive(
            self,
            word_b: str,
            pos_b: Optional[str] = None,
            pos_a: Optional[str] = None,
            words_m: Optional[List[str]] = None,
            poss_m: Optional[List[str]] = None,
            rule_id: Optional[str] = None,
            is_extended: bool = True,
            derive_simple: bool = True,
            derive_complex: bool = True,
            derive_compound: bool = True,
            tags: Optional[dict] = None,
            tags_m: Optional[List[dict]] = None,
            **kwargs
    ):
        tags_m_all = []

        if self.tag_guesser:
            tags_all = self.tag_guesser.guess(word=word_b, pos=pos_b, **kwargs)
            if not tags_all:
                tags_all = [tags or dict()]

            if words_m:
                for i, word_m in enumerate(words_m):
                    pos_m = poss_m[i] if poss_m else None
                    tags_m_all.append(
                        self.tag_guesser.guess(word=word_m, pos=pos_m, **kwargs)
                    )
        else:
            tags_all = [tags or dict()]
            if words_m:
                tags_m_all = tags_m or [dict()] * len(words_m)

        rule = self.rules_dict.get(rule_id)

        results = Results()
        for tags in tags_all:
            tags.update(**kwargs)
            results += self._derive(
                word_b, pos_b, pos_a, rule,
                words_m=words_m,
                tags_m=tags_m_all,
                poss_m=poss_m,
                derive_simple=derive_simple,
                derive_complex=derive_complex,
                derive_compound=derive_compound,
                **tags
            )

        if is_extended:
            d = defaultdict(list)
            for k in results.data:
                for wa in results.data[k]:
                    d[wa].append(k)
            return d
        else:
            return results.derived
