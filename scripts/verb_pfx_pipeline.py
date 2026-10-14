#!/usr/bin/env python
import os, sys, json, gzip, re, subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
REPO='/Users/a1234/.openclaw/workspace/DerivBaseRu'
os.chdir(REPO)
PY='.venv/bin/python'
OUTDIR='/tmp/pfx_gen'; os.makedirs(OUTDIR, exist_ok=True)
FINAL='data/derived/verb_pfx.jsonl'
DOUBT='/tmp/verb_pfx_doubt_dahl.jsonl'
STATS='/tmp/pfx_stats.json'
RULES=[
'rule854(без + verb -> verb)','rule855(в + verb -> verb)','rule855(вз + verb -> verb)','rule856(воз + verb -> verb)','rule857(вы + verb -> verb)','rule858(де + verb -> verb)','rule859(дис + verb -> verb)','rule860(до + verb -> verb)','rule861(за + verb -> verb)','rule862(из + verb -> verb)','rule863(на + verb -> verb)','rule864(над + verb -> verb)','rule865(недо + verb -> verb)','rule866(низ + verb -> verb)','rule867(о + verb -> verb)','rule868(об + verb -> verb)','rule869(от + verb -> verb)','rule870(пере + verb -> verb)','rule871(по + verb -> verb)','rule872(под + verb -> verb)','rule873(пре + verb -> verb)','rule874(пред + verb -> verb)','rule875(при + verb -> verb)','rule876(про + verb -> verb)','rule877(раз + verb -> verb)','rule878(ре + verb -> verb)','rule879(с + verb -> verb)','rule880(со2 + verb -> verb)','rule881(у + verb -> verb)','rule882(обез + verb -> verb)',
]
def norm(t):
    t=t.lower()
    for ch in ('\u0301','\u0300','\u00b4'): t=t.replace(ch,'')
    return t.replace('ё','е')
def load_sets():
    W=set()
    for line in gzip.open('data/wiktionary/parsed_ru.jsonl.gz','rt',encoding='utf-8'):
        r=json.loads(line); t=(r.get('title') or '').lower()
        for e in r.get('entries') or []:
            if e.get('pos')=='гл': W.add(t); break
    H=set(); T=set()
    for line in gzip.open('data/dahl/dahl.jsonl.gz','rt',encoding='utf-8'):
        r=json.loads(line); w=(r.get('word') or '').strip().lower()
        if w: H.add(norm(w))
        txt=r.get('text') or ''
        if txt: T.update(re.findall(r'[а-яё-]{2,}', norm(txt)))
    return W,H,T
def safe(r): return re.sub(r'[^A-Za-z0-9]+','_', r)[:60]
W,H,T=load_sets()
print('wiktionary-глаголов %d, далевских заголовков %d, токенов %d' % (len(W),len(H),len(T)), flush=True)
def gen(rule):
    out=os.path.join(OUTDIR, safe(rule)+'.jsonl')
    log=os.path.join(OUTDIR, safe(rule)+'.log')
    with open(log,'w') as lg:
        subprocess.run([PY,'scripts/run_pipeline.py','--pos-a','verb','--complexities','simple','--include-rules',rule,'--out',out], stdout=lg, stderr=subprocess.STDOUT)
    return rule,out
fl=open(FINAL,'w',encoding='utf-8'); dl=open(DOUBT,'w',encoding='utf-8')
stats={}
with ThreadPoolExecutor(max_workers=6) as ex:
    futs={ex.submit(gen,r):r for r in RULES}
    for f in as_completed(futs):
        rule,out=f.result(); k=w=d=0
        for line in open(out,encoding='utf-8'):
            line=line.strip()
            if not line: continue
            try: rec=json.loads(line)
            except: continue
            k+=1; word=rec['word']; nw=norm(word); by=[]
            if word.lower() in W: by.append('wiktionary')
            if nw in H or nw in T: by.append('dahl')
            if by:
                rec['verified_by']=by; fl.write(json.dumps(rec,ensure_ascii=False)+chr(10)); w+=1
                if by==['dahl']: d+=1; dl.write(json.dumps({'word':word,'parent':(rec.get('parents') or [{}])[0].get('word',''),'rule':rec.get('rule')}, ensure_ascii=False)+chr(10))
        stats[rule]={'gen':k,'kept':w,'dahl_only':d}
        print('DONE %-40s gen=%-7d kept=%-7d dahl_only=%d' % (rule[:40],k,w,d), flush=True)
fl.close(); dl.close()
json.dump(stats, open(STATS,'w',encoding='utf-8'), ensure_ascii=False, indent=1)
print('ALL DONE kept=%d' % sum(v['kept'] for v in stats.values()), flush=True)
