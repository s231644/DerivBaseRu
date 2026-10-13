'''Copy of demo/compound_rules.ipynb (2022_version).'''
import os, json
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
path = os.path.join(REPO, 'derivbase_ru', 'rules', 'rus', 'compounds.json')
data = json.load(open(path, encoding='utf-8'))['data']
rules = [x['rule_id'] for x in data]
print('compound rules loaded:', len(rules))
for r in rules[:10]:
    print('  ', r)
