"""Conservative signatures and grouped exports for rule842 review.

Signatures compare BOTH words and preserve reflexivity and the whole prefix.
A shared target ending or source inflection type by itself is insufficient.
"""
from collections import Counter, defaultdict
import json
from pathlib import Path
import re

RARE_DECISIONS = Path(__file__).resolve().parents[1] / 'data/reviews/verb_sfx_rare_types.jsonl'


def normalize(word):
    return re.sub('[\u0301\u0300\u00b4]', '', word.lower()).replace('ё', 'е')


def bare(word):
    word = normalize(word)
    for postfix in ('ся', 'сь'):
        if word.endswith(postfix):
            return word[:-len(postfix)], True
    return word, False


def type_key(value):
    return tuple((0, int(part)) if part.isdigit() else (1, part)
                 for part in re.split(r'(\d+)', value) if part)


def types_of(record):
    return tuple(sorted(set(record['parents'][0].get('inflect_type') or []), key=type_key))


def rare_decisions():
    with RARE_DECISIONS.open(encoding='utf-8') as stream:
        return {(r['rule'], r['parent'], r['word']): r for r in map(json.loads, stream)}


# Closed root families: no free inverse consonant or o/a alternations.
FAMILIES = [
    ({'3', '5', '5щ', '6', '6щ'}, [('гнуть', 'гибать'), ('мкнуть', 'мыкать'),
                                      ('гнать', 'гонять'), ('брать', 'бирать'),
                                      ('рвать', 'рывать'), ('звать', 'зывать'), ('драть', 'дирать'),
                                      ('вергнуть', 'вергать')]),
    ({'7б'}, [('скрести', 'скребать'), ('скрести', 'скребывать'),
              ('грести', 'гребать'), ('грести', 'гребывать')]),
    ({'7д'}, [('прясть', 'прядать'), ('прясть', 'прядывать'),
              ('класть', 'кладать'), ('класть', 'кладывать'),
              ('красть', 'крадывать'), ('брести', 'бредать'),
              ('пасть', 'падывать'), ('блюсти', 'блюдать'), ('сесть', 'седать')]),
    ({'7с'}, [('трясти', 'трясать'), ('трясти', 'тряхивать'), ('пасти', 'пасать')]),
    ({'7з'}, [('грызть', 'грызать'), ('лезть', 'лезать'), ('лезти', 'лезать'),
              ('ползти', 'ползать'), ('ползть', 'ползать'),
              ('верзть', 'верзать'), ('верзти', 'верзать')]),
    ({'7т'}, [('мести', 'метать'), ('плести', 'плетать'),
              ('гнести', 'гнетать'), ('цвести', 'цветать')]),
    ({'8к'}, [('волочь', 'волокать'), ('волочь', 'волакивать'),
              ('толочь', 'толакивать'), ('влечь', 'влекать'),
              ('печь', 'пекать'), ('сечь', 'секать'), ('течь', 'текать'),
              ('оболочь', 'оболокать'), ('оболочь', 'оболакивать'), ('обречь', 'обрекать')]),
    ({'8г'}, [('жечь', 'жигать'), ('стречь', 'стригать')]),
    ({'9'}, [('тереть', 'тирать'), ('переть', 'пирать'), ('мереть', 'мирать')]),
    ({'10ел', '10ол', '10ор'}, [('молоть', 'малывать'), ('колоть', 'калывать'),
                               ('полоть', 'палывать'), ('пороть', 'парывать'), ('бороть', 'барывать')]),
    ({'14н', '14м', '14ним', '14ьм', '14ым', '14им', '14йм'},
     [('нять', 'нимать'), ('жать', 'жимать')]),
]


def replace_tail(a, b, source, target):
    return a.endswith(source) and b == a[:-len(source)] + target


def strong_signature(record):
    if not record['rule'].startswith('rule842('):
        return None
    a, ar = bare(record['parents'][0]['word'])
    b, br = bare(record['word'])
    types = set(types_of(record))
    if ar != br:
        return 'rejected', 'reflexivity_changed', 'Rule842 не должен менять возвратность; требуется то же наличие -ся/-сь.'
    if '7д' in types:
        if any(replace_tail(a, b, 'вести', target) for target in ('ведать', 'ведывать')):
            return 'rejected', 'unrelated_vedat', 'Вести и ведать/посещать — разные корни; ложная замена ст/д.'
        if not ar and replace_tail(a, b, 'сесть', 'саживать'):
            return 'rejected', 'causative_instead_of_imperfective', 'Непереходное сесть заменено переходным саживать: каузатив вместо rule842.'
    if '8к' in types and (a, b) in {('бечь', 'бекать'), ('мочь', 'макать'), ('мочь', 'мокать'), ('мочь', 'макивать')}:
        return 'rejected', 'unrelated_root', 'Бечь/бежать и бекать, мочь и макать/мокать — разные корни.'
    if '2' in types and a.endswith(('овать', 'евать')):
        stem = a[:-3] if a.endswith('ать') else ''
        if stem.endswith('цев'):
            stem = stem[:-3] + 'цов'
        if stem and b == stem + 'ывать':
            return 'accepted', 'type2_ovyva', 'Тип 2: основа -ов/-ев сохраняется, добавлено -ыва-; допускается цев/цов. Возвратность и вся предшествующая часть совпадают.'
    # Retain the entire consonantal stem; do not generalize this to -нуть
    # (пахнуть → пахивать and вывернуть → выверивать can be unrelated).
    # In type14, я/а belongs to the root: мять → мывать and жать →
    # живать are not unchanged-root operations. Mixed types do not disambiguate it.
    if (types & {'1', '4', '4щ', '4*', '5', '5щ', '6', '6щ', '11'}
            and not any(t.startswith('14') for t in types)
            and not a.endswith(('врать', 'рвать', 'звать', 'драть', 'жать', 'мять', 'брать', 'нять', 'дать', 'ждать',
                                'гнать', 'знать', 'спать', 'стлать', 'прать', 'лгать'))):
        # -ить → -ывать is deliberately excluded: обрить → обрывать,
        # выкалить → выкалывать, поубить → поубывать are false matches.
        for ending, suffixes in [('ать', ('ивать', 'ывать')), ('ить', ('ивать',))]:
            if a.endswith(ending) and any(b == a[:-len(ending)] + suffix for suffix in suffixes):
                return 'accepted', 'unchanged_stem_iva', 'Перед -ива-/-ыва- целиком сохранена основа исходного -ать/-ить (для -ить допускается только -ивать); нет изменения приставки, корневых согласных и гласных или возвратности.'
    va_types = {'11', '12у', '12ы', '12и', '12греть', '12брить', '12петь', '15', '16', 'быть', 'дать'}
    # Type1 -еть → -евать is ambiguous (свежеть → свежевать,
    # помалеть → помалевать); only the dedicated va classes qualify.
    if types & va_types and a.endswith('ть') and b == a[:-2] + 'вать':
        return 'accepted', 'unchanged_stem_va', 'Для соответствующего типа перед -ть вставлено -ва-; остальная основа и возвратность полностью сохранены.'
    for allowed_types, pairs in FAMILIES:
        if not types & allowed_types:
            continue
        for source, target in pairs:
            if replace_tail(a, b, source, target):
                return 'accepted', 'closed_root_family', f'Проверенная узкая семья {source} → {target}; приставочная часть и возвратность совпадают.'
    return None


def pending_features(record):
    a, ar = bare(record['parents'][0]['word'])
    b, br = bare(record['word'])
    result = ['needs_root_and_sense_check']
    if len(types_of(record)) > 1:
        result.append('multiple_source_types')
    if record.get('lexical_evidence') == ['dahl_token']:
        result.append('dahl_token_only')
    if ar != br:
        result.append('reflexivity_changed')
    if not b.endswith(('ивать', 'ывать', 'вать')):
        result.append('short_a_ya_requires_semantics')
    return result


def group_pending(output):
    """Rewrite pending contiguously by parent type and export an index/subfiles."""
    pending = Path(output).with_suffix('.semantic_pending.jsonl')
    groups = defaultdict(list)
    for line in pending.read_text(encoding='utf-8').splitlines():
        record = json.loads(line)
        record['type_review_features'] = pending_features(record)
        groups[types_of(record)].append(record)
    directory = Path(output).with_suffix('.semantic_pending.by_inflect_type')
    directory.mkdir(exist_ok=True)
    for old in directory.glob('group-*.jsonl'):
        old.unlink()
    index, merged = [], []
    start = 1
    for number, (types, records) in enumerate(sorted(groups.items(), key=lambda item: tuple(type_key(t) for t in item[0])), 1):
        records.sort(key=lambda r: (r['parents'][0]['word'], r['word'], r['rule']))
        text = ''.join(json.dumps(record, ensure_ascii=False) + '\n' for record in records)
        file = directory / f'group-{number:03d}.jsonl'
        file.write_text(text, encoding='utf-8')
        index.append({'inflect_type': list(types), 'count': len(records),
                      'start_line': start, 'end_line': start + len(records) - 1,
                      'file': str(file), 'features': dict(Counter(f for r in records for f in r['type_review_features']))})
        merged.append(text)
        start += len(records)
    temporary = pending.with_name(pending.name + '.tmp')
    temporary.write_text(''.join(merged), encoding='utf-8')
    temporary.replace(pending)
    summary = {'grouping': 'parents[0].inflect_type; combinations retained without row duplication',
               'total': start - 1, 'groups': index}
    pending.with_suffix('.groups.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return summary
