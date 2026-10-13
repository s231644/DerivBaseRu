
# DerivBaseRu
A library for building a Russian derivational morphology resourse. 
It is based on the rules described in "The Russian Grammar" book 
and includes about 700 types of affixational derivation in Russian.

**TODO**: harmonization, visualization, compounds.

## Getting Started

### Prerequisites

You should have python3 installed on your machine (we recommend Anaconda3 package) and Python 3.11+ (dependencies are declared in pyproject.toml). If you do not have them, run in Terminal

```
pip install -e .
```

### Installing and Usage

#### Linux / MacOS
To install this project on your local machine, you should run the following commands in Terminal:

```
git init
git clone https://github.com/nsu-ai/DerivBaseRu.git\
cd DerivBaseRu
```

Examples of using DerivBaseRu:

```
>>> from derivbase_ru.derivation import Derivation
>>> evaluator = Derivation()

>>> print(evaluator.derive(word_b='красить', pos_b='verb', pos_a='adj'))
['красячий', 'крашливый', 'некрасиемый', 'красильный', 'красливый', 'закрасинный', 'красный', 'закрашенный', 'красительный', 'крашеный', 'красилой', 'краский', 'красьючий', 'красиючий', 'красистый', 'красной', 'красительский', 'краситый', 'бескрасной', 'красилый', 'красинный', 'некрасимый', 'красимый', 'бескрасный', 'некрасный', 'некрасной', 'красивучий', 'крашенный', 'красиемый']

>>> print(evaluator.derive_ext(word_b='красить', pos_b='verb', pos_a='adj'))
[('закраснить', 'rule888(за,и):2'), ('окраснить', 'rule888(за,и):2'), ('украснить', 'rule902(у,и):2'), ('прокраснить', 'rule899(про,и):2'), ('краснничать', 'rule814(нича):1'), ('отокраснить', 'rule894(от,и):2'), ('обкраснить', 'rule888(за,и):2'), ('подокраснить', 'rule896(по,и):1'), ('перекраснить', 'rule895(пере,и):1'), ('отокраснить', 'rule894(от,и):1'), ('подкраснить', 'rule896(по,и):2'), ('скраснить', 'rule899(про,и):2'), ('краснить', 'rule796(и):2'), ('краснничать', 'rule814(нича):2'), ('краснеть', 'rule830(е):3'), ('сокраснить', 'rule899(про,и):2'), ('украснить', 'rule902(у,и):1'), ('обескраснить', 'rule893(обез,и):2'), ('откраснить', 'rule894(от,и):1'), ('перекраснить', 'rule895(пере,и):2'), ('подокраснить', 'rule896(по,и):2'), ('обескраснить', 'rule893(обез,и):1'), ('раскраснить', 'rule900(раз,и):2'), ('покраснить', 'rule896(по,и):1'), ('краснить', 'rule796(и):1'), ('раскраснить', 'rule900(раз,и):1'), ('обокраснить', 'rule888(за,и):2'), ('окраснеть', 'rule905(о,е):2'), ('красовать', 'rule807(ова):1'), ('скраснить', 'rule899(про,и):1'), ('покраснеть', 'rule908(о,е):1'), ('накраснить', 'rule888(за,и):2'), ('сокраснить', 'rule899(про,и):1'), ('красеть', 'rule830(е):1'), ('покраснеть', 'rule908(о,е):2'), ('закраснеть', 'rule904(за,е):1'), ('краснеть', 'rule830(е):1'), ('красствовать', 'rule817(ствова):1'), ('откраснить', 'rule894(от,и):2'), ('прикраснить', 'rule898(при,и):1'), ('подкраснить', 'rule896(по,и):1'), ('искраснить', 'rule889(из,и):1'), ('окраснеть', 'rule905(о,е):1'), ('красниться', 'rule933(и,ся):1'), ('покраснить', 'rule896(по,и):2'), ('прикраснить', 'rule898(при,и):2'), ('красеть', 'rule830(е):2'), ('накраснить', 'rule888(за,и):1'), ('закраснить', 'rule888(за,и):1'), ('окраснить', 'rule888(за,и):1'), ('прокраснить', 'rule899(про,и):1'), ('закраснеть', 'rule904(за,е):2'), ('искраснить', 'rule889(из,и):2'), ('обокраснить', 'rule888(за,и):1'), ('красновать', 'rule807(ова):1'), ('обкраснить', 'rule888(за,и):1'), ('красновать', 'rule807(ова):2'), ('красниться', 'rule933(и,ся):2')]

```

## Notation

In this section, we describe the notation used in our rule system.

### Verbs (verb)

| Infl. type| inf | 1sg| 3sg|
| ------------- |-------------:| -----:|---:|
| 1      | дел**ать** | дел**аю** |дел**ает**|
| 1      | мен**ять** | мен**яю** |мен**яет**|
| 1      | ум**еть** | ум**ею** |ум**еет**|
| 2      | рис**овать** | рис**ую** |рис**ует**|
| 2      | танц**евать** | танц**ую** |танц**ует**|
| 2      | гор**евать** | гор**юю** |гор**юет**|
| 3      | то**нуть** | то**ну** |то**нет**|
| 4      | помн**ить** | помн**ю** |помн**ит**|
| 4      | крут**ить** | круч**у** |крут**ит**|
| 4      | обога**тить** | обога**щу** |обога**тит**|
|4       | ушиб**ить** | ушиб**у** |ушиб**ет**|
|4       | стел**ить** | стел**ю** |стел**ет**|
|4       | зижд**ить** | зижд**у** |зижд**ет**|
| 5      | держ**ать** | держ**у** |держ**ит**|
| 5      | сто**ять** | сто**ю** |сто**ит**|
| 5      | смотр**еть** | смотр**ю** |смотр**ит**|
|5       | беж**ать** | бег**у** |беж**ит**|
| 6      | плак**ать** | плач**у** |плач**ет**|
| 6      | ла**ять** | ла**ю** |ла**ет**|
| 6      | клеве**тать** | клеве**щу** |клеве**щет**|
| 7з     | ле**зть** | ле**зу** |ле**зет**|
| 7з     | пол**зти** | пол**зу** |пол**зет**|
| 7с     | тря**сти** | тря**су** |тря**сет**|
| 7д     | кра**сть** | кра**ду** |кра**дет**|
| 7д     | ве**сти** | ве**ду** |ве**дет**|
| 7т     | че**сть** | ч**ту** |ч**тет**|
| 7т     | ме**сти** | ме**ту** |ме**тет**|
| 7б     | гре**сти** | гре**бу** |гре**бет**|
| 7ст    | ра**сти** | ра**сту** |ра**стет**|
| 8г     | бере**чь** | бере**гу** |бере**жет**|
| 8к     | пе**чь** | пе**ку** |пе**чет**|
| 8*3    | дости**чь** | дости**гну** |дости**гнет**|
| 9      | т**ереть** | т**ру** |т**рет**|
| 10ел   | м**олоть** | м**елю** |м**елет**|
| 10ол   | к**олоть** | к**олю** |к**олет**|
| 10ор   | п**ороть** | п**орю** |п**орет**|
| 11     | б**ить** | б**ью** |б**ьет**|
| 12ы    | м**ыть** | м**ою** |м**оет**|
| 12у    | д**уть** | д**ую** |д**ует**|
| 12и    | гн**ить** | гн**ию** |гн**иет**|
| 12греть| **греть** | **грею** |**греет**|
| 12петь | **петь** | **пою** |**поет**|
| 12брить| **брить** | **брею** |**бреет**|
| 13     | д**авать** | да**ю** |да**ет**|
| 14м    | ж**ать** | ж**му** |ж**мет**|
| 14н    | нач**ать** | нач**ну** |нач**нет**|
| 14н    | м**ять** | м**ну** |м**нет**|
| 14ним  | с**нять** | с**ниму** |с**нимет**|
| 14йм   | по**нять** | по**йму** |по**ймет**|
| 14йм   | об**ъять** | обо**йму** |обо**ймет**|
| 14им   | при**нять** | при**му** |при**мет**|
| 14ым   | из**ъять** | из**ыму** |из**ымет**|
| 14ьм   | вз**ять** | воз**ьму** |воз**ьмет**|
| 15     | ст**ать** | ста**ну** |ста**нет**|
| 16     | жи**ть** | жи**ву** |жи**вет**|
|клясть  | кля**сть** | кля**ну** |кля**нет**|
|есть    | е**сть** | е**м** |е**ст**|
|дать    | **дать** | **дам** |**даст**|
|быть    | б**ыть** | б**уду** |б**удет**|
|ехать   | е**хать** | е**ду** |е**дет**|
|идти    |и**дти**|и**ду**|и**дет**|
|идти    |у**йти**|у**йду**|у**йдет**|
|идти    |из**ыти**|из**ыду**|из**ыдет**|


### Nouns (noun)

| Infl. type | f | m | n | p |
| ------------- |-------------:| -----:|---:|---:|
| 1      | корона | вирус | окно | джинсы |
| 2      | земля | олень | море | грабли |
| 3      | рука | снег | ухо | беруши |
| 4      | душа | корж | плечо |  |
| 5      | курица | птенец | солнце | ножницы |
| 6      | змея | воробей | удушье |  |
| 7      | линия | гений | подобие |  |
| 8      | лошадь | путь | время |  |


### Adjectives (adj)
| Infl. type | adj |
| ------------- |---:|
| 1      | белый |
| 2      | синий |
| 3      | короткий |
| 4      | нищий |
| 5      | куцый |


## Authors

* **Daniil Vodolazsky** - [s231644](https://github.com/s231644)

See also the list of [contributors](https://github.com/s231644/DerivBaseRu/contributors) who participated in this project.

## License
Apache 2.0, see LICENSE for more details.

## Publications
Daniil Vodolazsky. DerivBase.Ru: a Derivational Morphology Resource for Russian (LREC 2020).

```
@InProceedings{vodolazsky:2020:LREC,
author = {Vodolazsky, Daniil},
title = {DerivBase.Ru: a Derivational Morphology Resource for Russian},
booktitle = {Proceedings of The 12th Language Resources and Evaluation Conference},
month = {May},
year = {2020},
address = {Marseille, France},
publisher = {European Language Resources Association},
pages = {3930--3936},
abstract = {Russian morphology has been studied for decades, but there is still no large high coverage resource that contains the derivational families (groups of words that share the same root) of Russian words. The number of words used in different areas of the language grows rapidly, thus the human-made dictionaries published long time ago cannot cover the neologisms and the domain-specific lexicons. To fill such resource gap, we have developed a rule-based framework for deriving words and we applied it to build a derivational morphology resource named DerivBase.Ru, which we introduce in this paper.},
url = {https://www.aclweb.org/anthology/2020.lrec-1.484}
}
```