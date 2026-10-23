#!/usr/bin/env node
'use strict';

// DerivBaseRu graph viewer: zero-dependency Node HTTP service.
// Reads derivation edges from JSONL(.gz) files and exposes:
//   GET /                 -> single-page UI
//   GET /api/datasets     -> {datasets:[{name,edges,lexemes,mtime}]}
//   GET /api/search       -> ?q=&dataset=&limit=  matching lexemes
//   GET /api/graph        -> ?id=&dataset=&depth= neighbourhood nodes+edges
//   GET /api/lexeme       -> ?id=&dataset=        one lexeme + its edges

const http = require('http');
const fs = require('fs');
const path = require('path');
const zlib = require('zlib');
const crypto = require('crypto');

function parseArgs(argv) {
  const out = {};
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (!a.startsWith('--')) continue;
    const key = a.slice(2);
    const next = argv[i + 1];
    if (next !== undefined && !next.startsWith('--')) { out[key] = next; i++; }
    else out[key] = true;
  }
  return out;
}

const args = parseArgs(process.argv.slice(2));
const PORT = Number(args.port || 8791);
const HOST = args.host || '127.0.0.1';
const ROOT = __dirname;
const DATA_DIR = path.resolve(ROOT, args.data || '../data/derived');
const PUBLIC_DIR = path.resolve(ROOT, args.public || 'public');

// TEMP: multi-word lexemes (ids containing a space, e.g. 'двадцать восемь')
// are kept out of the graph for now. Set to false to bring them back.
const SKIP_MULTIWORD = true;

// Datasets bigger than this are listed but not loaded (a 5M-edge graph would
// not fit in memory); raise with --max-bytes.
const MAX_BYTES = Number(args['max-bytes'] || 20 * 1024 * 1024);
const ALL_DATASETS = '*';
// Datasets without a precomputed components sidecar are loaded eagerly only
// when small; bigger ones are listed as skipped instead of blocking the loop.
const EAGER_MAX = Number(args['eager-max'] || 5 * 1024 * 1024);

const MIME = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript; charset=utf-8',
  '.css': 'text/css; charset=utf-8', '.json': 'application/json; charset=utf-8',
  '.svg': 'image/svg+xml', '.ico': 'image/x-icon' };

function readMaybeGz(file) {
  const buf = fs.readFileSync(file);
  const magic = buf.length > 2 && buf[0] === 0x1f && buf[1] === 0x8b;
  return (file.endsWith('.gz') || magic) ? zlib.gunzipSync(buf).toString('utf8') : buf.toString('utf8');
}

function listDatasets() {
  if (!fs.existsSync(DATA_DIR)) return [];
  const seen = new Set();
  const names = [];
  for (const f of fs.readdirSync(DATA_DIR).sort()) {
    if (!/\.jsonl(\.gz)?$/.test(f)) continue;
    const base = f.replace(/\.gz$/, '');
    if (seen.has(base)) continue;
    seen.add(base);
    names.push(base);
  }
  return names;
}

function datasetPath(name) {
  const plain = path.join(DATA_DIR, name);
  if (fs.existsSync(plain)) return plain;
  const gz = plain + '.gz';
  if (fs.existsSync(gz)) return gz;
  return null;
}

function fileSize(name) {
  const f = datasetPath(name);
  return f ? fs.statSync(f).size : 0;
}

function usableDatasets() {
  return listDatasets().filter((n) => fileSize(n) <= MAX_BYTES);
}

// Datasets that feed the merged view. 'adv.rare.jsonl' is a subset of
// 'adv.rare.verified.jsonl', so when one stem extends another with a dot only
// the most specific one is kept. Override with --include a.jsonl,b.jsonl.
function mergedNames() {
  if (args.include) {
    return String(args.include).split(',').map((s) => s.trim()).filter(Boolean);
  }
  const usable = usableDatasets();
  // An aggregate dataset (unified.jsonl.gz, sidecar flagged aggregate:true by
  // build_unified.py) already unions the finals and drops duplicate records,
  // so the merged view IS that dataset. Intermediates that lie around in
  // --data stay out of '*' too, and its stats match the sidecar exactly.
  for (const n of usable) {
    const c = loadComponents(n);
    if (c && c.aggregate) return [n];
  }
  const stems = usable.map((n) => ({ n, s: n.replace(/\.jsonl(\.gz)?$/, '') }));
  return stems
    .filter((a) => !stems.some((b) => b.n !== a.n && b.s.indexOf(a.s + '.') === 0))
    .map((a) => a.n);
}

const cache = new Map();

// Precomputed connected components: sidecar <dataset>.components.json produced by
// scripts/build_components.py. Served as-is so the frontend never builds components.
const compCache = new Map();

function componentsPath(name) {
  const base = path.join(DATA_DIR, name.replace(/\.jsonl(\.gz)?$/, ''));
  const plain = base + '.components.json';
  if (fs.existsSync(plain)) return plain;
  const gz = plain + '.gz';
  if (fs.existsSync(gz)) return gz;
  return null;
}

function loadComponents(name) {
  const file = componentsPath(name);
  if (!file) return null;
  const mtime = fs.statSync(file).mtimeMs;
  const cached = compCache.get(name);
  if (cached && cached.mtime === mtime) return cached.data;
  let text;
  try { text = readMaybeGz(file); } catch (e) { return null; }
  let data;
  try { data = JSON.parse(text); } catch (e) { return null; }
  // Old sidecars include modifier bridges and cannot describe the visible graph.
  if (data.visualization_policy !== 'compound_head_only') return null;
  compCache.set(name, { mtime, data });
  return data;
}

// Components of the merged view: when '*' is served by the aggregate dataset
// (see mergedNames), its sidecar describes exactly that graph.
function componentsFor(name) {
  const direct = loadComponents(name);
  if (direct || name !== ALL_DATASETS) return direct;
  for (const n of usableDatasets()) {
    const c = loadComponents(n);
    if (c && c.aggregate) return c;
  }
  return null;
}

function loadAllDatasets() {
  const names = mergedNames();
  let mtime = 0;
  for (const n of names) {
    const f = datasetPath(n);
    if (f) mtime = Math.max(mtime, fs.statSync(f).mtimeMs);
  }
  const cached = cache.get(ALL_DATASETS);
  if (cached && cached.mtime === mtime) return cached;
  const merged = {
    name: ALL_DATASETS, file: null, mtime, lines: 0, includes: [],
    lexemes: new Map(), edges: [], children: new Map(), parents: new Map(),
  };
  const seen = new Set();
  for (const n of names) {
    const d = loadDataset(n);
    if (!d) continue;
    merged.includes.push(n);
    merged.lines += d.lines;
    for (const [id, node] of d.lexemes) {
      if (!merged.lexemes.has(id)) {
        merged.lexemes.set(id, { id, word: node.word, pos: node.pos, accented: node.accented, out: 0, in: 0 });
      }
    }
    for (const e of d.edges) {
      const key = e.source + '\\u0000' + e.target + '\\u0000' + (e.rule || '');
      if (seen.has(key)) continue;
      seen.add(key);
      merged.edges.push(e);
      let ch = merged.children.get(e.source);
      if (!ch) { ch = []; merged.children.set(e.source, ch); }
      ch.push(e);
      let pa = merged.parents.get(e.target);
      if (!pa) { pa = []; merged.parents.set(e.target, pa); }
      pa.push(e);
      const s = merged.lexemes.get(e.source); if (s) s.out++;
      const t = merged.lexemes.get(e.target); if (t) t.in++;
    }
  }
  cache.set(ALL_DATASETS, merged);
  return merged;
}

function loadDataset(name) {
  if (name === ALL_DATASETS) return loadAllDatasets();
  const file = datasetPath(name);
  if (!file) return null;
  if (fs.statSync(file).size > MAX_BYTES) return null;
  const mtime = fs.statSync(file).mtimeMs;
  const cached = cache.get(name);
  if (cached && cached.mtime === mtime) return cached;

  let text;
  try {
    text = readMaybeGz(file);
  } catch (e) {
    // The file may be written right now (truncated gzip) or corrupt.
    return null;
  }

  const lexemes = new Map();
  const edges = [];
  const children = new Map();
  const parents = new Map();
  let lines = 0;

  const upsert = (id, word, pos) => {
    let node = lexemes.get(id);
    if (!node) { node = { id, word, pos, out: 0, in: 0 }; lexemes.set(id, node); }
    return node;
  };

  for (const line of text.split('\n')) {
    const t = line.trim();
    if (!t) continue;
    lines++;
    let rec;
    try { rec = JSON.parse(t); } catch (e) { continue; }
    if (!rec || !rec.id) continue;
    if (SKIP_MULTIWORD && /\s/.test(rec.id)) continue;
    const node = upsert(rec.id, rec.word, rec.pos);
    if (rec.accented) node.accented = rec.accented;
    const ps = Array.isArray(rec.parents) ? rec.parents : [];
    for (const p of ps) {
      if (!p || !p.id) continue;
      if (rec.kind === 'compound' && p.role === 'modifier') continue;
      upsert(p.id, p.word, p.pos);
      const edge = { source: p.id, target: rec.id, rule: rec.rule, kind: rec.kind, role: p.role || 'head', slot: p.slot || 0 };
      edges.push(edge);
      if (!children.has(p.id)) children.set(p.id, []);
      children.get(p.id).push(edge);
      if (!parents.has(rec.id)) parents.set(rec.id, []);
      parents.get(rec.id).push(edge);
      lexemes.get(p.id).out++;
      node.in++;
    }
  }
  const data = { name, file, mtime, lexemes, edges, children, parents, lines };
  cache.set(name, data);
  return data;
}

// Compact edge label: the affix/relation part of the rule name.
// 'rule1032(num + надцать -> num)' -> 'надцать'
function ruleLabel(rule) {
  const m = /\(([^)]*)\)/.exec(rule || '');
  if (!m) return rule || '';
  let left = m[1].split('->')[0] || '';
  const plus = left.lastIndexOf('+');
  if (plus >= 0) left = left.slice(plus + 1);
  return left.trim();
}

function subgraph(ds, focusId, depth, maxNodes, upToRoot) {
  const nodes = new Map();
  const usedEdges = [];
  const seenEdges = new Set();
  const add = (id) => { if (!nodes.has(id)) nodes.set(id, ds.lexemes.get(id) || { id, word: id.split('|')[0], pos: (id.split('|')[1] || '') }); };
  const link = (e) => {
    const key = e.source + '\u0000' + e.target + '\u0000' + (e.rule || '');
    if (!seenEdges.has(key)) { seenEdges.add(key); usedEdges.push(e); }
  };
  add(focusId);

  // 1. neighbourhood in both directions, up to `depth` levels
  let frontier = [focusId];
  for (let d = 0; d < depth; d++) {
    const next = [];
    for (const id of frontier) {
      const around = (ds.parents.get(id) || []).concat(ds.children.get(id) || []);
      for (const e of around) {
        link(e);
        const other = e.source === id ? e.target : e.source;
        if (!nodes.has(other) && nodes.size < maxNodes) { add(other); next.push(other); }
      }
    }
    frontier = next;
    if (nodes.size >= maxNodes) break;
  }

  // 2. derivation trees are shallow: climb to the roots (unless roots=0)
  //    so a multi-word numeral still reaches its base numeral.
  if (upToRoot) {
    let changed = true;
    while (changed && nodes.size < maxNodes) {
      changed = false;
      for (const id of [...nodes.keys()]) {
        for (const e of ds.parents.get(id) || []) {
          link(e);
          if (!nodes.has(e.source) && nodes.size < maxNodes) { add(e.source); changed = true; }
        }
      }
    }
  }
  return {
    focus: focusId,
    nodes: [...nodes.values()],
    links: usedEdges.map((e) => ({ source: e.source, target: e.target, rule: e.rule, kind: e.kind, label: e.rule, short: ruleLabel(e.rule), pos: (ds.lexemes.get(e.target) || {}).pos || null })),
  };
}

function versionToken() {
  const files = ['index.html', 'app.js', 'styles.css'];
  const h = crypto.createHash('sha1');
  for (const f of files) {
    const p = path.join(PUBLIC_DIR, f);
    try { h.update(f + ':' + fs.statSync(p).mtimeMs); } catch (e) { h.update(f + ':0'); }
  }
  return h.digest('hex').slice(0, 10);
}

function sendJson(res, obj, status = 200) {
  const body = Buffer.from(JSON.stringify(obj), 'utf8');
  res.writeHead(status, { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-store', 'Content-Length': body.length });
  res.end(body);
}

function sendFile(res, file) {
  const ext = path.extname(file).toLowerCase();
  fs.readFile(file, (err, buf) => {
    if (err) { res.writeHead(404, { 'Content-Type': 'text/plain; charset=utf-8' }); res.end('not found'); return; }
    res.writeHead(200, { 'Content-Type': MIME[ext] || 'application/octet-stream', 'Cache-Control': 'no-store', 'Content-Length': buf.length });
    res.end(buf);
  });
}

function search(ds, q, limit) {
  const query = (q || '').toLowerCase().trim();
  const out = [];
  for (const node of ds.lexemes.values()) {
    const w = node.word.toLowerCase();
    let rank = -1;
    if (query === '') rank = 3;
    else if (w === query) rank = 0;
    else if (w.startsWith(query)) rank = 1;
    else if (w.includes(query)) rank = 2;
    if (rank < 0) continue;
    out.push({ rank, id: node.id, word: node.word, pos: node.pos, accented: node.accented || null, parents: node.in, children: node.out });
  }
  out.sort((a, b) => a.rank - b.rank || a.word.localeCompare(b.word, 'ru'));
  return out.slice(0, limit).map((r) => ({ id: r.id, word: r.word, pos: r.pos, accented: r.accented, parents: r.parents, children: r.children }));
}

const server = http.createServer((req, res) => {
  const url = new URL(req.url, 'http://' + HOST + ':' + PORT);
  const p = url.pathname;
  try {
    if (p === '/api/datasets') {
      // Cheap listing: counts come from precomputed <name>.components.json sidecars,
      // so we never load heavy datasets just to report their size.
      const names = listDatasets();
      const datasets = [];
      const skipped = [];
      const included = [];
      let sumEdges = 0, sumNodes = 0;
      let aggregate = null, aggregateName = null;
      for (const n of names) {
        const comp = loadComponents(n);
        if (comp) {
          datasets.push({ name: n, label: n.replace(/\.jsonl(\.gz)?$/, ''), edges: comp.edges, lexemes: comp.nodes, components: comp.n_components, largest: comp.largest, source: 'components' });
          // the aggregate (unified dataset) is shown as its own row; the '*'
          // totals are taken from it instead of summing it with the parts
          if (comp.aggregate) { if (!aggregate) { aggregate = comp; aggregateName = n; } continue; }
          included.push(n); sumEdges += comp.edges; sumNodes += comp.nodes;
          continue;
        }
        if (fileSize(n) > EAGER_MAX) { skipped.push({ name: n, bytes: fileSize(n), reason: 'no components, over eager-max' }); continue; }
        const d = loadDataset(n);
        if (d) {
          datasets.push({ name: n, label: n.replace(/\.jsonl(\.gz)?$/, ''), edges: d.edges.length, lexemes: d.lexemes.size, lines: d.lines, components: null, source: 'loaded' });
          included.push(n); sumEdges += d.edges.length; sumNodes += d.lexemes.size;
        } else { skipped.push({ name: n, bytes: fileSize(n), reason: 'unreadable' }); }
      }
      datasets.unshift({ name: ALL_DATASETS, label: 'все датасеты',
        edges: aggregate ? aggregate.edges : sumEdges,
        lexemes: aggregate ? aggregate.nodes : sumNodes,
        components: aggregate ? aggregate.n_components : null,
        largest: aggregate ? aggregate.largest : null,
        includes: aggregate ? [aggregateName] : included, source: 'components' });
      return sendJson(res, { dataDir: DATA_DIR, datasets, skipped });
    }
    if (p === '/api/components') {
      const cname = url.searchParams.get('dataset') || ALL_DATASETS;
      const comp = componentsFor(cname);
      if (!comp) return sendJson(res, { error: 'components not precomputed', dataset: cname }, 404);
      const fields = (url.searchParams.get('fields') || 'reps').split(',').map((s) => s.trim());
      const out = { dataset: cname, nodes: comp.nodes, edges: comp.edges, n_components: comp.n_components, largest: comp.largest };
      if (fields.indexOf('all') >= 0) { out.id2c = comp.id2c; out.sizes = comp.sizes; out.reps = comp.reps; }
      else {
        if (fields.indexOf('id2c') >= 0) out.id2c = comp.id2c;
        if (fields.indexOf('sizes') >= 0) out.sizes = comp.sizes;
        if (fields.indexOf('reps') >= 0) out.reps = comp.reps;
      }
      return sendJson(res, out);
    }
    if (p.startsWith('/api/')) {
      const name = url.searchParams.get('dataset') || ALL_DATASETS;
      const ds = name ? loadDataset(name) : null;
      if (!ds) return sendJson(res, { error: 'dataset not readable (missing or still being written)', dataset: name }, 503);
      if (p === '/api/search') {
        const limit = Math.max(1, Math.min(500, Number(url.searchParams.get('limit') || 50)));
        return sendJson(res, { dataset: ds.name, total: ds.lexemes.size, results: search(ds, url.searchParams.get('q') || '', limit) });
      }
      if (p === '/api/graph') {
        const id = url.searchParams.get('id');
        if (!id || !ds.lexemes.has(id)) return sendJson(res, { error: 'lexeme not found', id }, 404);
        const depth = Math.max(1, Math.min(10, Number(url.searchParams.get('depth') || 1)));
        const maxNodes = Math.max(10, Math.min(500, Number(url.searchParams.get('maxNodes') || 150)));
        const upToRoot = url.searchParams.get('roots') !== '0';
        const comp = componentsFor(ds.name);
        let compInfo = null;
        if (comp && comp.id2c && Object.prototype.hasOwnProperty.call(comp.id2c, id)) {
          const ci = comp.id2c[id];
          compInfo = { index: ci, size: comp.sizes ? comp.sizes[String(ci)] : null };
        }
        return sendJson(res, Object.assign({ dataset: ds.name, component: compInfo }, subgraph(ds, id, depth, maxNodes, upToRoot)));
      }
      if (p === '/api/lexeme') {
        const id = url.searchParams.get('id');
        const node = ds.lexemes.get(id);
        if (!node) return sendJson(res, { error: 'lexeme not found', id }, 404);
        return sendJson(res, {
          dataset: ds.name,
          lexeme: node,
          parents: (ds.parents.get(id) || []).map((e) => ({ id: e.source, rule: e.rule, kind: e.kind })),
          children: (ds.children.get(id) || []).map((e) => ({ id: e.target, rule: e.rule, kind: e.kind })),
        });
      }
      return sendJson(res, { error: 'unknown endpoint' }, 404);
    }
    if (p === '/' || p === '/index.html') {
      const file = path.join(PUBLIC_DIR, 'index.html');
      const html = fs.readFileSync(file, 'utf8').replace(/__V__/g, versionToken());
      const body = Buffer.from(html, 'utf8');
      res.writeHead(200, { 'Content-Type': MIME['.html'], 'Cache-Control': 'no-store', 'Content-Length': body.length });
      return res.end(body);
    }
    const file = path.join(PUBLIC_DIR, p);
    if (!path.resolve(file).startsWith(PUBLIC_DIR)) return sendJson(res, { error: 'forbidden' }, 403);
    return sendFile(res, file);
  } catch (e) {
    return sendJson(res, { error: String((e && e.message) || e) }, 500);
  }
});

server.listen(PORT, HOST, () => {
  console.log('DerivBaseRu graph viewer on http://' + HOST + ':' + PORT);
  console.log('data dir: ' + DATA_DIR);
  console.log('datasets: ' + (listDatasets().join(', ') || '(none)'));
});
