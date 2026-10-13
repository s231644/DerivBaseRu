# Схема хранения производных форм (derivation schema)

## 1. Базовая запись (идея)

```json
{"word": "красненький", "pos": "adj", "rule": "rule619(adj + еньк(ий) -> adj)", "parents": [{"word": "красный", "pos": "adj"}]}
```

- `word` + `pos` — **узел** (лексема);
- `parents` — **входящие рёбра** (откуда образовано);
- `rule` — правило, которым получен узел;
- `rule: null, parents: []` — **непроизводная** основа (красный, жить, грести).

Это минимально достаточное ядро. Ниже — что стоит додумать, чтобы схема стала универсальной.

## 2. Расширения

### 2.1 Стабильный идентификатор
Омонимия требует ключа не по слову: `печь/сущ` vs `печь/глаг`, `стих/сущ` vs `стихнуть/глаг`.
`id = word + "|" + pos` (человекочитаемо и детерминированно).

### 2.2 Роль родителя (нужно для сложных слов)
```json
"parents": [
  {"word": "пыль", "pos": "noun", "role": "modifier", "slot": 0},
  {"word": "сосать", "pos": "verb", "role": "head", "slot": 1}
]
```
`role`: `head` | `modifier` | `prefix` | `stem` | `postfix`; `slot` — позиция в композите.

### 2.3 Тип деривации на ребре
`kind`: `sfx` | `pfx` | `pfx_sfx` (циркумфикс) | `postfix` (‑ся) | `interfix` | `conversion` (конверсия) | `compound` | `abbreviation` | `suppletion`.

### 2.4 Правило — ссылка, а не строка
Правила переиспользуются тысячами рёбер; лучше отдельная таблица, а в ребре — id:
```json
"rule": "rule619(adj + еньк(ий) -> adj)"
```
и таблица `rules`: `{id, lang, kind, affix, pos_from, pos_to, productivity, doc}`.

### 2.5 Флаги реальности
`flags`: `real` (засвидетельствовано), `rare` (пометка `*`), `reconstructed` (основа только под приставками, напр. `*ять`), `potential` (правило даёт, слова нет).

### 2.6 Грамматика
`inflect_type` (Зализняк: `8г`, `14йм`…), `gram` (`gender`, `aspect`, `animacy`).

### 2.7 Провенанс и язык
`lang` (`rus`|`kaz`|`deu`|`uzb`), `source` (`derivbase`|`wiktionary`|`dahl`), `confidence`.

### 2.8 Несколько путей к одному слову
Если слово выводимо двумя способами — не два узла, а список дериваций у узла:
```json
"derivations": [
  {"rule": "ruleA", "kind": "sfx", "parents": [{"word": "X", "pos": "noun"}]},
  {"rule": "ruleB", "kind": "pfx", "parents": [{"word": "Y", "pos": "verb"}]}
]
```

## 3. Итоговая запись (денормализованная, self-contained)
```json
{
  "schema": 1,
  "id": "красненький|adj",
  "word": "красненький",
  "pos": "adj",
  "lang": "rus",
  "rule": "rule619(adj + еньк(ий) -> adj)",
  "kind": "sfx",
  "parents": [{"id": "красный|adj", "word": "красный", "pos": "adj", "role": "head", "slot": 0}],
  "inflect_type": "1",
  "flags": {"real": true, "rare": false, "reconstructed": false},
  "source": "derivbase"
}
```
Для непроизводного слова: `rule: null, kind: null, parents: []`.

## 4. Нормализованный вариант (3 таблицы) — когда нужен join/агрегация
- `lexemes.jsonl`  — `{id, word, pos, lang, inflect_type, gram, flags, source}`
- `rules.jsonl`    — `{id, lang, kind, affix, pos_from, pos_to, productivity}`
- `derivations.jsonl` — `{derived: id, parents: [id], rule: id, kind, flags}`

## 5. Много родителей: сложные слова
```json
{"word": "пылесос", "pos": "noun", "rule": "ruleCompound(noun + verb -> noun)", "kind": "compound",
 "parents": [{"word": "пыль", "pos": "noun", "role": "modifier", "slot": 0},
             {"word": "сосать", "pos": "verb", "role": "head", "slot": 1}]}
```

## 6. Непроизводные и «звёздочные» основы
- Реальные: `красный` → `{rule: null, parents: []}`.
- Восстановленные (только под приставками): узел `ять` с `flags.reconstructed=true`, `rule: null`;
  слова `изъять`/`объять` ссылаются на него как на родителя.

## 7. Инварианты (валидация)
1. `id` уникален в пределах датасета;
2. каждый `parent.id` разрешается (или помечен как external);
3. граф ацикличен (DAG);
4. `pos` согласован с `rule.pos_to`, `parent.pos` — с `rule.pos_from`;
5. родители хранятся в детерминированном порядке (по `slot`, затем по id);
6. `rule != null` ⇔ `parents != []`.

## 8. Хранение и сериализация
- **JSONL** (одно ребро/узел на строку) + сжатие `.gz`; детерминированный порядок → diff-friendly;
- шапка/`meta.json`: `{schema, generated_at, sources: [{name, version, md5}], counts}`;
- альтернативы: TSV в стиле DeriNet (`derived \t parent \t relation`) и GraphML/DOT для визуализации.

## 9. JSON Schema (фрагмент)
```json
{"type": "object",
 "required": ["word", "pos", "parents"],
 "properties": {
   "word": {"type": "string"}, "pos": {"type": "string"},
   "rule": {"type": ["string", "null"]},
   "parents": {"type": "array", "items": {"type": "object",
      "required": ["word", "pos"],
      "properties": {"word": {"type": "string"}, "pos": {"type": "string"},
                      "role": {"enum": ["head", "modifier", "prefix", "stem", "postfix"]},
                      "slot": {"type": "integer"}}}}}
```

## 10. Откуда брать данные
- Движок DerivBase: `derive(word_b, pos_b, is_extended=True)` → `{word: [rule_id]}` → рёбра `(word_b → word) `;
- сложные — из compound-разбора (2+ родителя);
- реальность/частоты — из Викисловаря/Даля;
- «звёздочные» основы — консенсусная реконструкция (`verbs_roots.csv`).

## 11. Совместимость
- DeriNet/DerivBase: тройка `derived, parent, relation` выводится из ребра;
- обратная совместимость с текущим форматом: `{word: [rules]}` → набор узлов с `parents`.
