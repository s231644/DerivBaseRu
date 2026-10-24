import json
from pathlib import Path
import re
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from review_verb_suffixes import POLICY, classify
from verb_suffix_type_review import rare_decisions, type7_decisions


class Type7ReviewTests(unittest.TestCase):
    def setUp(self):
        self.decisions = type7_decisions()
        self.policy = {'pending': [], 'rejected': [], '_rare_decisions': rare_decisions(),
                       '_type7_decisions': self.decisions}

    def classify_pair(self, rule, a, b):
        record = {'rule': rule + '(test)', 'word': b, 'parents': [{'word': a}]}
        return classify(record, {}, {}, self.policy)

    def test_explicit_review_covers_all_374_target_pairs_including_mixed_types(self):
        self.assertEqual(len(self.decisions), 374)
        for decision in self.decisions.values():
            self.assertTrue(any((match := re.match(r'\d+', t)) and int(match[0]) >= 7 or t in {'дать', 'быть', 'есть', 'ехать', 'идти', 'клясть'}
                                for t in decision['inflect_type']))
            self.assertTrue(decision['reason'])
            result = self.classify_pair(decision['rule'], decision['parent'], decision['word'])
            self.assertEqual(result[:2], (decision['status'], 'explicit_type7plus_review'))

    def test_historical_meanings_override_old_pending_and_modern_homonyms(self):
        self.policy['pending'].append({'rule': 'rule846', 'parent': 'отлечь', 'word': 'отложить', 'reason': 'old pending'})
        for rule, a, b in [('rule846', 'отлечь', 'отложить'), ('rule842', 'обдержаться', 'обдерживаться'),
                           ('rule842', 'покопить', 'покапливать'), ('rule842', 'умолиться', 'умаливаться'),
                           ('rule842', 'скипеть', 'скипать')]:
            self.assertEqual(self.classify_pair(rule, a, b)[0], 'accepted')
        self.assertIn('source_url', self.decisions[('rule842', 'скипеть', 'скипать')])

    def test_birth_homonym_corrects_the_previous_rejection(self):
        self.policy.update(json.loads(POLICY.read_text()))
        result = self.classify_pair('rule842', 'отродить', 'отражать')
        self.assertEqual(result[0], 'accepted')
        self.assertIn('Даля', result[2])

    def test_false_roots_and_nonverb_are_rejected_while_missing_evidence_stays_pending(self):
        for a, b in [('кровить', 'кровать'), ('припить', 'приплывать'), ('свежить', 'сведывать'),
                     ('позабить', 'позабывать'), ('пряжить', 'прядывать')]:
            self.assertEqual(self.classify_pair('rule842', a, b)[0], 'rejected')
        self.assertEqual(self.classify_pair('rule842', 'нудеть', 'нуждать')[0], 'pending')
        # This simple type4 pair was not in the requested scope and must not be overridden.
        self.assertNotIn(('rule842', 'подправить', 'подправивать'), self.decisions)


if __name__ == '__main__':
    unittest.main()
