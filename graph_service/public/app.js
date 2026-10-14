'use strict';

var svgNS = 'http://www.w3.org/2000/svg';
var state = { dataset: null, depth: 1, nodes: [], links: [], focus: null, raf: null, alpha: 1, active: null };

function el(id) { return document.getElementById(id); }
var svg = el('graph');

function api(endpoint, params) {
  var u = new URL(endpoint, location.origin);
  Object.keys(params || {}).forEach(function (k) {
    var v = params[k];
    if (v !== null && v !== undefined && v !== '') u.searchParams.set(k, v);
  });
  return fetch(u).then(function (r) {
    return r.json().then(function (j) { if (!r.ok) throw new Error(j.error || r.statusText); return j; });
  });
}

function setStatus(t) { el('status').textContent = t || ''; }

function initDatasets() {
  return api('/api/datasets').then(function (d) {
    var sel = el('dataset');
    sel.innerHTML = '';
    (d.datasets || []).forEach(function (ds) {
      var o = document.createElement('option');
      o.value = ds.name;
      o.textContent = ds.name + ' (' + ds.edges + ' рёбер, ' + ds.lexemes + ' лексем)';
      sel.appendChild(o);
    });
    state.dataset = sel.value || null;
    setStatus(d.datasets && d.datasets.length ? '' : 'нет .jsonl в каталоге данных');
    if (state.dataset) return search('');
  });
}

var searchTimer = null;
function scheduleSearch() {
  clearTimeout(searchTimer);
  searchTimer = setTimeout(function () { search(el('q').value); }, 150);
}

function search(q) {
  return api('/api/search', { q: q, dataset: state.dataset, limit: 60 }).then(function (d) {
    renderResults(d.results || [], d.total);
  }).catch(function (e) { setStatus(String(e.message || e)); });
}

function renderResults(results, total) {
  var box = el('results');
  box.innerHTML = '';
  if (!results.length) { box.textContent = 'ничего не найдено'; return; }
  results.forEach(function (r) {
    var row = document.createElement('div');
    row.className = 'result' + (r.id === state.active ? ' active' : '');
    row.dataset.id = r.id;
    var left = document.createElement('div');
    var w = document.createElement('div');
    w.className = 'w';
    w.textContent = r.word;
    var m = document.createElement('div');
    m.className = 'meta';
    m.textContent = (r.accented || '') + ' · ↓' + r.parents + ' ↑' + r.children;
    left.appendChild(w); left.appendChild(m);
    var pos = document.createElement('span');
    pos.className = 'pos';
    pos.textContent = r.pos || '';
    row.appendChild(left); row.appendChild(pos);
    row.addEventListener('click', function () { loadGraph(r.id); });
    box.appendChild(row);
  });
  setStatus((total || 0) + ' лексем · показано ' + results.length);
}

function loadGraph(id) {
  state.active = id;
  Array.prototype.forEach.call(document.querySelectorAll('.result'), function (r) {
    r.classList.toggle('active', r.dataset.id === id);
  });
  return api('/api/graph', { id: id, dataset: state.dataset, depth: el('depth').value }).then(function (g) {
    buildGraph(g);
    var f = g.nodes.filter(function (n) { return n.id === g.focus; })[0] || {};
    el('info').innerHTML = '<b>' + escapeHtml(f.word || g.focus) + '</b> <span class="pos">' + (f.pos || '') + '</span><br>' +
      'родители: ' + (f.in || 0) + ' · производные: ' + (f.out || 0) + '<br>узлов: ' + g.nodes.length + ' · связей: ' + g.links.length;
  }).catch(function (e) { setStatus(String(e.message || e)); });
}

function escapeHtml(s) { return String(s).replace(/[&<>]/g, function (c) { return ({ '&': '&amp;', '<': '&lt;', '>': '&gt;' })[c]; }); }

function buildGraph(g) {
  var w = svg.clientWidth || 800, h = svg.clientHeight || 600;
  var byId = new Map();
  state.nodes = (g.nodes || []).map(function (n, i) {
    var a = (i / Math.max(1, g.nodes.length)) * Math.PI * 2;
    var node = { id: n.id, word: n.word, pos: n.pos, x: w / 2 + Math.cos(a) * 110, y: h / 2 + Math.sin(a) * 110, vx: 0, vy: 0, isParent: false };
    byId.set(n.id, node);
    return node;
  });
  state.focus = g.focus;
  state.links = (g.links || []).map(function (l) {
    var s = byId.get(l.source), t = byId.get(l.target);
    if (!s || !t) return null;
    s.isParent = true;
    return { source: s, target: t, rule: l.rule, kind: l.kind };
  }).filter(Boolean);
  state.alpha = 1;
  draw();
  runSim();
}

function draw() {
  while (svg.firstChild) svg.removeChild(svg.firstChild);
  state.links.forEach(function (l) {
    var line = document.createElementNS(svgNS, 'line');
    line.setAttribute('class', 'link' + (l.kind === 'interfix' ? ' rare' : ''));
    svg.appendChild(line);
    l.el = line;
  });
  state.nodes.forEach(function (n) {
    var g = document.createElementNS(svgNS, 'g');
    g.setAttribute('class', 'node' + (n.id === state.focus ? ' focus' : '') + (n.isParent ? ' parent' : ''));
    var c = document.createElementNS(svgNS, 'circle');
    c.setAttribute('r', n.id === state.focus ? 10 : 7);
    g.appendChild(c);
    var t = document.createElementNS(svgNS, 'text');
    t.setAttribute('dx', 11); t.setAttribute('dy', 4);
    t.textContent = n.word;
    g.appendChild(t);
    g.addEventListener('click', function (ev) { ev.stopPropagation(); loadGraph(n.id); });
    svg.appendChild(g);
    n.el = g;
  });
  update();
}

function update() {
  state.links.forEach(function (l) {
    l.el.setAttribute('x1', l.source.x.toFixed(1)); l.el.setAttribute('y1', l.source.y.toFixed(1));
    l.el.setAttribute('x2', l.target.x.toFixed(1)); l.el.setAttribute('y2', l.target.y.toFixed(1));
  });
  state.nodes.forEach(function (n) {
    n.el.setAttribute('transform', 'translate(' + n.x.toFixed(1) + ',' + n.y.toFixed(1) + ')');
  });
}

function step() {
  var w = svg.clientWidth || 800, h = svg.clientHeight || 600;
  var nodes = state.nodes, links = state.links, k = 70, a = state.alpha;
  for (var i = 0; i < nodes.length; i++) {
    for (var j = i + 1; j < nodes.length; j++) {
      var dx = nodes[i].x - nodes[j].x, dy = nodes[i].y - nodes[j].y;
      var d2 = dx * dx + dy * dy || 0.01, d = Math.sqrt(d2);
      var f = (k * k) / d2 * a;
      var fx = dx / d * f, fy = dy / d * f;
      nodes[i].x += fx; nodes[i].y += fy; nodes[j].x -= fx; nodes[j].y -= fy;
    }
  }
  links.forEach(function (l) {
    var dx = l.target.x - l.source.x, dy = l.target.y - l.source.y;
    var d = Math.sqrt(dx * dx + dy * dy) || 0.01;
    var f = (d * d) / k * 0.015 * a;
    var fx = dx / d * f, fy = dy / d * f;
    l.target.x -= fx; l.target.y -= fy; l.source.x += fx; l.source.y += fy;
  });
  nodes.forEach(function (n) {
    n.x += (w / 2 - n.x) * 0.012 * a;
    n.y += (h / 2 - n.y) * 0.012 * a;
    n.x = Math.max(20, Math.min(w - 20, n.x));
    n.y = Math.max(20, Math.min(h - 20, n.y));
  });
}

function runSim() {
  if (state.raf) cancelAnimationFrame(state.raf);
  var frames = 0;
  function loop() {
    step();
    state.alpha = Math.max(0.02, state.alpha * 0.985);
    update();
    frames++;
    if (frames < 400) state.raf = requestAnimationFrame(loop);
  }
  loop();
}

function enableDrag() {
  var drag = null;
  svg.addEventListener('mousedown', function (e) {
    var g = e.target.closest ? e.target.closest('.node') : null;
    if (!g) return;
    var node = state.nodes.filter(function (n) { return n.el === g; })[0];
    if (!node) return;
    drag = node;
    e.preventDefault();
  });
  svg.addEventListener('mousemove', function (e) {
    if (!drag) return;
    var r = svg.getBoundingClientRect();
    drag.x = e.clientX - r.left; drag.y = e.clientY - r.top;
    update();
  });
  window.addEventListener('mouseup', function () {
    if (drag) { drag = null; state.alpha = Math.max(state.alpha, 0.4); runSim(); }
  });
}

document.addEventListener('DOMContentLoaded', function () {
  el('q').addEventListener('input', scheduleSearch);
  el('q').addEventListener('keydown', function (e) {
    if (e.key === 'Enter') {
      var first = document.querySelector('.result');
      if (first) loadGraph(first.dataset.id);
    }
  });
  el('dataset').addEventListener('change', function () { state.dataset = el('dataset').value; search(el('q').value); });
  el('depth').addEventListener('change', function () { if (state.active) loadGraph(state.active); });
  enableDrag();
  initDatasets();
});
