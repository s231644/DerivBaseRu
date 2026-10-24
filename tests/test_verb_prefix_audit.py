from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from audit_verb_prefixes import audit, normalize, prefix_family


def relation(source, target, prefix='по', evidence=('wiktionary_verb',)):
    return {'word': target, 'pos': 'verb', 'kind': 'pfx',
            'rule': f'r({prefix} + verb -> verb)', 'lexical_evidence': list(evidence),
            'parents': [{'word': source, 'pos': 'verb', 'role': 'head'}]}


def family(source, prefixes=('вы', 'за', 'по', 'пере', 'при'), **kwargs):
    return [relation(source, prefix + source, prefix, **kwargs) for prefix in prefixes]


def find(candidates, source, target):
    return next(c for c in candidates if c['source'] == source and c['target'] == target)


def test_sparse_source_and_productive_target_are_independent_signals():
    rows = [relation('тегать', 'стегать', 'с'), relation('лечь', 'влечь', 'в')]
    rows += family('стегать') + family('лечь') + family('влечь')
    candidates, _ = audit(rows)
    sparse = find(candidates, 'тегать', 'стегать')
    assert sparse['priority'] == 'high'
    assert sparse['source_other_prefixes'] == []
    productive = find(candidates, 'лечь', 'влечь')
    assert productive['priority'] == 'medium'
    assert productive['reasons'] == ['productive_target']


def test_duplicates_reflexives_yo_and_prefix_allomorphs_do_not_inflate_counts():
    rows = [relation('мётать', 'сметать', 'с'), relation('метаться', 'сметаться', 'со2')]
    candidates, summary = audit(rows * 10)
    assert summary['normalized_edges'] == 1
    assert len(candidates) == 1
    assert candidates[0]['source_profile']['count'] == 1
    assert len(candidates[0]['variants']) == 2
    assert normalize('мёта́ться') == 'метать'
    assert prefix_family('r(в + verb + ить -> verb)') is None


def test_token_only_productivity_does_not_create_high_priority():
    rows = [relation('тегать', 'стегать', 'с')]
    rows += family('стегать', evidence=('dahl_token',))
    candidate = find(audit(rows)[0], 'тегать', 'стегать')
    assert candidate['priority'] == 'low'
    assert candidate['target_profile']['count'] == 5
    assert candidate['target_profile']['strong_count'] == 0


def test_productive_source_and_unproductive_target_are_not_flagged():
    rows = family('писать') + [relation('писать', 'записать', 'за')]
    assert not any(c['source'] == 'писать' for c in audit(rows)[0])


def test_back_edges_self_loops_and_rejected_records_cannot_supply_support():
    rows = [relation('тегать', 'стегать', 'с'), relation('стегать', 'тегать', 'за'),
            relation('стегать', 'стегать', 'по')]
    rejected = relation('тегать', 'натегать', 'на')
    rejected['review_status'] = 'rejected'
    rows.append(rejected)
    candidate = find(audit(rows)[0], 'тегать', 'стегать')
    assert candidate['source_profile']['count'] == 1
    assert candidate['target_profile']['count'] == 0


def test_order_independence_and_source_records_are_not_mutated():
    import copy
    rows = family('стегать') + [relation('тегать', 'стегать', 'с')]
    original = copy.deepcopy(rows)
    assert audit(rows) == audit(reversed(rows))
    assert rows == original


def test_real_dataset_catches_requested_examples_but_does_not_reject_them():
    from audit_verb_prefixes import read_records
    path = Path(__file__).resolve().parents[1] / 'data/derived/verb_pfx.jsonl'
    candidates, _ = audit(read_records(path))
    assert find(candidates, 'тегать', 'стегать')['priority'] == 'high'
    assert find(candidates, 'лечь', 'влечь')['priority'] == 'medium'
    assert all(c['decision'] == 'review' for c in candidates)


def test_cli_is_reproducible_and_refuses_to_overwrite_input():
    import json
    import subprocess
    import tempfile
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        source, output, summary, report = [root / name for name in
                                           ('input.jsonl', 'output.jsonl', 'summary.json', 'report.tsv')]
        rows = family('стегать') + [relation('тегать', 'стегать', 'с')]
        source.write_text(''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in rows))
        before = source.read_bytes()
        script = Path(__file__).resolve().parents[1] / 'scripts/audit_verb_prefixes.py'
        command = [sys.executable, str(script), '--input', str(source), '--output', str(output),
                   '--summary', str(summary), '--report', str(report)]
        subprocess.run(command, check=True, capture_output=True)
        first = [p.read_bytes() for p in (output, summary, report)]
        subprocess.run(command, check=True, capture_output=True)
        assert first == [p.read_bytes() for p in (output, summary, report)]
        assert len(report.read_text().splitlines()) == 2
        assert source.read_bytes() == before
        command[command.index('--output') + 1] = str(source)
        assert subprocess.run(command, capture_output=True).returncode != 0
        assert source.read_bytes() == before
