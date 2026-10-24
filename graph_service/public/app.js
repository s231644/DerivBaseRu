'use strict';

var svgNS = 'http://www.w3.org/2000/svg';
var POS_COLORS = { noun: '#348674', adj: '#4b80b1', verb: '#8b70af', adv: '#aa861e', num: '#bf7242' };
var POS_LABELS = { noun: 'сущ', adj: 'прил', verb: 'гл', adv: 'нар', num: 'числ' };
var RELATION_COLORS = { pfx: '#477eb8', sfx: '#3a9272', postfix: '#2495a4', compound: '#cb8045', pfx_sfx: '#a06bb1', complex: '#7866b3', interfix: '#aa861e', conversion: '#b2708d', other: '#8793a3' };
var RELATION_LABELS = { pfx: 'Приставка', sfx: 'Суффикс', postfix: 'Постфикс', compound: 'Сложение', pfx_sfx: 'Приставка + суффикс', complex: 'Комплексное', interfix: 'Интерфикс', conversion: 'Конверсия', other: 'Другой тип' };
function relationKey(kind) {
  var key = String(kind || 'other').toLowerCase();
  key = ({ prefix: 'pfx', suffix: 'sfx', ptfx: 'postfix', pfxsfx: 'pfx_sfx', confix: 'pfx_sfx', conv: 'conversion' })[key] || key;
  return Object.prototype.hasOwnProperty.call(RELATION_COLORS, key) ? key : 'other';
}
var POS_FULL = { noun: 'Существительное', adj: 'Прилагательное', verb: 'Глагол', adv: 'Наречие', num: 'Числительное' };
var DATASET_LABELS = { '*': 'Все наборы данных', 'unified.jsonl': 'Общий граф', 'verb_pfx.jsonl': 'Глаголы · приставочные', 'verb_compound.jsonl': 'Глаголы · сложения', 'verb_sfx.jsonl': 'Глаголы · суффиксальные', 'verb_complex.jsonl': 'Глаголы · приставка + суффикс', 'num.jsonl': 'Числительные', 'adv.rare.verified.jsonl': 'Наречия · исключения', 'adv_pfx.final.clean.jsonl': 'Наречия · приставочные', 'adv_sfx.clean.jsonl': 'Наречия · суффиксальные', 'adv_g1.final.clean.jsonl': 'Наречия · группа 1', 'adv_g2.final.clean.jsonl': 'Наречия · группа 2', 'adv_g5.clean.jsonl': 'Наречия · сложения', 'adv_ymx.clean.jsonl': 'Наречия · усилительные' };
var affixCatalogue = { affixes: {}, rules: {} };
var datasetInfo = {}, searchVersion = 0, graphVersion = 0;
var state = { dataset: null, depth: 1, nodes: [], links: [], focus: null, raf: null, alpha: 1, active: null, bounds: { w: 800, h: 600 }, view: { x: 0, y: 0, w: 800, h: 600 } };

function el(id) { return document.getElementById(id); }
var svg = el('graph');

function posKey(pos) { return POS_COLORS[pos] ? pos : 'other'; }
function posColor(pos) { return POS_COLORS[pos] || '#8b98a5'; }
function posLabel(pos) { return POS_LABELS[pos] || (pos || ''); }
function linkLabel(link) {
  if (link.kind === 'compound') return 'сложение';
  var match = (link.rule || '').match(/\((.*?)\s*->/);
  if (link.kind === 'pfx' && match) return match[1].split('+')[0].trim().replace(/\d+$/, '') + '-';
  if (link.short && !/^(verb|noun|adj|adv|num)$/.test(link.short)) return link.short;
  return match ? match[1].trim() : (link.label || 'связь');
}
function escapeHtml(s) { return String(s).replace(/[&<>]/g, function (c) { return ({ '&': '&amp;', '<': '&lt;', '>': '&gt;' })[c]; }); }

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
function number(n) { return Number(n || 0).toLocaleString('ru-RU'); }
function updateDatasetInfo() {
  var info = datasetInfo[state.dataset] || {};
  el('datasetWords').textContent = number(info.lexemes);
  el('datasetEdges').textContent = number(info.edges);
}

/* ---------- view transform (zoom / pan) ---------- */
function applyView() {
  var v = state.view;
  svg.setAttribute('viewBox', [v.x, v.y, v.w, v.h].map(function (n) { return n.toFixed(2); }).join(' '));
}
function resetView() {
  state.bounds = { w: svg.clientWidth || 800, h: svg.clientHeight || 600 };
  state.view = { x: 0, y: 0, w: state.bounds.w, h: state.bounds.h };
  applyView();
}
function toGraph(clientX, clientY) {
  var r = svg.getBoundingClientRect();
  var v = state.view;
  return { x: v.x + (clientX - r.left) / r.width * v.w, y: v.y + (clientY - r.top) / r.height * v.h };
}
function zoomAt(cx, cy, factor) {
  var p = toGraph(cx, cy);
  var v = state.view;
  var nw = Math.max(80, Math.min(8000, v.w * factor));
  var scale = nw / v.w;
  v.x = p.x - (p.x - v.x) * scale;
  v.y = p.y - (p.y - v.y) * scale;
  v.w = nw; v.h = v.h * scale;
  applyView();
}

/* ---------- data + sidebar ---------- */
function initDatasets() {
  return api('/api/datasets').then(function (d) {
    var sel = el('dataset');
    sel.innerHTML = '';
    (d.datasets || []).forEach(function (ds) {
      var o = document.createElement('option');
      o.value = ds.name;
      o.textContent = DATASET_LABELS[ds.name] || ds.label || ds.name;
      datasetInfo[ds.name] = ds;
      sel.appendChild(o);
    });
    state.dataset = sel.value || null;
    updateDatasetInfo();
    var skipped = (d.skipped || []).map(function (s) {
      return s.name + ' (' + Math.round(s.bytes / 1048576) + ' МБ)';
    });
    if (!state.dataset) setStatus('нет .jsonl в каталоге данных');
    else if (skipped.length) setStatus('не показаны (слишком большие): ' + skipped.join(', '));
    if (state.dataset) {
      el('q').value = 'писать';
      return search('писать').then(function (results) {
        if (results.length) return loadGraph(results[0].id);
      });
    }
  }).catch(function (e) { setStatus('Не удалось загрузить данные: ' + e.message); });
}

var searchTimer = null;
function scheduleSearch() {
  clearTimeout(searchTimer);
  searchTimer = setTimeout(function () { search(el('q').value); }, 150);
}

function search(q) {
  var version = ++searchVersion;
  return api('/api/search', { q: q, dataset: state.dataset, limit: 60 }).then(function (d) {
    if (version !== searchVersion) return [];
    renderResults(d.results || [], d.total);
    return d.results || [];
  }).catch(function (e) { if (version === searchVersion) setStatus(String(e.message || e)); return []; });
}

function renderResults(results, total) {
  var box = el('results');
  box.innerHTML = '';
  el('resultCount').textContent = number(results.length) + (results.length === 60 ? '+' : '');
  if (!results.length) {
    box.innerHTML = '<div class="search-empty"><strong>Слово не найдено</strong>Попробуйте другую форму или выберите другой набор данных.</div>';
    setStatus('Нет результатов в выбранном наборе');
    return;
  }
  results.forEach(function (r) {
    var row = document.createElement('button');
    row.type = 'button';
    row.className = 'result' + (r.id === state.active ? ' active' : '');
    row.dataset.id = r.id;
    var left = document.createElement('div');
    var w = document.createElement('div');
    w.className = 'w';
    w.textContent = r.word;
    var m = document.createElement('div');
    m.className = 'meta';
    m.textContent = 'Основ: ' + r.parents + ' · производных: ' + r.children;
    left.appendChild(w); left.appendChild(m);
    var pos = document.createElement('span');
    pos.className = 'pos';
    pos.textContent = posLabel(r.pos);
    pos.style.borderColor = posColor(r.pos);
    row.appendChild(left); row.appendChild(pos);
    row.addEventListener('click', function () { loadGraph(r.id); });
    box.appendChild(row);
  });
  setStatus('Найдено ' + number(results.length) + (results.length === 60 ? ' или больше' : ''));
}

function loadGraph(id) {
  var version = ++graphVersion;
  el('stage').setAttribute('aria-busy', 'true');
  state.active = id;
  Array.prototype.forEach.call(document.querySelectorAll('.result'), function (r) {
    r.classList.toggle('active', r.dataset.id === id);
  });
  return api('/api/graph', { id: id, dataset: state.dataset, depth: el('depth').value }).then(function (g) {
    if (version !== graphVersion) return;
    el('emptyState').hidden = true;
    buildGraph(g);
    var f = g.nodes.filter(function (n) { return n.id === g.focus; })[0] || {};
    el('focusWord').textContent = f.word || g.focus;
    el('graphSummary').textContent = number(g.nodes.length) + ' вершин · ' + number(g.links.length) + ' связей';
    svg.setAttribute('aria-label', 'Связи слова ' + (f.word || g.focus));
    var comp = g.component ? '<div class="component-card"><strong>Компонента № ' +
      (g.component.index + 1) + '</strong>' + number(g.component.size) + ' связанных вершин</div>' : '';
    el('info').innerHTML = '<h2>' + escapeHtml(f.word || g.focus) + '</h2>' +
      '<span class="word-pos">' + escapeHtml(POS_FULL[f.pos] || f.pos || '') + '</span>' +
      '<div class="word-metrics"><div><strong>' + number(f.in) + '</strong><span>производящих основ</span></div>' +
      '<div><strong>' + number(f.out) + '</strong><span>производных слов</span></div></div>' +
      '<span class="eyebrow">В ЭТОМ ГРАФЕ</span>' +
      '<div class="detail-row"><span>Вершины</span><strong>' + number(g.nodes.length) + '</strong></div>' +
      '<div class="detail-row"><span>Связи</span><strong>' + number(g.links.length) + '</strong></div>' +
      '<div class="detail-row"><span>Глубина</span><strong>' + el('depth').value + '</strong></div>' + comp;
  }).catch(function (e) { if (version === graphVersion) setStatus(String(e.message || e)); })
    .finally(function () { if (version === graphVersion) el('stage').setAttribute('aria-busy', 'false'); });
}

/* ---------- graph ---------- */
function svgEl(name, attrs) {
  var e = document.createElementNS(svgNS, name);
  Object.keys(attrs || {}).forEach(function (k) { e.setAttribute(k, attrs[k]); });
  return e;
}

function buildGraph(g) {
  state.bounds = { w: svg.clientWidth || 800, h: svg.clientHeight || 600 };
  state.view = { x: 0, y: 0, w: state.bounds.w, h: state.bounds.h };
  applyView();
  var w = state.bounds.w, h = state.bounds.h;
  var byId = new Map();
  state.nodes = (g.nodes || []).map(function (n) {
    var node = { id: n.id, word: n.word, pos: n.pos, x: w / 2, y: h / 2, isParent: false };
    byId.set(n.id, node);
    return node;
  });
  state.focus = g.focus;
  state.links = (g.links || []).map(function (l) {
    var s = byId.get(l.source), t = byId.get(l.target);
    if (!s || !t) return null;
    s.isParent = true;
    return { source: s, target: t, rule: l.rule, kind: l.kind, label: linkLabel(l), pos: t.pos };
  }).filter(Boolean);
  state.layout = AffixLayout.layout(state.nodes, state.links, affixCatalogue);
  state.links.forEach(function (link) {
    var labels = link.affixVector.affixes.map(function (key) { return affixCatalogue.affixes[key] ? affixCatalogue.affixes[key].label : ''; }).filter(Boolean);
    if (labels.length) link.label = labels.join(' + ');
  });
  draw();
  renderLegend();
  fitView();
  update();
}

/* Fit the current layout into the viewport with a margin. */
function fitView() {
  if (!state.nodes.length) return;
  var minX = Infinity, minY = Infinity, maxX = -Infinity, maxY = -Infinity;
  state.nodes.forEach(function (n) {
    minX = Math.min(minX, n.x); maxX = Math.max(maxX, n.x);
    minY = Math.min(minY, n.y); maxY = Math.max(maxY, n.y);
  });
  var pad = 90;
  // Include word labels, not just circle centres, in the fitted viewport.
  state.nodes.forEach(function (n) { maxX = Math.max(maxX, n.x + n.word.length * 8 + 16); });
  var bw = Math.max(300, maxX - minX + pad * 2), bh = Math.max(240, maxY - minY + pad * 2);
  var b = state.bounds;
  var vw = bw, vh = bh;
  if (vw / vh > b.w / b.h) { vh = vw * (b.h / b.w); } else { vw = vh * (b.w / b.h); }
  state.view = { x: (minX + maxX) / 2 - vw / 2, y: (minY + maxY) / 2 - vh / 2, w: vw, h: vh };
  applyView();
}

function drawAffixAxes() {
  var maxX = 400, maxY = 400;
  state.nodes.forEach(function (n) { maxX = Math.max(maxX, n.x + n.word.length * 8 + 60); maxY = Math.max(maxY, n.y + 60); });
  var group = svgEl('g', { class: 'affix-axes', 'aria-hidden': 'true' });
  group.appendChild(svgEl('path', { d: 'M -55 ' + maxY + ' V -55 H ' + maxX }));
  for (var x = 0; x < maxX; x += 200) group.appendChild(svgEl('path', { class: 'axis-tick', d: 'M ' + x + ' -60 v 10' }));
  for (var y = 0; y < maxY; y += 200) group.appendChild(svgEl('path', { class: 'axis-tick', d: 'M -60 ' + y + ' h 10' }));
  var suffix = svgEl('text', { x: 12, y: -72 }); suffix.textContent = 'СУФФИКСЫ →'; group.appendChild(suffix);
  var prefix = svgEl('text', { x: -78, y: 12, transform: 'rotate(-90 -78 12)', 'text-anchor': 'end' }); prefix.textContent = 'ПРИСТАВКИ ↓'; group.appendChild(prefix);
  svg.appendChild(group);
}

function draw() {
  while (svg.firstChild) svg.removeChild(svg.firstChild);
  var defs = svgEl('defs', {});
  Object.keys(RELATION_COLORS).forEach(function (kind) {
    var marker = svgEl('marker', {
      id: 'arrow-' + kind, viewBox: '0 0 10 10', refX: '9', refY: '5',
      markerWidth: '6', markerHeight: '6', orient: 'auto-start-reverse',
    });
    marker.appendChild(svgEl('path', { d: 'M 0 0 L 10 5 L 0 10 z', fill: RELATION_COLORS[kind] }));
    defs.appendChild(marker);
  });
  svg.appendChild(defs);
  drawAffixAxes();

  var gLinks = svgEl('g', { class: 'links' });
  var gLabels = svgEl('g', { class: 'labels' });
  var gNodes = svgEl('g', { class: 'nodes' });
  state.links.forEach(function (l) {
    var key = relationKey(l.kind);
    var line = svgEl('line', { class: 'link relation-' + key + (l.layoutConflict ? ' layout-conflict' : ''), 'marker-end': 'url(#arrow-' + key + ')' });
    line.style.setProperty('--relation-color', RELATION_COLORS[key]);
    var title = svgEl('title');
    title.textContent = RELATION_LABELS[key] + ': ' + (l.rule || l.label) +
      '\nВектор аффиксов: (' + l.affixVector.x.toFixed(1) + '; ' + l.affixVector.y.toFixed(1) + ')' +
      (l.layoutConflict ? '\nРазные разборы расходятся: отклонение от вектора ' + l.layoutResidual.toFixed(1) : '') +
      (l.affixVector.ambiguous ? '\nВариант аффикса неоднозначен; использовано направление правила.' : '');
    line.appendChild(title);
    gLinks.appendChild(line);
    l.el = line;
    var text = svgEl('text', { class: 'edge-label', 'text-anchor': 'middle' });
    text.textContent = l.label;
    gLabels.appendChild(text);
    l.labelEl = text;
  });
  state.nodes.forEach(function (n) {
    n.positionLeader = svgEl('line', { class: 'position-leader', x1: n.semanticX, y1: n.semanticY, x2: n.x, y2: n.y });
    n.semanticPoint = svgEl('circle', { class: 'semantic-point', cx: n.semanticX, cy: n.semanticY, r: 2 });
    gLinks.appendChild(n.positionLeader);
    gLinks.appendChild(n.semanticPoint);
    var g = svgEl('g', { class: 'node pos-' + posKey(n.pos) + (n.layoutRoot ? ' layout-root' : '') + (n.id === state.focus ? ' focus' : ''),
      tabindex: '0', role: 'button', 'aria-label': 'Показать связи: ' + n.word });
    var nodeTitle = svgEl('title');
    nodeTitle.textContent = n.word + (n.layoutRoot ? (n.rootUncertain ? '\nОпорная точка замкнутой цепи' : '\nОснова в показанном графе') : '') + '\nАффиксная позиция: (' + n.semanticX.toFixed(1) + '; ' + n.semanticY.toFixed(1) + ')';
    g.appendChild(nodeTitle);
    if (n.layoutRoot) g.appendChild(svgEl('circle', { class: 'base-halo', r: 16 }));
    g.appendChild(svgEl('circle', { r: n.id === state.focus ? 10 : 7 }));
    var t = svgEl('text', { dx: 11, dy: 4 });
    t.textContent = n.word;
    g.appendChild(t);
    g.addEventListener('click', function (ev) { ev.stopPropagation(); if (!state.moved) loadGraph(n.id); });
    g.addEventListener('keydown', function (ev) {
      if (ev.key === 'Enter' || ev.key === ' ') { ev.preventDefault(); loadGraph(n.id); }
    });
    gNodes.appendChild(g);
    n.el = g;
  });
  svg.appendChild(gLinks);
  svg.appendChild(gLabels);
  svg.appendChild(gNodes);
  svg.classList.toggle('hide-labels', !el('labels').checked);
  update();
}

function shorten(s, t, r) {
  var dx = t.x - s.x, dy = t.y - s.y;
  var d = Math.sqrt(dx * dx + dy * dy) || 1;
  return { x: t.x - dx / d * r, y: t.y - dy / d * r };
}

function update() {
  state.links.forEach(function (l) {
    var end = shorten(l.source, l.target, l.target.id === state.focus ? 12 : 9);
    l.el.setAttribute('x1', l.source.x.toFixed(1)); l.el.setAttribute('y1', l.source.y.toFixed(1));
    l.el.setAttribute('x2', end.x.toFixed(1)); l.el.setAttribute('y2', end.y.toFixed(1));
    var mx = (l.source.x + l.target.x) / 2, my = (l.source.y + l.target.y) / 2 - 3;
    var ang = Math.atan2(l.target.y - l.source.y, l.target.x - l.source.x) * 180 / Math.PI;
    if (ang > 90) ang -= 180; else if (ang < -90) ang += 180;
    l.labelEl.setAttribute('x', mx.toFixed(1));
    l.labelEl.setAttribute('y', my.toFixed(1));
    l.labelEl.setAttribute('transform', 'rotate(' + ang.toFixed(1) + ' ' + mx.toFixed(1) + ' ' + my.toFixed(1) + ')');
  });
  state.nodes.forEach(function (n) {
    var shifted = Math.hypot(n.x - n.semanticX, n.y - n.semanticY) > 1;
    n.positionLeader.setAttribute('visibility', shifted ? 'visible' : 'hidden');
    n.semanticPoint.setAttribute('visibility', shifted ? 'visible' : 'hidden');
    n.positionLeader.setAttribute('x2', n.x); n.positionLeader.setAttribute('y2', n.y);
    n.el.setAttribute('transform', 'translate(' + n.x.toFixed(1) + ',' + n.y.toFixed(1) + ')');
  });
}

function renderLegend() {
  var pos = [];
  state.nodes.forEach(function (n) { if (pos.indexOf(n.pos) < 0) pos.push(n.pos); });
  var nodes = pos.map(function (p) {
    return '<span><i style="background:' + posColor(p) + '"></i>' + escapeHtml(posLabel(p)) + '</span>';
  }).join('');
  var present = new Set(state.links.map(function (link) { return relationKey(link.kind); }));
  var links = Object.keys(RELATION_COLORS).filter(function (key) { return present.has(key); }).map(function (key) {
    return '<span><i class="relation-key" style="color:' + RELATION_COLORS[key] + '"></i>' + RELATION_LABELS[key] + '</span>';
  }).join('');
  var keys = Array.from(new Set(state.links.flatMap(function (link) { return link.affixVector.affixes; }))).sort();
  el('affixVectorList').innerHTML = keys.map(function (key) {
    var affix = affixCatalogue.affixes[key];
    if (!affix) return '';
    var length = Math.hypot(affix.x, affix.y);
    return '<div class="affix-vector-row"><span>' + escapeHtml(affix.label) + '</span><svg viewBox="0 0 40 28" aria-hidden="true"><line x1="3" y1="3" x2="' + (3 + affix.x / length * 24).toFixed(1) + '" y2="' + (3 + affix.y / length * 24).toFixed(1) + '" stroke="' + (RELATION_COLORS[affix.category] || RELATION_COLORS.other) + '" stroke-width="2"/></svg><code>(' + Math.round(affix.x) + '; ' + Math.round(affix.y) + ')</code></div>';
  }).join('');
  el('legend').innerHTML = '<div class="legend-group"><b>Вершины</b>' + nodes + '</div>' +
    (links ? '<div class="legend-group"><b>Связи</b>' + links + '</div>' : '');
}

/* ---------- interaction: drag nodes, pan, zoom ---------- */
function enableInteraction() {
  var drag = null, pan = null;

  svg.addEventListener('pointerdown', function (e) {
    if (e.button !== 0) return;
    var g = e.target.closest ? e.target.closest('.node') : null;
    state.moved = false;
    if (g) {
      var node = state.nodes.filter(function (n) { return n.el === g; })[0];
      if (!node) return;
      node.pinned = true;
      drag = { node: node, ox: toGraph(e.clientX, e.clientY).x - node.x, oy: toGraph(e.clientX, e.clientY).y - node.y };
      svg.style.cursor = 'grabbing';
    } else {
      pan = { x: e.clientX, y: e.clientY, vx: state.view.x, vy: state.view.y };
      svg.style.cursor = 'grabbing';
    }
    e.preventDefault();
  });

  svg.addEventListener('pointermove', function (e) {
    if (drag) {
      var p = toGraph(e.clientX, e.clientY);
      drag.node.x = p.x - drag.ox; drag.node.y = p.y - drag.oy;
      state.moved = true;
      update();
    } else if (pan) {
      var r = svg.getBoundingClientRect();
      var v = state.view;
      v.x = pan.vx - (e.clientX - pan.x) / r.width * v.w;
      v.y = pan.vy - (e.clientY - pan.y) / r.height * v.h;
      state.moved = true;
      applyView();
    }
  });

  function endDrag() {
    if (drag) { drag = null; svg.style.cursor = 'grab'; }
    if (pan) { pan = null; svg.style.cursor = 'grab'; }
  }
  window.addEventListener('pointerup', endDrag);
  window.addEventListener('pointercancel', endDrag);

  svg.addEventListener('wheel', function (e) {
    e.preventDefault();
    zoomAt(e.clientX, e.clientY, e.deltaY < 0 ? 0.88 : 1.14);
  }, { passive: false });

  svg.addEventListener('dblclick', function (e) {
    if (!(e.target.closest && e.target.closest('.node'))) resetView();
  });

  el('zoomIn').addEventListener('click', function () { var r = svg.getBoundingClientRect(); zoomAt(r.left + r.width / 2, r.top + r.height / 2, 0.8); });
  el('zoomOut').addEventListener('click', function () { var r = svg.getBoundingClientRect(); zoomAt(r.left + r.width / 2, r.top + r.height / 2, 1.25); });
  el('zoomReset').addEventListener('click', fitView);
}

document.addEventListener('DOMContentLoaded', function () {
  el('q').addEventListener('input', scheduleSearch);
  el('q').addEventListener('keydown', function (e) {
    if (e.key === 'Enter') {
      var first = document.querySelector('.result');
      if (first) loadGraph(first.dataset.id);
    }
  });
  el('labels').addEventListener('change', function () {
    svg.classList.toggle('hide-labels', !el('labels').checked);
  });
  el('dataset').addEventListener('change', function () {
    state.dataset = el('dataset').value;
    updateDatasetInfo();
    ++graphVersion;
    state.active = null;
    state.nodes = []; state.links = [];
    svg.replaceChildren();
    el('legend').replaceChildren();
    el('stage').setAttribute('aria-busy', 'false');
    el('emptyState').hidden = false;
    el('focusWord').textContent = 'Выберите слово';
    el('graphSummary').textContent = 'Исследуйте словообразование';
    el('info').innerHTML = '<div class="inspector-placeholder">Выберите слово</div><p>Найдите лексему в этом наборе данных.</p>';
    search(el('q').value);
  });
  el('depth').addEventListener('change', function () { if (state.active) loadGraph(state.active); });
  document.querySelectorAll('[data-example]').forEach(function (button) {
    button.addEventListener('click', function () {
      el('q').value = button.dataset.example;
      clearTimeout(searchTimer);
      search(el('q').value).then(function (results) { if (results.length) loadGraph(results[0].id); });
    });
  });
  document.addEventListener('keydown', function (event) {
    if (event.key === '/' && !/INPUT|TEXTAREA|SELECT/.test(document.activeElement.tagName)) {
      event.preventDefault(); el('q').focus();
    }
    if (event.key === 'Escape' && document.activeElement === el('q')) {
      el('q').value = ''; scheduleSearch();
    }
  });
  var resizeTimer;
  window.addEventListener('resize', function () {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(function () {
      state.bounds = { w: svg.clientWidth || 800, h: svg.clientHeight || 600 };
      if (state.nodes.length) fitView();
    }, 100);
  });
  enableInteraction();
  fetch('/affix-vectors.json?v=' + encodeURIComponent(document.querySelector('script[src*="app.js"]').src.split('v=')[1] || '1'))
    .then(function (r) { if (!r.ok) throw new Error('Не удалось загрузить векторы аффиксов'); return r.json(); })
    .then(function (catalogue) { affixCatalogue = catalogue; return initDatasets(); })
    .catch(function (e) { setStatus(e.message); });
});
