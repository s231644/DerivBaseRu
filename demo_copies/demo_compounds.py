'''Copy of demo/Demo compounds.ipynb (2022_version branch).

The original notebook uses an older API: import paths derivbase_ru.compounding.fsm_part /
derivbase_ru.compounding.compound_analyzer, a class-level DerivedFSM.derivator, positional DerivedFSM
arguments and Derivation(use_guesser=True). This copy targets the current code:
  * imports from derivbase_ru.compounding.*
  * DerivedFSM(derivator, name, pos_b, pos_a, rule_id, wordlist)
  * Derivation(guesser=TagGuesserWrapper())
  * guarded multiprocessing entry point (DerivedFSM uses Pool) to avoid spawn recursion
'''
import os, sys
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, REPO)

from derivbase_ru.derivation import Derivation, TagGuesserWrapper
from derivbase_ru.compounding.fsm_part import DerivedFSM
from derivbase_ru.compounding.compound_analyzer import CompoundAnalyzer


def main():
    derivator = Derivation(guesser=TagGuesserWrapper(lang='rus'))
    cr = derivator.loaded_rules['compound']
    print('compound rules:', len(cr))

    # Left (modifier) and right (head) finite-state parts. With rule_id=None a part
    # stores its surface forms literally; a real run would pass a rule_id to derive them.
    left = DerivedFSM(derivator, 'left', 'noun', 'noun', rule_id=None, wordlist=['еже', 'полу'])
    right = DerivedFSM(derivator, 'right', 'noun', 'noun', rule_id=None, wordlist=['монета', 'сладкий'])
    ca = CompoundAnalyzer('demo([mod] + [head] -> noun)', 'noun', left, right)
    for w in ['ежемонета', 'полумонета', 'монета']:
        print('  analyze', w, '->', ca.analyze(w, 'noun'))

    print('  left.analyze_word(ежемонета) ->', left.analyze_word('ежемонета'))
    print('  right.analyze_word(монета)   ->', right.analyze_word('монета'))


if __name__ == '__main__':
    main()
