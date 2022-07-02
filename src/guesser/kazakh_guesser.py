from typing import List, Dict


class BarakhninGuesser:
    hard_vowels = {"а", "о", "ұ", "ы"}
    soft_vowels = {"ә", "е", "ө", "ү", "i"}
    all_vowels = {
        "а", "ә", "е", "ё", "и", "о", "ө",
        "у", "ұ", "ү", "ы", "і", "э", "ю", "я"
    }

    def __init__(self, *args, **kwargs):
        self.pos_all = ['noun', 'adj', 'verb', 'adv']

    def guess_if_hard(self, stem: str) -> bool:
        for letter in stem[::-1]:
            if letter in self.hard_vowels:
                return True
            if letter in self.soft_vowels:
                return False
        return False

    def _find_possible_tags_non_verb(
            self, word: str
    ) -> List[Dict[str, str]]:
        if len(word) < 2:
            return []
        stem_end = word[-1]
        is_hard = self.guess_if_hard(word)
        if is_hard:
            if stem_end in self.all_vowels:
                return [{"stem_class": "1"}]
            if stem_end in {"б", "в", "ғ", "д"}:
                return [{"stem_class": "2"}]
            if stem_end in {"ж", "з"}:
                return [{"stem_class": "3"}]
            if stem_end in {"л"}:
                return [{"stem_class": "4"}]
            if stem_end in {"м", "н", "ң"}:
                return [{"stem_class": "5"}]
            if stem_end in {"р", "у", "й"}:
                return [{"stem_class": "6"}]
            if stem_end in {
                "к", "қ", "п", "с", "т", "ф",
                "х", "һ", "ц", "ч", "ш", "щ"
            }:
                return [{"stem_class": "7"}]
            return []
        else:
            if stem_end in self.all_vowels:
                return [{"stem_class": "8"}]
            if stem_end in {"б", "в", "г", "д"}:
                return [{"stem_class": "9"}]
            if stem_end in {"ж", "з"}:
                return [{"stem_class": "10"}]
            if stem_end in {"л"}:
                return [{"stem_class": "11"}]
            if stem_end in {"м", "н", "ң"}:
                return [{"stem_class": "12"}]
            if stem_end in {"р", "у", "й"}:
                return [{"stem_class": "13"}]
            if stem_end in {
                "к", "қ", "п", "с", "т", "ф",
                "х", "һ", "ц", "ч", "ш", "щ"
            }:
                return [{"stem_class": "14"}]
            return []

    def _find_possible_tags_verb(
            self, word: str
    ) -> List[Dict[str, str]]:
        if len(word) < 2:
            return []

        stem = word[:-1]
        stem_end = stem[-1]
        is_hard = self.guess_if_hard(stem)

        if word.endswith("ю"):
            if is_hard:
                return [{"stem_class": "15"}]
            else:
                return [{"stem_class": "16"}]

        if not word.endswith("у"):
            return []

        if stem_end == "у":
            return [{"stem_class": "17"}]

        if is_hard:
            if stem_end in self.all_vowels:
                return [{"stem_class": "1"}]
            if stem_end in {"б", "ғ"}:
                return [{"stem_class": "3"}]
            if stem_end in {"з"}:
                return [{"stem_class": "5"}]
            if stem_end in {"р", "л"}:
                return [{"stem_class": "7"}]
            if stem_end in {"м", "н", "ң"}:
                return [{"stem_class": "9"}]
            if stem_end in {"д", "ж"}:
                return [{"stem_class": "11"}]
            if stem_end in {
                "к", "қ", "п", "с", "т", "ф",
                "х", "һ", "ц", "ч", "ш", "щ"
            }:
                return [{"stem_class": "13"}]
            return []
        else:
            if stem_end in self.all_vowels:
                return [{"stem_class": "2"}]
            if stem_end in {"б", "г"}:
                return [{"stem_class": "4"}]
            if stem_end in {"з"}:
                return [{"stem_class": "6"}]
            if stem_end in {"р", "л"}:
                return [{"stem_class": "8"}]
            if stem_end in {"м", "н", "ң"}:
                return [{"stem_class": "10"}]
            if stem_end in {"д", "ж"}:
                return [{"stem_class": "12"}]
            if stem_end in {
                "к", "қ", "п", "с", "т", "ф",
                "х", "һ", "ц", "ч", "ш", "щ"
            }:
                return [{"stem_class": "14"}]
            return []

    def guess(
            self, word: str, pos: str = None, **kwargs
    ) -> List[Dict[str, str]]:
        possible_variants = list()
        pos = [pos] if pos is not None else self.pos_all
        for pos_ in pos:
            if pos_ == 'verb':
                possible_variants.extend(
                    self._find_possible_tags_verb(word)
                )
            else:
                possible_variants.extend(
                    self._find_possible_tags_non_verb(word)
                )
        return possible_variants
