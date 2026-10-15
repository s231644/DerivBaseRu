# DerivBaseRu graph viewer

Zero-dependency Node service that renders word-relation graphs from the JSONL
derivation files (`data/derived/*.jsonl[.gz]`, schema in `docs/derivation_schema.md`).

## Run

    node server.js --port 8791 --data ../data/derived

Opens on http://127.0.0.1:8791 (loopback only).

## API

| endpoint | params | returns |
|---|---|---|
| `GET /api/datasets` | — | `{dataDir, datasets:[{name, edges, lexemes, components, largest}]}` |
| `GET /api/components` | `dataset`, `fields=meta\|id2c\|sizes\|reps\|all` | precomputed connected components |
| `GET /api/search` | `q`, `dataset`, `limit` | matching lexemes (exact > prefix > substring) |
| `GET /api/graph` | `id`, `dataset`, `depth`, `maxNodes` | neighbourhood `{focus, nodes, links, component}` |
| `GET /api/lexeme` | `id`, `dataset` | one lexeme with its parents/children |

Datasets are re-read when the file mtime changes; HTTP responses use `Cache-Control: no-store`
and asset URLs carry a token derived from the assets' mtimes.

## Datasets

Every `*.jsonl[.gz]` in the data dir shows up in the picker. The first entry is
`все датасеты` (`dataset=*`), which merges them into one graph and searches across all.

- If the data dir contains an **aggregate dataset** (`unified.jsonl.gz`, built by
  `scripts/build_unified.py` + `scripts/build_components.py --aggregate`, see
  `DATASETS.md`), the merged view IS that dataset: its sidecar provides the `*`
  totals and the components of the whole graph, and intermediate files that may
  lie around in the data dir stay out of `*`. Override with `--include a.jsonl,b.jsonl`.
- Datasets larger than `--max-bytes` (default 20 MB) are listed under `skipped` and
  are not loaded; a 5M-edge dataset would not fit in memory.
- When one dataset stem extends another with a dot (`adv.rare.jsonl` vs
  `adv.rare.verified.jsonl`) only the most specific one feeds the merged view.
- Multi-word lexemes are skipped while `SKIP_MULTIWORD` is true.

## Components

Connected components are precomputed per dataset by `scripts/build_components.py`
into `<name>.components.json` sidecars (`{nodes, edges, n_components, largest, id2c,
sizes, reps}`); the service serves them via `/api/components` and attaches
`{index, size}` of the lexeme's component to every `/api/graph` response. The UI
shows the component count in the dataset picker and the lexeme's component in the
info panel. Rebuild sidecars after regenerating the data (see `DATASETS.md`).

## UI

Left panel: dataset picker + lexeme search (debounced). Click a result or a graph node to
build that lexeme's neighbourhood; drag nodes to rearrange; depth selector 1–3.
Parent (producing) words are blue, the focused lexeme is gold.

## Keep alive (launchd)

    launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/ai.openclaw.derivbase-graphview.plist

Restart: `launchctl kickstart -k gui/$(id -u)/ai.openclaw.derivbase-graphview`
Stop:    `launchctl bootout gui/$(id -u)/ai.openclaw.derivbase-graphview`
