#!/usr/bin/env python3
"""Deterministic structural triage of prefix relations, without changing source data."""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
import csv
import hashlib
import gzip
import json
from pathlib import Path
import re

STRONG_EVIDENCE = {'wiktionary_verb', 'dahl_head'}
REJECTED = {'reject', 'rejected', 'semantic_reject', 'semantic_rejected'}
ALIASES = {'со': 'с', 'во': 'в', 'взо': 'вз', 'возо': 'воз', 'вос': 'воз',
           'изо': 'из', 'ис': 'из', 'обо': 'об', 'ото': 'от', 'подо': 'под',
           'надо': 'над', 'разо': 'раз', 'рас': 'раз', 'безо': 'без', 'бес': 'без'}


def normalize(word: str) -> str:
    """Pool reflexive/non-reflexive variants; neither spelling doubles productivity."""
    word = re.sub('[\u0300\u0301]', '', word.lower()).replace('ё', 'е')
    return re.sub(r'(ся|сь)$', '', word)


def prefix_family(rule: str) -> str | None:
    match = re.search(r'\(([^+()]+)\s*\+\s*verb\s*->\s*verb\)', rule)
    if not match:
        return None
    prefix = re.sub(r'[\d\s*]', '', match[1]).lower()
    return ALIASES.get(prefix, prefix)


@dataclass(frozen=True, order=True)
class Edge:
    source: str
    target: str
    prefix: str


@dataclass(frozen=True)
class Thresholds:
    # Counts refer to DISTINCT affix families, never raw rows/word forms.
    sparse_max: int = 1
    productive_min: int = 5
    strong_min: int = 3
    target_source_ratio: float = 0.5


def read_records(path: Path):
    opener = gzip.open if path.suffix == '.gz' else open
    with opener(path, 'rt', encoding='utf-8') as stream:
        for number, line in enumerate(stream, 1):
            if line.strip():
                try:
                    yield json.loads(line)
                except json.JSONDecodeError as exc:
                    raise ValueError(f'{path}:{number}: {exc}') from exc


def audit(records, thresholds: Thresholds = Thresholds()):
    """Return reproducible review candidates and a summary; no semantic verdicts.

    Two independent graph motifs:
      sparse_source: the alleged base has at most one distinct prefix family;
      productive_target: the alleged derivative has >=5 families, >=3 with
        headword evidence and at least half the source's family count.
    The tested edge is excluded from target evidence (self/back edges too).
    All statistics are computed once on the same immutable input graph.
    """
    if (thresholds.sparse_max < 0 or thresholds.productive_min < 1
            or thresholds.strong_min < 1 or thresholds.target_source_ratio <= 0):
        raise ValueError('Thresholds must be positive (sparse_max may be zero)')
    grouped = defaultdict(list)
    strong = set()
    row_count = skipped = 0
    for record in records:
        row_count += 1
        if (record.get('pos') != 'verb' or record.get('kind') not in {'pfx', 'prefix'}
                or record.get('review_status') in REJECTED):
            skipped += 1
            continue
        prefix = prefix_family(record.get('rule', ''))
        if not prefix:
            skipped += 1
            continue
        for parent in record.get('parents', []):
            if parent.get('role', 'head') != 'head' or parent.get('pos') != 'verb':
                continue
            source, target = normalize(parent['word']), normalize(record['word'])
            if source == target:
                continue
            edge = Edge(source, target, prefix)
            grouped[edge].append((parent['word'], record['word'], record.get('rule', '')))
            evidence = set(record.get('lexical_evidence', []))
            if evidence & STRONG_EVIDENCE or 'wiktionary' in record.get('verified_by', []):
                strong.add(edge)
    outgoing = defaultdict(set)
    for edge in grouped:
        outgoing[edge.source].add(edge)

    def profile(word, excluded_target=None):
        edges = [e for e in sorted(outgoing[word])
                 if e.target not in {word, excluded_target}]
        families = sorted({e.prefix for e in edges})
        trusted = sorted({e.prefix for e in edges if e in strong})
        # One representative per affix family keeps explanations compact.
        examples = {}
        for e in edges:
            if e.prefix not in examples or (e in strong and not examples[e.prefix]['headword_evidence']):
                examples[e.prefix] = {'word': e.target, 'headword_evidence': e in strong}
        return {'count': len(families), 'strong_count': len(trusted), 'prefixes': families,
                'strong_prefixes': trusted, 'examples': examples}

    profiles = {word: profile(word) for word in list(outgoing)}
    candidates = []
    for edge in sorted(grouped):
        source = profiles[edge.source]
        target = profile(edge.target, excluded_target=edge.source)
        sparse = source['count'] <= thresholds.sparse_max
        ratio = target['count'] / max(1, source['count'])
        productive = (target['count'] >= thresholds.productive_min
                      and target['strong_count'] >= thresholds.strong_min
                      and ratio >= thresholds.target_source_ratio)
        if not (sparse or productive):
            continue
        reasons = []
        if sparse:
            reasons.append('sparse_source')
        if productive:
            reasons.append('productive_target')
        # A ranking tier, not a probability or automatic reject decision.
        priority = 'high' if sparse and productive else 'medium' if productive else 'low'
        candidates.append({
            'source': edge.source, 'target': edge.target, 'prefix': edge.prefix,
            'decision': 'review', 'priority': priority, 'reasons': reasons,
            'source_profile': source, 'target_profile': target,
            'target_source_ratio': round(ratio, 4),
            'source_other_prefixes': [p for p in source['prefixes'] if p != edge.prefix],
            'variants': [dict(zip(('source', 'target', 'rule'), v))
                         for v in sorted(set(grouped[edge]))],
        })
    rank = {'high': 0, 'medium': 1, 'low': 2}
    candidates.sort(key=lambda c: (rank[c['priority']], -c['target_profile']['strong_count'],
                                   -c['target_profile']['count'], c['source'], c['target'], c['prefix']))
    summary = {'schema': 1, 'decision': 'review_only', 'thresholds': asdict(thresholds),
               'input_rows': row_count, 'skipped_rows': skipped,
               'normalized_edges': len(grouped), 'flagged_edges': len(candidates),
               'priorities': dict(sorted(Counter(c['priority'] for c in candidates).items())),
               'reasons': dict(sorted(Counter(r for c in candidates for r in c['reasons']).items()))}
    return candidates, summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, default=Path('data/derived/verb_pfx.jsonl'))
    parser.add_argument('--output', type=Path, default=Path('data/derived/verb_pfx.structural_review.jsonl'))
    parser.add_argument('--summary', type=Path, default=Path('docs/verb_prefix_structural_audit_2026.json'))
    parser.add_argument('--report', type=Path, default=Path('docs/verb_prefix_structural_review_2026.tsv'))
    parser.add_argument('--sparse-max', type=int, default=1)
    parser.add_argument('--productive-min', type=int, default=5)
    parser.add_argument('--strong-min', type=int, default=3)
    parser.add_argument('--target-source-ratio', type=float, default=0.5)
    args = parser.parse_args()
    paths = (args.input, args.output, args.summary, args.report)
    if len({p.resolve() for p in paths}) != len(paths):
        parser.error('Input and all output paths must be different')
    candidates, summary = audit(read_records(args.input), Thresholds(
        args.sparse_max, args.productive_min, args.strong_min, args.target_source_ratio))
    summary['input'] = str(args.input)
    with args.input.open('rb') as stream:
        summary['input_sha256'] = hashlib.file_digest(stream, 'sha256').hexdigest()
    summary['output'] = str(args.output)
    summary['report'] = str(args.report)
    summary['report_scope'] = 'high_and_medium_priority_only'
    for path in (args.output, args.summary, args.report):
        path.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open('w', encoding='utf-8') as stream:
        for candidate in candidates:
            stream.write(json.dumps(candidate, ensure_ascii=False, sort_keys=True) + '\n')
    with args.report.open('w', encoding='utf-8', newline='') as stream:
        writer = csv.writer(stream, delimiter='\t', lineterminator='\n')
        writer.writerow(['priority', 'source', 'target', 'prefix', 'reasons',
                         'source_prefixes', 'target_prefixes', 'target_strong_prefixes', 'ratio'])
        for c in candidates:
            if c['priority'] != 'low':
                writer.writerow([c['priority'], c['source'], c['target'], c['prefix'],
                                 ','.join(c['reasons']), c['source_profile']['count'],
                                 c['target_profile']['count'], c['target_profile']['strong_count'],
                                 c['target_source_ratio']])
    args.summary.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
