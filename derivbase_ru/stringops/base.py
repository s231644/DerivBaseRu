import re
from typing import Set, Tuple, Any

from abc import ABC, abstractmethod


class StringOperation(ABC):
    @classmethod
    def __call__(cls, *args, **kwargs) -> Set[str]:
        return cls.apply(*args, **kwargs)

    @classmethod
    def apply(cls, word: str, args: Set[Any], mode: str = "do") -> Set[str]:
        if mode == "do":
            return cls.apply_do(word, args)
        if mode == "try":
            return cls.apply_try(word, args)
        if mode == "opt":
            return cls.apply_opt(word, args)
        raise ValueError(f"Incorrect mode {mode}!")

    @classmethod
    @abstractmethod
    def apply_do(cls, word: str, args: Set[Any]) -> Set[str]:
        raise NotImplementedError

    @classmethod
    def apply_try(cls, word: str, args: Set[Any]) -> Set[str]:
        res = cls.apply_do(word, args)
        if res:
            return res
        return {word}

    @classmethod
    def apply_opt(cls, word: str, args: Set[Any]) -> Set[str]:
        return cls.apply_try(word, args) | {word}


class NochangeOperation(StringOperation):
    @classmethod
    def apply_do(cls, word: str, args: Set[Any]) -> Set[str]:
        return {word}


class CapitalizeOperation(StringOperation):
    @classmethod
    def apply_do(cls, word: str, args: Set[Any]) -> Set[str]:
        return {word.capitalize()}


class UppercaseOperation(StringOperation):
    @classmethod
    def apply_do(cls, word: str, args: Set[Any]) -> Set[str]:
        return {word.upper()}


class LowercaseOperation(StringOperation):
    @classmethod
    def apply_do(cls, word: str, args: Set[Any]) -> Set[str]:
        return {word.lower()}


class OnlysfxOperation(StringOperation):
    @classmethod
    def apply_do(cls, word: str, args: Set[str]) -> Set[str]:
        possible_results = set()
        for sfx_b in args:
            if word.endswith(sfx_b):
                possible_results.add(word)
        return possible_results

    @classmethod
    def apply_try(cls, word: str, args: Set[str]) -> Set[str]:
        return {word}


class ExcsfxOperation(StringOperation):
    @classmethod
    def apply_do(cls, word: str, args: Set[str]) -> Set[str]:
        c = 0
        for sfx_b in args:
            if not word.endswith(sfx_b):
                c += 1
        if c == len(args):
            return {word}
        return set()

    @classmethod
    def apply_try(cls, word: str, args: Set[str]) -> Set[str]:
        return {word}


class AddsfxOperation(StringOperation):
    @classmethod
    def apply_do(cls, word: str, args: Set[str]) -> Set[str]:
        possible_results = set()
        for sfx_a in args:
            possible_results.add(word + sfx_a)
        return possible_results


class DelsfxOperation(StringOperation):
    @classmethod
    def apply_do(cls, word: str, args: Set[str]) -> Set[str]:
        possible_results = set()
        for sfx_b in args:
            if word.endswith(sfx_b):
                possible_results.add(word[:-len(sfx_b)])
        return possible_results


class ReplsfxOperation(StringOperation):
    @classmethod
    def apply_do(cls, word: str, args: Set[Tuple[str, str]]) -> Set[str]:
        possible_results = set()
        for sfx_b, sfx_a in args:
            if word.endswith(sfx_b):
                possible_results.add(word[:-len(sfx_b)] + sfx_a)
        return possible_results


class OnlypfxOperation(StringOperation):
    @classmethod
    def apply_do(cls, word: str, args: Set[str]) -> Set[str]:
        possible_results = set()
        for pfx_b in args:
            if word.startswith(pfx_b):
                possible_results.add(word)
        return possible_results

    @classmethod
    def apply_try(cls, word: str, args: Set[str]) -> Set[str]:
        return {word}


class ExcpfxOperation(StringOperation):
    @classmethod
    def apply_do(cls, word: str, args: Set[str]) -> Set[str]:
        c = 0
        for pfx_b in args:
            if not word.startswith(pfx_b):
                c += 1
        if c == len(args):
            return {word}
        return set()

    @classmethod
    def apply_try(cls, word: str, args: Set[str]) -> Set[str]:
        return {word}


class AddpfxOperation(StringOperation):
    @classmethod
    def apply_do(cls, word: str, args: Set[str]) -> Set[str]:
        possible_results = set()
        for pfx_a in args:
            possible_results.add(pfx_a + word)
        return possible_results


class DelpfxOperation(StringOperation):
    @classmethod
    def apply_do(cls, word: str, args: Set[str]) -> Set[str]:
        possible_results = set()
        for pfx_b in args:
            if word.startswith(pfx_b):
                possible_results.add(word[len(pfx_b):])
        return possible_results


class ReplpfxOperation(StringOperation):
    @classmethod
    def apply_do(cls, word: str, args: Set[Tuple[str, str]]) -> Set[str]:
        possible_results = set()
        for pfx_b, pfx_a in args:
            if word.startswith(pfx_b):
                possible_results.add(pfx_a + word[len(pfx_b):])
        return possible_results


class LanguageAlphabet:
    # TODO: design

    __wordpunkt_pattern = re.compile(r"\w+|[^\w\s]+")

    @classmethod
    def eval_args(cls, expr: str) -> Set[Any]:
        attrs = dir(cls)
        tokens = re.findall(cls.__wordpunkt_pattern, expr)
        new_tokens = [
            x if x not in attrs else str(getattr(cls, x))
            for x in tokens
        ]
        new_expr = "".join(new_tokens)
        # cannot use ast.literal_eval because it might contain set operations
        return eval(new_expr)


class LanguageOps(ABC):
    alphabet = LanguageAlphabet()

    def eval_args(self, expr: str) -> Set[Any]:
        return self.alphabet.eval_args(expr)

    # trivial ops
    nochange = NochangeOperation()

    # case ops
    capitalize = CapitalizeOperation()
    uppercase = UppercaseOperation()
    lowercase = LowercaseOperation()

    # suffix condition ops
    onlysfx = OnlysfxOperation()
    excsfx = ExcsfxOperation()

    # suffix ops
    addsfx = AddsfxOperation()
    delsfx = DelsfxOperation()
    replsfx = ReplsfxOperation()

    # prefix condition ops
    onlypfx = OnlypfxOperation()
    excpfx = ExcpfxOperation()

    # prefix ops
    addpfx = AddpfxOperation()
    delpfx = DelpfxOperation()
    replpfx = ReplpfxOperation()
