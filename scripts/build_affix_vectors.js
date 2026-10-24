#!/usr/bin/env node
'use strict';
const fs = require('node:fs');
const path = require('node:path');
const geometry = require('../graph_service/public/affix-layout.js');
const root = path.resolve(__dirname, '..');
const rules = [];
function visit(directory) {
  for (const entry of fs.readdirSync(directory, { withFileTypes: true }).sort((a, b) => a.name < b.name ? -1 : 1)) {
    const file = path.join(directory, entry.name);
    if (entry.isDirectory()) visit(file);
    else if (entry.name.endsWith('.json')) rules.push(...(JSON.parse(fs.readFileSync(file, 'utf8')).data || []));
  }
}
visit(path.join(root, 'derivbase_ru/rules/rus'));
const catalogue = geometry.buildCatalogue(rules);
fs.writeFileSync(path.join(root, 'graph_service/public/affix-vectors.json'), JSON.stringify(catalogue) + '\n');
process.stdout.write(Object.keys(catalogue.affixes).length + ' stable vectors; ' + Object.keys(catalogue.rules).length + ' rules\n');
