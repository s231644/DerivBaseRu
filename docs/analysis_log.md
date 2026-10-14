# Журнал анализа правил словообразования

Порядок работ и результаты. Данные не коммитятся (артефакты), скрипты и журнал — коммитятся.

| # | группа правил | правила | рёбер | итог |
|---|---|---|---:|---|
| 1 | префиксальные «pfx + adv → adv» | `rule992`, `rule993`×10, `rule993*`, `rule1022` | 91 714 | **1 159** = 782 (Викисловарь) + 377 (Даль, проверено субагентами) |
| 2 | суффиксальные «adv + суффикс → adv» | `rule988`, `rule989`, `rule990`, `rule991` | 27 544 | **379** |
| 3 | суффиксальные от других ЧР | `rule982`, `rule977`, `rule981`, `rule979`, `rule985`, `rule987*`, `rule986`, `rule983`, `rule980` | ~1,52 млн | **6 494** = 4 357 (Викисловарь) + 1 850 (Викисловарь+Даль) + 287 (Даль, проверено по ЧР) |
| 4 | префиксально-суффиксальные (complex) | `rule1020`×4, `rule994`, `rule998`, `rule1010`×3, `rule999`, `rule1001–1004`, `rule996`, `rule995`, `rule1017`, `rule1018` | ~3,3 млн | **1 452** = 348 (Викисловарь) + 578 (Викисловарь+Даль) + 526 (Даль, проверено по ЧР) |
| 5 | compound-правила наречий | `rule1026`, `rule1026*`, `rule1027`, `rule1028`, `rule1029`, `rule981*` | — | ожидает; ранее признаны мусорными |

## Метод

1. Просев по словарям (`filter_by_dictionaries.py filter`): запись держится, если слово есть
   в Викисловаре с нужной частью речи либо встречается у Даля (заголовок или токен толкования).
2. Записи, подтверждённые **только Далей**, уходят в `--doubtful` и проверяются:
   - группа 1 (499 шт.) — **субагентами** (`dahl-judge-1/2`: 212 + 165 одобрено);
   - группы 3 (16 087) и 4 (6 604) — субагентами не масштабируется, поэтому применяется
     детерминированная проверка: слова, известные Викисловарю **с другой частью речи**,
     отбрасываются сразу, остальные проверяются морфологически (`pymorphy3`, тег `ADVB`).
3. Итог — `*.final.jsonl` со `verified` и `verified_by`.

## Как воспроизвести

```sh
# генерация
.venv/bin/python scripts/run_pipeline.py --pos-a adv --complexities simple,complex \
    --extra-dataset data/derived/num.jsonl --out data/derived/adv.jsonl.gz

# этап 1: просев группы по словарям (группа 3)
.venv/bin/python scripts/filter_by_dictionaries.py filter \
    --rules-prefix rule982,rule977,rule981,rule979,rule985,rule987,rule986,rule983,rule980 \
    --pos-a adv --input data/derived/adv.jsonl.gz \
    --out data/derived/adv_g1.jsonl --doubtful /tmp/g1_doubtful.jsonl

# группа 4
.venv/bin/python scripts/filter_by_dictionaries.py filter \
    --rules-prefix rule1020,rule994,rule998,rule1010,rule999,rule1001,rule1002,rule1003,rule1004,rule996,rule995,rule1017,rule1018 \
    --pos-a adv --input data/derived/adv.jsonl.gz \
    --out data/derived/adv_g2.jsonl --doubtful /tmp/g2_doubtful.jsonl

# этап 2: слияние вердиктов субагентов
.venv/bin/python scripts/filter_by_dictionaries.py merge \
    --filtered data/derived/adv_pfx.jsonl \
    --judged /tmp/dahl_ok1.jsonl --judged /tmp/dahl_ok2.jsonl \
    --final data/derived/adv_pfx.final.jsonl
```

## Инструменты

- `scripts/run_pipeline.py` — генерация (`--extra-dataset` — цепочки, `--exclude-file` — псевдо-леммы, `--real-only`).
- `scripts/filter_by_dictionaries.py` — просев по Викисловарю и Далю (`filter`) и слияние вердиктов (`merge`).
- `scripts/sort_edges.py` — группировка по частоте правила и сортировка записей.
- `docs/verification_policy.md` — де-факто важнее устаревшей грамматики; диалектное и устаревшее подходит.

## Файлы результатов (data/derived/)

- `adv.jsonl.gz` — все наречия, 4 966 548 рёбер.
- `adv_pfx.jsonl` → `adv_pfx.final.jsonl` — группа 1: 1 281 → **1 159**.
- `adv_sfx.jsonl` — группа 2: **379**.
- `adv_g1.jsonl` → `adv_g1.final.jsonl` — группа 3: 22 291 → **6 494**.
- `adv_g2.jsonl` → `adv_g2.final.jsonl` — группа 4: 7 530 → **1 452**.
- `adv.rare.jsonl` / `adv.rare.verified.jsonl` — правила с `per_rule ≤ 100`: 157 записей, 76 verified.

## Наблюдения

- Префиксальные типы почти не продуктивны (1.4% подтверждений); исключение — `не + adv` (7%).
- Суффиксальные от наречий (`-овато/-онько/-охонько/-ком`) чисты: мусора практически нет.
- Суффиксальные от других ЧР: ядро дают `adj + о/и` (5 205 + 812); `noun + INSTR` — лишь 379 из 787 324 (0.05%).
- Префиксально-суффиксальные: подтверждается ~0.04% (1 452 из 3,3 млн); лучшие — `rule1010(в + noun + ACC)` (252) и `rule1020(в/на + verb + ку/0m2)` (220/211/190/64).
- Остаточные дефекты: в Dahl-части остаются слова с заглавной буквы (`заМало ← Малый`, `вБежку ← Бежка`) и совпадения по токену толкования (`набедно ← бедный`); их стоит отдельно дочистить.
- Данные содержат статьи Викисловаря с заглавной буквы (`Куце ← Куцый`, `Бегом ← Бег`) — учитывать при фильтрации.
