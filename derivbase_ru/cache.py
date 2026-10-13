"""Content-addressed caching for derivation results.

A cached result is keyed by the identity of the source word plus a hash of the
rule CONTENT (not its name): a rule can be edited, so the name alone is not a
stable key. The fingerprint covers the rule subrules, their operators, the
operator arguments, tags and the rare-form tables.
"""
from __future__ import annotations

import hashlib
import json
import os
from typing import Any, Dict, Iterable, Optional


def _stable(value: Any) -> Any:
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, dict):
        return {str(k): _stable(v) for k, v in sorted(value.items(), key=lambda kv: str(kv[0]))}
    if isinstance(value, (set, frozenset)):
        return sorted((_stable(v) for v in value), key=str)
    if isinstance(value, (list, tuple)):
        return [_stable(v) for v in value]
    return _stable_object(value)


def _stable_object(obj: Any) -> Any:
    state = getattr(obj, "__dict__", None)
    if not isinstance(state, dict):
        return repr(obj)
    out = {}
    for key, value in state.items():
        if key in ("simple_rules", "before_merge_rules", "after_merge_rules", "tree"):
            continue
        out[key] = _stable(value)
    return out


def rule_fingerprint(rule: Any) -> str:
    """Short, stable content hash of a rule (changes when the rule changes)."""
    state = _stable_object(rule)
    state["_class"] = type(rule).__name__
    blob = json.dumps(state, ensure_ascii=False, sort_keys=True, default=str)
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()[:16]


class ResultCache:
    """Cache mapping (source word, rule content hash, flags) -> derived words."""

    def __init__(self, path: Optional[str] = None):
        self.path = path
        self._data: Dict[str, list] = {}
        self.hits = 0
        self.misses = 0
        if path and os.path.exists(path):
            with open(path, encoding="utf-8") as fh:
                self._data = json.load(fh)

    @staticmethod
    def make_key(word: str, pos_b: Any, pos_a: Any, fingerprint: str,
                 flags: Optional[Dict[str, Any]] = None) -> str:
        payload = [word, pos_b, pos_a, fingerprint, sorted((flags or {}).items(), key=str)]
        blob = json.dumps(payload, ensure_ascii=False, default=str)
        return hashlib.md5(blob.encode("utf-8")).hexdigest()

    def get(self, key: str):
        values = self._data.get(key)
        if values is None:
            self.misses += 1
            return None
        self.hits += 1
        return set(values)

    def set(self, key: str, values: Iterable[str]) -> None:
        self._data[key] = sorted(set(values))

    def save(self) -> None:
        if not self.path:
            return
        directory = os.path.dirname(os.path.abspath(self.path))
        if directory:
            os.makedirs(directory, exist_ok=True)
        with open(self.path, "w", encoding="utf-8") as fh:
            json.dump(self._data, fh, ensure_ascii=False, sort_keys=True)

    def __len__(self) -> int:
        return len(self._data)
