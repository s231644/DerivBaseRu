"""Guard against typos in rule operators.

Every operator referenced in the rule JSON files must resolve to a method of the
corresponding language ops class. An unknown name silently disables the rule
(SubRule.apply swallows the AttributeError), so fail the build instead.
"""

import json
import re
from pathlib import Path

import derivbase_ru
from derivbase_ru.stringops.base import LanguageOps
from derivbase_ru.stringops.kaz import KazakhOps
from derivbase_ru.stringops.rus import RussianOps

RULES_DIR = Path(derivbase_ru.__file__).parent / "rules"
OPS_CLASSES = {"rus": RussianOps, "kaz": KazakhOps}
OPERATOR_RE = re.compile("[(][ ]*(?:(?:do|try|opt|only|exc)[ ]+)?([A-Za-z_][A-Za-z0-9_]*)")


def _iter_rule_texts():
    """Yield (lang, path, rule_string) for every rule string in the package."""
    for path in sorted(RULES_DIR.rglob("*.json")):
        lang = path.relative_to(RULES_DIR).parts[0]
        try:
            data = json.loads(path.read_text(encoding="utf-8"))["data"]
        except (KeyError, ValueError):
            continue
        for rule in data:
            texts = []
            if isinstance(rule.get("rules"), str):
                texts.append(rule["rules"])
            for case in (rule.get("cases") or []):
                if isinstance(case, dict) and isinstance(case.get("rules"), str):
                    texts.append(case["rules"])
            for text in texts:
                yield lang, path, text


def test_all_rule_operators_are_known():
    ops = {lang: cls() for lang, cls in OPS_CLASSES.items()}
    unknown = {}
    checked = 0
    for lang, path, text in _iter_rule_texts():
        cls_ops = ops.get(lang) or LanguageOps()
        for match in OPERATOR_RE.finditer(text):
            operator = match.group(1)
            checked += 1
            if not hasattr(cls_ops, operator):
                unknown.setdefault(operator, set()).add(path.name)
    assert checked > 1000, f"too few operators checked: {checked}"
    assert not unknown, f"unknown rule operators: {unknown}"
