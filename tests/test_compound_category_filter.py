import hashlib
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from filter_verb_compounds import CONFIG, exclusion, filter_dataset, prefix_stats


def record(word, modifier, form, pos='noun'):
    return {'word': word, 'rule': 'rule961', 'parents': [
        {'role': 'head', 'word': word[len(form):], 'pos': 'verb'},
        {'role': 'modifier', 'word': modifier, 'form': form, 'pos': pos}]}


def test_categories_match_exact_modifier_form_and_pos():
    categories = json.loads(CONFIG.read_text())['categories']
    assert exclusion(record('проговорить', 'пря', 'про'), categories)
    assert exclusion(record('самоочищаться', 'самый', 'само', 'adj'), categories)
    assert not exclusion(record('прососать', 'просо', 'просо'), categories)
    assert not exclusion(record('прянуть', 'пря', 'пря'), categories)
    assert not exclusion(record('разномыслить', 'разный', 'разно', 'adj'), categories)
    assert not exclusion(record('руководить', 'рука', 'руко'), categories)


def test_prefix_counts_are_relations_and_filter_is_auditable(tmp_path):
    rows = [record('проговорить', 'пря', 'про'),
            record('прососать', 'просо', 'просо'),
            record('прососать', 'просо', 'просо', 'adj'),
            record('самоочищаться', 'самый', 'само', 'adj')]
    assert prefix_stats(rows)['про']['relations'] == 3
    assert prefix_stats(rows)['про']['unique_words'] == 2
    path = tmp_path / 'verb_compound.jsonl'
    path.write_text(''.join(json.dumps(r) + '\n' for r in rows))
    path.with_suffix('.manifest.json').write_text('{}')
    report = filter_dataset(path)
    kept = [json.loads(l) for l in path.read_text().splitlines()]
    removed = [json.loads(l) for l in path.with_suffix('.rejected.jsonl').read_text().splitlines()]
    assert report['before_relations'] == 4
    assert report['after_relations'] == report['removed_relations'] == 2
    assert kept == rows[1:3]
    assert [r['record'] for r in removed] == [rows[0], rows[3]]
    assert all(r['reason'] and r['category'] for r in removed)
    manifest = json.loads(path.with_suffix('.manifest.json').read_text())
    assert manifest['sha256'] == hashlib.sha256(path.read_bytes()).hexdigest()
    assert filter_dataset(path) == report
    assert len(path.with_suffix('.rejected.jsonl').read_text().splitlines()) == 2
