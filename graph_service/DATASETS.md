# Данные для графового сервиса (DerivBaseRu graph viewer)

Сервис `graph_service/server.js` читает **только готовые файлы отношений деривации**
из каталога `--data` (по умолчанию `data/derived`) и строит по ним граф.
Промежуточные стадии конвейера сервису **не нужны** — их в каталог класть не следует.

## Что кладём в `--data` (финальные файлы)

| файл | группа | что внутри |
|---|---|---|
| `num.jsonl.gz` | числительные | готовые рёбра (compound/суффикс) |
| `adv.rare.verified.jsonl` | наречия | редкие, подтверждённые |
| `adv_pfx.final.clean.jsonl` | наречия | префиксальные, финал |
| `adv_sfx.clean.jsonl` | наречия | суффиксальные, финал |
| `adv_g1.final.clean.jsonl` | наречия | группа 1, финал |
| `adv_g2.final.clean.jsonl` | наречия | группа 2, финал |
| `adv_g5.clean.jsonl` | наречия | группа 5 (compound), финал |
| `adv_ymx.clean.jsonl` | наречия | исключения, финал |
| `verb_pfx.jsonl` | глаголы | **prefix + verb → verb**, очищено по Вики/Далю |
| `verb_compound.jsonl` | глаголы | **компаунды** (`[модификатор + интерфикс] + verb`), отобраны субагентом |
| `verb_sfx.jsonl` | глаголы | **verb + суффикс → verb** (ну2/ану/ива/ся…), очищено по Вики/Далю |
| `verb_complex.jsonl` | глаголы | **префикс + verb + суффикс → verb** (complex, 52 правила) |
| `verb_complex.jsonl` | глаголы | **префикс + verb + суффикс → verb** (complex), очищено по Вики/Далю |

Дальше сюда добавятся (тем же форматом): `verb_verb.jsonl` (verb→verb, прочие способы),
`verb_noun.jsonl` / `verb_adj.jsonl` / `verb_num.jsonl` (другие ЧР → verb) и т.д.

## Единый датасет (`unified.jsonl.gz`)

`unified.jsonl.gz` — **агрегат всех финалов выше**: все рёбра деривации в одном файле,
дубликаты записей схлопнуты. Собирается `scripts/build_unified.py` (по умолчанию берёт
именно список финалов из таблицы выше — при добавлении нового финального файла просто
пересоберите единый датасет):

```
.venv/bin/python scripts/build_unified.py --out data/derived/unified.jsonl.gz
.venv/bin/python scripts/build_components.py \
    --input data/derived/unified.jsonl.gz --aggregate --out-dir data/derived
```

Для него считается **общее разбиение на компоненты связности** (`unified.components.json`,
флаг `--aggregate` помечает сайдкар агрегатом). Сервис показывает `unified` отдельным
датасетом, а строка «все датасеты» (`*`) берёт итоговые счётчики (рёбра, лексемы,
компоненты, размер крупнейшей) из этого сайдкара — агрегат не суммируется с частями.

Текущие цифры: ~77,9 тыс. рёбер, ~71,4 тыс. узлов, ~11,2 тыс. компонент, крупнейшая ~14,3 тыс. узлов.

## Схема записи (одно ребро = одна строка JSONL)

```json
{"schema":1,"id":"газифицировать|verb","word":"газифицировать","pos":"verb",
 "lang":"rus","accented":null,"hom_index":0,
 "rule":"rule962(noun + [фиц] -> verb)","kind":"sfx",
 "parents":[{"id":"газ|noun","word":"газ","pos":"noun","role":"head","slot":0}],
 "verified":true,"verified_by":["wiktionary"]}
```

Обязательные поля: `id`, `word`, `pos`, `parents[].id`. Опциональные: `accented`, `rule`,
`kind` (`sfx` / `pfx` / `compound`), `verified`, `verified_by`. У компаунда — 2 родителя
(`role` = `head` и `modifier`, `slot` 0/1).

## Компоненты связности (предрасчёт)

Чтобы сервис не строил компоненты на фронте, рядом с каждым файлом кладётся сайдкар
`<name>.components.json`, созданный `scripts/build_components.py`:

```
.venv/bin/python scripts/build_components.py \
    --input data/derived/verb_pfx.jsonl --input data/derived/adv.jsonl.gz \
    --out-dir data/derived
```

Формат сайдкара: `{nodes, edges, n_components, largest, id2c, sizes, reps}`.
Сервис подхватывает сайдкар автоматически и берёт счётчики из него,
не загружая сам датасет (`/api/datasets` больше не блокирует цикл).

Для единого датасета сайдкар строится с `--aggregate` (см. выше): помимо счётчиков
он помечается `"aggregate": true`, по которому сервис понимает, что датасет —
агрегат остальных. Нюанс: сайдкар считает все узлы датасета, а вьюер пока скрывает
многословные id (типа `двадцать восемь|num`, все они — в `num.jsonl.gz`), поэтому
числа могут расходиться на пару десятков узлов.

## Чего в `--data` быть не должно (промежуточные)

- `adv.jsonl.gz`, `adv_g1.jsonl`, `adv_g2.jsonl`, `adv.rare.jsonl`, `adv_*.final.jsonl` — сырые/промежуточные стадии;
- `verb.jsonl.gz`, `verb_pfx.filtered.jsonl`, `verb_pfx.inf.jsonl`, `verb_compound_fsm.jsonl`, `verb_doubtful*.jsonl` —
  промежуточные результаты глагольного конвейера (сырьё, сомнительные, FSM-анализ);
- `*.tsv` — рабочие таблицы.

Сервис листает **любой** `*.jsonl(.gz)` в каталоге, поэтому лишние файлы засоряют
список датасетов (а большие — попадают в `skipped`). Держите в `--data` только финалы.

## Discovery и лимиты сервиса

- Подхватывает все `*.jsonl` и `*.jsonl.gz` в `--data`; счётчики — из сайдкара, иначе (если файл ≤ `--eager-max`,
  по умолчанию 5 МБ) файл загружается; более крупные файлы без сайдкара попадают в `skipped`.
- Запуск: `node server.js --port 8791 --data <dir> --max-bytes 80000000`.

## Эндпоинты

- `GET /api/datasets` — список датасетов со счётчиками (из сайдкаров), `includes` для `*`. 
- `GET /api/components?dataset=<name>&fields=meta|id2c|sizes|reps|all` — предрасчитанные компоненты.
- `GET /api/search?q=&dataset=&limit=` — поиск лексем.
- `GET /api/graph?id=&dataset=&depth=&maxNodes=&roots=` — окрестность узла (+ `component`).
- `GET /api/lexeme?id=&dataset=` — лексема и её рёбра.
