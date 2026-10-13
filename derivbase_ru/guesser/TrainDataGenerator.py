import pandas as pd

gram_types = set()

data_input = open('data/zalizniak.txt', encoding='cp1251')

data_records = []
for line in data_input:
    l = line.replace('\n', '').split(' ')
    l = list(filter(lambda x: x, l))
    if not l:
        continue
    word, accent = l[0], l[1]
    gram = ''
    infl_type = ''
    label = ''
    pf_forms_state = 0
    pf_forms = []
    for field in l[2:]:
        if not infl_type:
            if field[0] == '@':
                infl_type = field
            if field[0].isdigit():
                tmp_it = field[0]
                for i in range(1, len(field)):
                    if field[i].isdigit():
                        tmp_it += field[i]
                    else:
                        break
                infl_type = tmp_it
            else:
                gram += field
        if len(field) > 4 and field[:2] == '(-' and field[-2:] == '-)':
            label = field
        if pf_forms_state == 1:
            pf_forms.append(field)
            if field[-1] == ';':
                pf_forms_state = 2
        if field in {'_наст_', '_буд_'}:
            pf_forms_state = 1

    gram_types |= {gram}

    data_records.append((word, accent, gram, infl_type, label, '.'.join(pf_forms)))

verb_records = []
noun_records = []
adj_records = []
adv_records = []
num_records = []

for elem in data_records:
    if 'св' in elem[2] and len(elem[3]) and elem[3][0].isdigit():
        verb_records.append(elem)

verb_table = pd.DataFrame(verb_records, columns=['word', 'accent', 'gram', 'infltype', 'label', 'forms'])
verb_table.to_csv('data/Zaliznyak_verb_table.csv', index=False)
#data_table = pd.DataFrame(data_records, columns=['word', 'accent', 'gram', 'infltype', 'label', 'forms'])

#data_table.to_csv('data/Zaliznyak_table.csv', index=False)
