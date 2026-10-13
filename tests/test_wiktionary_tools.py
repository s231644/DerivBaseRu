"""Tests for the Russian-word checker."""

from derivbase_ru.wiktionary_tools import (
    has_russian_section,
    in_russian_dictionary,
    is_russian_script,
    is_russian_word,
    russian_langs,
)


def test_script():
    assert is_russian_script("чеснок")
    assert is_russian_script("Чеснок")
    assert is_russian_script("по-русски")
    assert not is_russian_script("hello")
    assert not is_russian_script("чеснок2")
    assert not is_russian_script("")
    assert not is_russian_script("железная дорога")
    assert is_russian_script("железная дорога", allow_space=True)


def test_sections():
    assert has_russian_section({"entries": [{"lang": "ru"}]})
    assert not has_russian_section({"entries": [{"lang": "uk"}]})
    assert russian_langs({"entries": [{"lang": "uk"}, {"lang": "ru"}]}) == ["ru", "uk"]


def test_word():
    assert is_russian_word("чеснок", {"entries": [{"lang": "ru"}]})
    assert not is_russian_word("чеснок", {"entries": [{"lang": "uk"}]})
    assert not is_russian_word("hello")


def test_dictionary():
    assert in_russian_dictionary("чеснок")
    assert not in_russian_dictionary("фывапр")
