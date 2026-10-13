"""Tests for the derivation result cache (content-addressed by rule hash)."""

from derivbase_ru.cache import ResultCache, rule_fingerprint
from derivbase_ru.derivation import Derivation


def test_cache_serves_second_call():
    cache = ResultCache()
    d = Derivation(cache=cache)
    first = d.derive(word_b="сын", pos_b="noun", pos_a="noun", is_extended=False)
    assert first
    hits = cache.hits
    second = d.derive(word_b="сын", pos_b="noun", pos_a="noun", is_extended=False)
    assert second == first
    assert cache.hits > hits
    assert len(cache) > 0


def test_no_new_misses_on_repeat():
    cache = ResultCache()
    d = Derivation(cache=cache)
    a = d.derive(word_b="сын", pos_b="noun", pos_a="adj", is_extended=True)
    misses = cache.misses
    b = d.derive(word_b="сын", pos_b="noun", pos_a="adj", is_extended=True)
    assert b == a
    assert cache.misses == misses


def test_fingerprint_stable_and_content_sensitive():
    d = Derivation()
    rule = next(iter(d.rules_dict.values()))
    assert rule_fingerprint(rule) == rule_fingerprint(rule)
    before = rule_fingerprint(rule)
    rule.rare.append("__probe__")
    assert rule_fingerprint(rule) != before


def test_fingerprint_distinct_for_distinct_rules():
    d = Derivation()
    fingerprints = {rule_fingerprint(r) for r in d.rules_dict.values()}
    assert len(fingerprints) > 100
