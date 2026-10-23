"""Conservative paradigm check for interfix forms of compound modifiers.

The rule engine proposes forms; a known, declinable lemma's genitive stem
must support them. This checks morphology, not semantic derivation.
"""


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
    parses = [p for p in morph.parse(word)
              if p.is_known and normalize(p.normal_form) == normalize(word)
              and p.tag.POS == {'noun': 'NOUN', 'adj': 'ADJF'}[pos]
              and 'nomn' in p.tag]
    if not parses:
        return {}, 'no_known_lemma'
    declinable = [p for p in parses if 'Fixd' not in p.tag]
    if not declinable:
        return {}, 'indeclinable'
    evidence = []
    for parse in declinable:
        plural = 'Pltm' in parse.tag
        gen = parse.inflect({'gent', 'plur' if plural else 'sing'})
        if gen is None or gen.word == parse.word:
            continue
        stem = genitive_stem(gen.word, pos, plural)
        if stem:
            evidence.append({'lemma': parse.normal_form, 'tag': str(parse.tag),
                             'genitive': gen.word, 'stem': stem,
                             'source': 'pymorphy3'})
    if not evidence:
        return {}, 'no_genitive_stem'
    current = {word}
    for subrule in chain:
        current = {v for w in current for v in subrule.apply(w, use_rare=True)}
    # Rebuild from the attested oblique stem too: the generic delvowel
    # operation incorrectly inserts a soft sign in ложь -> льже.
    if pos == 'noun':
        for e in evidence:
            rebuilt = {e['stem']}
            for subrule in chain:
                rebuilt = {v for w in rebuilt
                           for v in subrule.apply(w, use_rare=True)}
            current.update(v for v in rebuilt
                           if v.endswith(('о', 'е'))
                           and normalize(v[:-1]) == normalize(e['stem']))
    exceptions = (chain[0].rare_straight.get(word, set())
                  if len(chain) == 1 else set())
    accepted = {}
    for form in sorted(current):
        # Interfix-bearing form, or a bare stem licensed by nochange.
        stems = {normalize(form)}
        if form.endswith(('о', 'е')):
            stems.add(normalize(form[:-1]))
        proofs = [e for e in evidence if normalize(e['stem']) in stems]
        if proofs:
            accepted[form] = proofs
        elif form in exceptions:
            accepted[form] = [dict(e, rule_exception=True) for e in evidence]
    return accepted, None if accepted else 'unsupported_stem'
