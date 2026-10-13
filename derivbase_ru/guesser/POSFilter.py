import pandas as pd

all_words = pd.read_csv('data/Zaliznyak_verb_table.csv')

verbs = []

for i in range(len(all_words)):
    if i % 1000 == 0:
        print(i // 1000)
    slice = all_words[i:i + 1]
    nans = pd.isna(slice)
    vals = slice.values[0]
    nans = nans.values[0]
    if not nans[4]:
        vals[3] = str(vals[3]) + vals[4][2:-2]
    if vals[1].isdecimal():
        verbs.append((vals[0], vals[1], str(vals[3])))

verb_df = pd.DataFrame(verbs, columns=['word', 'accent', 'infltype1'])

verb_df.to_csv('short_verbs.csv', index=False)
