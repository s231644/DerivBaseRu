from pathlib import Path
import gzip
import json
import sys
import tempfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from refine_verb_inflect_types import prefixed_root, refine_mapping, TYPE11_ROOTS


def test_type11_requires_a_real_root_and_prefix_sequence():
    for word in ['лить', 'вить', 'бить', 'пить', 'шить', 'недоперелить', 'развиться']:
        assert prefixed_root(word, TYPE11_ROOTS), word
    for word in ['апрувить', 'амшить', 'батлить', 'валить']:
        assert not prefixed_root(word, TYPE11_ROOTS), word


def test_known_forms_templates_and_unresolved_predictions():
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        dictionary, overrides = root / 'dictionary.gz', root / 'roots.tsv'
        with gzip.open(dictionary, 'wt', encoding='utf-8') as stream:
            for word in ['упережать', 'убредать', 'юродеть']:
                stream.write(json.dumps({'title': word, 'entries': [
                    {'pos': 'гл', 'inflection': {'template': 'гл ru 1a'}}]}) + '\n')
        overrides.write_text('lemma\tinflect_type\nтест\t1\n', encoding='utf-8')
        mapping = {'упережать': ['14м', '14н', '5'], 'убредать': ['1', 'дать'],
                   'юродеть': ['1', '15'], 'амшить': ['11', '4'],
                   'лить': ['11', '4'], 'полить': ['11', '4'],
                   'солить': ['11', '4'], 'оборжать': ['14м', '14н', '5', '6'],
                   'тест': ['1', '2']}
        old = json.loads(json.dumps(mapping))
        output, audit = refine_mapping(mapping, dictionary, overrides)
        for word in ['упережать', 'убредать', 'юродеть']:
            assert output[word] == ['1']
        assert output['амшить'] == ['4']
        assert output['лить'] == output['полить'] == ['11']
        assert output['солить'] == ['4']
        assert output['оборжать'] == sorted(mapping['оборжать'])
        assert output['тест'] == ['1', '2']
        assert mapping == old
        again, _ = refine_mapping(output, dictionary, overrides)
        assert again == output
        assert all(r['evidence'] for r in audit if r['changed'])
