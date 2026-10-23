"""Conservative paradigm check for interfix forms of compound modifiers.

The rule engine proposes forms; a known, declinable lemma's genitive stem
must support them. This checks morphology, not semantic derivation.
"""
from functools import lru_cache
from pathlib import Path

from derivbase_ru.rule_utils import load_rules_from_json


PROPER_TAGS = {'Name', 'Surn', 'Patr', 'Geox', 'Orgn', 'Trad'}
INFLECTION_PATH = (Path(__file__).resolve().parents[1] /
                   'derivbase_ru/rules/rus/rules_inflection.json')


@lru_cache(maxsize=1)
def nominal_rules():
    return {r.pos_b: r for r in load_rules_from_json(str(INFLECTION_PATH), 'a')
            if r.pos_b in {'noun', 'adj'}}


def declension_tags(word, pos, parse):
    """Structural Zaliznyak types from existing rules, constrained by morphology.

    These are the engine's types 1–8, not school declensions or accent classes.
    Preserve alternatives as separate contexts; never union their genders/types.
    """
    gender = {'masc': 'm', 'femn': 'f', 'neut': 'n'}.get(parse.tag.gender)
    number = {'sing': 's', 'plur': 'p'}.get(parse.tag.number)
    if not gender and number != 'p':
        return []
    result = []
    for subrule in nominal_rules()[pos].subrules:
        tags = subrule.tags_b
        if 'number' in tags and number not in tags['number']:
            continue
        if gender and gender not in tags.get('gender', {gender}):
            # Masculine nouns in -а/-я share the corresponding feminine
            # structural pattern (папа, дядя); retain their actual gender.
            if not (pos == 'noun' and gender == 'm'
                    and word.endswith(('а', 'я')) and 'f' in tags['gender']):
                continue
        if not subrule.apply(word):
            continue
        context = {k: set(v) for k, v in tags.items()}
        context['gender'] = {gender or 'p'}
        if context not in result:
            result.append(context)
    return result


def apply_tagged_chain(word, chain, tags):
    current = {word}
    for rule in chain:
        # The engine treats missing tags as wildcards. Fail closed here.
        if any(set(sub.tags_b) - tags.keys() for sub in rule.subrules):
            raise ValueError('Missing interfix context: ' + rule.name)
        current = {v for w in current for v in rule.apply(w, use_rare=True, **tags)}
    return current


def normalize(word):
    return word.lower().replace('ё', 'е')


def genitive_stem(word, pos, plural=False):
    endings = ('ого', 'его') if pos == 'adj' else (
        ('ов', 'ев', 'ей', 'ий', 'ь', 'й') if plural
        else ('ы', 'и', 'а', 'я'))
    for ending in endings:
        if word.endswith(ending):
            return word[:-len(ending)]
    # A zero genitive ending is possible for plural-only nouns.
    return word if plural else None


def checked_modifier_forms(word, pos, chain, morph):
    """Return (form -> evidence, exclusion reason).

    Keep all matching dictionary paradigms, never just the most likely parse.
    Unknown/predicted lemmas and missing paradigms are excluded explicitly.
    Explicit rule exceptions can override stem matching, but not declinability.
    """
    if any(c.isupper() for c in word):
        return {}, 'proper_name'
    parses = [p for p in morph.parse(word)
              if p.is_known and normalize(p.normal_form) == normalize(word)
              and p.tag.POS == {'noun': 'NOUN', 'adj': 'ADJF'}[pos]
              and 'nomn' in p.tag]
    if not parses:
        return {}, 'no_known_lemma'
    parses = [p for p in parses if not (PROPER_TAGS & p.tag.grammemes)]
    if not parses:
        return {}, 'proper_name'
    declinable = [p for p in parses if 'Fixd' not in p.tag]
    if not declinable:
        return {}, 'indeclinable'
    accepted = {}
    has_type = False
    has_genitive = False
    for parse in declinable:
        contexts = declension_tags(word, pos, parse)
        if not contexts:
            continue
        has_type = True
        plural = 'Pltm' in parse.tag
        gen = parse.inflect({'gent', 'plur' if plural else 'sing'})
        if gen is None or gen.word == parse.word:
            continue
        stem = genitive_stem(gen.word, pos, plural)
        if not stem:
            continue
        has_genitive = True
        for tags in contexts:
            e = {'lemma': parse.normal_form, 'tag': str(parse.tag),
                 'genitive': gen.word, 'stem': stem, 'source': 'pymorphy3',
                 'declension_source': 'rules_inflection.json+pymorphy3',
                 'inflect_type': sorted(tags['inflect_type']),
                 'rule_tags': {k: sorted(v) for k, v in sorted(tags.items())}}
            current = apply_tagged_chain(word, chain, tags)
            # Repair fleeting vowels using only interfixes licensed by
            # this very paradigm, e.g. ложь -> лжи -> лже, not льже.
            if pos == 'noun':
                current |= {stem + v[-1] for v in current
                            if v.endswith(('о', 'е'))}
            exceptions = (chain[0].rare_straight.get(word, set())
                          if len(chain) == 1 else set())
            for form in sorted(current):
                if (form.endswith(('о', 'е'))
                        and normalize(form[:-1]) == normalize(stem)):
                    proof = e
                elif form in exceptions:
                    proof = dict(e, rule_exception=True)
                else:
                    continue
                if proof not in accepted.setdefault(form, []):
                    accepted[form].append(proof)
    if accepted:
        return dict(sorted(accepted.items())), None
    return {}, ('no_declension_type' if not has_type else
                'no_genitive_stem' if not has_genitive else 'unsupported_stem')
