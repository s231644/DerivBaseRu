"""Read the canonical verb registry, or a legacy flat inflection-type map."""
import gzip
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REGISTRY = ROOT / 'data/verbs_registry.jsonl.gz'


def load_inflect_types(path=DEFAULT_REGISTRY):
    path = Path(path)
    if path.suffix == '.json':
        mapping = json.loads(path.read_text(encoding='utf-8'))
        if not isinstance(mapping, dict):
            raise ValueError('Expected a legacy {word: [types]} mapping')
    else:
        mapping = {}
        opener = gzip.open if path.suffix == '.gz' else open
        with opener(path, 'rt', encoding='utf-8') as stream:
            for number, line in enumerate(stream, 1):
                if not line.strip():
                    continue
                row = json.loads(line)
                word = row.get('word')
                if (not isinstance(word, str) or row.get('schema') != 1
                        or row.get('pos') != 'verb' or word in mapping):
                    raise ValueError(f'{path}:{number}: invalid or duplicate registry record')
                mapping[word] = row.get('inflect_type')
    for word, types in mapping.items():
        if (not isinstance(word, str) or not word or not isinstance(types, list) or not types
                or any(not isinstance(t, str) or not t for t in types)
                or len(set(types)) != len(types)):
            raise ValueError(f'Invalid types for {word!r}')
    return mapping
