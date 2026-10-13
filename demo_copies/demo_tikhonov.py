'''Copy of demo/Tikhonov.ipynb (2022_version). Connections between dictionary lemmas.'''
import os, sys
from collections import defaultdict
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, REPO)
import pandas as pd
from src.derivation import Derivation, TagGuesserWrapper

DEMO = os.path.join(REPO, 'demo')
train_df = pd.read_csv(os.path.join(DEMO, 'classification_train.csv'))
test_df = pd.read_csv(os.path.join(DEMO, 'classification_test.csv'))
print('train/test rows:', len(train_df), len(test_df))
train_compounds = train_df[train_df['n_roots'] > 1][['lemma_c', 'pos_c']]
test_compounds = test_df[test_df['n_roots'] > 1][['lemma_c', 'pos_c']]
print('compound lemmas train/test:', len(train_compounds), len(test_compounds))

derivator = Derivation(guesser=TagGuesserWrapper(lang='rus'))
morph = derivator.tag_guesser.guesser.morph   # 2022 API: wrapper.guesser.morph

def get_pos_tag(word):
    try:
        tag = morph.parse(word)[0].tag.POS
        return {'INFN': 'VERB', 'NUMR': 'NUM', 'ADJF': 'ADJ', 'PRTF': 'PART', 'GRND': 'TRG'}.get(tag, tag)
    except Exception:
        return None

words_by_pos = defaultdict(set)
derivator.pos_all.append('part')
pos_all = derivator.pos_all
for dataset in (train_compounds, test_compounds):
    for lemma, pos in dataset.values:
        if pos is None:
            pos = get_pos_tag(lemma)
        try:
            pos = pos.strip().lower()
        except Exception:
            pos = None
        if pos is None:
            if any(lemma.endswith(s) for s in ('ый', 'ий', 'ой')):
                words_by_pos['adj'].add(lemma)
            elif any(lemma.endswith(s) for s in ('ть', 'ти', 'ться', 'тись')):
                words_by_pos['verb'].add(lemma)
            else:
                words_by_pos['noun'].add(lemma)
        else:
            words_by_pos[pos].add(lemma)
print('vocab by pos:', {k: len(v) for k, v in sorted(words_by_pos.items())})

def find_connections(word_b, pos_b, pos_a):
    out = []
    derived = derivator.derive(word_b, pos_b=pos_b, pos_a=pos_a, is_extended=True, use_rare=True)
    exist = set(derived) & words_by_pos[pos_a]
    out.extend([(word_b, pos_b, wa, pos_a, tuple(derived[wa])) for wa in exist])
    return out

def find_all_word_connections(word_b, pos_b):
    out = []
    for pos_a in pos_all:
        out.extend(find_connections(word_b, pos_b, pos_a))
    return out

print('== connections of морфема/noun ==')
for c in find_all_word_connections('морфема', 'noun'):
    print('  ', c)
