from typing import Set, Any

from src.stringops.base import (
    LanguageOps,
    LanguageAlphabet,
    StringOperation,
    ReplsfxOperation,
    DelsfxOperation,
)


class RussianAlphabet(LanguageAlphabet):
    paired = {'б', 'п', 'м', 'в', 'ф', 'д', 'т', 'з', 'с', 'н', 'л', 'р'}
    velar = {'г', 'к', 'х'}
    sh_hard = {'ш', 'ж'}
    sh_soft = {'щ', 'ч'}

    voiced = {'б', 'м', 'в', 'д', 'з', 'н', 'л', 'р', 'г', 'ж'}
    unvoiced = {'п', 'ф', 'т', 'с', 'к', 'х', 'ш', 'ч', 'щ', 'ц'}

    plt_pairs = {
        ('к', 'ч'),
        ('г', 'ж'),
        ('х', 'ш')
    }
    inv_plt_pairs = {
        ('ч', 'к'),
        ('ж', 'г'),
        ('ш', 'х')
    }

    plt5_pairs = {
        ('ц', 'ч')
    }
    inv_plt5_pairs = {
        ('ч', 'ц')
    }

    alt7_pairs = {
        ('е', 'о')
    }

    altcons_pairs = {
        ('б', 'бл'),
        ('п', 'пл'),
        ('в', 'вл'),
        ('ф', 'фл'),
        ('м', 'мл'),
        ('з', 'ж'),
        ('с', 'ш'),
        ('д', 'ж'),
        ('т', 'ч'),
        ('т', 'щ'),
        ('ст', 'щ'),
        ('к', 'ч'),
        ('г', 'ж'),
        ('х', 'ш'),
        ('ск', 'щ')
    }

    inv_altcons_pairs = {
        ('бл', 'б'),
        ('пл', 'п'),
        ('вл', 'в'),
        ('фл', 'ф'),
        ('мл', 'м'),
        ('ж', 'з'),
        ('ш', 'с'),
        ('ж', 'д'),
        ('ч', 'т'),
        ('щ', 'т'),
        ('щ', 'ст'),
        ('ч', 'к'),
        ('ж', 'г'),
        ('ш', 'х'),
        ('щ', 'ск')
    }

    vowels = {'а', 'о', 'у', 'ы', 'и', 'э', 'я', 'ё', 'ю', 'е'}
    double_vowels = {'я', 'ё', 'ю', 'е'}

    sh = sh_hard | sh_soft

    consonants = paired | velar | sh_hard | sh_soft

    morphobad = velar | sh_hard | sh_soft | {'ц'}

    all_letters = consonants | vowels | {'ъ', 'ь'}


class DelptfxOperation(DelsfxOperation):
    @classmethod
    def apply(cls, word: str, args: Set[Any], mode: str = "do") -> Set[str]:
        return super().apply(word, {"ся", "сь"}, mode=mode)


class AltconsOperation(ReplsfxOperation):
    @classmethod
    def apply(cls, word: str, args: Set[Any], mode: str = "do") -> Set[str]:
        return super().apply(word, RussianAlphabet.altcons_pairs, mode=mode)


class PltOperation(ReplsfxOperation):
    @classmethod
    def apply(cls, word: str, args: Set[Any], mode: str = "do") -> Set[str]:
        return super().apply(word, RussianAlphabet.plt_pairs, mode=mode)


class Plt5Operation(ReplsfxOperation):
    @classmethod
    def apply(cls, word: str, args: Set[Any], mode: str = "do") -> Set[str]:
        return super().apply(word, RussianAlphabet.plt5_pairs, mode=mode)


class InvPltOperation(ReplsfxOperation):
    @classmethod
    def apply(cls, word: str, args: Set[Any], mode: str = "do") -> Set[str]:
        return super().apply(word, RussianAlphabet.inv_plt_pairs, mode=mode)


class InvPlt5Operation(ReplsfxOperation):
    @classmethod
    def apply(cls, word: str, args: Set[Any], mode: str = "do") -> Set[str]:
        return super().apply(word, RussianAlphabet.inv_plt5_pairs, mode=mode)


class InvAltconsOperation(ReplsfxOperation):
    @classmethod
    def apply(cls, word: str, args: Set[Any], mode: str = "do") -> Set[str]:
        return super().apply(word, RussianAlphabet.inv_altcons_pairs, mode=mode)


class LSoftOperation(ReplsfxOperation):
    @classmethod
    def apply(cls, word: str, args: Set[Any], mode: str = "do") -> Set[str]:
        return super().apply(word, ({('л', 'ль')}), mode=mode)


class LHardOperation(ReplsfxOperation):
    @classmethod
    def apply(cls, word: str, args: Set[Any], mode: str = "do") -> Set[str]:
        return super().apply(word, ({('ль', 'л')}), mode=mode)


class Alt7Operation(StringOperation):
    @classmethod
    def apply_do(cls, word: str, args: Set[Any]) -> Set[str]:
        # вывести -> вывод
        for i in range(len(word) - 1, -1, -1):
            if word[i] == 'е':
                return {word[:i] + 'о' + word[i + 1:]}
        return set()


class InsPfxOperation(StringOperation):
    # only for prefixes like из, раз, без, ...
    @classmethod
    def apply_do(cls, word: str, args: Set[str]) -> Set[str]:
        possible_results = set()
        for pfx_a in args:
            if not pfx_a.endswith('з'):
                continue
            if word[0] in RussianAlphabet.unvoiced:
                possible_results.add(pfx_a[:-1] + 'с' + word)
            else:
                possible_results.add(pfx_a + word)
        return possible_results


class AltPfxOperation(StringOperation):
    @classmethod
    def apply_do(cls, word: str, args: Set[Any]) -> Set[str]:
        if word[0] == 'и':
            return {'ы' + word[1:]}
        if word[0] in RussianAlphabet.double_vowels:
            return {'ъ' + word}
        return {word}


class AltPfxIOperation(StringOperation):
    @classmethod
    def apply_do(cls, word: str, args: Set[Any]) -> Set[str]:
        if word[0] in RussianAlphabet.double_vowels:
            return {'ъ' + word}
        return {word}


class AltAOperation(StringOperation):
    # выкорм|ить -> выкарм|ливать
    @classmethod
    def apply_do(cls, word: str, args: Set[Any]) -> Set[str]:
        for i in range(len(word) - 1, -1, -1):
            if word[i] == 'о':
                return {word[:i] + 'а' + word[i + 1:]}


class SoftOperation(StringOperation):
    @classmethod
    def apply_do(cls, word: str, args: Set[Any]) -> Set[str]:
        return {word + 'ь'}


class HardOperation(StringOperation):
    @classmethod
    def apply_do(cls, word: str, args: Set[Any]) -> Set[str]:
        if word.endswith('ь'):
            return {word[:-1]}
        return set()


class DelNOperation(StringOperation):
    # разнообразн|ый -> разнообраз|ить
    @classmethod
    def apply_do(cls, word: str, args: Set[Any]) -> Set[str]:
        if len(word) < 3 or word[-1] != 'н' or word[-2] in RussianAlphabet.vowels:
            return set()
        word = word[:-1]
        if word.endswith('ь'):
            word = word[:-1]
        return {word}


class DelKOperation(StringOperation):
    # крепк|ий -> креп|ить
    @classmethod
    def apply_do(cls, word: str, args: Set[Any]) -> Set[str]:
        if len(word) < 3 or word[-1] != 'к' or word[-2] in RussianAlphabet.vowels:
            return set()
        word = word[:-1]
        if word.endswith('ь'):
            word = word[:-1]
        return {word}


class DelvowelOperation(StringOperation):
    @classmethod
    def apply_do(cls, word: str, args: Set[Any]) -> Set[str]:
        if len(word) < 3:
            return set()
        if (
                word[-1] in RussianAlphabet.consonants
                and word[-2] in {'о', 'е', 'ё'}
                and word[-3] in RussianAlphabet.consonants
        ):
            w_a = word[:-2]
            if w_a.endswith('л'):
                w_a += 'ь'
            return {w_a + word[-1]}
        return set()


class AddvowelOperation(StringOperation):
    @classmethod
    def apply_do(cls, word: str, args: Set[Any]) -> Set[str]:
        if len(word) < 3:
            return set()
        if word[-1] not in RussianAlphabet.consonants:
            return set()

        possible_results = set()
        w_a = word[:-1]
        if w_a[-1] == 'ь':
            w_a = w_a[:-1]
        if w_a[-1] == 'й':
            return {w_a[:-1] + 'е' + word[-1]}
        if w_a[-1] in RussianAlphabet.consonants:
            for add_vowel in {'о', 'е', 'ё'}:
                possible_results.add(w_a + add_vowel + word[-1])
        return possible_results


class Atleast3Operation(StringOperation):
    @classmethod
    def apply_do(cls, word: str, args: Set[Any]) -> Set[str]:
        if len(word) < 3:
            return set()
        return {word}


class RussianOps(LanguageOps):
    alphabet = RussianAlphabet()

    # check ops
    atleast3 = Atleast3Operation()

    # postfix ops
    delptfx = DelptfxOperation()

    # alternation ops
    altcons = AltconsOperation()
    plt = PltOperation()
    plt5 = Plt5Operation()
    inv_altcons = InvAltconsOperation()
    inv_plt = InvPltOperation()
    inv_plt5 = InvPlt5Operation()

    l_soft = LSoftOperation()
    l_hard = LHardOperation()
    alt7 = Alt7Operation()
    alt_a = AltAOperation()
    soft = SoftOperation()
    hard = HardOperation()
    del_n = DelNOperation()
    del_k = DelKOperation()
    delvowel = DelvowelOperation()
    addvowel = AddvowelOperation()

    ins_pfx = InsPfxOperation()
    alt_pfx = AltPfxOperation()
    alt_pfxi = AltPfxIOperation()
