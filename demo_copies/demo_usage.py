'''Adapted copy of demo/demo_usage.ipynb for the 2022_version code base.

Fixes vs. the original notebook:
  * import path case:  src.Derivation      -> src.derivation
  * constructor API:   use_guesser=True    -> guesser=TagGuesserWrapper(lang='rus')
  * attribute names:   derivator.rules     -> derivator.loaded_rules / rules_dict
'''
import os, sys
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, REPO)

from src.derivation import Derivation, TagGuesserWrapper

derivator = Derivation(guesser=TagGuesserWrapper(lang='rus'))

print('== tag guesser ==')
for w, p in [('конь','noun'), ('красивый','adj'), ('желать','verb')]:
    print(' ', w, '/', p, '->', derivator.tag_guesser.guess(word=w, pos=p))

print('== rules ==')
print(' loaded_rules:', {k: len(v) for k, v in derivator.loaded_rules.items()})
print(' rules_dict  :', len(derivator.rules_dict))

print('== rule apply ==')
rule = derivator.rules_dict['rule213(verb + щик -> noun)']
print(' rule213(укладывать) ->', rule.apply('укладывать'))

print('== derive(смотреть, verb) ==')
res = derivator.derive('смотреть', pos_b='verb', is_extended=False, use_rare=True)
print(' flat:', len(res), 'words ->', sorted(res)[:15], '...')
res_ext = derivator.derive('смотреть', pos_b='verb', is_extended=True, use_rare=True)
print(' extended: rules with hits =', len(res_ext))

from collections import defaultdict
stats = defaultdict(int)
for r in (derivator.loaded_rules['simple'] + derivator.loaded_rules['complex']):
    stats[(r.pos_b, r.pos_a, getattr(r, 'info', None))] += 1
print('== derivation-type stats (sample) ==')
for k, v in list(stats.items())[:6]:
    print('  ', k, v)
print(' total rule types:', len(stats))
