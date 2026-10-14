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

const cache = new Map();

function loadDataset(name) {
  const file = datasetPath(name);
  if (!file) return null;
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
      const datasets = [];
      for (const n of listDatasets()) {
        const d = loadDataset(n);
        if (d) datasets.push({ name: n, edges: d.edges.length, lexemes: d.lexemes.size, lines: d.lines });
      }
      return sendJson(res, { dataDir: DATA_DIR, datasets });
    }
    if (p.startsWith('/api/')) {
      const name = url.searchParams.get('dataset') || listDatasets()[0];
      const ds = name ? loadDataset(name) : null;
      if (!ds) return sendJson(res, { error: 'dataset not readable (missing or still being written)', dataset: name }, 503);
      if (p === '/api/search') {
        const limit = Math.max(1, Math.min(500, Number(url.searchParams.get('limit') || 50)));
        return sendJson(res, { dataset: ds.name, total: ds.lexemes.size, results: search(ds, url.searchParams.get('q') || '', limit) });
      }
      if (p === '/api/graph') {
        const id = url.searchParams.get('id');
        if (!id || !ds.lexemes.has(id)) return sendJson(res, { error: 'lexeme not found', id }, 404);
        const depth = Math.max(1, Math.min(4, Number(url.searchParams.get('depth') || 1)));
        const maxNodes = Math.max(10, Math.min(500, Number(url.searchParams.get('maxNodes') || 150)));
        const upToRoot = url.searchParams.get('roots') !== '0';
        return sendJson(res, Object.assign({ dataset: ds.name }, subgraph(ds, id, depth, maxNodes, upToRoot)));
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
