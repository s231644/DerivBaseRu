import gzip
import json
from pathlib import Path
import sys
import tempfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from build_verb_registry import export_registry, reflexive_variant
from verb_registry import DEFAULT_REGISTRY, ROOT, load_inflect_types


def test_canonical_registry_matches_current_types_and_preserves_variants():
    mapping = load_inflect_types()
    assert mapping == json.loads((ROOT / 'data/verb_inflect_types.json').read_text())
    with gzip.open(DEFAULT_REGISTRY, 'rt', encoding='utf-8') as stream:
        rows = [json.loads(line) for line in stream]
    assert len(rows) == len({r['word'] for r in rows}) == len(mapping)
    assert [r['word'] for r in rows] == sorted(mapping, key=lambda w: (w.replace('ё', 'е'), w))
    by_word = {r['word']: r for r in rows}
    assert by_word['спеть']['ambiguity'] == 'confirmed_variants'
    assert {v['per1_sg'] for v in by_word['спеть']['variants']} == {'спе́ю', 'спою́'}
    assert by_word['посыпаться']['inherited_from'] == 'посыпать'
    assert by_word['посыпаться']['ambiguity'] == 'confirmed_variants'
    assert by_word['докликаться']['review_status'] == 'pending_missing_base'
    assert by_word['докликаться']['needs_review']


def test_loader_supports_legacy_maps_and_rejects_invalid_registry():
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        legacy = root / 'types.json'
        legacy.write_text(json.dumps({'спеть': ['1', '12петь']}))
        assert load_inflect_types(legacy) == {'спеть': ['1', '12петь']}
        path = root / 'registry.jsonl'
        row = {'schema': 1, 'word': 'спеть', 'pos': 'verb', 'inflect_type': ['1', '12петь']}
        for records in [[row, row], [{**row, 'inflect_type': []}], [{**row, 'pos': 'noun'}]]:
            path.write_text(''.join(json.dumps(r)+'\n' for r in records))
            try:
                load_inflect_types(path)
            except ValueError:
                pass
            else:
                raise AssertionError('Invalid registry accepted')


def test_registry_export_is_reproducible_and_does_not_change_types():
    before = (ROOT / 'data/verb_inflect_types.json').read_bytes()
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        paths = [root / p for p in ['verbs.jsonl.gz', 'verbs.tsv', 'manifest.json']]
        first = export_registry(output=paths[0], table=paths[1], manifest=paths[2])
        content = [p.read_bytes() for p in paths]
        second = export_registry(output=paths[0], table=paths[1], manifest=paths[2])
        assert first == second
        assert content == [p.read_bytes() for p in paths]
        assert load_inflect_types(paths[0]) == load_inflect_types()
    assert before == (ROOT / 'data/verb_inflect_types.json').read_bytes()


def test_inherited_stress_and_meanings_are_marked_as_inherited():
    variant = {'infinitive': 'посы́пать', 'per1_sg': 'посы́плю', 'meaning': 'насыпать сверху'}
    result = reflexive_variant(variant, 'ся')
    assert result['infinitive'] == 'посы́паться'
    assert result['per1_sg'] == 'посы́плюсь'
    assert result['base_meaning'] == 'насыпать сверху'
    assert 'meaning' not in result
    assert variant['infinitive'] == 'посы́пать'
