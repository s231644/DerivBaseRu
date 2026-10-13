# Исправленные ноутбуки Даши Родионовой

Оригиналы присланы как есть:
- `rodionova_test_derivbase.ipynb`
- `rodionova_generate_word_sets_derivbase.ipynb`

Приведены к актуальной ветке `2022_version` и Python 3.11. Что исправлено:

1. `from src.Derivation import ...` -> `from src.derivation import ...` (регистр ломает импорт).
2. Метод `Derivation.derive_ext` удалён — добавлена совместимая функция `derive_ext`, возвращающая список пар `(слово, rule_id)`.
3. Порядок ячеек: `evaluator = Derivation()` определяется **до** первого использования (`derive_ext` вызывался раньше).
4. `pymorphy_to_derivbase` дополнен `infn->verb` и `comp->adj` и переведён на `.get()`: pymorphy отдаёт инфинитивы как `INFN`, а не `VERB`, поэтому глаголы раньше выпадали.
5. Блок **MorphBerta** вынесен под флаг `RUN_MORPHBERTA` (нужны `simpletransformers` и каталог модели `morphberta-t`).
6. Блок **Викисловаря** — под флагом `RUN_WIKTIONARY`: кэш, задержка `WIKTIONARY_DELAY`, обработка сетевых ошибок (без пауз тысячи запросов дают 429).
7. Исправлен путь в архиве: зиповалось `derivat_families_derivbases/`, а писалось в `derivat_families_derivbase/`.

## Про NoneType

Ошибка `'NoneType' object is not iterable` на слове `язык` (и расхождение счётчиков: у неё `сын`=289, в актуальной версии 567) указывают на **другую ревизию репозитория**. В ветке `2022_version` ошибка не воспроизводится: её полный список слов и ещё 150 существительных отрабатывают без исключений.

## Проверка

Обе тетрадки исполнены в `.venv` (Python 3.11) в офлайн-режиме (`RUN_MORPHBERTA=0`, `RUN_WIKTIONARY=0`) — без ошибок; в `rodionova_generate_word_sets_derivbase.ipynb` сгенерировано 64 файла гнёзд.
