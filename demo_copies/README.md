# DerivBaseRu — demo copies (branch `2022_version`)

Runnable copies of the notebooks/scripts from `demo/`, adapted to the code on
branch `2022_version`. The originals under `demo/` are left untouched.

## Environment

    python3.11 -m venv .venv
    .venv/bin/python -m pip install lark pymorphy2 pandas tqdm lxml requests beautifulsoup4 pypdf

- Python 3.11 is used because pymorphy2 0.9.1 relies on `inspect.getargspec`,
  removed in Python 3.11+. A venv `sitecustomize.py` restores it.
- Run each script from anywhere: the copies fix `sys.path` themselves.

## Fixes applied vs. the notebooks

1. Import case: `from derivbase_ru.derivation import ...` -> `from derivbase_ru.derivation import ...`.
2. Constructor: `Derivation(use_guesser=True)` -> `Derivation(guesser=TagGuesserWrapper(lang='rus'))`.
3. Removed attribute `Derivation.rules` -> `loaded_rules` / `rules_dict`.
4. `is_extended=True` returns `{word_a: [rule_id, ...]}` (the notebooks assumed `{rule_id: words}`).
5. Compound paths: `src.fsm_part` -> `src.compounding.fsm_part`,
   `src.compound_analyzer` -> `src.compounding.compound_analyzer`,
   `src.FinateStateMachine` -> `src.compounding.fsm`.
6. Rule file path: `src/rules/compounds.json` -> `src/rules/rus/compounds.json`.
7. `derivator.tag_guesser.morph` -> `derivator.tag_guesser.guesser.morph`.
8. `DerivedFSM` uses `multiprocessing.Pool`; the copy wraps work in
   `if __name__ == '__main__':` to avoid spawn recursion on macOS.

## Scripts

- demo_usage.py         - guesser, rule counts, rule apply, derive (main demo)
- demo_readme.py        - README derive example
- demo_graph.py         - derivational connections vs Wiktionary vocabulary
- demo_tikhonov.py      - connections among the compound lemmas from the Tikhonov set
- demo_compounds.py     - finite-state compound splitting / analysis
- demo_compound_rules.py- list the compound rules
- demo_kazakh.py        - Kazakh derivational demo

## Not runnable as-is (missing inputs)

- demo/graph.ipynb   - needs `gensim`, a `tagged_texts/` corpus, and the removed
  `derive_with_pos_ext` method.
- demo/FOREIGN.ipynb - needs the absent `data/rusgram_roots_f.txt` and old module paths.
