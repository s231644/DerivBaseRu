import unittest

from src.guesser.ZaliznyakGuesser import *


class TestZaliznyakGuesser(unittest.TestCase):
    def setUp(self):
        self.guesser = ZaliznyakGuesser()

    def tearDown(self):
        del self.guesser

    def test_noun_01(self):
        results = self.guesser.guess('погода', pos_b='noun')
        self.assertIn({'pos_b': 'noun', 'gender': ['f'], 'number': ['s'], 'inflect_type': ['1']}, results)
        results = self.guesser.guess('трос', pos_b='noun')
        self.assertIn({'pos_b': 'noun', 'gender': ['m'], 'number': ['s'], 'inflect_type': ['1']}, results)
        results = self.guesser.guess('слово', pos_b='noun')
        self.assertIn({'pos_b': 'noun', 'gender': ['n'], 'number': ['s'], 'inflect_type': ['1']}, results)

        results = self.guesser.guess('сёстры', pos_b='noun')
        self.assertIn({'pos_b': 'noun', 'gender': ['f'], 'number': ['p'], 'inflect_type': ['1']}, results)
        results = self.guesser.guess('кабаны', pos_b='noun')
        self.assertIn({'pos_b': 'noun', 'gender': ['m'], 'number': ['p'], 'inflect_type': ['1']}, results)
        results = self.guesser.guess('окна', pos_b='noun')
        self.assertIn({'pos_b': 'noun', 'gender': ['n'], 'number': ['p'], 'inflect_type': ['1']}, results)

    def test_noun_02(self):
        results = self.guesser.guess('земля', pos_b='noun')
        self.assertIn({'pos_b': 'noun', 'gender': ['f'], 'number': ['s'], 'inflect_type': ['2']}, results)
        results = self.guesser.guess('гость', pos_b='noun')
        self.assertIn({'pos_b': 'noun', 'gender': ['m'], 'number': ['s'], 'inflect_type': ['2']}, results)
        results = self.guesser.guess('море', pos_b='noun')
        self.assertIn({'pos_b': 'noun', 'gender': ['n'], 'number': ['s'], 'inflect_type': ['2']}, results)

        results = self.guesser.guess('бури', pos_b='noun')
        self.assertIn({'pos_b': 'noun', 'gender': ['f'], 'number': ['p'], 'inflect_type': ['2']}, results)
        results = self.guesser.guess('олени', pos_b='noun')
        self.assertIn({'pos_b': 'noun', 'gender': ['m'], 'number': ['p'], 'inflect_type': ['2']}, results)
        results = self.guesser.guess('моря', pos_b='noun')
        self.assertIn({'pos_b': 'noun', 'gender': ['n'], 'number': ['p'], 'inflect_type': ['2']}, results)

    def test_noun_03(self):
        results = self.guesser.guess('собака', pos_b='noun')
        self.assertIn({'pos_b': 'noun', 'gender': ['f'], 'number': ['s'], 'inflect_type': ['3']}, results)
        results = self.guesser.guess('предок', pos_b='noun')
        self.assertIn({'pos_b': 'noun', 'gender': ['m'], 'number': ['s'], 'inflect_type': ['3']}, results)
        results = self.guesser.guess('личико', pos_b='noun')
        self.assertIn({'pos_b': 'noun', 'gender': ['n'], 'number': ['s'], 'inflect_type': ['3']}, results)

        results = self.guesser.guess('коряги', pos_b='noun')
        self.assertIn({'pos_b': 'noun', 'gender': ['f'], 'number': ['p'], 'inflect_type': ['3']}, results)
        results = self.guesser.guess('петухи', pos_b='noun')
        self.assertIn({'pos_b': 'noun', 'gender': ['m'], 'number': ['p'], 'inflect_type': ['3']}, results)
        results = self.guesser.guess('блага', pos_b='noun')
        self.assertIn({'pos_b': 'noun', 'gender': ['n'], 'number': ['p'], 'inflect_type': ['3']}, results)

    def test_noun_04(self):
        results = self.guesser.guess('саранча', pos_b='noun')
        self.assertIn({'pos_b': 'noun', 'gender': ['f'], 'number': ['s'], 'inflect_type': ['4']}, results)
        results = self.guesser.guess('хрящ', pos_b='noun')
        self.assertIn({'pos_b': 'noun', 'gender': ['m'], 'number': ['s'], 'inflect_type': ['4']}, results)
        results = self.guesser.guess('игрище', pos_b='noun')
        self.assertIn({'pos_b': 'noun', 'gender': ['n'], 'number': ['s'], 'inflect_type': ['4']}, results)

        results = self.guesser.guess('партнёрши', pos_b='noun')
        self.assertIn({'pos_b': 'noun', 'gender': ['f'], 'number': ['p'], 'inflect_type': ['4']}, results)
        results = self.guesser.guess('стражи', pos_b='noun')
        self.assertIn({'pos_b': 'noun', 'gender': ['m'], 'number': ['p'], 'inflect_type': ['4']}, results)
        results = self.guesser.guess('побоища', pos_b='noun')
        self.assertIn({'pos_b': 'noun', 'gender': ['n'], 'number': ['p'], 'inflect_type': ['4']}, results)

    def test_noun_05(self):
        results = self.guesser.guess('улица', pos_b='noun')
        self.assertIn({'pos_b': 'noun', 'gender': ['f'], 'number': ['s'], 'inflect_type': ['5']}, results)
        results = self.guesser.guess('блиц', pos_b='noun')
        self.assertIn({'pos_b': 'noun', 'gender': ['m'], 'number': ['s'], 'inflect_type': ['5']}, results)
        results = self.guesser.guess('лицо', pos_b='noun')
        self.assertIn({'pos_b': 'noun', 'gender': ['n'], 'number': ['s'], 'inflect_type': ['5']}, results)

        results = self.guesser.guess('улицы', pos_b='noun')
        self.assertIn({'pos_b': 'noun', 'gender': ['f'], 'number': ['p'], 'inflect_type': ['5']}, results)
        results = self.guesser.guess('блицы', pos_b='noun')
        self.assertIn({'pos_b': 'noun', 'gender': ['m'], 'number': ['p'], 'inflect_type': ['5']}, results)
        results = self.guesser.guess('лица', pos_b='noun')
        self.assertIn({'pos_b': 'noun', 'gender': ['n'], 'number': ['p'], 'inflect_type': ['5']}, results)

    def test_noun_06(self):
        results = self.guesser.guess('галерея', pos_b='noun')
        self.assertIn({'pos_b': 'noun', 'gender': ['f'], 'number': ['s'], 'inflect_type': ['6']}, results)
        results = self.guesser.guess('ходатай', pos_b='noun')
        self.assertIn({'pos_b': 'noun', 'gender': ['m'], 'number': ['s'], 'inflect_type': ['6']}, results)
        results = self.guesser.guess('ружьё', pos_b='noun')
        self.assertIn({'pos_b': 'noun', 'gender': ['n'], 'number': ['s'], 'inflect_type': ['6']}, results)

        results = self.guesser.guess('ралереи', pos_b='noun')
        self.assertIn({'pos_b': 'noun', 'gender': ['f'], 'number': ['p'], 'inflect_type': ['6']}, results)
        results = self.guesser.guess('чародеи', pos_b='noun')
        self.assertIn({'pos_b': 'noun', 'gender': ['m'], 'number': ['p'], 'inflect_type': ['6']}, results)
        results = self.guesser.guess('воробьи', pos_b='noun')
        self.assertIn({'pos_b': 'noun', 'gender': ['m'], 'number': ['p'], 'inflect_type': ['6']}, results)
        results = self.guesser.guess('ружья', pos_b='noun')
        self.assertIn({'pos_b': 'noun', 'gender': ['n'], 'number': ['p'], 'inflect_type': ['6']}, results)

    def test_noun_07(self):
        results = self.guesser.guess('Австрия', pos_b='noun')
        self.assertIn({'pos_b': 'noun', 'gender': ['f'], 'number': ['s'], 'inflect_type': ['7']}, results)
        results = self.guesser.guess('гелий', pos_b='noun')
        self.assertIn({'pos_b': 'noun', 'gender': ['m'], 'number': ['s'], 'inflect_type': ['7']}, results)
        results = self.guesser.guess('пение', pos_b='noun')
        self.assertIn({'pos_b': 'noun', 'gender': ['n'], 'number': ['s'], 'inflect_type': ['7']}, results)

        results = self.guesser.guess('Анастасии', pos_b='noun')
        self.assertIn({'pos_b': 'noun', 'gender': ['f'], 'number': ['p'], 'inflect_type': ['7']}, results)
        results = self.guesser.guess('гении', pos_b='noun')
        self.assertIn({'pos_b': 'noun', 'gender': ['m'], 'number': ['p'], 'inflect_type': ['7']}, results)
        results = self.guesser.guess('оружия', pos_b='noun')
        self.assertIn({'pos_b': 'noun', 'gender': ['n'], 'number': ['p'], 'inflect_type': ['7']}, results)

    def test_noun_08(self):
        results = self.guesser.guess('лань', pos_b='noun')
        self.assertIn({'pos_b': 'noun', 'gender': ['f'], 'number': ['s'], 'inflect_type': ['8']}, results)
        results = self.guesser.guess('путь', pos_b='noun')
        self.assertIn({'pos_b': 'noun', 'gender': ['m'], 'number': ['s'], 'inflect_type': ['8']}, results)
        results = self.guesser.guess('пламя', pos_b='noun')
        self.assertIn({'pos_b': 'noun', 'gender': ['n'], 'number': ['s'], 'inflect_type': ['8']}, results)

        results = self.guesser.guess('рыси', pos_b='noun')
        self.assertIn({'pos_b': 'noun', 'gender': ['f'], 'number': ['p'], 'inflect_type': ['8']}, results)
        results = self.guesser.guess('пути', pos_b='noun')
        self.assertIn({'pos_b': 'noun', 'gender': ['m'], 'number': ['p'], 'inflect_type': ['8']}, results)
        results = self.guesser.guess('племена', pos_b='noun')
        self.assertIn({'pos_b': 'noun', 'gender': ['n'], 'number': ['p'], 'inflect_type': ['8']}, results)

    def test_adj_01(self):
        results = self.guesser.guess('левый', pos_b='adj')
        self.assertIn({'pos_b': 'adj', 'gender': ['m'], "form": ['full'], 'inflect_type': ['1']}, results)
        results = self.guesser.guess('голубой', pos_b='adj')
        self.assertIn({'pos_b': 'adj', 'gender': ['m'], "form": ['full'], 'inflect_type': ['1']}, results)

    def test_adj_02(self):
        results = self.guesser.guess('синий', pos_b='adj')
        self.assertIn({'pos_b': 'adj', 'gender': ['m'], "form": ['full'], 'inflect_type': ['2']}, results)

    def test_adj_03(self):
        results = self.guesser.guess('громкий', pos_b='adj')
        self.assertIn({'pos_b': 'adj', 'gender': ['m'], "form": ['full'], 'inflect_type': ['3']}, results)

    def test_adj_04(self):
        results = self.guesser.guess('рыжий', pos_b='adj')
        self.assertIn({'pos_b': 'adj', 'gender': ['m'], "form": ['full'], 'inflect_type': ['4']}, results)

    def test_adj_05(self):
        results = self.guesser.guess('куцый', pos_b='adj')
        self.assertIn({'pos_b': 'adj', 'gender': ['m'], "form": ['full'], 'inflect_type': ['5']}, results)


    def test_verb_01(self):
        results = self.guesser.guess('делать', 'делаю', 'делает', pos_b='verb')
        self.assertIn({'pos_b': 'verb', 'inflect_type': ['1']}, results)
        results = self.guesser.guess('менять', 'меняю', 'меняет', pos_b='verb')
        self.assertIn({'pos_b': 'verb', 'inflect_type': ['1']}, results)
        results = self.guesser.guess('греть', 'грею', 'греет', pos_b='verb')
        self.assertIn({'pos_b': 'verb', 'inflect_type': ['1']}, results)

    def test_verb_02(self):
        results = self.guesser.guess('рисовать', 'рисую', 'рисует', pos_b='verb')
        self.assertIn({'pos_b': 'verb', 'inflect_type': ['2']}, results)
        results = self.guesser.guess('танцевать', 'танцую', 'танцует', pos_b='verb')
        self.assertIn({'pos_b': 'verb', 'inflect_type': ['2']}, results)
        results = self.guesser.guess('горевать', 'горюю', 'горюет', pos_b='verb')
        self.assertIn({'pos_b': 'verb', 'inflect_type': ['2']}, results)

    def test_verb_03(self):
        results = self.guesser.guess('прыгнуть', 'прыгну', 'прыгнет', pos_b='verb')
        self.assertIn({'pos_b': 'verb', 'inflect_type': ['3']}, results)

    def test_verb_04(self):
        results = self.guesser.guess('помнить', 'помню', 'помнит', pos_b='verb')
        self.assertIn({'pos_b': 'verb', 'inflect_type': ['4']}, results)
        results = self.guesser.guess('обратить', 'обращу', 'обратит', pos_b='verb')
        self.assertIn({'pos_b': 'verb', 'inflect_type': ['4щ']}, results)

    def test_verb_05(self):
        results = self.guesser.guess('держать', 'держу', 'держит', pos_b='verb')
        self.assertIn({'pos_b': 'verb', 'inflect_type': ['5']}, results)

    def test_verb_06(self):
        results = self.guesser.guess('лаять', 'лаю', 'лает', pos_b='verb')
        self.assertIn({'pos_b': 'verb', 'inflect_type': ['6']}, results)
        results = self.guesser.guess('трепетать', 'трепещу', 'трепещет', pos_b='verb')
        self.assertIn({'pos_b': 'verb', 'inflect_type': ['6щ']}, results)

    def test_verb_07(self):
        results = self.guesser.guess('лезть', 'лезу', 'лезет', pos_b='verb')
        self.assertIn({'pos_b': 'verb', 'inflect_type': ['7з']}, results)
        results = self.guesser.guess('нести', 'несу', 'несет', pos_b='verb')
        self.assertIn({'pos_b': 'verb', 'inflect_type': ['7с']}, results)
        results = self.guesser.guess('вести', 'веду', 'ведет', pos_b='verb')
        self.assertIn({'pos_b': 'verb', 'inflect_type': ['7д']}, results)
        results = self.guesser.guess('мести', 'мету', 'метет', pos_b='verb')
        self.assertIn({'pos_b': 'verb', 'inflect_type': ['7т']}, results)
        results = self.guesser.guess('расти', 'расту', 'растет', pos_b='verb')
        self.assertIn({'pos_b': 'verb', 'inflect_type': ['7ст']}, results)
        results = self.guesser.guess('грести', 'гребу', 'гребет', pos_b='verb')
        self.assertIn({'pos_b': 'verb', 'inflect_type': ['7б']}, results)

    def test_verb_08(self):
        results = self.guesser.guess('беречь', 'берегу', 'бережет', pos_b='verb')
        self.assertIn({'pos_b': 'verb', 'inflect_type': ['8г']}, results)
        results = self.guesser.guess('печь', 'пеку', 'печет', pos_b='verb')
        self.assertIn({'pos_b': 'verb', 'inflect_type': ['8к']}, results)
        results = self.guesser.guess('достичь', 'достигну', 'достигнет', pos_b='verb')
        self.assertIn({'pos_b': 'verb', 'inflect_type': ['8*3']}, results)

    def test_verb_09(self):
        results = self.guesser.guess('тереть', 'тру', 'трет', pos_b='verb')
        self.assertIn({'pos_b': 'verb', 'inflect_type': ['9']}, results)

    def test_verb_10(self):
        results = self.guesser.guess('пороть', 'порю', 'порет', pos_b='verb')
        self.assertIn({'pos_b': 'verb', 'inflect_type': ['10ор']}, results)
        results = self.guesser.guess('колоть', 'колю', 'колет', pos_b='verb')
        self.assertIn({'pos_b': 'verb', 'inflect_type': ['10ол']}, results)
        results = self.guesser.guess('молоть', 'мелю', 'мелет', pos_b='verb')
        self.assertIn({'pos_b': 'verb', 'inflect_type': ['10ел']}, results)

    def test_verb_11(self):
        results = self.guesser.guess('бить', 'бью', 'бьет', pos_b='verb')
        self.assertIn({'pos_b': 'verb', 'inflect_type': ['11']}, results)

    def test_verb_12(self):
        results = self.guesser.guess('мыть', 'мою', 'моет', pos_b='verb')
        self.assertIn({'pos_b': 'verb', 'inflect_type': ['12ы']}, results)
        results = self.guesser.guess('дуть', 'дую', 'дует', pos_b='verb')
        self.assertIn({'pos_b': 'verb', 'inflect_type': ['12у']}, results)
        results = self.guesser.guess('гнить', 'гнию', 'гниет', pos_b='verb')
        self.assertIn({'pos_b': 'verb', 'inflect_type': ['12и']}, results)
        results = self.guesser.guess('петь', 'пою', 'поет', pos_b='verb')
        self.assertIn({'pos_b': 'verb', 'inflect_type': ['12петь']}, results)
        results = self.guesser.guess('греть', 'грею', 'греет', pos_b='verb')
        self.assertIn({'pos_b': 'verb', 'inflect_type': ['12греть']}, results)
        results = self.guesser.guess('брить', 'брею', 'бреет', pos_b='verb')
        self.assertIn({'pos_b': 'verb', 'inflect_type': ['12брить']}, results)

    def test_verb_13(self):
        results = self.guesser.guess('давать', 'даю', 'дает', pos_b='verb')
        self.assertIn({'pos_b': 'verb', 'inflect_type': ['13']}, results)

    def test_verb_14(self):
        results = self.guesser.guess('мять', 'мну', 'мнет', pos_b='verb')
        self.assertIn({'pos_b': 'verb', 'inflect_type': ['14н']}, results)
        results = self.guesser.guess('жать', 'жму', 'жмет', pos_b='verb')
        self.assertIn({'pos_b': 'verb', 'inflect_type': ['14м']}, results)
        results = self.guesser.guess('снять', 'сниму', 'снимет', pos_b='verb')
        self.assertIn({'pos_b': 'verb', 'inflect_type': ['14ним']}, results)
        results = self.guesser.guess('взять', 'возьму', 'возьмет', pos_b='verb')
        self.assertIn({'pos_b': 'verb', 'inflect_type': ['14ьм']}, results)
        results = self.guesser.guess('изъять', 'изыму', 'изымет', pos_b='verb')
        self.assertIn({'pos_b': 'verb', 'inflect_type': ['14ым']}, results)
        results = self.guesser.guess('принять', 'приму', 'примет', pos_b='verb')
        self.assertIn({'pos_b': 'verb', 'inflect_type': ['14им']}, results)
        results = self.guesser.guess('занять', 'займу', 'займет', pos_b='verb')
        self.assertIn({'pos_b': 'verb', 'inflect_type': ['14йм']}, results)

    def test_verb_15(self):
        results = self.guesser.guess('стать', 'стану', 'станет', pos_b='verb')
        self.assertIn({'pos_b': 'verb', 'inflect_type': ['15']}, results)

    def test_verb_16(self):
        results = self.guesser.guess('жить', 'живу', 'живет', pos_b='verb')
        self.assertIn({'pos_b': 'verb', 'inflect_type': ['16']}, results)


if __name__ == '__main__':
    unittest.main(verbosity=2)