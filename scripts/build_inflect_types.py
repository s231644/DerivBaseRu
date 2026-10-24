import sys, json, gzip, csv
sys.path.insert(0, '.')
from derivbase_ru.guesser.ZaliznyakGuesser import ZaliznyakGuesser
g = ZaliznyakGuesser(use_morph=True)
words = []
seen = set()
for line in gzip.open('data/wiktionary/parsed_ru.jsonl.gz','rt',encoding='utf-8'):
    d = json.loads(line); t = d.get('title') or ''
    if ' ' in t or t in seen: continue
    for e in d.get('entries') or []:
        if e.get('pos') == 'гл':
            seen.add(t); words.append(t); break
out = {}
for w in words:
    try:
        variants = g.guess(word=w, pos='verb')
    except Exception:
        variants = []
    types = sorted({x for v in variants for x in (v.get('inflect_type') or [])})
    if types: out[w] = types
csv_map = {}
with open('data/verbs_roots.csv', encoding='utf-8') as fh:
    for row in csv.DictReader(fh, delimiter='\t'):
        lm = (row.get('lemma') or '').strip()
        it = (row.get('inflect_type') or '').strip()
        if lm and it:
            csv_map[lm] = [x.strip() for x in it.split(',') if x.strip()]
before = len(out)
out.update(csv_map)
from refine_verb_inflect_types import refine_mapping
out, refinement = refine_mapping(out, "data/wiktionary/parsed_ru.jsonl.gz",
                                 "data/verbs_roots.csv", guesser=g)
print("refined assignments:", sum(r["changed"] for r in refinement))
print('csv types:', len(csv_map), '| overrode/added:', len(out) - before)
json.dump(out, open('data/verb_inflect_types.json','w',encoding='utf-8'), ensure_ascii=False)
print('verbs:', len(words), '| with types:', len(out))
