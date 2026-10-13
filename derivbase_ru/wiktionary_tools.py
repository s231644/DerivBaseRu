"""Decide whether a title from parsed.jsonl is a word of the Russian language.

Two independent signals are used:
  * orthography - the title is spelled with Russian letters (plus allowed separators);
  * page data    - the parsed record has a Russian (`ru`) language section;
  * optionally   - pymorphy3 knows the lemma (a large Russian lexicon).

Example:
    from derivbase_ru.wiktionary_tools import is_russian_word
    import json
    for line in open("parsed.jsonl", encoding="utf-8"):
        rec = json.loads(line)
        if is_russian_word(rec["title"], rec):
            ...
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

STRESS_SIGNS = "́´"
RU_LETTERS = frozenset("абвгдеёжзийклмнопрстуфхцчшщъыьэюя")
HYPHENS = ("-", "‐", "‑")


def normalize(title: str) -> str:
    """Lowercase the title and drop stress marks."""
    out = title.strip().lower()
    for sign in STRESS_SIGNS:
        out = out.replace(sign, "")
    return out


def is_russian_script(title: str, allow_hyphen: bool = True, allow_space: bool = False) -> bool:
    """True if the title is spelled with Russian letters (and allowed separators)."""
    text = normalize(title)
    if not text:
        return False
    allowed = set(RU_LETTERS)
    if allow_hyphen:
        allowed.update(HYPHENS)
    if allow_space:
        allowed.add(" ")
    if any(ch not in allowed for ch in text):
        return False
    return any(ch in RU_LETTERS for ch in text)


def russian_langs(record: Dict[str, Any]) -> List[str]:
    """Language codes present in the parsed record (e.g. ["ru", "uk"])."""
    return sorted({e.get("lang") for e in (record.get("entries") or []) if e.get("lang")})


def has_russian_section(record: Dict[str, Any]) -> bool:
    """True if the parsed page has a Russian (ru) language section."""
    return "ru" in russian_langs(record)


_MORPH = None


def _morph():
    global _MORPH
    if _MORPH is None:
        import pymorphy3
        _MORPH = pymorphy3.MorphAnalyzer()
    return _MORPH


def in_russian_dictionary(word: str) -> bool:
    """True if pymorphy3 knows the word (its dictionary covers Russian lemmas)."""
    try:
        return bool(_morph().word_is_known(normalize(word)))
    except Exception:
        return False


def is_russian_word(title: str,
                    record: Optional[Dict[str, Any]] = None,
                    *,
                    dictionary: bool = False,
                    allow_hyphen: bool = True,
                    allow_space: bool = False) -> bool:
    """True if the title is a Russian word.

    record     - if given, the page must also have a Russian (ru) language section;
    dictionary - if True, additionally require pymorphy3 to know the lemma.
    """
    if not is_russian_script(title, allow_hyphen=allow_hyphen, allow_space=allow_space):
        return False
    if record is not None and not has_russian_section(record):
        return False
    if dictionary and not in_russian_dictionary(title):
        return False
    return True
