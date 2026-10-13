"""Minimal smoke tests for the derivbase_ru package."""

import derivbase_ru
from derivbase_ru.derivation import Derivation, TagGuesserWrapper


def test_version():
    assert derivbase_ru.__version__


def test_rules_loaded():
    d = Derivation()
    assert set(d.loaded_rules) == {"simple", "complex", "compound"}
    assert len(d.rules_dict) > 500
    assert len(d.loaded_rules["simple"]) > 100


def test_derive_returns_words():
    d = Derivation()
    res = d.derive(word_b="сын", pos_b="noun", is_extended=False)
    assert isinstance(res, set)
    assert res
    assert all(isinstance(w, str) for w in res)


def test_derive_extended_mapping():
    d = Derivation()
    res = d.derive(word_b="желать", pos_b="verb", is_extended=True)
    assert isinstance(res, dict)
    assert res
    assert all(isinstance(v, list) for v in res.values())


def test_guesser():
    d = Derivation(guesser=TagGuesserWrapper(lang="rus"))
    tags = d.tag_guesser.guess(word="конь", pos="noun")
    assert isinstance(tags, list)
    assert tags
