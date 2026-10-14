#!/usr/bin/env python
"""Generic verb group pipeline: for each rule in a rules JSON file run generation,
immediately filter by Wiktionary (verb) + Dahl (headwords AND full text)."""
import os, sys, json, gzip, re, subprocess, argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
REPO='/Users/a1234/.openclaw/workspace/DerivBaseRu'
os.chdir(REPO)
PY='.venv/bin/python'
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
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--rules-file', required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--doubtful', required=True)
    ap.add_argument('--stats', required=True)
    ap.add_argument('--gen-dir', required=True)
    ap.add_argument('--workers', type=int, default=6)
    args=ap.parse_args()
    data=json.load(open(args.rules_file, encoding='utf-8'))['data']
    rules=[r['rule_id'] for r in data]
    os.makedirs(args.gen_dir, exist_ok=True)
    W,H,T=load_sets()
    print('правил %d | wiktionary-глаголов %d, далевских заголовков %d, токенов %d' % (len(rules),len(W),len(H),len(T)), flush=True)
    def gen(rule):
        out=os.path.join(args.gen_dir, safe(rule)+'.jsonl')
        log=os.path.join(args.gen_dir, safe(rule)+'.log')
        with open(log,'w') as lg:
            subprocess.run([PY,'scripts/run_pipeline.py','--pos-a','verb','--complexities','simple','--guesser','--include-rules',rule,'--out',out], stdout=lg, stderr=subprocess.STDOUT)
        return rule,out
    fl=open(args.out,'w',encoding='utf-8'); dl=open(args.doubtful,'w',encoding='utf-8')
    stats={}
    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        futs={ex.submit(gen,r):r for r in rules}
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
            print('DONE %-42s gen=%-7d kept=%-7d dahl_only=%d' % (rule[:42],k,w,d), flush=True)
    fl.close(); dl.close()
    json.dump(stats, open(args.stats,'w',encoding='utf-8'), ensure_ascii=False, indent=1)
    print('ALL DONE kept=%d' % sum(v['kept'] for v in stats.values()), flush=True)
if __name__=='__main__':
    main()
