'''Copy of the README usage example, adapted to the 2022_version API.

Note: the README also shows derive_ext(...), which no longer exists on Derivation;
is_extended=True now returns a {rule_id: {words}} mapping instead of (word, rule) tuples.
'''
import os, sys
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, REPO)
from src.derivation import Derivation

evaluator = Derivation()
out = evaluator.derive(word_b='красить', pos_b='verb', pos_a='adj')
print('derive(красить, verb->adj):', len(out), 'words')
print(sorted(out))
