import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from verb_suffix_type_review import group_pending, rare_decisions, strong_signature


def record(a, b, types, rule='rule842'):
    return {'id': b + '|verb', 'word': b, 'rule': rule + '(test)',
            'parents': [{'id': a + '|verb', 'word': a, 'inflect_type': types}],
            'lexical_evidence': ['wiktionary_verb']}


class TypeReviewTests(unittest.TestCase):
    def test_type2_is_pairwise_and_reflexivity_is_preserved(self):
        for a, b in [('арендовать', 'арендовывать'), ('межевать', 'межёвывать'),
                     ('танцевать', 'танцовывать'), ('арендоваться', 'арендовываться')]:
            self.assertEqual(strong_signature(record(a, b, ['2']))[:2], ('accepted', 'type2_ovyva'))
        self.assertIsNone(strong_signature(record('арендовать', 'переворовывать', ['2'])))
        self.assertEqual(strong_signature(record('арендовать', 'арендовываться', ['2']))[0], 'rejected')

    def test_no_unrestricted_vowel_or_consonant_alternation(self):
        for a, b, types in [('крошиться', 'крашиваться', ['4']), ('пахнуть', 'пахивать', ['3']),
                            ('вывернуть', 'выверивать', ['3']), ('ослабеть', 'ослаблять', ['1']), ('обрить', 'обрывать', ['11']),
                            ('выкалить', 'выкалывать', ['4']), ('поубить', 'поубывать', ['11']),
                            ('свежеть', 'свежевать', ['1']), ('помалеть', 'помалевать', ['1']),
                            ('писяться', 'писываться', ['1']), ('догнать', 'догнивать', ['6'])]:
            self.assertIsNone(strong_signature(record(a, b, types)))
        self.assertEqual(strong_signature(record('подправить', 'подправивать', ['4']))[0], 'accepted')
        self.assertEqual(strong_signature(record('подогреть', 'подогревать', ['12греть']))[0], 'accepted')

    def test_closed_families_do_not_confuse_causatives_and_unrelated_roots(self):
        for a, b, types in [('доплести', 'доплетать', ['7т']), ('домолоть', 'домалывать', ['10ел']),
                            ('поднять', 'поднимать', ['14ним']), ('протолочь', 'протолакивать', ['8к'])]:
            self.assertEqual(strong_signature(record(a, b, types))[0], 'accepted')
        for a, b in [('провести', 'проведывать'), ('присесть', 'присаживать')]:
            self.assertEqual(strong_signature(record(a, b, ['7д']))[0], 'rejected')
        self.assertIsNone(strong_signature(record('подмяться', 'подмываться', ['14м', '1'])))

    def test_all_rare_decisions_are_explicit_and_override_automatic_signatures(self):
        decisions = rare_decisions()
        self.assertEqual(len(decisions), 289)
        self.assertTrue(all(r['reason'] and r['group_size_before'] <= 20 for r in decisions.values()))
        self.assertEqual(decisions[('rule842', 'взяться', 'взиматься')]['status'], 'accepted')
        self.assertIn('Даля', decisions[('rule842', 'взяться', 'взиматься')]['reason'])
        from review_verb_suffixes import classify
        policy = {'pending': [], 'rejected': [], '_rare_decisions': decisions}
        # The generic family has a plausible form; an explicit unresolved decision wins.
        result = classify(record('обдержаться', 'обдерживаться', ['1', '14м', '5']),
                          {'обдержаться': {'обдерживаться'}}, {'rule842': set()}, policy)
        self.assertEqual(result[0], 'pending')

    def test_grouping_is_stable_keeps_combinations_and_exports_complete_partition(self):
        with tempfile.TemporaryDirectory() as folder:
            output = Path(folder) / 'verbs.jsonl'
            pending = output.with_suffix('.semantic_pending.jsonl')
            rows = [record('первый', 'цельа', ['10ел']), record('второй', 'цельб', ['2']),
                    record('третий', 'цельв', ['14м', '1']), record('четвёртый', 'цельг', ['2'])]
            pending.write_text(''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in rows))
            summary = group_pending(output)
            first = pending.read_bytes()
            self.assertEqual(summary['total'], 4)
            self.assertEqual([g['inflect_type'] for g in summary['groups']], [['1', '14м'], ['2'], ['10ел']])
            self.assertEqual(sum(g['count'] for g in summary['groups']), 4)
            for group in summary['groups']:
                exported = Path(group['file']).read_text().splitlines()
                indexed = pending.read_text().splitlines()[group['start_line'] - 1:group['end_line']]
                self.assertEqual(exported, indexed)
            self.assertEqual(group_pending(output), summary)
            self.assertEqual(pending.read_bytes(), first)


if __name__ == '__main__':
    unittest.main()
