"""Compare indexed compound search with exhaustive engine generation."""
import json
from pathlib import Path
import subprocess
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from run_pipeline import Derivation, apply_compound_rule


def test_indexed_compounds_match_exhaustive_search(tmp_path):
    words = {
        'noun': ['вода', 'пар'],
        'adj': ['красный', 'синий'],
        'verb': ['носить', 'ходить', 'водоносить', 'пароходить',
                 'красноносить', 'синоходить', 'самоносить', 'полуходить'],
    }
    tags = {'noun': 'сущ', 'adj': 'прил', 'verb': 'гл'}
    dictionary, output = tmp_path / 'dict.jsonl', tmp_path / 'out.jsonl'
    dictionary.write_text(''.join(
        json.dumps({'title': word, 'entries': [{'pos': tags[pos]}]}) + '\n'
        for pos, bucket in words.items() for word in bucket))
    root = Path(__file__).resolve().parents[1]
    subprocess.run([sys.executable, str(root / 'scripts/rebuild_verb_compounds.py'),
                    '--dict', str(dictionary), '--out', str(output)],
                   cwd=root, check=True)
    records = [json.loads(line) for line in output.read_text().splitlines()]
    actual = {(r['word'], r['rule'], tuple(p['word'] for p in r['parents']))
              for r in records}
    expected = set()
    for rule in Derivation(lang='rus').loaded_rules['compound']:
        if rule.pos_a != 'verb':
            continue
        for head in words['verb']:
            for modifier in words[rule.poss_m[0]]:
                if head == modifier:
                    continue
                for word in apply_compound_rule(rule, head, modifier, True):
                    if word in words['verb']:
                        expected.add((word, rule.name, (head, modifier)))
    assert actual == expected
    assert len(actual) == len(records) == 4
    assert all(not r['verified'] and r['review_status'] == 'pending'
               for r in records)
