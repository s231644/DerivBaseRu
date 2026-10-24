'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const L = require('../graph_service/public/affix-layout.js');
const catalogue = require('../graph_service/public/affix-vectors.json');
const rules = [
  { rule_id: 'r1(на + verb -> verb)', info: 'PFX' },
  { rule_id: 'r2(verb + ива(ть)/ва(ть)/а3(ть) -> verb)', info: 'SFX' },
  { rule_id: 'r3(на + verb + ива(ть) -> verb)', info: 'PFX,SFX' },
  { rule_id: 'r4(verb + ся -> verb)', info: 'PTFX' },
];
const C = L.buildCatalogue(rules);
const node = word => ({ id: word, word });
const edge = (source, target, rule, kind) => ({ source, target, rule: rules[rule].rule_id, kind });
const close = (a, b) => assert.ok(Math.abs(a - b) < 0.01, `${a} != ${b}`);

test('the global catalogue assigns a unique stable vector to every affix', () => {
  const vectors = Object.values(catalogue.affixes);
  assert.ok(vectors.length > 400);
  assert.equal(new Set(vectors.map(v => `${v.x}:${v.y}`)).size, vectors.length);
  for (const v of vectors) {
    assert.ok(v.x > 0 && v.y > 0);
    if (v.category === 'pfx') assert.ok(v.y > v.x * 3);
    if (v.category === 'sfx') assert.ok(v.x > v.y * 3);
  }
  assert.deepEqual(L.buildCatalogue(rules), L.buildCatalogue([...rules].reverse()));
});

test('affix sums form a commutative diamond independent of focus and input order', () => {
  const nodes = ['писать', 'написать', 'писывать', 'написывать'].map(node);
  const edges = [edge('писать', 'написать', 0, 'pfx'), edge('писать', 'писывать', 1, 'sfx'),
    edge('написать', 'написывать', 1, 'sfx'), edge('писывать', 'написывать', 0, 'pfx')];
  const result = L.layout(nodes, edges, C);
  assert.deepEqual(result.roots, ['писать']);
  assert.ok(result.residual < 0.01);
  const p = L.edgeVector(edges[0], C), s = L.edgeVector(edges[1], C);
  const last = nodes.find(n => n.id === 'написывать');
  close(last.semanticX, p.x + s.x); close(last.semanticY, p.y + s.y);
  const confix = L.edgeVector(edge('писать', 'написывать', 2, 'pfx_sfx'), C);
  close(confix.x, p.x + s.x); close(confix.y, p.y + s.y);
  const reversed = nodes.map(n => node(n.word)).reverse();
  L.layout(reversed, [...edges].reverse(), C);
  for (const n of reversed) {
    const original = nodes.find(o => o.id === n.id);
    close(n.semanticX, original.semanticX); close(n.semanticY, original.semanticY);
    close(n.x, original.x); close(n.y, original.y);
  }
});

test('alternative suffixes and postfixes are selected rather than summed', () => {
  const iva = L.edgeVector(edge('писать', 'писывать', 1, 'sfx'), C);
  const va = L.edgeVector(edge('быть', 'бывать', 1, 'sfx'), C);
  assert.deepEqual(iva.affixes, ['sfx:ива']); assert.deepEqual(va.affixes, ['sfx:ва']);
  const postfix = L.edgeVector(edge('мыть', 'мыться', 3, 'postfix'), C);
  assert.deepEqual(postfix.affixes, ['postfix:ся']);
  const compound = L.descriptor('r5(num + сто -> num)', 'COMPOUND');
  assert.equal(compound.length, 1); assert.equal(compound[0][0].category, 'compound');
});

test('cycles, self loops, isolated nodes and contradictory analyses stay finite', () => {
  const nodes = ['а', 'наа', 'изолированный'].map(node);
  const edges = [edge('а', 'наа', 0, 'pfx'), edge('наа', 'а', 1, 'sfx'), edge('изолированный', 'изолированный', 0, 'pfx')];
  const result = L.layout(nodes, edges, C);
  assert.equal(result.cycles, 2);
  assert.equal(result.roots.length, 2);
  for (const n of nodes) assert.ok(Number.isFinite(n.x + n.y + n.semanticX + n.semanticY));
});

test('500 coincident derivations keep semantic vectors and separate all label boxes', () => {
  const nodes = [node('основа'), ...Array.from({ length: 499 }, (_, i) => node('наслово_' + i))];
  const edges = nodes.slice(1).map(n => edge('основа', n.id, 0, 'pfx'));
  L.layout(nodes, edges, C);
  for (const n of nodes.slice(1)) {
    close(n.semanticX, nodes[1].semanticX); close(n.semanticY, nodes[1].semanticY);
    assert.ok(n.x >= 0 && n.y >= 0);
  }
  const boxes = nodes.map(n => ({ x: n.x - 13, y: n.y - 18, w: Math.max(65, n.word.length * 8 + 34), h: 38 }));
  for (let i = 0; i < boxes.length; i++) for (let j = i + 1; j < boxes.length; j++) {
    const a = boxes[i], b = boxes[j];
    assert.ok(!(a.x < b.x + b.w && a.x + a.w > b.x && a.y < b.y + b.h && a.y + a.h > b.y), `${i}/${j} overlap`);
  }
});


test('inconsistent derivations are marked and semantic coordinates stay in the root quadrant', () => {
  const nodes = ['писать', 'написать', 'писывать'].map(node);
  const edges = [edge('писать', 'написать', 0, 'pfx'), edge('писать', 'писывать', 1, 'sfx'),
    edge('написать', 'писывать', 0, 'pfx')];
  const result = L.layout(nodes, edges, C);
  assert.ok(result.residual > 60);
  assert.ok(edges.some(e => e.layoutConflict));
  assert.ok(nodes.every(n => n.semanticX >= 0 && n.semanticY >= 0));
});

test('лечь/ложить/полечь/положить remain a rendered parallelogram despite noise and collisions', () => {
  const words = ['лечь', 'ложить', 'полечь', 'положить', 'помеха'];
  const nodes = words.map(node);
  const prefix = 'rule871(по + verb -> verb)', suffix = 'rule846(verb + и2(ть) -> verb)';
  const edges = [
    ['лечь', 'полечь', prefix, 'pfx'], ['ложить', 'положить', prefix, 'pfx'],
    ['лечь', 'ложить', suffix, 'sfx'], ['полечь', 'положить', suffix, 'sfx'],
    ['полечь', 'ложить', prefix, 'pfx'], // contradictory extra analysis
    ['лечь', 'помеха', suffix, 'sfx'], // colliding label
  ].map(([source, target, rule, kind]) => ({ source, target, rule, kind }));
  L.layout(nodes, edges, catalogue);
  const [a, b, c, d] = nodes;
  const p = L.edgeVector(edges[0], catalogue), s = L.edgeVector(edges[2], catalogue);
  for (const [x, y] of [['x', 'y'], ['semanticX', 'semanticY']]) {
    close(c[x] - a[x], p.x); close(c[y] - a[y], p.y);
    close(b[x] - a[x], s.x); close(b[y] - a[y], s.y);
    close(a[x] + d[x], b[x] + c[x]); close(a[y] + d[y], b[y] + c[y]);
  }
  assert.ok(edges[4].layoutConflict);
  const reversed = words.map(node).reverse();
  L.layout(reversed, [...edges].reverse(), catalogue);
  for (const n of reversed) { const o = nodes.find(o => o.id === n.id); close(n.x, o.x); close(n.y, o.y); }
});
