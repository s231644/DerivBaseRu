"""Compound modifiers must not bridge families in the visualization."""
import json

from scripts.build_components import build


def test_compound_modifier_family_is_separate(tmp_path):
    records = [
        {'id': 'живописать|verb', 'kind': 'compound', 'parents': [
            {'id': 'живой|adj', 'role': 'modifier'},
            {'id': 'писать|verb', 'role': 'head'}]},
        {'id': 'вживую|adv', 'kind': 'complex', 'parents': [
            {'id': 'живой|adj', 'role': 'head'}]},
        {'id': 'написать|verb', 'kind': 'pfx', 'parents': [
            {'id': 'писать|verb', 'role': 'head'}]},
    ]
    source = tmp_path / 'relations.jsonl'
    original = '\n'.join(json.dumps(r, ensure_ascii=False) for r in records)
    source.write_text(original, encoding='utf-8')
    full = build(str(source))
    visible = build(str(source), exclude_compound_modifiers=True)
    assert full['n_components'] == 1
    assert visible['edges'] == 3
    assert visible['n_components'] == 2
    ids = visible['id2c']
    assert ids['живописать|verb'] == ids['писать|verb'] == ids['написать|verb']
    assert ids['живой|adj'] == ids['вживую|adv']
    assert ids['вживую|adv'] != ids['написать|verb']
    assert source.read_text(encoding='utf-8') == original
