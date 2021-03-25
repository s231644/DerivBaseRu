import json
from src.Derivation import Derivation

import pandas as pd
df = pd.read_csv('wiki_ADV.csv')

evaluator = Derivation()

advs_test = []
pos = 0
neg = 0

pos_examples = []
neg_examples = []

for i in range(df.shape[0]):
    s = df[i:i + 1].values[0]

    w_a = s[0].lower()
    w_b = s[1].lower()

    advs_test.append(w_a.replace('ё', 'е'))

    pos_a = 'adv'

    correct_generated = False

    results = evaluator.derive(word_b=w_b, pos_a=pos_a)
    for res in results:
        if w_a.replace('ё', 'е') == res[0].replace('ё', 'е'):
            correct_generated = True

    if correct_generated:
        pos += 1
        pos_examples.append(w_a)
    else:
        neg += 1
        neg_examples.append((w_b[::-1], w_a))

print(pos, neg)


def comp(a, b):
    return a[0] >= b[0]


neg_examples.sort()

for neg_ex in neg_examples:
    print(neg_ex[0][::-1] + ',' + neg_ex[1])

print(pos / (neg + pos))