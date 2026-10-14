"""Tests for the Wiktionary wikitext parser (scripts/parse_wiktionary.py)."""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "scripts"))

import parse_wiktionary as pw

ADV = """= {{-ru-}} =
{{Лексема в Викиданных|L1}}
=== Морфологические и синтаксические свойства ===
{{нар-ru|безальтернати́вно}}
=== Произношение ===
{{transcription-ru|безальтернати́вно}}
=== Семантические свойства ===
==== Значение ====
# исключая любую [[альтернатива|альтернативу]]
==== Синонимы ====
# [[альтернативно]]
"""

NOUN = """= {{-ru-}} =
=== Морфологические и синтаксические свойства ===
{{сущ ru m a 2a}}
"""


def test_pos_from_suffixed_template():
    entries = pw.parse_page("безальтернативно", ADV)["entries"]
    assert entries
    e = entries[0]
    assert e["pos"] == "нар"
    assert e["senses"]
    assert e["synonyms"] == ["альтернативно"]
    assert e["wikidata_lexeme"] == "L1"


def test_pos_from_plain_template():
    e = pw.parse_page("тест", NOUN)["entries"][0]
    assert e["pos"] == "сущ"


def test_pos_from_english_and_special_templates():
    assert pw.detect_pos("prep ru") == "предл"
    assert pw.detect_pos("adv ru") == "нар"
    assert pw.detect_pos("interj ru") == "межд"
    assert pw.detect_pos("Фам ru m 2b") == "сущ"
    assert pw.detect_pos("abbrev") == "аббр"
    assert pw.detect_pos("аббр.") == "аббр"
    assert pw.detect_pos("наречие") == "нар"


PREP = """= {{-ru-}} =
=== Морфологические и синтаксические свойства ===
{{prep ru|за|п=творительным}}
=== Произношение ===
{{transcription-ru|за}}
=== Семантические свойства ===
==== Значение ====
# [[позади]] чего-либо
"""


def test_prep_entry_gets_pos():
    e = pw.parse_page("за", PREP)["entries"][0]
    assert e["pos"] == "предл"
    assert e["inflection"]["template"] == "prep ru"


def test_detect_pos():
    assert pw.detect_pos("сущ-ru") == "сущ"
    assert pw.detect_pos("нар-ru") == "нар"
    assert pw.detect_pos("сущ ru m a 2a") == "сущ"
    assert pw.detect_pos("морфо-ru") is None
