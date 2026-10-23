"""Generate all verb=verb+sfx.json candidates, including its postfix rule."""
import argparse

from rebuild_verb_prefixes import ROOT, run

RULES = ROOT / 'derivbase_ru/rules/rus/verb/simple/verb=verb+sfx.json'


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dict', default=str(ROOT / 'data/wiktionary/parsed_ru.jsonl.gz'))
    parser.add_argument('--dahl', default=str(ROOT / 'data/dahl/dahl.jsonl.gz'))
    parser.add_argument('--inflect-types', default=str(ROOT / 'data/verb_inflect_types.json'))
    parser.add_argument('--out', default=str(ROOT / 'data/derived/verb_sfx.jsonl'))
    args = parser.parse_args()
    run(args.dict, args.dahl, args.inflect_types, args.out,
        rules_path=RULES, allowed_info={'SFX', 'PTFX'})
