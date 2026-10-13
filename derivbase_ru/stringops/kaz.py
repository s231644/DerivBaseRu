from typing import Set, Any

from derivbase_ru.stringops.base import (
    LanguageOps,
    LanguageAlphabet,
    StringOperation,
    ReplsfxOperation,
    DelsfxOperation,
)


class KazakhAlphabet(LanguageAlphabet):
    vowels = {
        "а", "ә", "е", "ё", "и", "о", "ө",
        "у", "ұ", "ү", "ы", "і", "э", "ю", "я"
    }


class RegrAssimOperation(ReplsfxOperation):
    @classmethod
    def apply(cls, word: str, args: Set[Any], mode: str = "do") -> Set[str]:
        return super().apply(word, ({('қ', 'ғ'), ('к', 'г'), ('п', 'б')}), mode=mode)


class Syl1pOperation(StringOperation):
    @classmethod
    def apply_do(cls, word: str, args: Set[Any]) -> Set[str]:
        for i, c in enumerate(word):
            if c in KazakhAlphabet.vowels:
                return {word[:i+1] + 'п-' + word}
        return set()


class KazakhOps(LanguageOps):
    alphabet = KazakhAlphabet()

    regrassim = RegrAssimOperation()
    syl1p = Syl1pOperation()
