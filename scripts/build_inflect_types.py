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
from audit_verb_type_roots import refine_by_roots
out, root_audit = refine_by_roots(out, "data/verbs_roots.csv")
print("root-family refinements:", sum(r["changed"] for r in root_audit))
from verb_type2_policy import apply_type2
out, type2_changes = apply_type2(out, words)
print("explicit type-2 assignments:", len(type2_changes))
from apply_verb_inflect_llm_review import apply_review
out, reviewed_nonreflexive = apply_review(out)
print("reviewed non-reflexive paradigms:", len(reviewed_nonreflexive))
from inherit_reflexive_verb_types import inherit_types
out, reflexive_inheritance = inherit_types(out)
print("reflexive type inheritance:", sum(r["status"] == "copied" for r in reflexive_inheritance))
print('csv types:', len(csv_map), '| overrode/added:', len(out) - before)
json.dump(out, open('data/verb_inflect_types.json','w',encoding='utf-8'), ensure_ascii=False)
print('verbs:', len(words), '| with types:', len(out))
