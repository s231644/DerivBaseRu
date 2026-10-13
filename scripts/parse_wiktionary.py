"""Parse Russian Wiktionary (ru.wiktionary) wikitext pages into JSON.

Per language section and homonym block extracts:
  wikidata lexeme, part of speech + inflection, morphology, pronunciation,
  senses, synonyms, antonyms, hypernyms, hyponyms, related words, etymology,
  phraseologisms.

CLI:
  python scripts/parse_wiktionary.py --file data/wiktionary/sample_article.xml
  python scripts/parse_wiktionary.py --dump data/wiktionary/ruwiktionary-latest-pages-articles.xml.bz2 --word чеснок
  python scripts/parse_wiktionary.py --dump ... --limit 200 --out out.jsonl
"""
from __future__ import annotations

import argparse
import bz2
import json
import re
import xml.etree.ElementTree as ET

HEADING_RE = re.compile(r"^(={1,6})\s*(.*?)\s*\1\s*$")
LINK_RE = re.compile(r"\[\[([^|\]]+)(?:\|([^\]]*))?\]\]")
TMPL_RE = re.compile(r"\{\{([^{}]*)\}\}")
LEXEME_RE = re.compile(r"\{\{\s*Лексема в Викиданных\s*\|\s*(L[0-9]+)")
LANG_RE = re.compile(r"\{\{-([a-zA-Z-]+)-\}\}")

POS_PREFIXES = ("сущ", "прил", "гл", "нар", "мест", "числ", "предл", "союз",
                "част", "межд", "предик", "вводн", "прич", "деепр", "предикатив")

SECTION_MORPH = ("Морфологические и синтаксические свойства",)
SECTION_PRON = ("Произношение",)
SECTION_SEM = ("Семантические свойства",)
SECTION_REL = ("Родственные слова",)
SECTION_ETYM = ("Этимология",)
SECTION_PHRASE = ("Фразеологизмы и устойчивые сочетания",)
SUBS = {"senses": ("Значение",), "synonyms": ("Синонимы",),
        "antonyms": ("Антонимы",), "hypernyms": ("Гиперонимы",),
        "hyponyms": ("Гипонимы",)}


def split_top_level(s, sep="|"):
    parts, depth, cur = [], 0, ""
    for ch in s:
        if ch in "{[(":
            depth += 1
        elif ch in "}])":
            depth -= 1
        if ch == sep and depth == 0:
            parts.append(cur)
            cur = ""
        else:
            cur += ch
    parts.append(cur)
    return parts


def find_templates(text):
    out, i, n = [], 0, len(text)
    while i < n - 1:
        if text[i:i + 2] == "{{":
            depth, j = 0, i
            while j < n - 1:
                two = text[j:j + 2]
                if two == "{{":
                    depth += 1; j += 2; continue
                if two == "}}":
                    depth -= 1; j += 2
                    if depth == 0:
                        break
                    continue
                j += 1
            parts = split_top_level(text[i + 2:j - 2])
            out.append((parts[0].strip(), parts[1:]))
            i = j
        else:
            i += 1
    return out


def template_args(args):
    positional, params = [], {}
    for a in args:
        head = a.split("{{")[0].split("[[")[0]
        if "=" in head:
            k, v = a.split("=", 1)
            params[k.strip()] = v.strip()
        else:
            positional.append(a.strip())
    return positional, params


def clean(s):
    s = LINK_RE.sub(lambda m: (m.group(2) or m.group(1)).strip(), s)
    def repl(m):
        parts = split_top_level(m.group(1))
        name = parts[0].strip()
        args = [a.strip() for a in parts[1:]]
        if name.startswith("этимология:"):
            return name.split(":", 1)[1]
        if name == "lang" and len(args) >= 2:
            return args[1]
        if name in ("выдел", "по-слогам", "aslinks", "з", "Cf", "?", "!", "-ru-"):
            return args[-1] if args else ""
        return ""
    prev = None
    while prev != s:
        prev = s
        s = TMPL_RE.sub(repl, s)
    s = s.replace("'''", "").replace("''", "")
    return re.sub(r"\s+", " ", s).strip()


def link_texts(raw):
    out = [ (m.group(2) or m.group(1)).strip() for m in LINK_RE.finditer(raw) ]
    for name, args in find_templates(raw):
        if name == "aslinks":
            for a in args:
                out.extend([clean(x) for x in a.split(",") if x.strip()])
    if not out:
        c = clean(raw)
        if c and c not in ("—", "-"):
            out.append(c)
    return [o for o in out if o]


def bullets(section):
    if section is None:
        return []
    out, buf, depth = [], None, 0
    for ln in section["content"]:
        t = ln.strip()
        if buf is not None and depth > 0:
            buf += " " + (t.lstrip("#").strip() if t.startswith("#") else t)
            depth += t.count("{{") - t.count("}}")
            continue
        if t.startswith("#"):
            if buf is not None:
                out.append(buf)
            buf = t.lstrip("#").strip()
            depth = buf.count("{{") - buf.count("}}")
        else:
            buf = None
    if buf is not None:
        out.append(buf)
    return out


def full_text(node):
    parts = list(node["content"])
    for ch in node["children"]:
        parts.append(ch["title"])
        parts.append(full_text(ch))
    return chr(10).join(parts)


def parse_sections(text):
    root = {"title": None, "level": 0, "content": [], "children": []}
    stack = [root]
    for line in text.splitlines():
        m = HEADING_RE.match(line)
        if m:
            level = len(m.group(1))
            node = {"title": m.group(2).strip(), "level": level, "content": [], "children": []}
            while len(stack) > 1 and stack[-1]["level"] >= level:
                stack.pop()
            stack[-1]["children"].append(node)
            stack.append(node)
        else:
            stack[-1]["content"].append(line)
    return root


def find_child(node, names):
    if node is None:
        return None
    for ch in node["children"]:
        if ch["title"] in names:
            return ch
    return None


def parse_entry(node):
    e = {"homonym": clean(node["title"])}
    block = full_text(node)
    m = LEXEME_RE.search(block)
    if m:
        e["wikidata_lexeme"] = m.group(1)
    morph = find_child(node, SECTION_MORPH)
    if morph:
        mt = full_text(morph)
        for name, args in find_templates(mt):
            first = name.split()[0] if name else ""
            if name.startswith("морфо"):
                pos, _ = template_args(args)
                e["morphology"] = [a for a in pos if a]
            elif first in POS_PREFIXES:
                pos, params = template_args(args)
                e["pos"] = first
                e["inflection"] = {"template": name, "positional": pos, "params": params}
    pron = find_child(node, SECTION_PRON)
    if pron:
        for name, args in find_templates(full_text(pron)):
            if name.startswith("transcription") or name.startswith("произнош"):
                pos, _ = template_args(args)
                audio = [a for a in pos if re.search(r"\.(ogg|oga|wav|mp3|flac)$", a)]
                e["pronunciation"] = {"transcriptions": [a for a in pos if a not in audio], "audio": audio}
    sem = find_child(node, SECTION_SEM)
    for key, names in SUBS.items():
        sec = find_child(sem, names)
        if key == "senses":
            vals = [v for v in (clean(b) for b in bullets(sec)) if v]
        else:
            vals = []
            for b in bullets(sec):
                vals.extend(link_texts(b))
            vals = [v for v in vals if v]
        if vals:
            e[key] = vals
    rel = find_child(node, SECTION_REL)
    if rel:
        for name, args in find_templates(full_text(rel)):
            if name.startswith("родств"):
                _, params = template_args(args)
                grouped = {}
                for k, v in params.items():
                    items = [x for x in (clean(part) for part in v.split(",")) if x]
                    if items:
                        grouped[k] = items
                if grouped:
                    e["related"] = grouped
    etym = find_child(node, SECTION_ETYM)
    if etym:
        t = clean(full_text(etym))
        if t:
            e["etymology"] = t
    phrase = find_child(node, SECTION_PHRASE)
    if phrase:
        items = []
        for name, args in find_templates(full_text(phrase)):
            if name.startswith("Фразеологизмы"):
                for a in args:
                    for part in split_top_level(a, "*"):
                        c = clean(part)
                        if c:
                            items.append(c)
        for b in bullets(phrase):
            c = clean(b)
            if c:
                items.append(c)
        if items:
            e["phraseologisms"] = items
    return e


def parse_page(title, text, page_id=None, revision_id=None, timestamp=None):
    root = parse_sections(text)
    entries = []
    for lang_node in root["children"]:
        lm = LANG_RE.search(lang_node["title"])
        lang = lm.group(1) if lm else clean(lang_node["title"])
        for blk in lang_node["children"]:
            if blk["level"] != 2:
                continue
            e = parse_entry(blk)
            e["lang"] = lang
            entries.append(e)
    return {"title": title, "page_id": page_id, "revision_id": revision_id,
            "timestamp": timestamp, "entries": entries}


def iter_dump(path, word=None, limit=None):
    op = bz2.open if path.endswith(".bz2") else open
    n = 0
    with op(path, "rb") as f:
        for _, el in ET.iterparse(f, events=("end",)):
            if not el.tag.endswith("page"):
                continue
            title = el.findtext("{*}title") or ""
            if word and title != word:
                el.clear(); continue
            ns = el.findtext("{*}ns") or ""
            rev = el.find("{*}revision")
            text = (rev.findtext("{*}text") if rev is not None else "") or ""
            if ns == "0" and text:
                yield parse_page(title, text,
                                 el.findtext("{*}id"),
                                 rev.findtext("{*}id") if rev is not None else None,
                                 rev.findtext("{*}timestamp") if rev is not None else None)
                n += 1
                if word or (limit and n >= limit):
                    el.clear(); return
            el.clear()


def main(argv=None):
    ap = argparse.ArgumentParser(description="Parse ru.wiktionary wikitext into JSON")
    ap.add_argument("--dump", help="dump path (.xml or .xml.bz2)")
    ap.add_argument("--file", help="single page XML file (e.g. sample_article.xml)")
    ap.add_argument("--word", help="extract only this title")
    ap.add_argument("--limit", type=int, help="max pages")
    ap.add_argument("--out", help="output file (json or jsonl)")
    ap.add_argument("--jsonl", action="store_true", help="emit JSONL")
    args = ap.parse_args(argv)
    objs = []
    if args.file:
        root = ET.parse(args.file).getroot()
        title = root.findtext("{*}title") or ""
        rev = root.find("{*}revision")
        text = (rev.findtext("{*}text") if rev is not None else "") or ""
        objs.append(parse_page(title, text, root.findtext("{*}id"),
                               rev.findtext("{*}id") if rev is not None else None,
                               rev.findtext("{*}timestamp") if rev is not None else None))
    elif args.dump:
        objs = list(iter_dump(args.dump, args.word, args.limit))
    else:
        ap.error("need --file or --dump")
    payload = json.dumps(objs[0] if (args.word and len(objs) == 1) else objs,
                         ensure_ascii=False, indent=2)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(payload)
        print("wrote", args.out, "objects", len(objs))
    else:
        print(payload)


if __name__ == "__main__":
    main()
