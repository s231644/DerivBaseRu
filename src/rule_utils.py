import json
import warnings

from src.rule import SubRule, WholeRule, ComplexRule, CompoundRule


def load_rules_from_json(
        json_file,
        tag_type='b',
        rule_type='simple',
        lang='rus'
):
    if lang == "rus":
        from src.stringops.rus import RussianOps
        lang_ops = RussianOps()
    else:
        from src.stringops.base import LanguageOps
        lang_ops = LanguageOps()
        warnings.warn(
            f"Unsupported language {lang}! "
            f"You can use only language-independent functions on strings."
        )

    rules = []
    with open(json_file, encoding='utf-8') as data_file:
        try:
            data = json.loads(data_file.read())
        except Exception as e:
            warnings.warn(f'Could not load file {json_file}: {e}')
        for json_rule in data['data']:
            try:
                if rule_type == 'simple':
                    subrules = [
                        SubRule(
                            tags_b=case[f'tags_{tag_type}'],
                            raw_rules=case['rules'],
                            lang_ops=lang_ops

                        ) for case in json_rule.get('cases', [])
                    ]
                    rule = WholeRule(
                        name=json_rule.get('rule_id'),
                        short_id=json_rule.get('short_id'),
                        pos_b=json_rule.get('pos_b'),
                        pos_a=json_rule.get('pos_a'),
                        info=json_rule.get('info'),
                        only_complex=json_rule.get('only_complex') is not None,
                        rare=json_rule.get('rare') or [],
                        subrules=subrules
                    )
                elif rule_type == 'complex':
                    rule = ComplexRule(
                        name=json_rule.get('rule_id'),
                        pos_b=json_rule.get('pos_b'),
                        pos_a=json_rule.get('pos_a'),
                        info=json_rule.get('info'),
                        only_complex=False,
                        rare=json_rule.get('rare') or [],
                        simple_rule_ids=json_rule.get('complex')
                    )
                elif rule_type == 'compound':
                    rule = CompoundRule(
                        name=json_rule.get('rule_id'),
                        pos_b=json_rule.get('pos_b'),
                        pos_a=json_rule.get('pos_a'),
                        info=json_rule.get('info'),
                        only_complex=False,
                        rare=json_rule.get('rare') or [],
                        compound_rules=json_rule.get('compound_rules')
                    )
                else:
                    continue
                rules.append(rule)
            except Exception as e:
                warnings.warn(
                    f"Could not read the rule {json_rule.get('rule_id')}: {e}"
                )
    return rules
