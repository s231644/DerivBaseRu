import pickle
from tqdm import tqdm
from typing import Optional, List
from multiprocessing import Pool

from src.Derivation import Derivation
from src.FinateStateMachine import FSM


class DerivedFSM:
    derivator = Derivation(use_guesser=True)

    def __init__(
            self,
            name: str,
            pos_b: str,
            pos_a: Optional[str] = None,
            rule_id: Optional[str] = None,
            wordlist: Optional[List[str]] = None
    ):
        self.name = name
        self.pos_b = pos_b
        self.pos_a = pos_a or pos_b
        self.rule_id = rule_id or name
        self.fsm = FSM({self.rule_id})

        wordlist = wordlist or []
        if rule_id:
            with Pool(30) as p:
                results = list(tqdm(p.imap(self.get_derived, wordlist), total=len(wordlist)))
                for result_, word in zip(results, wordlist):
                    for result in result_:
                        self.add_word(form=result, lemma=word, pos=self.pos_b)
        else:
            for word in tqdm(wordlist):
                self.add_word(form=word, lemma=word, pos=self.pos_b)

    def get_derived(self, word: str):
        derived = self.derivator.derive(
            word_b=word.lower(), pos_b=self.pos_b, rule_id=self.rule_id, use_rare=True
        )
        if derived:
            return derived[self.rule_id]
        return []

    def add_word(self, form: str, lemma: Optional[str] = None, pos: Optional[str] = None):
        self.fsm.add_word(list(form.lower()) + [self.rule_id, (lemma or form, pos or self.pos_b)])

    def analyze_word(self, word: str):
        return self.fsm.analyze_word(word.lower())

    def to_dict(self):
        return {
            "name": self.name,
            "pos_b": self.pos_b,
            "pos_a": self.pos_a,
            "rule_id": self.rule_id,
            "fsm": self.fsm.to_dict()
        }

    @classmethod
    def from_dict(cls, d):
        c = cls(name=d["name"], pos_b=d["pos_b"], pos_a=d["pos_a"], rule_id=d["rule_id"])
        c.fsm = FSM.from_dict(d["fsm"])
        return c

    def save(self):
        with open(self.name.replace('/', '_') + ".pickle", "wb") as f:
            pickle.dump(self.to_dict(), f)

    @classmethod
    def load(cls, f):
        d = pickle.load(open(f, "rb"))
        return cls.from_dict(d)


# f = DerivedFSM(
#     "rule211(verb + тель -> noun)", "verb", "noun",
#     rule_id="rule211(verb + тель -> noun)", wordlist=["учить", "читать"]
# )
# print(f.analyze_word("читатель"))
# print(f.analyze_word("учитель"))
# print(f.analyze_word("водитель"))
