from typing import Optional

from src.fsm_part import DerivedFSM


class CompoundAnalyzer:
    def __init__(
            self, name: str, pos: str, left: DerivedFSM, right: DerivedFSM
    ):
        self.name = name
        self.pos = pos
        self.left = left
        self.right = right

    def analyze(self, word: str, pos: Optional[str] = None):
        if pos != self.pos:
            return []
        left_res = self.left.analyze_word(word)
        final_res = []
        for st, left, left_rule in left_res:
            if st == len(word):
                continue
            if word[st] == '-':
                st += 1
            right_res = self.right.analyze_word(word[st:])
            for fi, right, right_rule in right_res:
                if st + fi == len(word):
                    final_res.append(
                        (word, self.pos, self.name, left, left_rule, right, right_rule)
                    )
        return final_res
