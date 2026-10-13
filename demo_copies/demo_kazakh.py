'''Copy of demo/demo_kazakh.py (2022_version branch). Kazakh derivational demo.'''
import os, sys
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, REPO)
from derivbase_ru.derivation import Derivation, TagGuesserWrapper

guesser = TagGuesserWrapper(lang='kaz')
derivation = Derivation(lang='kaz', guesser=guesser)
res = derivation.derive(word_b='аласа', pos_b='adj', is_extended=True)
for k, vs in res.items():
    print(k, vs)
