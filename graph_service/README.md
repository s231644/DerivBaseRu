# DerivBaseRu graph viewer

Zero-dependency Node service that renders word-relation graphs from the JSONL
derivation files (`data/derived/*.jsonl[.gz]`, schema in `docs/derivation_schema.md`).

## Run

    node server.js --port 8791 --data ../data/derived

Opens on http://127.0.0.1:8791 (loopback only).

## API

| endpoint | params | returns |
|---|---|---|
| `GET /api/datasets` | — | `{dataDir, datasets:[{name, edges, lexemes, lines}]}` |
| `GET /api/search` | `q`, `dataset`, `limit` | matching lexemes (exact > prefix > substring) |
| `GET /api/graph` | `id`, `dataset`, `depth`, `maxNodes` | neighbourhood `{focus, nodes, links}` |
| `GET /api/lexeme` | `id`, `dataset` | one lexeme with its parents/children |

Datasets are re-read when the file mtime changes; HTTP responses use `Cache-Control: no-store`
and asset URLs carry a token derived from the assets' mtimes.

## Datasets

Every `*.jsonl[.gz]` in the data dir shows up in the picker. The first entry is
`все датасеты` (`dataset=*`), which merges them into one graph and searches across all.

- Datasets larger than `--max-bytes` (default 20 MB) are listed under `skipped` and
  are not loaded; a 5M-edge dataset would not fit in memory.
- When one dataset stem extends another with a dot (`adv.rare.jsonl` vs
  `adv.rare.verified.jsonl`) only the most specific one feeds the merged view.
  Override with `--include a.jsonl,b.jsonl`.
- Multi-word lexemes are skipped while `SKIP_MULTIWORD` is true.

## UI

Left panel: dataset picker + lexeme search (debounced). Click a result or a graph node to
build that lexeme's neighbourhood; drag nodes to rearrange; depth selector 1–3.
Parent (producing) words are blue, the focused lexeme is gold.

## Keep alive (launchd)

    launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/ai.openclaw.derivbase-graphview.plist

Restart: `launchctl kickstart -k gui/$(id -u)/ai.openclaw.derivbase-graphview`
Stop:    `launchctl bootout gui/$(id -u)/ai.openclaw.derivbase-graphview`
