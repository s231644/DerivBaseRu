"""Generate all verb=verb+sfx.json candidates, including its postfix rule."""
import argparse
from pathlib import Path

from rebuild_verb_prefixes import ROOT, run
from verb_registry import DEFAULT_REGISTRY

RULES = ROOT / 'derivbase_ru/rules/rus/verb/simple/verb=verb+sfx.json'


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dict', default=str(ROOT / 'data/wiktionary/parsed_ru.jsonl.gz'))
    parser.add_argument('--dahl', default=str(ROOT / 'data/dahl/dahl.jsonl.gz'))
    parser.add_argument('--inflect-types', default=str(DEFAULT_REGISTRY))
    parser.add_argument('--out', default=str(ROOT / 'data/derived/verb_sfx.jsonl'))
    parser.add_argument('--include-rules', nargs='+', help='rule IDs, e.g. rule836 rule840')
    parser.add_argument('--candidates-only', action='store_true',
                        help='generate candidates without applying semantic review')
    args = parser.parse_args()
    if args.include_rules and (not args.candidates_only or
            Path(args.out).resolve() == ROOT / 'data/derived/verb_sfx.jsonl'):
        parser.error('Selective generation requires --candidates-only and a separate --out')
    run(args.dict, args.dahl, args.inflect_types, args.out,
        rules_path=RULES, allowed_info={'SFX', 'PTFX'}, include_rules=args.include_rules)
    if not args.candidates_only:
        from review_verb_suffixes import review
        review(args.out, args.dict)
