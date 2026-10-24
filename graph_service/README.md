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

The light interface has search and dataset statistics on the left, the graph in
the centre, and details about the selected word on the right. The layout adapts
to narrow screens. Search is debounced; `/` focuses search and Enter opens the
first result. Example words are clickable. Select depth 1–10 or toggle edge labels
in the graph toolbar. Prefix labels are compact; hover over an edge for its full rule.

Click a result or graph node to explore its neighbourhood. Graph nodes also work
with Enter/Space. Drag the background to pan or a vertex to reposition it, including
with touch. The wheel and zoom controls change scale; the fit button includes word
labels in the view. Part of speech determines node colour; an orange outline marks
the focus. Arrow lines and heads share a colour based on relation kind (prefix,
suffix, postfix, compound, prefix+suffix, complex, interfix or conversion), with a
neutral fallback for unknown kinds. The legend separates node POS colours from
relation colours and shows only categories present in the current graph.
The inspector shows producing bases, derivatives and component statistics.

## Keep alive (launchd)

From the repository root, prepare the curated datasets and install the user service:

    .venv/bin/python scripts/prepare_graph_viewer.py
    .venv/bin/python scripts/install_graph_viewer_service.py --install

The permanent viewer runs at http://127.0.0.1:8792 using `data/derived/viewer`.
It runs independently of terminal/chat sessions, starts at login, and restarts
automatically after process exit. macOS must be awake and the user logged in.
The installer updates the existing agent (no second competing instance), saves
the previous plist as `.plist.previous`, and uses absolute Node and repository paths.
Without `--install` it prints the proposed plist. Use `--port` to change the port.

Status: `launchctl print gui/$(id -u)/ai.openclaw.derivbase-graphview`

Logs: `graph_service/logs/out.log` and `graph_service/logs/err.log`.

Restart: `launchctl kickstart -k gui/$(id -u)/ai.openclaw.derivbase-graphview`
Stop:    `launchctl bootout gui/$(id -u)/ai.openclaw.derivbase-graphview`

Compound relations display only their head links. Modifier links are excluded
from traversal and component statistics, so their word families do not bridge
otherwise separate graphs. Original JSONL derivations retain all parents.
Component sidecars for the viewer must be built with
`--exclude-compound-modifiers` (included in `prepare_graph_viewer.py`).

## Affix coordinate layout

The viewer places visible producing bases at the top left instead of centring
on the selected word. Prefix vectors point mostly down; suffix vectors mostly
right. Postfixes and other relation kinds occupy separate diagonal sectors.
Confixes add their prefix/suffix/postfix vectors. Alternative suffixes are
selected from the pair rather than added together (including -ива-/-ыва-
allomorphy and the distinction between -ива- and -ва- in пить → пивать).
Numbered homonymous affixes remain distinct and show their indices as subscripts.

`public/affix-vectors.json` is the shared catalogue: 467 unique vectors from 979
Russian rule descriptions. A stable key determines each angle and length;
collisions are resolved when building the complete sorted catalogue. Vectors
do not depend on the focus, visible subset, viewport or input ordering. Regenerate
the catalogue after changing the rule inventory:

    node scripts/build_affix_vectors.js

`public/affix-layout.js` is shared by the browser, builder and Node tests. It finds
source strongly connected components, uses actual zero-indegree bases when
available, and chooses an explicitly marked reference point for cyclic data.
Several roots are anchored along the top. A root here means a base in the loaded
graph, not a claim that no derivation exists outside the loaded dataset/depth.

Coordinates solve an anchored least-squares problem for edge vector constraints
in the positive quadrant. Compatible alternative paths add exactly (a prefix
then a suffix reaches the same point as the opposite order); contradictory
analyses are reconciled. Coloured dashed arrows mark geometric residuals over
20% of the intended step (minimum 60 coordinate units). This is a layout conflict,
not an automatic linguistic rejection of the derivation.

Semantic coordinates remain separate from rendered positions. A deterministic
spatial index spreads overlapping word labels; fine grey leaders and dots retain
the original affix positions. Dragging nodes also preserves these reference
positions. The reading guide has an expandable list of the current affix vectors;
edge/node tooltips show intended offsets and semantic coordinates. Colour still
encodes relation kind and node POS, and compound modifiers stay excluded.

Validation:

    node --test tests/test_affix_layout.cjs

Tests cover stable unique vectors, additive diamonds/confixes, allomorph choice,
cycles, contradictory paths and 500 coincident derivations without label overlap.

Параллелограммы из перестановки двух одинаковых аффиксных шагов закрепляются
как жёсткие группы: противоречивые соседние разборы не меняют их форму,
а при устранении наложений группа переносится целиком. Например,
`лечь → полечь`, `лечь → ложить`, `полечь → положить`,
`ложить → положить` образуют параллелограмм.

Стрелки и их подписи по умолчанию полупрозрачны. Наведение на ребро
выделяет только его, наведение на слово (включая подпись) — все исходящие
рёбра. Аналогичное выделение доступно при переходе клавишей Tab.
У рёбер расширена невидимая область наведения.
