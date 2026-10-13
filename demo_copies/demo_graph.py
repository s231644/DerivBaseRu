'''Copy of demo/demo_graph.ipynb (2022_version). Derivational connections vs Wiktionary vocab.'''
import os, sys
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, REPO)
from src.derivation import Derivation, TagGuesserWrapper

derivator = Derivation(guesser=TagGuesserWrapper(lang='rus'))

def load_words_by_pos(pos):
    res = set()
    with open(os.path.join(REPO, 'data', 'wiktionary', pos + '.txt'), encoding='utf8') as f:
        for l in f:
            res.add(l.strip())
    return res

pos_all = ['noun', 'adj', 'verb', 'adv']
words_by_pos = {pos: load_words_by_pos(pos) for pos in pos_all}
print('vocabulary sizes:', {k: len(v) for k, v in words_by_pos.items()})

def find_connections(word_b, pos_b, pos_a):
    connections = []
    # 2022 API: is_extended=True returns {word_a: [rule_id, ...]}
    derived = derivator.derive(word_b, pos_b=pos_b, pos_a=pos_a, is_extended=True, use_rare=True)
    exist = set(derived) & words_by_pos[pos_a]
    connections.extend([(word_b, pos_b, wa, pos_a, tuple(derived[wa])) for wa in sorted(exist)])
    return connections

def find_all_word_connections(word_b, pos_b):
    out = []
    for pos_a in pos_all:
        out.extend(find_connections(word_b, pos_b, pos_a))
    return out

print('== connections of желать/verb ==')
for c in find_all_word_connections('желать', 'verb'):
    print('  ', c)

derived = derivator.derive('быстро', pos_b='adv', is_extended=True, use_rare=True)
print('== derive быстро/adv: rules with hits =', len(derived), '==')
