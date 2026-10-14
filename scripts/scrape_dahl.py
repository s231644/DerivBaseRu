import json, re, time, os, threading
from concurrent.futures import ThreadPoolExecutor
from curl_cffi import requests as req

OUT='data/dahl/dahl.jsonl'
os.makedirs('data/dahl', exist_ok=True)
if not os.path.exists('data/dahl/ids.json'):
    import shutil; shutil.copy('/tmp/dahl_ids.json', 'data/dahl/ids.json')
ids=json.load(open('data/dahl/ids.json'))

def parse(html):
    m=re.search(r'словарная статья,\s*([^"<]+)', html)
    word=m.group(1).strip() if m else ''
    h=re.sub(r'(?is)<script.*?</script>',' ',html)
    h=re.sub(r'(?is)<style.*?</style>',' ',h)
    t=re.sub(r'(?s)<[^>]+>',' ',h)
    for a,b in (('&nbsp;',' '),('&quot;','"'),('&amp;','&'),('&lt;','<'),('&gt;','>'),('&#39;',chr(39))):
        t=t.replace(a,b)
    t=re.sub(r'[ \t\r]+',' ',t)
    t=re.sub(r'\n\s*\n+',chr(10),t)
    t=t.split('Copyright(C)')[0]
    parts=t.rsplit('Толковый словарь Даля онлайн',1)
    return word, parts[-1].strip().lstrip('-—> ').strip()

done=set()
if os.path.exists(OUT):
    for line in open(OUT, encoding='utf-8'):
        try: done.add(json.loads(line)['wordid'])
        except Exception: pass
todo=[i for i in ids if i not in done]
print('todo', len(todo), 'done', len(done), flush=True)
lock=threading.Lock(); f=open(OUT,'a',encoding='utf-8'); cnt=[0]; okc=[0]
def work(i):
    for _ in range(3):
        try:
            r=req.get('https://slovardalja.net/word.php?wordid=%d'%i, impersonate='chrome', timeout=40)
            if r.status_code==200 and len(r.text)>300:
                w,t=parse(r.text)
                with lock:
                    f.write(json.dumps({'wordid':i,'word':w,'text':t}, ensure_ascii=False)+chr(10))
                    cnt[0]+=1; okc[0]+= (1 if t else 0)
                    if cnt[0]%500==0:
                        f.flush(); print('saved', cnt[0], 'nonempty', okc[0], flush=True)
            return
        except Exception:
            time.sleep(1.0)
    return
with ThreadPoolExecutor(max_workers=8) as ex:
    list(ex.map(work, todo))
f.flush(); f.close()
print('DONE saved', cnt[0], 'nonempty', okc[0], flush=True)
