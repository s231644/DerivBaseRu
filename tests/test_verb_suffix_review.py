import gzip
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from review_verb_suffixes import POLICY, RULES, classify, correspondences, review


def record(rule, parent, word, evidence=None):
    return {'id': word + '|verb', 'word': word, 'rule': rule + '(test)',
            'parents': [{'id': parent + '|verb', 'word': parent}],
            'lexical_evidence': ['wiktionary_verb'] if evidence is None else evidence,
            'verified': False, 'review_status': 'pending'}


class SuffixReviewTests(unittest.TestCase):
    def setUp(self):
        self.policy = json.loads(POLICY.read_text())
        self.explicit = {r['rule_id'].split('(')[0]: {tuple(p.split(';')) for p in r.get('rare', [])}
                         for r in json.loads(RULES.read_text())['data']}

    def test_manual_rejection_overrides_dictionary_and_regular_postfix_is_trusted(self):
        row = record('rule842', 'подавить', 'подавать')
        self.assertEqual(classify(row, {'подавать': {'подавить'}}, self.explicit, self.policy)[0], 'rejected')
        self.assertEqual(classify(record('rule930', 'чёкать', 'чёкаться'), {}, self.explicit, self.policy)[0], 'accepted')

    def test_missing_evidence_is_pending_and_explicit_pairs_include_archaisms(self):
        self.assertEqual(classify(record('rule842', 'дописать', 'дописывать'), {}, self.explicit, self.policy)[0], 'pending')
        self.assertEqual(classify(record('rule850', 'жалеть', 'жалить'), {}, self.explicit, self.policy)[0], 'accepted')
        self.assertEqual(classify(record('rule846', 'слечь', 'сложить'), {}, self.explicit, self.policy)[0], 'rejected')
        self.assertEqual(classify(record('rule846', 'отлечь', 'отложить'), {}, self.explicit, self.policy)[0], 'pending')
        self.assertEqual(classify(record('rule846', 'лечь', 'разрушить'), {}, self.explicit, self.policy)[0], 'pending')

    def test_dictionary_fields_and_repeatable_partition(self):
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory)
            dictionary = folder / 'dictionary.jsonl.gz'
            pages = [{'title': 'дописывать', 'entries': [
                {'lang': 'ru', 'pos': 'гл', 'inflection': {'params': {'соотв': '[[дописать|дописа́ть]]'}},
                 'related': {'глаголы': ['подавить']}}]}]
            with gzip.open(dictionary, 'wt', encoding='utf-8') as stream:
                stream.write(json.dumps(pages[0], ensure_ascii=False) + '\n')
            links = correspondences(dictionary)
            self.assertIn('дописать', links['дописывать'])
            self.assertNotIn('подавить', links['дописывать'])
            output = folder / 'verbs.jsonl'
            rows = [record('rule842', 'дописать', 'дописывать'),
                    record('rule842', 'подавить', 'подавать'),
                    record('rule842', 'писать', 'писывать'),
                    record('rule930', 'чёкать', 'чёкаться', ['dahl_token']),
                    record('rule836', 'абвгать', 'абвгнуть', []),
                    record('rule840', 'черкать', 'черкануть', ['dahl_token'])]
            with gzip.open(output.with_suffix('.raw.jsonl.gz'), 'wt', encoding='utf-8') as stream:
                for row in rows:
                    stream.write(json.dumps(row, ensure_ascii=False) + '\n')
            review(output, dictionary)
            first = output.read_bytes()
            review(output, dictionary)
            self.assertEqual(first, output.read_bytes())
            main = [json.loads(line) for line in output.read_text().splitlines()]
            self.assertEqual(len(main), 3)
            self.assertEqual(len(output.with_suffix('.semantic_pending.jsonl').read_text().splitlines()), 1)
            self.assertEqual(len(output.with_suffix('.semantic_rejected.jsonl').read_text().splitlines()), 1)
            doubtful = [json.loads(line) for line in output.with_suffix('.doubtful.jsonl').read_text().splitlines()]
            self.assertEqual([row['word'] for row in doubtful], ['черкануть'])


if __name__ == '__main__':
    unittest.main()
