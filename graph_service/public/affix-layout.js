/* Shared, dependency-free affix geometry: browser + Node catalogue/tests. */
(function (root, factory) {
  if (typeof module === 'object' && module.exports) module.exports = factory();
  else root.AffixLayout = factory();
})(typeof globalThis !== 'undefined' ? globalThis : this, function () {
  'use strict';
  function cmp(a, b) { return a < b ? -1 : a > b ? 1 : 0; }
  function kind(value) {
    var k = String(value || '').toLowerCase();
    return ({ prefix: 'pfx', suffix: 'sfx', ptfx: 'postfix', confix: 'pfx_sfx', pfxsfx: 'pfx_sfx' })[k] || k;
  }
  function norm(word) { return String(word || '').toLowerCase().replace(/[\u0300\u0301]/g, '').replace(/ё/g, 'е'); }
  function hash(text) {
    var h = 2166136261;
    for (var i = 0; i < text.length; i++) h = Math.imul(h ^ text.charCodeAt(i), 16777619);
    return h >>> 0;
  }
  function vector(key, category, salt) {
    var h = hash(key + ':' + (salt || 0)), h2 = hash('length:' + key + ':' + (salt || 0));
    var ranges = { pfx: [73, 87, 310, 450], sfx: [3, 18, 330, 470],
      postfix: [27, 39, 230, 320], compound: [43, 57, 350, 440],
      interfix: [35, 43, 260, 330], conversion: [20, 28, 280, 350], other: [38, 48, 300, 380] };
    var r = ranges[category] || ranges.other;
    var angle = (r[0] + (r[1] - r[0]) * h / 4294967295) * Math.PI / 180;
    var length = r[2] + (r[3] - r[2]) * h2 / 4294967295;
    return { x: Number((Math.cos(angle) * length).toFixed(6)), y: Number((Math.sin(angle) * length).toFixed(6)) };
  }
  function descriptor(rule, info) {
    var arrow = rule.indexOf('->'), opening = rule.indexOf('(');
    var category = kind(info);
    if (arrow < 0 || opening < 0) return [];
    var body = rule.slice(opening + 1, arrow).replace(/\[[^\]]*\]/g, '');
    var tokens = body.split('+').map(function (t) { return t.trim(); }).filter(Boolean);
    var pos = /^(noun|adj|verb|adv|num|pron|part|intj|prep|conj)$/;
    var first = tokens.findIndex(function (t) { return pos.test(t); });
    var groups = [];
    tokens.forEach(function (token, index) {
      if (/compound/i.test(info) && !/(SFX|PFX|PTFX)/i.test(info)) return;
      if (pos.test(token) || /^(ITFX|GEN|INFL|CONV)/.test(token)) return;
      var cat = /^(ся|сь)$/.test(token) || category === 'postfix' ? 'postfix' : index < first ? 'pfx' : 'sfx';
      var alternatives = token.split('/').map(function (part) {
        var canonical = norm(part).replace(/\([^)]*\)/g, '').replace(/[\s\[\]]/g, '');
        var surface = canonical.replace(/[0-9*]/g, '');
        if (/^0/.test(canonical)) surface = '';
        var display = canonical.replace(/^0/, '∅').replace(/[0-9]/g, function (digit) { return '₀₁₂₃₄₅₆₇₈₉'[Number(digit)]; });
        return { key: cat + ':' + canonical, category: cat, surface: surface,
          label: cat === 'pfx' ? display + '-' : '-' + (display || '∅') + (cat === 'postfix' ? '' : '-') };
      });
      if (alternatives.length) groups.push(alternatives);
    });
    if (/compound/i.test(info) || category === 'compound') {
      groups.unshift([{ key: 'compound:' + rule.slice(0, opening), category: 'compound', label: 'сложение', surface: '' }]);
    }
    if (!groups.length) {
      var cat = /conv/i.test(info) ? 'conversion' : /interfix/i.test(info) ? 'interfix' : category || 'other';
      groups.push([{ key: cat + ':' + rule.slice(0, opening), category: cat, label: cat, surface: '' }]);
    }
    return groups;
  }
  function buildCatalogue(rules) {
    var entries = {}, definitions = {};
    rules.slice().sort(function (a, b) { return cmp(a.rule_id, b.rule_id); }).forEach(function (rule) {
      if (!rule.rule_id || !rule.rule_id.includes('->')) return;
      var groups = descriptor(rule.rule_id, rule.info || 'other');
      // A rule's short label is editorial metadata; it must not change the
      // canonical affix key, matching surface, or stable geometry.
      if (rule.info === 'SFX' && typeof rule.short_id === 'string' &&
          groups.length === 1 && groups[0].length === 1) {
        groups[0][0].label = rule.short_id.replace(/[0-9]/g, function (digit) { return '₀₁₂₃₄₅₆₇₈₉'[Number(digit)]; });
      }
      definitions[rule.rule_id] = groups;
      groups.forEach(function (group) { group.forEach(function (affix) { entries[affix.key] = affix; }); });
    });
    var used = new Set();
    Object.keys(entries).sort(cmp).forEach(function (key) {
      var salt = 0, v;
      do { v = vector(key, entries[key].category, salt++); } while (used.has(v.x + ',' + v.y));
      used.add(v.x + ',' + v.y);
      entries[key].x = v.x; entries[key].y = v.y;
    });
    return { schema: 1, affixes: entries, rules: definitions };
  }
  function endpoint(link, side) { return typeof link[side] === 'object' ? link[side].word || link[side].id.split('|')[0] : String(link[side]).split('|')[0]; }
  function edgeVector(link, catalogue) {
    catalogue = catalogue || { affixes: {}, rules: {} };
    var groups = catalogue.rules[link.rule] || descriptor(link.rule || '', kind(link.kind));
    if (!groups.length) groups = [[{ key: 'relation:' + kind(link.kind), category: kind(link.kind), label: link.kind || 'связь', surface: '' }]];
    var target = norm(endpoint(link, 'target')).replace(/(?:ся|сь)$/, '');
    // Rule labels put inflectional endings in parentheses; strip them for matching.
    var stem = target.replace(/(?:ть|ти|чь)$/, '');
    var sourceWord = norm(endpoint(link, 'source')).replace(/(?:ся|сь)$/, '');
    var addedPrefix = '';
    var result = { x: 0, y: 0, affixes: [], ambiguous: false };
    groups.forEach(function (group) {
      var ranked = group.slice().sort(function (a, b) { return b.surface.length - a.surface.length || cmp(a.key, b.key); });
      var matches = ranked.filter(function (a) {
        if (!a.surface) return false;
        if (a.category === 'pfx') return target.startsWith(a.surface);
        return stem.endsWith(a.surface) || target.endsWith(a.surface) || (a.surface === 'ива' && stem.endsWith('ыва'));
      });
      var va = ranked.find(function (a) { return a.category === 'sfx' && a.surface === 'ва'; });
      var suffixTarget = addedPrefix && target.startsWith(addedPrefix) ? target.slice(addedPrefix.length) : target;
      var chosen = va && sourceWord.endsWith('ть') && suffixTarget === sourceWord.slice(0, -2) + 'вать' ? va : matches[0] || ranked[0];
      if (chosen.category === 'pfx') addedPrefix += chosen.surface;
      if (ranked.length > 1 && !matches.length) result.ambiguous = true;
      var v = catalogue.affixes[chosen.key] || vector(chosen.key, chosen.category);
      result.x += v.x; result.y += v.y;
      result.affixes.push(chosen.key);
    });
    return result;
  }
  function layout(inputNodes, inputLinks, catalogue) {
    var nodes = inputNodes.slice().sort(function (a, b) { return cmp(a.id, b.id); });
    var byId = new Map(nodes.map(function (n) { return [n.id, n]; }));
    var edges = inputLinks.map(function (e) {
      var source = byId.get(typeof e.source === 'object' ? e.source.id : e.source);
      var target = byId.get(typeof e.target === 'object' ? e.target.id : e.target);
      return source && target ? { source: source, target: target, vector: edgeVector(e, catalogue), original: e } : null;
    }).filter(Boolean).sort(function (a, b) { return cmp(a.source.id + ':' + a.target.id + ':' + a.original.rule, b.source.id + ':' + b.target.id + ':' + b.original.rule); });
    var incoming = new Map(), outgoing = new Map(), neighbours = new Map();
    nodes.forEach(function (n) { incoming.set(n.id, []); outgoing.set(n.id, []); neighbours.set(n.id, []); });
    edges.forEach(function (e) { incoming.get(e.target.id).push(e); outgoing.get(e.source.id).push(e); neighbours.get(e.source.id).push(e); neighbours.get(e.target.id).push(e); e.original.affixVector = e.vector; });
    // Tarjan SCCs identify real source components even if the data contains cycles.
    var index = 0, stack = [], components = [], number = new Map(), low = new Map(), onStack = new Set();
    function visit(n) {
      number.set(n.id, index); low.set(n.id, index++); stack.push(n); onStack.add(n.id);
      outgoing.get(n.id).forEach(function (e) {
        var t = e.target;
        if (!number.has(t.id)) { visit(t); low.set(n.id, Math.min(low.get(n.id), low.get(t.id))); }
        else if (onStack.has(t.id)) low.set(n.id, Math.min(low.get(n.id), number.get(t.id)));
      });
      if (low.get(n.id) === number.get(n.id)) {
        var component = [], member;
        do { member = stack.pop(); onStack.delete(member.id); component.push(member); } while (member !== n);
        components.push(component);
      }
    }
    nodes.forEach(function (n) { if (!number.has(n.id)) visit(n); });
    var componentOf = new Map(), hasParent = new Set();
    components.forEach(function (group, i) { group.forEach(function (n) { componentOf.set(n.id, i); }); });
    edges.forEach(function (e) { if (componentOf.get(e.source.id) !== componentOf.get(e.target.id)) hasParent.add(componentOf.get(e.target.id)); });
    var roots = [];
    nodes.forEach(function (n) { n.layoutRoot = false; n.rootUncertain = false; });
    components.forEach(function (group, i) {
      if (hasParent.has(i)) return;
      group.sort(function (a, b) { return (a.word || a.id).length - (b.word || b.id).length || cmp(a.id, b.id); });
      group[0].layoutRoot = true;
      group[0].rootUncertain = group.length > 1 || incoming.get(group[0].id).length > 0;
      roots.push(group[0]);
    });
    roots.sort(function (a, b) { return cmp(a.id, b.id); });
    var placed = new Set(), queue = [], anchorX = 0;
    roots.forEach(function (n) { n.semanticX = anchorX; n.semanticY = 0; anchorX += Math.max(380, (n.word || n.id).length * 9 + 140); placed.add(n.id); queue.push(n); });
    for (var qi = 0; qi < queue.length; qi++) {
      var n = queue[qi];
      neighbours.get(n.id).forEach(function (e) {
        var forward = e.source === n, other = forward ? e.target : e.source;
        if (placed.has(other.id)) return;
        other.semanticX = n.semanticX + (forward ? e.vector.x : -e.vector.x);
        other.semanticY = n.semanticY + (forward ? e.vector.y : -e.vector.y);
        placed.add(other.id); queue.push(other);
      });
    }
    // Anchored least squares: reconcile alternative derivations instead of
    // choosing a path according to the selected/focused word.
    for (var iteration = 0; iteration < 240; iteration++) {
      var maxChange = 0;
      nodes.forEach(function (n) {
        if (n.layoutRoot) return;
        var around = neighbours.get(n.id), x = 0, y = 0;
        around.forEach(function (e) {
          var forward = e.target === n, other = forward ? e.source : e.target;
          x += other.semanticX + (forward ? e.vector.x : -e.vector.x);
          y += other.semanticY + (forward ? e.vector.y : -e.vector.y);
        });
        if (!around.length) return;
        x = Math.max(0, x / around.length); y = Math.max(0, y / around.length);
        maxChange = Math.max(maxChange, Math.abs(x - n.semanticX), Math.abs(y - n.semanticY));
        n.semanticX = x; n.semanticY = y;
      });
      if (maxChange < 0.001) break;
    }
    // Opposite sides of a commutative diamond are hard constraints. Merge
    // compatible diamonds into rigid components, keeping inconsistent extra
    // analyses as soft constraints rather than bending the parallelogram.
    var rigid = new Map(), offsets = new Map();
    nodes.forEach(function (n) { rigid.set(n.id, [n]); offsets.set(n.id, { x: 0, y: 0 }); });
    function signature(e) { return e.vector.affixes.join('+'); }
    function join(e) {
      var a = rigid.get(e.source.id), b = rigid.get(e.target.id);
      var u = offsets.get(e.source.id), v = offsets.get(e.target.id);
      if (a === b) return;
      var dx = u.x + e.vector.x - v.x, dy = u.y + e.vector.y - v.y;
      b.forEach(function (n) {
        var o = offsets.get(n.id); o.x += dx; o.y += dy;
        rigid.set(n.id, a); a.push(n);
      });
    }
    nodes.forEach(function (n) {
      var paths = new Map();
      outgoing.get(n.id).forEach(function (first) {
        outgoing.get(first.target.id).forEach(function (second) {
          if (new Set([n.id, first.target.id, second.target.id]).size !== 3) return;
          var key = second.target.id + ':' + signature(second) + ':' + signature(first);
          var opposite = paths.get(key);
          if (opposite && opposite[0].target !== first.target && signature(first) !== signature(second)) {
            // Check all four constraints before merging; incompatible cycles
            // must never silently distort an already accepted rigid component.
            var candidates = [opposite[0], opposite[1], first, second];
            var local = new Map(), valid = true;
            function collect(node, x, y) {
              var group = rigid.get(node.id), o = offsets.get(node.id);
              var origin = { x: x - o.x, y: y - o.y };
              if (local.has(group)) {
                var prior = local.get(group);
                if (Math.hypot(prior.x - origin.x, prior.y - origin.y) > 0.01) valid = false;
              } else local.set(group, origin);
            }
            collect(n, 0, 0);
            collect(first.target, first.vector.x, first.vector.y);
            collect(opposite[0].target, opposite[0].vector.x, opposite[0].vector.y);
            collect(second.target, first.vector.x + second.vector.x, first.vector.y + second.vector.y);
            if (valid) candidates.forEach(join);
          }
          paths.set(second.target.id + ':' + signature(first) + ':' + signature(second), [first, second]);
        });
      });
    });
    var groups = Array.from(new Set(nodes.map(function (n) { return rigid.get(n.id); })));
    groups.forEach(function (group) {
      var anchor = group.find(function (n) { return n.layoutRoot; });
      var x = 0, y = 0;
      (anchor ? [anchor] : group).forEach(function (n) {
        var o = offsets.get(n.id); x += n.semanticX - o.x; y += n.semanticY - o.y;
      });
      if (!anchor) { x /= group.length; y /= group.length; }
      x = Math.max(x, -Math.min.apply(null, group.map(function (n) { return offsets.get(n.id).x; })));
      y = Math.max(y, -Math.min.apply(null, group.map(function (n) { return offsets.get(n.id).y; })));
      group.forEach(function (n) { var o = offsets.get(n.id); n.semanticX = x + o.x; n.semanticY = y + o.y; });
    });
    // Keep semantic coordinates; spread rendered nodes/labels into nearby slots.
    // Grid-indexed label rectangles make this practical at the 500-node API cap.
    var cells = new Map(), minX = Math.min.apply(null, roots.map(function (n) { return n.semanticX; }).concat([0]));
    function box(n, x, y) { return { x: x - 13, y: y - 18, w: Math.max(65, (n.word || n.id).length * 8 + 34), h: 38 }; }
    function keys(b) {
      var result = [];
      for (var x = Math.floor(b.x / 80); x <= Math.floor((b.x + b.w) / 80); x++)
        for (var y = Math.floor(b.y / 50); y <= Math.floor((b.y + b.h) / 50); y++) result.push(x + ':' + y);
      return result;
    }
    function overlaps(b) {
      return keys(b).some(function (k) { return (cells.get(k) || []).some(function (o) { return b.x < o.x + o.w && b.x + b.w > o.x && b.y < o.y + o.h && b.y + b.h > o.y; }); });
    }
    groups.sort(function (a, b) {
      function root(g) { return g.some(function (n) { return n.layoutRoot; }); }
      return Number(root(b)) - Number(root(a)) || a[0].semanticY - b[0].semanticY || a[0].semanticX - b[0].semanticX || cmp(a[0].id, b[0].id);
    }).forEach(function (group) {
      function fits(dx, dy) {
        return group.every(function (n) { return n.semanticX + dx >= minX && n.semanticY + dy >= 0 && !overlaps(box(n, n.semanticX + dx, n.semanticY + dy)); });
      }
      var shift = [0, 0], found = fits(0, 0);
      for (var radius = 1; !found && radius < 80; radius++) {
        var slots = [];
        for (var dx = -radius; dx <= radius; dx++) for (var dy = -radius; dy <= radius; dy++) {
          if (Math.max(Math.abs(dx), Math.abs(dy)) === radius) slots.push([dx * 44, dy * 42]);
        }
        slots.sort(function (a, b) { return a[0] * a[0] + a[1] * a[1] - b[0] * b[0] - b[1] * b[1] || a[1] - b[1] || a[0] - b[0]; });
        for (var i = 0; i < slots.length; i++) {
          if (fits(slots[i][0], slots[i][1])) { shift = slots[i]; found = true; break; }
        }
      }
      group.forEach(function (n) {
        n.x = n.semanticX + shift[0]; n.y = n.semanticY + shift[1];
        var chosen = box(n, n.x, n.y);
        keys(chosen).forEach(function (k) { if (!cells.has(k)) cells.set(k, []); cells.get(k).push(chosen); });
      });
    });
    var residual = 0;
    edges.forEach(function (e) {
      e.original.layoutResidual = Math.hypot(e.target.semanticX - e.source.semanticX - e.vector.x, e.target.semanticY - e.source.semanticY - e.vector.y);
      e.original.layoutConflict = e.original.layoutResidual > Math.max(60, Math.hypot(e.vector.x, e.vector.y) * 0.2);
      residual = Math.max(residual, e.original.layoutResidual);
    });
    return { roots: roots.map(function (n) { return n.id; }), residual: residual, cycles: components.filter(function (g) { return g.length > 1 || outgoing.get(g[0].id).some(function (e) { return e.target === g[0]; }); }).length };
  }
  return { buildCatalogue: buildCatalogue, descriptor: descriptor, edgeVector: edgeVector, vector: vector, layout: layout };
});
