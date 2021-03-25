# -*- coding: utf-8 -*-

import unittest

from src.Derivation import Derivation


class TestDerivationADJ(unittest.TestCase):
    def setUp(self):
        self.derivation = Derivation()

    def tearDown(self):
        del self.derivation

    def test_adj_611(self):
        results = self.derivation.derive(word_b='дед', pos_b='noun', pos_a='adj*')
        self.assertIn('дедов', results)
        results = self.derivation.derive(word_b='государь', pos_b='noun', pos_a='adj*')
        self.assertIn('государев', results)
        results = self.derivation.derive(word_b='пастух', pos_b='noun', pos_a='adj*')
        self.assertIn('пастухов', results)
        results = self.derivation.derive(word_b='царевич', pos_b='noun', pos_a='adj*')
        self.assertIn('царевичев', results)
        results = self.derivation.derive(word_b='отец', pos_b='noun', pos_a='adj*')
        self.assertIn('отцов', results)
        results = self.derivation.derive(word_b='Сергей', pos_b='noun', pos_a='adj*')
        self.assertIn('Сергеев', results)

    @unittest.skip
    def test_adj_611_2(self):
        results = self.derivation.derive(word_b='Довженко', pos_b='noun', pos_a='adj*')
        self.assertIn('Довженков', results)
        results = self.derivation.derive(word_b='Вивальди', pos_b='noun', pos_a='adj*')
        self.assertIn('Вивальдиев', results)

    @unittest.skip
    def test_adj_611_3(self):
        results = self.derivation.derive(word_b='Аврора', pos_b='noun', pos_a='adj*')
        self.assertIn('Авроров', results)
        results = self.derivation.derive(word_b='коммуна', pos_b='noun', pos_a='adj*')
        self.assertIn('коммунова', results)
        results = self.derivation.derive(word_b='одеяло', pos_b='noun', pos_a='adj*')
        self.assertIn('одеялово', results)

    def test_adj_612(self):
        results = self.derivation.derive(word_b='мама', pos_b='noun', pos_a='adj*')
        self.assertIn('мамин', results)
        results = self.derivation.derive(word_b='дядя', pos_b='noun', pos_a='adj*')
        self.assertIn('дядин', results)
        results = self.derivation.derive(word_b='бабушка', pos_b='noun', pos_a='adj*')
        self.assertIn('бабушкин', results)
        results = self.derivation.derive(word_b='директорша', pos_b='noun', pos_a='adj*')
        self.assertIn('директоршин', results)
        results = self.derivation.derive(word_b='синица', pos_b='noun', pos_a='adj*')
        self.assertIn('синицын', results)
        results = self.derivation.derive(word_b='Илья', pos_b='noun', pos_a='adj*')
        self.assertIn('Ильин', results)
        results = self.derivation.derive(word_b='матерь', pos_b='noun', pos_a='adj*')
        self.assertIn('материн', results)

    @unittest.skip
    def test_adj_612_2(self):
        results = self.derivation.derive(word_b='листик', pos_b='noun', pos_a='adj*')
        self.assertIn('листикин', results)
        results = self.derivation.derive(word_b='поэт', pos_b='noun', pos_a='adj*')
        self.assertIn('поэтин', results)

    @unittest.skip
    def test_adj_612_3(self):
        results = self.derivation.derive(word_b='Вилли', pos_b='noun', pos_a='adj*')
        self.assertIn('Виллин', results)
        results = self.derivation.derive(word_b='Мэри', pos_b='noun', pos_a='adj*')
        self.assertIn('Мэрин', results)

    @unittest.skip
    def test_adj_613(self):
        results = self.derivation.derive(word_b='брат', pos_b='noun', pos_a='adj*')
        self.assertIn('братнин', results)
        results = self.derivation.derive(word_b='муж', pos_b='noun', pos_a='adj*')
        self.assertIn('мужнин', results)
        results = self.derivation.derive(word_b='зять', pos_b='noun', pos_a='adj*')
        self.assertIn('зятнин', results)
        results = self.derivation.derive(word_b='дочерь', pos_b='noun', pos_a='adj*')
        self.assertIn('дочернин', results)

    @unittest.skip
    def test_adj_614(self):
        results = self.derivation.derive(word_b='вдова', pos_b='noun', pos_a='adj*')
        self.assertIn('вдовий', results)
        results = self.derivation.derive(word_b='баран', pos_b='noun', pos_a='adj*')
        self.assertIn('бараний', results)
        results = self.derivation.derive(word_b='митрополит', pos_b='noun', pos_a='adj*')
        self.assertIn('митрополичий', results)

        results = self.derivation.derive(word_b='пескарь', pos_b='noun', pos_a='adj*')
        self.assertIn('пескарий', results)
        results = self.derivation.derive(word_b='человек', pos_b='noun', pos_a='adj*')
        self.assertIn('человечий', results)
        results = self.derivation.derive(word_b='медведь', pos_b='noun', pos_a='adj*')
        self.assertIn('медвежий', results)
        results = self.derivation.derive(word_b='птица', pos_b='noun', pos_a='adj*')
        self.assertIn('птичий', results)
        results = self.derivation.derive(word_b='лошадь', pos_b='noun', pos_a='adj*')
        self.assertIn('лошажий', results)

    @unittest.skip
    def test_adj_614_2(self):
        results = self.derivation.derive(word_b='бык', pos_b='noun', pos_a='adj*')
        self.assertIn('бычачий', results)
        results = self.derivation.derive(word_b='овца', pos_b='noun', pos_a='adj*')
        self.assertIn('овечий', results)
        results = self.derivation.derive(word_b='кошка', pos_b='noun', pos_a='adj*')
        self.assertIn('кошачий', results)
        results = self.derivation.derive(word_b='русалка', pos_b='noun', pos_a='adj*')
        self.assertIn('русалочий', results)
        results = self.derivation.derive(word_b='медведь', pos_b='noun', pos_a='adj*')
        self.assertIn('медвежачий', results)
        results = self.derivation.derive(word_b='утка', pos_b='noun', pos_a='adj*')
        self.assertIn('утячий', results)
        results = self.derivation.derive(word_b='щегол', pos_b='noun', pos_a='adj*')
        self.assertIn('щеглячий', results)

    @unittest.skip
    def test_adj_614_3(self):
        results = self.derivation.derive(word_b='белка', pos_b='noun', pos_a='adj*')
        self.assertIn('беличий', results)
        results = self.derivation.derive(word_b='попугай', pos_b='noun', pos_a='adj*')
        self.assertIn('попугаичий', results)

    @unittest.skip
    def test_adj_614_4(self):
        results = self.derivation.derive(word_b='вол', pos_b='noun', pos_a='adj*')
        self.assertIn('воловий', results)

    @unittest.skip
    def test_adj_614_5(self):
        results = self.derivation.derive(word_b='кукушка', pos_b='noun', pos_a='adj*')
        self.assertIn('кукушечий', results)
        results = self.derivation.derive(word_b='куропатка', pos_b='noun', pos_a='adj*')
        self.assertIn('куропачий', results)
        results = self.derivation.derive(word_b='жаворонок', pos_b='noun', pos_a='adj*')
        self.assertIn('жавороночий', results)

    @unittest.skip
    def test_adj_614_6(self):
        results = self.derivation.derive(word_b='курица', pos_b='noun', pos_a='adj*')
        self.assertIn('куричий', results)
        self.assertIn('курячий', results)
        self.assertIn('курий', results)
        results = self.derivation.derive(word_b='свинья', pos_b='noun', pos_a='adj*')
        self.assertIn('свинячий', results)

    @unittest.skip
    def test_adj_614_7(self):
        results = self.derivation.derive(word_b='кенгуру', pos_b='noun', pos_a='adj*')
        self.assertIn('кенгурий', results)

    @unittest.skip
    def test_adj_614_8(self):
        results = self.derivation.derive(word_b='ребенок', pos_b='noun', pos_a='adj*')
        self.assertIn('ребячий', results)

    @unittest.skip
    def test_adj_614_9(self):
        results = self.derivation.derive(word_b='гага', pos_b='noun', pos_a='adj*')
        self.assertIn('гагачий', results)

    @unittest.skip
    def test_adj_614_10(self):
        results = self.derivation.derive(word_b='князь', pos_b='noun', pos_a='adj*')
        self.assertIn('княжий', results)
        results = self.derivation.derive(word_b='сёмга', pos_b='noun', pos_a='adj*')
        self.assertIn('сёмужий', results)
        results = self.derivation.derive(word_b='лебедь', pos_b='noun', pos_a='adj*')
        self.assertIn('лебяжий', results)

    def test_adj_616(self):
        results = self.derivation.derive(word_b='зверь', pos_b='noun', pos_a='adj')
        self.assertIn('звериный', results)
        results = self.derivation.derive(word_b='лев', pos_b='noun', pos_a='adj')
        self.assertIn('львиный', results)
        results = self.derivation.derive(word_b='козел', pos_b='noun', pos_a='adj')
        self.assertIn('козлиный', results)
        results = self.derivation.derive(word_b='воробей', pos_b='noun', pos_a='adj')
        self.assertIn('воробьиный', results)
        results = self.derivation.derive(word_b='змея', pos_b='noun', pos_a='adj')
        self.assertIn('змеиный', results)
        results = self.derivation.derive(word_b='утка', pos_b='noun', pos_a='adj')
        self.assertIn('утиный', results)
        results = self.derivation.derive(word_b='куры', pos_b='noun', pos_a='adj')
        self.assertIn('куриный', results)
        results = self.derivation.derive(word_b='петух', pos_b='noun', pos_a='adj')
        self.assertIn('петушиный', results)
        results = self.derivation.derive(word_b='скворец', pos_b='noun', pos_a='adj')
        self.assertIn('скворчиный', results)

    def test_adj_619_1(self):
        results = self.derivation.derive(word_b='одеяло', pos_b='noun', pos_a='adj')
        self.assertIn('одеяльный', results)
        results = self.derivation.derive(word_b='аренда', pos_b='noun', pos_a='adj')
        self.assertIn('арендный', results)
        results = self.derivation.derive(word_b='школа', pos_b='noun', pos_a='adj')
        self.assertIn('школьный', results)
        results = self.derivation.derive(word_b='топор', pos_b='noun', pos_a='adj')
        self.assertIn('топорный', results)
        results = self.derivation.derive(word_b='буря', pos_b='noun', pos_a='adj')
        self.assertIn('бурный', results)
        results = self.derivation.derive(word_b='неделя', pos_b='noun', pos_a='adj')
        self.assertIn('недельный', results)
        results = self.derivation.derive(word_b='уголь', pos_b='noun', pos_a='adj')
        self.assertIn('угольный', results)
        results = self.derivation.derive(word_b='футбол', pos_b='noun', pos_a='adj')
        self.assertIn('футбольный', results)
        results = self.derivation.derive(word_b='молоко', pos_b='noun', pos_a='adj')
        self.assertIn('молочный', results)
        results = self.derivation.derive(word_b='цепочка', pos_b='noun', pos_a='adj')
        self.assertIn('цепочный', results)
        results = self.derivation.derive(word_b='каторга', pos_b='noun', pos_a='adj')
        self.assertIn('каторжный', results)
        results = self.derivation.derive(word_b='долг', pos_b='noun', pos_a='adj')
        self.assertIn('должный', results)
        results = self.derivation.derive(word_b='творог', pos_b='noun', pos_a='adj')
        self.assertIn('творожный', results)
        results = self.derivation.derive(word_b='плечо', pos_b='noun', pos_a='adj')
        self.assertIn('плечной', results)
        results = self.derivation.derive(word_b='продажа', pos_b='noun', pos_a='adj')
        self.assertIn('продажный', results)
        results = self.derivation.derive(word_b='массаж', pos_b='noun', pos_a='adj')
        self.assertIn('массажный', results)
        results = self.derivation.derive(word_b='футбол', pos_b='noun', pos_a='adj')
        self.assertIn('футбольный', results)
        results = self.derivation.derive(word_b='молоко', pos_b='noun', pos_a='adj')
        self.assertIn('молочный', results)
        results = self.derivation.derive(word_b='лицо', pos_b='noun', pos_a='adj')
        self.assertIn('личный', results)
        results = self.derivation.derive(word_b='страница', pos_b='noun', pos_a='adj')
        self.assertIn('страничный', results)
        results = self.derivation.derive(word_b='огурец', pos_b='noun', pos_a='adj')
        self.assertIn('огуречный', results)
        results = self.derivation.derive(word_b='зловонье', pos_b='noun', pos_a='adj')
        self.assertIn('зловонный', results)
        results = self.derivation.derive(word_b='ружьё', pos_b='noun', pos_a='adj')
        self.assertIn('ружейный', results)
        results = self.derivation.derive(word_b='шея', pos_b='noun', pos_a='adj')
        self.assertIn('шейный', results)
        results = self.derivation.derive(word_b='бой', pos_b='noun', pos_a='adj')
        self.assertIn('бойный', results)
        results = self.derivation.derive(word_b='край', pos_b='noun', pos_a='adj')
        self.assertIn('крайний', results)
        results = self.derivation.derive(word_b='мгновение', pos_b='noun', pos_a='adj')
        self.assertIn('мгновенный', results)
        results = self.derivation.derive(word_b='сословие', pos_b='noun', pos_a='adj')
        self.assertIn('сословный', results)
        results = self.derivation.derive(word_b='лаборатория', pos_b='noun', pos_a='adj')
        self.assertIn('лабораторный', results)
        results = self.derivation.derive(word_b='инерция', pos_b='noun', pos_a='adj')
        self.assertIn('инертный', results)
        results = self.derivation.derive(word_b='сценарий', pos_b='noun', pos_a='adj')
        self.assertIn('сценарный', results)
        results = self.derivation.derive(word_b='калий', pos_b='noun', pos_a='adj')
        self.assertIn('калийный', results)
        results = self.derivation.derive(word_b='верфь', pos_b='noun', pos_a='adj')
        self.assertIn('верфный', results)
        results = self.derivation.derive(word_b='путь', pos_b='noun', pos_a='adj')
        self.assertIn('путный', results)
        results = self.derivation.derive(word_b='пламя', pos_b='noun', pos_a='adj')
        self.assertIn('пламенный', results)

    def test_adj_619_1_2(self):
        results = self.derivation.derive(word_b='гротеск', pos_b='noun', pos_a='adj')
        self.assertIn('гротескный', results)

    def test_adj_619_1_3(self):
        results = self.derivation.derive(word_b='матрац', pos_b='noun', pos_a='adj')
        self.assertIn('матрацный', results)

    @unittest.skip
    def test_adj_619_1_4(self):
        results = self.derivation.derive(word_b='факсимиле', pos_b='noun', pos_a='adj')
        self.assertIn('факсимильный', results)
        results = self.derivation.derive(word_b='барокко', pos_b='noun', pos_a='adj')
        self.assertIn('барочный', results)
        results = self.derivation.derive(word_b='соло', pos_b='noun', pos_a='adj')
        self.assertIn('сольный', results)
        results = self.derivation.derive(word_b='фортепьяно', pos_b='noun', pos_a='adj')
        self.assertIn('фортепьянный', results)

    @unittest.skip
    def test_adj_619_1_5(self):
        results = self.derivation.derive(word_b='кабаре', pos_b='noun', pos_a='adj')
        self.assertIn('кабаретный', results)
        results = self.derivation.derive(word_b='комильфо', pos_b='noun', pos_a='adj')
        self.assertIn('комильфотный', results)
        results = self.derivation.derive(word_b='буржуа', pos_b='noun', pos_a='adj')
        self.assertIn('буржуазный', results)

    @unittest.skip
    def test_adj_619_1_6(self):
        results = self.derivation.derive(word_b='дерево', pos_b='noun', pos_a='adj')
        self.assertIn('древесный', results)
        results = self.derivation.derive(word_b='слово', pos_b='noun', pos_a='adj')
        self.assertIn('словесный', results)

    @unittest.skip
    def test_adj_619_1_7(self):
        results = self.derivation.derive(word_b='яйцо', pos_b='noun', pos_a='adj')
        self.assertIn('яичный', results)

    @unittest.skip
    def test_adj_619_1_8(self):
        results = self.derivation.derive(word_b='амуниция', pos_b='noun', pos_a='adj')
        self.assertIn('амуничный', results)

    @unittest.skip
    def test_adj_619_1_9(self):
        results = self.derivation.derive(word_b='вакансия', pos_b='noun', pos_a='adj')
        self.assertIn('вакантный', results)

    def test_adj_619_1_10(self):
        results = self.derivation.derive(word_b='семья', pos_b='noun', pos_a='adj')
        self.assertIn('семейный', results)

    @unittest.skip
    def test_adj_619_1_11(self):
        results = self.derivation.derive(word_b='барахло', pos_b='noun', pos_a='adj')
        self.assertIn('барахольный', results)
        results = self.derivation.derive(word_b='игла', pos_b='noun', pos_a='adj')
        self.assertIn('игольный', results)
        results = self.derivation.derive(word_b='очки', pos_b='noun', pos_a='adj')
        self.assertIn('очёчный', results)
        results = self.derivation.derive(word_b='свёкла', pos_b='noun', pos_a='adj')
        self.assertIn('свекольный', results)
        results = self.derivation.derive(word_b='тайга', pos_b='noun', pos_a='adj')
        self.assertIn('таёжный', results)

    @unittest.skip
    def test_adj_619_1_12(self):
        results = self.derivation.derive(word_b='война', pos_b='noun', pos_a='adj')
        self.assertIn('военный', results)
        results = self.derivation.derive(word_b='корабль', pos_b='noun', pos_a='adj')
        self.assertIn('корабельный', results)
        results = self.derivation.derive(word_b='служба', pos_b='noun', pos_a='adj')
        self.assertIn('служебный', results)
        results = self.derivation.derive(word_b='польза', pos_b='noun', pos_a='adj')
        self.assertIn('полезный', results)

    @unittest.skip
    def test_adj_619_1_13(self):
        results = self.derivation.derive(word_b='дирижабль', pos_b='noun', pos_a='adj')
        self.assertIn('дирижабельный', results)
        results = self.derivation.derive(word_b='жабры', pos_b='noun', pos_a='adj')
        self.assertIn('жаберный', results)
        results = self.derivation.derive(word_b='калибр', pos_b='noun', pos_a='adj')
        self.assertIn('калиберный', results)
        results = self.derivation.derive(word_b='кегль', pos_b='noun', pos_a='adj')
        self.assertIn('кегельный', results)
        results = self.derivation.derive(word_b='солнце', pos_b='noun', pos_a='adj')
        self.assertIn('солнечный', results)
        results = self.derivation.derive(word_b='тяжба', pos_b='noun', pos_a='adj')
        self.assertIn('тяжебный', results)
        results = self.derivation.derive(word_b='легкие', pos_b='noun', pos_a='adj')
        self.assertIn('легочный', results)
        results = self.derivation.derive(word_b='насморк', pos_b='noun', pos_a='adj')
        self.assertIn('насморочный', results)
        results = self.derivation.derive(word_b='пасха', pos_b='noun', pos_a='adj')
        self.assertIn('пасочный', results)
        results = self.derivation.derive(word_b='фейерверк', pos_b='noun', pos_a='adj')
        self.assertIn('фейерверочный', results)
        results = self.derivation.derive(word_b='шеренга', pos_b='noun', pos_a='adj')
        self.assertIn('шереножный', results)

    @unittest.skip
    def test_adj_619_1_14(self):
        results = self.derivation.derive(word_b='линия', pos_b='noun', pos_a='adj')
        self.assertIn('линейный', results)
        results = self.derivation.derive(word_b='оружие', pos_b='noun', pos_a='adj')
        self.assertIn('оружейный', results)
        results = self.derivation.derive(word_b='келья', pos_b='noun', pos_a='adj')
        self.assertIn('келейный', results)
        results = self.derivation.derive(word_b='партия', pos_b='noun', pos_a='adj')
        self.assertIn('партийный', results)

    @unittest.skip
    def test_adj_619_1_15(self):
        results = self.derivation.derive(word_b='отделение', pos_b='noun', pos_a='adj')
        self.assertIn('отделённый', results)

    @unittest.skip
    def test_adj_619_1_16(self):
        results = self.derivation.derive(word_b='бунчук', pos_b='noun', pos_a='adj')
        self.assertIn('бунчужный', results)
        results = self.derivation.derive(word_b='скорняк', pos_b='noun', pos_a='adj')
        self.assertIn('скорняжный', results)
        results = self.derivation.derive(word_b='армяк', pos_b='noun', pos_a='adj')
        self.assertIn('армяжный', results)

    @unittest.skip
    def test_adj_619_1_17(self):
        results = self.derivation.derive(word_b='колодец', pos_b='noun', pos_a='adj')
        self.assertIn('колодезный', results)

    @unittest.skip
    def test_adj_619_1_18(self):
        results = self.derivation.derive(word_b='претензия', pos_b='noun', pos_a='adj')
        self.assertIn('претенциозный', results)

    @unittest.skip
    def test_adj_619_1_19(self):
        results = self.derivation.derive(word_b='земля', pos_b='noun', pos_a='adj')
        self.assertIn('земной', results)

    @unittest.skip
    def test_adj_619_1_20(self):
        results = self.derivation.derive(word_b='молоко', pos_b='noun', pos_a='adj')
        self.assertIn('млечный', results)
        results = self.derivation.derive(word_b='дерево', pos_b='noun', pos_a='adj')
        self.assertIn('древесный', results)

    @unittest.skip
    def test_adj_619_1_21(self):
        results = self.derivation.derive(word_b='бассейн', pos_b='noun', pos_a='adj')
        self.assertIn('бассейный', results)
        results = self.derivation.derive(word_b='антенна', pos_b='noun', pos_a='adj')
        self.assertIn('антенный', results)

    def test_adj_619_2(self):
        results = self.derivation.derive(word_b='язва', pos_b='noun', pos_a='adj')
        self.assertIn('язвенный', results)
        results = self.derivation.derive(word_b='манёвр', pos_b='noun', pos_a='adj')
        self.assertIn('манёвренный', results)
        results = self.derivation.derive(word_b='лекарство', pos_b='noun', pos_a='adj')
        self.assertIn('лекарственный', results)
        results = self.derivation.derive(word_b='огонь', pos_b='noun', pos_a='adj')
        self.assertIn('огненный', results)
        results = self.derivation.derive(word_b='восторг', pos_b='noun', pos_a='adj')
        self.assertIn('восторженный', results)
        results = self.derivation.derive(word_b='следствие', pos_b='noun', pos_a='adj')
        self.assertIn('следственный', results)
        results = self.derivation.derive(word_b='болезнь', pos_b='noun', pos_a='adj')
        self.assertIn('болезненный', results)

    @unittest.skip
    def test_adj_619_2_2(self):
        results = self.derivation.derive(word_b='тундра', pos_b='noun', pos_a='adj')
        self.assertIn('тундреный', results)
        results = self.derivation.derive(word_b='ветер', pos_b='noun', pos_a='adj')
        self.assertIn('ветреный', results)

    @unittest.skip
    def test_adj_619_2_3(self):
        results = self.derivation.derive(word_b='крыжовник', pos_b='noun', pos_a='adj')
        self.assertIn('крыжовенный', results)

    def test_adj_619_3(self):
        results = self.derivation.derive(word_b='индукция', pos_b='noun', pos_a='adj')
        self.assertIn('индукционный', results)
        results = self.derivation.derive(word_b='профессия', pos_b='noun', pos_a='adj')
        self.assertIn('профессиональный', results)

    def test_adj_619_4(self):
        results = self.derivation.derive(word_b='патриархат', pos_b='noun', pos_a='adj')
        self.assertIn('патриархальный', results)
        results = self.derivation.derive(word_b='уникум', pos_b='noun', pos_a='adj')
        self.assertIn('уникальный', results)
        results = self.derivation.derive(word_b='радиус', pos_b='noun', pos_a='adj')
        self.assertIn('радиальный', results)
        results = self.derivation.derive(word_b='пасха', pos_b='noun', pos_a='adj')
        self.assertIn('пасхальный', results)
        results = self.derivation.derive(word_b='федерация', pos_b='noun', pos_a='adj')
        self.assertIn('федеральный', results)
        results = self.derivation.derive(word_b='премия', pos_b='noun', pos_a='adj')
        self.assertIn('премиальный', results)
        results = self.derivation.derive(word_b='гений', pos_b='noun', pos_a='adj')
        self.assertIn('гениальный', results)

    def test_adj_619_5(self):
        results = self.derivation.derive(word_b='молекула', pos_b='noun', pos_a='adj')
        self.assertIn('молекулярный', results)
        results = self.derivation.derive(word_b='пленум', pos_b='noun', pos_a='adj')
        self.assertIn('пленарный', results)
        results = self.derivation.derive(word_b='полюс', pos_b='noun', pos_a='adj')
        self.assertIn('полярный', results)
        results = self.derivation.derive(word_b='дёготь', pos_b='noun', pos_a='adj')
        self.assertIn('дегтярный', results)

    def test_adj_619_6(self):
        results = self.derivation.derive(word_b='вена', pos_b='noun', pos_a='adj')
        self.assertIn('венозный', results)
        results = self.derivation.derive(word_b='грипп', pos_b='noun', pos_a='adj')
        self.assertIn('гриппозный', results)
        results = self.derivation.derive(word_b='скандал', pos_b='noun', pos_a='adj')
        self.assertIn('скандалёзный', results)
        results = self.derivation.derive(word_b='религия', pos_b='noun', pos_a='adj')
        self.assertIn('религиозный', results)

    @unittest.skip
    def test_adj_619_6_2(self):
        results = self.derivation.derive(word_b='экзема', pos_b='noun', pos_a='adj')
        self.assertIn('экзематозный', results)

    def test_adj_619_7(self):
        results = self.derivation.derive(word_b='рефлекс', pos_b='noun', pos_a='adj')
        self.assertIn('рефлекторный', results)
        results = self.derivation.derive(word_b='экстрасенс', pos_b='noun', pos_a='adj')
        self.assertIn('экстрасенсорный', results)
        results = self.derivation.derive(word_b='иллюзия', pos_b='noun', pos_a='adj')
        self.assertIn('иллюзорный', results)
        results = self.derivation.derive(word_b='комбинация', pos_b='noun', pos_a='adj')
        self.assertIn('комбинаторный', results)

    def test_adj_619_8(self):
        results = self.derivation.derive(word_b='текст', pos_b='noun', pos_a='adj')
        self.assertIn('текстуальный', results)
        results = self.derivation.derive(word_b='процесс', pos_b='noun', pos_a='adj')
        self.assertIn('процессуальный', results)
        results = self.derivation.derive(word_b='концепция', pos_b='noun', pos_a='adj')
        self.assertIn('концептуальный', results)

    def test_adj_619_9(self):
        results = self.derivation.derive(word_b='ультиматум', pos_b='noun', pos_a='adj')
        self.assertIn('ультимативный', results)
        results = self.derivation.derive(word_b='прогресс', pos_b='noun', pos_a='adj')
        self.assertIn('прогрессивный', results)
        results = self.derivation.derive(word_b='конверсия', pos_b='noun', pos_a='adj')
        self.assertIn('конвертивный', results)
        results = self.derivation.derive(word_b='федерация', pos_b='noun', pos_a='adj')
        self.assertIn('федеративный', results)

    @unittest.skip
    def test_adj_619_9_2(self):
        results = self.derivation.derive(word_b='консерватор', pos_b='noun', pos_a='adj')
        self.assertIn('консервативный', results)

    @unittest.skip
    def test_adj_619_9_3(self):
        results = self.derivation.derive(word_b='арго', pos_b='noun', pos_a='adj')
        self.assertIn('арготивный', results)

    def test_adj_619_10(self):
        results = self.derivation.derive(word_b='халва', pos_b='noun', pos_a='adj')
        self.assertIn('халвичный', results)
        results = self.derivation.derive(word_b='хаос', pos_b='noun', pos_a='adj')
        self.assertIn('хаотичный', results)
        results = self.derivation.derive(word_b='тип', pos_b='noun', pos_a='adj')
        self.assertIn('типичный', results)
        results = self.derivation.derive(word_b='скрипка', pos_b='noun', pos_a='adj')
        self.assertIn('скрипичный', results)
        results = self.derivation.derive(word_b='энергия', pos_b='noun', pos_a='adj')
        self.assertIn('энергичный', results)

    @unittest.skip
    def test_adj_619_10_2(self):
        results = self.derivation.derive(word_b='будни', pos_b='noun', pos_a='adj')
        self.assertIn('будничный', results)

    @unittest.skip
    def test_adj_619_10_3(self):
        results = self.derivation.derive(word_b='маслина', pos_b='noun', pos_a='adj')
        self.assertIn('масличный', results)

    @unittest.skip
    def test_adj_619_10_4(self):
        results = self.derivation.derive(word_b='драма', pos_b='noun', pos_a='adj')
        self.assertIn('драматичный', results)
        results = self.derivation.derive(word_b='симптом', pos_b='noun', pos_a='adj')
        self.assertIn('симптоматичный', results)

    @unittest.skip
    def test_adj_619_10_5(self):
        results = self.derivation.derive(word_b='гипотеза', pos_b='noun', pos_a='adj')
        self.assertIn('гипотетичный', results)

    def test_adj_619_11(self):
        results = self.derivation.derive(word_b='принцип', pos_b='noun', pos_a='adj')
        self.assertIn('принципиальный', results)
        results = self.derivation.derive(word_b='бронха', pos_b='noun', pos_a='adj')
        self.assertIn('бронхиальный', results)
        results = self.derivation.derive(word_b='провинция', pos_b='noun', pos_a='adj')
        self.assertIn('провинциальный', results)

    def test_adj_619_12(self):
        results = self.derivation.derive(word_b='образование', pos_b='noun', pos_a='adj')
        self.assertIn('образовательный', results)

    def test_adj_619_13(self):
        results = self.derivation.derive(word_b='зрение', pos_b='noun', pos_a='adj')
        self.assertIn('зрительный', results)

    @unittest.skip
    def test_adj_619_14(self):
        results = self.derivation.derive(word_b='обмолот', pos_b='noun', pos_a='adj')
        self.assertIn('обмолоточный', results)
        results = self.derivation.derive(word_b='отёлка', pos_b='noun', pos_a='adj')
        self.assertIn('отёлочный', results)
        results = self.derivation.derive(word_b='карта', pos_b='noun', pos_a='adj')
        self.assertIn('карточный', results)

    @unittest.skip
    def test_adj_619_15(self):
        results = self.derivation.derive(word_b='вина', pos_b='noun', pos_a='adj')
        self.assertIn('виновный', results)
        results = self.derivation.derive(word_b='чин', pos_b='noun', pos_a='adj')
        self.assertIn('чиновный', results)
        results = self.derivation.derive(word_b='грех', pos_b='noun', pos_a='adj')
        self.assertIn('греховный', results)
        results = self.derivation.derive(word_b='зуб', pos_b='noun', pos_a='adj')
        self.assertIn('зубовный', results)

    @unittest.skip
    def test_adj_619_16(self):
        results = self.derivation.derive(word_b='душа', pos_b='noun', pos_a='adj')
        self.assertIn('душевный', results)
        results = self.derivation.derive(word_b='плач', pos_b='noun', pos_a='adj')
        self.assertIn('плачевный', results)
        results = self.derivation.derive(word_b='день', pos_b='noun', pos_a='adj')
        self.assertIn('дневной', results)

    @unittest.skip
    def test_adj_619_17(self):
        results = self.derivation.derive(word_b='враг', pos_b='noun', pos_a='adj')
        self.assertIn('враждебный', results)
        results = self.derivation.derive(word_b='суд', pos_b='noun', pos_a='adj')
        self.assertIn('судебный', results)
        results = self.derivation.derive(word_b='врач', pos_b='noun', pos_a='adj')
        self.assertIn('врачебный', results)

    @unittest.skip
    def test_adj_619_18(self):
        results = self.derivation.derive(word_b='желе', pos_b='noun', pos_a='adj')
        self.assertIn('желейный', results)
        results = self.derivation.derive(word_b='жалюзи', pos_b='noun', pos_a='adj')
        self.assertIn('жалюзийный', results)
        results = self.derivation.derive(word_b='кино', pos_b='noun', pos_a='adj')
        self.assertIn('киношный', results)
        results = self.derivation.derive(word_b='фэзэу', pos_b='noun', pos_a='adj')
        self.assertIn('фэзэушный', results)

    @unittest.skip
    def test_adj_619_18_2(self):
        results = self.derivation.derive(word_b='алоэ', pos_b='noun', pos_a='adj')
        self.assertIn('алойный', results)

    def test_adj_619_19(self):
        results = self.derivation.derive(word_b='ум', pos_b='noun', pos_a='adj')
        self.assertIn('умственный', results)
        results = self.derivation.derive(word_b='женщина', pos_b='noun', pos_a='adj')
        self.assertIn('женственный', results)
        results = self.derivation.derive(word_b='насилие', pos_b='noun', pos_a='adj')
        self.assertIn('насильственный', results)

    @unittest.skip
    def test_adj_619_20(self):
        results = self.derivation.derive(word_b='солод', pos_b='noun', pos_a='adj')
        self.assertIn('солодовенный', results)

    @unittest.skip
    def test_adj_619_21(self):
        results = self.derivation.derive(word_b='смерть', pos_b='noun', pos_a='adj')
        self.assertIn('смертельный', results)
        results = self.derivation.derive(word_b='платье', pos_b='noun', pos_a='adj')
        self.assertIn('плательный', results)

    @unittest.skip
    def test_adj_619_22(self):
        results = self.derivation.derive(word_b='гвоздь', pos_b='noun', pos_a='adj')
        self.assertIn('гвоздильный', results)

    @unittest.skip
    def test_adj_619_23(self):
        results = self.derivation.derive(word_b='геморрой', pos_b='noun', pos_a='adj')
        self.assertIn('геморроидальный', results)
        results = self.derivation.derive(word_b='трапеция', pos_b='noun', pos_a='adj')
        self.assertIn('трапецеидальный', results)

    @unittest.skip
    def test_adj_619_24(self):
        results = self.derivation.derive(word_b='скерцо', pos_b='noun', pos_a='adj')
        self.assertIn('скерциозный', results)
        results = self.derivation.derive(word_b='претензия', pos_b='noun', pos_a='adj')
        self.assertIn('претенциозный', results)

    @unittest.skip
    def test_adj_619_25(self):
        results = self.derivation.derive(word_b='помпа', pos_b='noun', pos_a='adj')
        self.assertIn('помпезный', results)

    @unittest.skip
    def test_adj_619_26(self):
        results = self.derivation.derive(word_b='цинга', pos_b='noun', pos_a='adj')
        self.assertIn('цинготный', results)
        results = self.derivation.derive(word_b='кроха', pos_b='noun', pos_a='adj')
        self.assertIn('крохотный', results)

    @unittest.skip
    def test_adj_619_27(self):
        results = self.derivation.derive(word_b='телевидение', pos_b='noun', pos_a='adj')
        self.assertIn('телевизионный', results)

    @unittest.skip
    def test_adj_619_28(self):
        results = self.derivation.derive(word_b='экзамен', pos_b='noun', pos_a='adj')
        self.assertIn('экзаменационный', results)

    @unittest.skip
    def test_adj_619_29(self):
        results = self.derivation.derive(word_b='портной', pos_b='noun', pos_a='adj')
        self.assertIn('портняжный', results)

    def test_adj_623(self):
        results = self.derivation.derive(word_b='супруг', pos_b='noun', pos_a='adj')
        self.assertIn('супружний', results)
        results = self.derivation.derive(word_b='матерь', pos_b='noun', pos_a='adj')
        self.assertIn('матерний', results)
        results = self.derivation.derive(word_b='сын', pos_b='noun', pos_a='adj')
        self.assertIn('сыновний', results)
        results = self.derivation.derive(word_b='перед', pos_b='noun', pos_a='adj')
        self.assertIn('передний', results)
        results = self.derivation.derive(word_b='верх', pos_b='noun', pos_a='adj')
        self.assertIn('верхний', results)
        results = self.derivation.derive(word_b='низ', pos_b='noun', pos_a='adj')
        self.assertIn('нижний', results)
        results = self.derivation.derive(word_b='край', pos_b='noun', pos_a='adj')
        self.assertIn('крайний', results)
        results = self.derivation.derive(word_b='сторона', pos_b='noun', pos_a='adj')
        self.assertIn('сторонний', results)
        results = self.derivation.derive(word_b='лето', pos_b='noun', pos_a='adj')
        self.assertIn('летний', results)
        results = self.derivation.derive(word_b='весна', pos_b='noun', pos_a='adj')
        self.assertIn('весенний', results)
        results = self.derivation.derive(word_b='утро', pos_b='noun', pos_a='adj')
        self.assertIn('утренний', results)
        results = self.derivation.derive(word_b='утро', pos_b='noun', pos_a='adj')
        self.assertIn('утрешний', results)
        results = self.derivation.derive(word_b='будни', pos_b='noun', pos_a='adj')
        self.assertIn('буднишний', results)
        results = self.derivation.derive(word_b='правда', pos_b='noun', pos_a='adj')
        self.assertIn('правдашний', results)

    def test_adj_624(self):
        results = self.derivation.derive(word_b='береста', pos_b='noun', pos_a='adj')
        self.assertIn('берестяной', results)
        results = self.derivation.derive(word_b='волос', pos_b='noun', pos_a='adj')
        self.assertIn('волосяной', results)
        results = self.derivation.derive(word_b='ветер', pos_b='noun', pos_a='adj')
        self.assertIn('ветряный', results)
        results = self.derivation.derive(word_b='дупло', pos_b='noun', pos_a='adj')
        self.assertIn('дупляной', results)
        results = self.derivation.derive(word_b='гвоздь', pos_b='noun', pos_a='adj')
        self.assertIn('гвоздяной', results)
        results = self.derivation.derive(word_b='кожа', pos_b='noun', pos_a='adj')
        self.assertIn('кожаный', results)
        results = self.derivation.derive(word_b='ветвь', pos_b='noun', pos_a='adj')
        self.assertIn('ветвяной', results)
        results = self.derivation.derive(word_b='таволги', pos_b='noun', pos_a='adj')
        self.assertIn('таволжаный', results)
        results = self.derivation.derive(word_b='мох', pos_b='noun', pos_a='adj')
        self.assertIn('мшаный', results)
        results = self.derivation.derive(word_b='воск', pos_b='noun', pos_a='adj')
        self.assertIn('вощаной', results)
        results = self.derivation.derive(word_b='лёд', pos_b='noun', pos_a='adj')
        self.assertIn('ледяной', results)
        results = self.derivation.derive(word_b='платье', pos_b='noun', pos_a='adj')
        self.assertIn('платяной', results)
        results = self.derivation.derive(word_b='хлопья', pos_b='noun', pos_a='adj')
        self.assertIn('хлопяной', results)
        results = self.derivation.derive(word_b='мёд', pos_b='noun', pos_a='adj')
        self.assertIn('медвяный', results)
        results = self.derivation.derive(word_b='дух', pos_b='noun', pos_a='adj')
        self.assertIn('духмяный', results)
        results = self.derivation.derive(word_b='тростник', pos_b='noun', pos_a='adj')
        self.assertIn('тростяной', results)

    def test_adj_625(self):
        results = self.derivation.derive(word_b='стекло', pos_b='noun', pos_a='adj')
        self.assertIn('стеклянный', results)

    def test_adj_626(self):
        results = self.derivation.derive(word_b='рента', pos_b='noun', pos_a='adj')
        self.assertIn('рентабельный', results)
        results = self.derivation.derive(word_b='комфорт', pos_b='noun', pos_a='adj')
        self.assertIn('комфортабельный', results)
        results = self.derivation.derive(word_b='коммуникация', pos_b='noun', pos_a='adj')
        self.assertIn('коммуникабельный', results)

    def test_adj_627(self):
        results = self.derivation.derive(word_b='купе', pos_b='noun', pos_a='adj')
        self.assertIn('купированный', results)
        results = self.derivation.derive(word_b='квалификация', pos_b='noun', pos_a='adj')
        self.assertIn('квалифицированный', results)
        results = self.derivation.derive(word_b='привилегия', pos_b='noun', pos_a='adj')
        self.assertIn('привилегированный', results)
        results = self.derivation.derive(word_b='экзальтация', pos_b='noun', pos_a='adj')
        self.assertIn('экзальтированный', results)
        results = self.derivation.derive(word_b='эрудиция', pos_b='noun', pos_a='adj')
        self.assertIn('эрудированный', results)

    def test_adj_628(self):
        results = self.derivation.derive(word_b='тундра', pos_b='noun', pos_a='adj')
        self.assertIn('тундровый', results)
        results = self.derivation.derive(word_b='дом', pos_b='noun', pos_a='adj')
        self.assertIn('домовый', results)
        results = self.derivation.derive(word_b='одеяло', pos_b='noun', pos_a='adj')
        self.assertIn('одеяловый', results)
        results = self.derivation.derive(word_b='вишня', pos_b='noun', pos_a='adj')
        self.assertIn('вишнёвый', results)
        results = self.derivation.derive(word_b='соболь', pos_b='noun', pos_a='adj')
        self.assertIn('соболевый', results)
        results = self.derivation.derive(word_b='поле', pos_b='noun', pos_a='adj')
        self.assertIn('полевой', results)
        results = self.derivation.derive(word_b='грядка', pos_b='noun', pos_a='adj')
        self.assertIn('грядковый', results)
        results = self.derivation.derive(word_b='берег', pos_b='noun', pos_a='adj')
        self.assertIn('береговой', results)
        results = self.derivation.derive(word_b='стрелок', pos_b='noun', pos_a='adj')
        self.assertIn('стрелковый', results)
        results = self.derivation.derive(word_b='замша', pos_b='noun', pos_a='adj')
        self.assertIn('замшевый', results)
        results = self.derivation.derive(word_b='морж', pos_b='noun', pos_a='adj')
        self.assertIn('моржовый', results)
        results = self.derivation.derive(word_b='синица', pos_b='noun', pos_a='adj')
        self.assertIn('синицевый', results)
        results = self.derivation.derive(word_b='ситец', pos_b='noun', pos_a='adj')
        self.assertIn('ситцевый', results)
        results = self.derivation.derive(word_b='лицо', pos_b='noun', pos_a='adj')
        self.assertIn('лицевой', results)
        results = self.derivation.derive(word_b='горностай', pos_b='noun', pos_a='adj')
        self.assertIn('горностаевый', results)
        results = self.derivation.derive(word_b='сырьё', pos_b='noun', pos_a='adj')
        self.assertIn('сырьевой', results)
        results = self.derivation.derive(word_b='боль', pos_b='noun', pos_a='adj')
        self.assertIn('болевой', results)
        results = self.derivation.derive(word_b='путь', pos_b='noun', pos_a='adj')
        self.assertIn('путевой', results)

    def test_adj_628_2(self):
        results = self.derivation.derive(word_b='звено', pos_b='noun', pos_a='adj')
        self.assertIn('звеньевой', results)
        results = self.derivation.derive(word_b='перо', pos_b='noun', pos_a='adj')
        self.assertIn('перьевой', results)
        results = self.derivation.derive(word_b='судно', pos_b='noun', pos_a='adj')
        self.assertIn('судовой', results)

    def test_adj_628_3(self):
        results = self.derivation.derive(word_b='кенгуру', pos_b='noun', pos_a='adj')
        self.assertIn('кенгуровый', results)
        results = self.derivation.derive(word_b='джерси', pos_b='noun', pos_a='adj')
        self.assertIn('джерсевый', results)
        results = self.derivation.derive(word_b='джерсе', pos_b='noun', pos_a='adj')
        self.assertIn('джерсовый', results)
        results = self.derivation.derive(word_b='такси', pos_b='noun', pos_a='adj')
        self.assertIn('таксовый', results)

    def test_adj_628_4(self):
        results = self.derivation.derive(word_b='можжевельник', pos_b='noun', pos_a='adj')
        self.assertIn('можжевёловый', results)

    def test_adj_628_5(self):
        results = self.derivation.derive(word_b='клеть', pos_b='noun', pos_a='adj')
        self.assertIn('клетьевой', results)
        results = self.derivation.derive(word_b='глубь', pos_b='noun', pos_a='adj')
        self.assertIn('глубьевой', results)
        results = self.derivation.derive(word_b='герань', pos_b='noun', pos_a='adj')
        self.assertIn('гераниевый', results)

    def test_adj_628_6(self):
        results = self.derivation.derive(word_b='греча', pos_b='noun', pos_a='adj')
        self.assertIn('гречневый', results)

    def test_adj_628_7(self):
        results = self.derivation.derive(word_b='кора', pos_b='noun', pos_a='adj')
        self.assertIn('корковый', results)
        results = self.derivation.derive(word_b='ячмень', pos_b='noun', pos_a='adj')
        self.assertIn('ячневый', results)

    def test_adj_628_8(self):
        results = self.derivation.derive(word_b='какао', pos_b='noun', pos_a='adj')
        self.assertIn('какаовый', results)

    def test_adj_628_9(self):
        results = self.derivation.derive(word_b='жёрнов', pos_b='noun', pos_a='adj')
        self.assertIn('жерновой', results)
        results = self.derivation.derive(word_b='бечева', pos_b='noun', pos_a='adj')
        self.assertIn('бечевой', results)
        results = self.derivation.derive(word_b='швартов', pos_b='noun', pos_a='adj')
        self.assertIn('швартовый', results)

    def test_adj_628_10(self):
        results = self.derivation.derive(word_b='узел', pos_b='noun', pos_a='adj')
        self.assertIn('узловой', results)
        results = self.derivation.derive(word_b='сосна', pos_b='noun', pos_a='adj')
        self.assertIn('сосновый', results)

    def test_adj_628_11(self):
        results = self.derivation.derive(word_b='лёд', pos_b='noun', pos_a='adj')
        self.assertIn('ледовый', results)
        results = self.derivation.derive(word_b='лоб', pos_b='noun', pos_a='adj')
        self.assertIn('лобовой', results)

    def test_adj_628_12(self):
        results = self.derivation.derive(word_b='рана', pos_b='noun', pos_a='adj')
        self.assertIn('раневой', results)
        results = self.derivation.derive(word_b='смола', pos_b='noun', pos_a='adj')
        self.assertIn('смолевой', results)
        results = self.derivation.derive(word_b='смола', pos_b='noun', pos_a='adj')
        self.assertIn('смолёвый', results)
        results = self.derivation.derive(word_b='плюсна', pos_b='noun', pos_a='adj')
        self.assertIn('плюсневой', results)
        results = self.derivation.derive(word_b='гол', pos_b='noun', pos_a='adj')
        self.assertIn('голевой', results)
        results = self.derivation.derive(word_b='зверь', pos_b='noun', pos_a='adj')
        self.assertIn('зверовой', results)
        results = self.derivation.derive(word_b='дробь', pos_b='noun', pos_a='adj')
        self.assertIn('дробовой', results)
        results = self.derivation.derive(word_b='ель', pos_b='noun', pos_a='adj')
        self.assertIn('еловый', results)
        results = self.derivation.derive(word_b='весть', pos_b='noun', pos_a='adj')
        self.assertIn('вестовой', results)
        results = self.derivation.derive(word_b='жёлудь', pos_b='noun', pos_a='adj')
        self.assertIn('желудовый', results)

    def test_adj_628_13(self):
        results = self.derivation.derive(word_b='холст', pos_b='noun', pos_a='adj')
        self.assertIn('холщевый', results)
        results = self.derivation.derive(word_b='зябь', pos_b='noun', pos_a='adj')
        self.assertIn('зяблевый', results)

    def test_adj_631_1(self):
        results = self.derivation.derive(word_b='Одесса', pos_b='noun', pos_a='adj')
        self.assertIn('одесский', results)
        results = self.derivation.derive(word_b='сосед', pos_b='noun', pos_a='adj')
        self.assertIn('соседский', results)
        results = self.derivation.derive(word_b='арсенал', pos_b='noun', pos_a='adj')
        self.assertIn('арсенальский', results)
        results = self.derivation.derive(word_b='февраль', pos_b='noun', pos_a='adj')
        self.assertIn('февральский', results)
        results = self.derivation.derive(word_b='конь', pos_b='noun', pos_a='adj')
        self.assertIn('конский', results)
        results = self.derivation.derive(word_b='Сумы', pos_b='noun', pos_a='adj')
        self.assertIn('сумский', results)
        results = self.derivation.derive(word_b='море', pos_b='noun', pos_a='adj')
        self.assertIn('морской', results)
        results = self.derivation.derive(word_b='чех', pos_b='noun', pos_a='adj')
        self.assertIn('чешский', results)
        results = self.derivation.derive(word_b='казак', pos_b='noun', pos_a='adj')
        self.assertIn('казацкий', results)
        results = self.derivation.derive(word_b='Париж', pos_b='noun', pos_a='adj')
        self.assertIn('парижский', results)
        results = self.derivation.derive(word_b='Винница', pos_b='noun', pos_a='adj')
        self.assertIn('винницкий', results)
        results = self.derivation.derive(word_b='немец', pos_b='noun', pos_a='adj')
        self.assertIn('немецкий', results)
        results = self.derivation.derive(word_b='май', pos_b='noun', pos_a='adj')
        self.assertIn('майский', results)
        results = self.derivation.derive(word_b='Мордовия', pos_b='noun', pos_a='adj')
        self.assertIn('мордовский', results)
        results = self.derivation.derive(word_b='Англия', pos_b='noun', pos_a='adj')
        self.assertIn('английский', results)
        results = self.derivation.derive(word_b='Бразилия', pos_b='noun', pos_a='adj')
        self.assertIn('бразильский', results)
        results = self.derivation.derive(word_b='Пермь', pos_b='noun', pos_a='adj')
        self.assertIn('пермский', results)

    def test_adj_631_1_2(self):
        results = self.derivation.derive(word_b='Моздок', pos_b='noun', pos_a='adj')
        self.assertIn('моздокский', results)
        results = self.derivation.derive(word_b='Лейпциг', pos_b='noun', pos_a='adj')
        self.assertIn('лейпцигский', results)
        results = self.derivation.derive(word_b='Палех', pos_b='noun', pos_a='adj')
        self.assertIn('палехский', results)
        results = self.derivation.derive(word_b='нивхи', pos_b='noun', pos_a='adj')
        self.assertIn('нивхский', results)

    def test_adj_631_1_3(self):
        results = self.derivation.derive(word_b='герцог', pos_b='noun', pos_a='adj')
        self.assertIn('герцогский', results)
        results = self.derivation.derive(word_b='шах', pos_b='noun', pos_a='adj')
        self.assertIn('шахский', results)

    def test_adj_631_1_4(self):
        results = self.derivation.derive(word_b='сентябрь', pos_b='noun', pos_a='adj')
        self.assertIn('сентябрьский', results)
        results = self.derivation.derive(word_b='июнь', pos_b='noun', pos_a='adj')
        self.assertIn('июньский', results)
        results = self.derivation.derive(word_b='день', pos_b='noun', pos_a='adj')
        self.assertIn('деньской', results)

    def test_adj_631_1_5(self):
        results = self.derivation.derive(word_b='Ямал', pos_b='noun', pos_a='adj')
        self.assertIn('ямалский', results)
        results = self.derivation.derive(word_b='Пномпень', pos_b='noun', pos_a='adj')
        self.assertIn('пномпеньский', results)

    def test_adj_631_1_6(self):
        results = self.derivation.derive(word_b='Бордо', pos_b='noun', pos_a='adj')
        self.assertIn('бордоский', results)
        results = self.derivation.derive(word_b='Ватерлоо', pos_b='noun', pos_a='adj')
        self.assertIn('ватерлооский', results)
        results = self.derivation.derive(word_b='майя', pos_b='noun', pos_a='adj')
        self.assertIn('майяский', results)
        results = self.derivation.derive(word_b='Тарту', pos_b='noun', pos_a='adj')
        self.assertIn('тартуский', results)
        results = self.derivation.derive(word_b='Раквере', pos_b='noun', pos_a='adj')
        self.assertIn('раквереский', results)
        results = self.derivation.derive(word_b='Чарджоу', pos_b='noun', pos_a='adj')
        self.assertIn('чарджоуский', results)

    def test_adj_631_2(self):
        results = self.derivation.derive(word_b='ребята', pos_b='noun', pos_a='adj')
        self.assertIn('ребяческий', results)
        results = self.derivation.derive(word_b='князь', pos_b='noun', pos_a='adj')
        self.assertIn('княжеский', results)
        results = self.derivation.derive(word_b='логика', pos_b='noun', pos_a='adj')
        self.assertIn('логический', results)
        results = self.derivation.derive(word_b='друг', pos_b='noun', pos_a='adj')
        self.assertIn('дружеский', results)
        results = self.derivation.derive(word_b='ханжа', pos_b='noun', pos_a='adj')
        self.assertIn('ханжеский', results)
        results = self.derivation.derive(word_b='трюкач', pos_b='noun', pos_a='adj')
        self.assertIn('трюкаческий', results)
        results = self.derivation.derive(word_b='купец', pos_b='noun', pos_a='adj')
        self.assertIn('купеческий', results)

    def test_adj_631_2_2(self):
        results = self.derivation.derive(word_b='князь', pos_b='noun', pos_a='adj')
        self.assertIn('княжеский', results)

    def test_adj_631_3(self):
        results = self.derivation.derive(word_b='Массандра', pos_b='noun', pos_a='adj')
        self.assertIn('массандровский', results)
        results = self.derivation.derive(word_b='вор', pos_b='noun', pos_a='adj')
        self.assertIn('воровской', results)
        results = self.derivation.derive(word_b='кремль', pos_b='noun', pos_a='adj')
        self.assertIn('кремлевский', results)
        results = self.derivation.derive(word_b='жених', pos_b='noun', pos_a='adj')
        self.assertIn('жениховский', results)
        results = self.derivation.derive(word_b='фриц', pos_b='noun', pos_a='adj')
        self.assertIn('фрицевский', results)
        results = self.derivation.derive(word_b='отец', pos_b='noun', pos_a='adj')
        self.assertIn('отцовский', results)

    def test_adj_631_3_2(self):
        results = self.derivation.derive(word_b='Горький', pos_b='noun_adj', pos_a='adj')
        self.assertIn('горьковский', results)
        results = self.derivation.derive(word_b='Гойя', pos_b='noun', pos_a='adj')
        self.assertIn('гойевский', results)
        results = self.derivation.derive(word_b='ЖюльВерн', pos_b='noun', pos_a='adj')
        self.assertIn('жюльверновский', results)

    def test_adj_631_3_3(self):
        results = self.derivation.derive(word_b='Клинцы', pos_b='noun', pos_a='adj')
        self.assertIn('клинцовский', results)
        results = self.derivation.derive(word_b='Нагорье', pos_b='noun', pos_a='adj')
        self.assertIn('нагорьевский', results)

    def test_adj_632_1(self):
        results = self.derivation.derive(word_b='Америка', pos_b='noun', pos_a='adj')
        self.assertIn('американский', results)
        results = self.derivation.derive(word_b='Бирма', pos_b='noun', pos_a='adj')
        self.assertIn('бирманский', results)
        results = self.derivation.derive(word_b='Рудня', pos_b='noun', pos_a='adj')
        self.assertIn('руднянский', results)
        results = self.derivation.derive(word_b='Орша', pos_b='noun', pos_a='adj')
        self.assertIn('оршанский', results)
        results = self.derivation.derive(word_b='Венеция', pos_b='noun', pos_a='adj')
        self.assertIn('венецианский', results)
        results = self.derivation.derive(word_b='Россошь', pos_b='noun', pos_a='adj')
        self.assertIn('россошанский', results)

    def test_adj_632_1_2(self):
        results = self.derivation.derive(word_b='Перу', pos_b='noun', pos_a='adj')
        self.assertIn('перуанский', results)

    def test_adj_632_2(self):
        results = self.derivation.derive(word_b='Чита', pos_b='noun', pos_a='adj')
        self.assertIn('читинский', results)
        results = self.derivation.derive(word_b='Лодзь', pos_b='noun', pos_a='adj')
        self.assertIn('лодзинский', results)
        results = self.derivation.derive(word_b='Шахты', pos_b='noun', pos_a='adj')
        self.assertIn('шахтинский', results)
        results = self.derivation.derive(word_b='Мирный', pos_b='noun', pos_a='adj')
        self.assertIn('мирнинский', results)
        results = self.derivation.derive(word_b='Мытыщи', pos_b='noun', pos_a='adj')
        self.assertIn('мытищинский', results)
        results = self.derivation.derive(word_b='Пенза', pos_b='noun', pos_a='adj')
        self.assertIn('пензенский', results)
        results = self.derivation.derive(word_b='Керчь', pos_b='noun', pos_a='adj')
        self.assertIn('керченский', results)
        results = self.derivation.derive(word_b='городище', pos_b='noun', pos_a='adj')
        self.assertIn('городищенский', results)
        results = self.derivation.derive(word_b='Екатерина', pos_b='noun', pos_a='adj')
        self.assertIn('екатерининский', results)
        results = self.derivation.derive(word_b='матерь', pos_b='noun', pos_a='adj')
        self.assertIn('материнский', results)
        results = self.derivation.derive(word_b='сатана', pos_b='noun', pos_a='adj')
        self.assertIn('сатанинский', results)
        results = self.derivation.derive(word_b='нищий', pos_b='noun_adj', pos_a='adj')
        self.assertIn('нищенский', results)
        results = self.derivation.derive(word_b='кладбище', pos_b='noun', pos_a='adj')
        self.assertIn('кладбищенский', results)
        results = self.derivation.derive(word_b='рождество', pos_b='noun', pos_a='adj')
        self.assertIn('рождественский', results)
        results = self.derivation.derive(word_b='Фрунзе', pos_b='noun', pos_a='adj')
        self.assertIn('фрунзенский', results)
        results = self.derivation.derive(word_b='Известия', pos_b='noun', pos_a='adj')
        self.assertIn('известинский', results)

    def test_adj_632_3(self):
        results = self.derivation.derive(word_b='эвенки', pos_b='noun', pos_a='adj')
        self.assertIn('эвенкийский', results)
        results = self.derivation.derive(word_b='Альпы', pos_b='noun', pos_a='adj')
        self.assertIn('альпийский', results)
        results = self.derivation.derive(word_b='Уганда', pos_b='noun', pos_a='adj')
        self.assertIn('угандийский', results)
        results = self.derivation.derive(word_b='Олимп', pos_b='noun', pos_a='adj')
        self.assertIn('олимпийский', results)

    def test_adj_632_4(self):
        results = self.derivation.derive(word_b='сцена', pos_b='noun', pos_a='adj')
        self.assertIn('сценический', results)
        results = self.derivation.derive(word_b='алгебра', pos_b='noun', pos_a='adj')
        self.assertIn('алгебраический', results)
        results = self.derivation.derive(word_b='эпизод', pos_b='noun', pos_a='adj')
        self.assertIn('эпизодический', results)
        results = self.derivation.derive(word_b='идеолог', pos_b='noun', pos_a='adj')
        self.assertIn('идеологический', results)
        results = self.derivation.derive(word_b='герой', pos_b='noun', pos_a='adj')
        self.assertIn('героический', results)
        results = self.derivation.derive(word_b='верноподданный', pos_b='noun_adj', pos_a='adj')
        self.assertIn('верноподданнический', results)

    def test_adj_632_5(self):
        results = self.derivation.derive(word_b='краевед', pos_b='noun', pos_a='adj')
        self.assertIn('краеведческий', results)
        results = self.derivation.derive(word_b='винодел', pos_b='noun', pos_a='adj')
        self.assertIn('винодельческий', results)
        results = self.derivation.derive(word_b='учреждение', pos_b='noun', pos_a='adj')
        self.assertIn('учрежденческий', results)

    def test_adj_632_6(self):
        results = self.derivation.derive(word_b='ханты', pos_b='noun', pos_a='adj')
        self.assertIn('хантыйский', results)
        results = self.derivation.derive(word_b='Чу', pos_b='noun', pos_a='adj')
        self.assertIn('чуйский', results)
        results = self.derivation.derive(word_b='Хуло', pos_b='noun', pos_a='adj')
        self.assertIn('хулойский', results)

    def test_adj_632_7(self):
        results = self.derivation.derive(word_b='Улан-Удэ', pos_b='noun', pos_a='adj')
        self.assertIn('улан-удэнский', results)
        results = self.derivation.derive(word_b='эрзя', pos_b='noun', pos_a='adj')
        self.assertIn('эрзянский', results)

    def test_adj_632_8(self):
        results = self.derivation.derive(word_b='Ришелье', pos_b='noun', pos_a='adj')
        self.assertIn('ришельевский', results)

    def test_adj_632_9(self):
        results = self.derivation.derive(word_b='Верди', pos_b='noun', pos_a='adj')
        self.assertIn('вердиевский', results)

    def test_adj_632_10(self):
        results = self.derivation.derive(word_b='Венера', pos_b='noun', pos_a='adj')
        self.assertIn('венерианский', results)
        results = self.derivation.derive(word_b='Меркурий', pos_b='noun', pos_a='adj')
        self.assertIn('меркурианский', results)

    def test_adj_632_11(self):
        results = self.derivation.derive(word_b='путь', pos_b='noun', pos_a='adj')
        self.assertIn('путейский', results)
        results = self.derivation.derive(word_b='Европа', pos_b='noun', pos_a='adj')
        self.assertIn('европейский', results)

    def test_adj_632_12(self):
        results = self.derivation.derive(word_b='Генуя', pos_b='noun', pos_a='adj')
        self.assertIn('генуэзский', results)
        results = self.derivation.derive(word_b='Ангола', pos_b='noun', pos_a='adj')
        self.assertIn('анголезский', results)
        results = self.derivation.derive(word_b='Конго', pos_b='noun', pos_a='adj')
        self.assertIn('конголезский', results)
        results = self.derivation.derive(word_b='Того', pos_b='noun', pos_a='adj')
        self.assertIn('тоголезский', results)

    def test_adj_632_13(self):
        results = self.derivation.derive(word_b='король', pos_b='noun', pos_a='adj')
        self.assertIn('королевский', results)

    def test_adj_632_14(self):
        results = self.derivation.derive(word_b='Брно', pos_b='noun', pos_a='adj')
        self.assertIn('брненский', results)

    def test_adj_632_15(self):
        results = self.derivation.derive(word_b='Уфа', pos_b='noun', pos_a='adj')
        self.assertIn('уфимский', results)

    def test_adj_632_16(self):
        results = self.derivation.derive(word_b='Выкса', pos_b='noun', pos_a='adj')
        self.assertIn('выксунский', results)

    def test_adj_632_17(self):
        results = self.derivation.derive(word_b='табу', pos_b='noun', pos_a='adj')
        self.assertIn('табуистический', results)

    def test_adj_632_18(self):
        results = self.derivation.derive(word_b='хохол', pos_b='noun', pos_a='adj')
        self.assertIn('хохлацкий', results)

    def test_adj_632_19(self):
        results = self.derivation.derive(word_b='Чикаго', pos_b='noun', pos_a='adj')
        self.assertIn('чикагский', results)
        results = self.derivation.derive(word_b='Миссисипи', pos_b='noun', pos_a='adj')
        self.assertIn('миссисипский', results)
        results = self.derivation.derive(word_b='саами', pos_b='noun', pos_a='adj')
        self.assertIn('саамский', results)
        results = self.derivation.derive(word_b='Урарту', pos_b='noun', pos_a='adj')
        self.assertIn('урартский', results)
        results = self.derivation.derive(word_b='Кошице', pos_b='noun', pos_a='adj')
        self.assertIn('кошицкий', results)
        results = self.derivation.derive(word_b='Кони', pos_b='noun', pos_a='adj')
        self.assertIn('коневский', results)
        results = self.derivation.derive(word_b='Цхакая', pos_b='noun', pos_a='adj')
        self.assertIn('цхакаевский', results)
        results = self.derivation.derive(word_b='Фрунзе', pos_b='noun', pos_a='adj')
        self.assertIn('фрунзенский', results)
        results = self.derivation.derive(word_b='Туапсе', pos_b='noun', pos_a='adj')
        self.assertIn('туапсинский', results)
        results = self.derivation.derive(word_b='Баку', pos_b='noun', pos_a='adj')
        self.assertIn('бакинский', results)
        results = self.derivation.derive(word_b='Сорренто', pos_b='noun', pos_a='adj')
        self.assertIn('соррентийский', results)

    def test_adj_632_20(self):
        results = self.derivation.derive(word_b='крещение', pos_b='noun', pos_a='adj')
        self.assertIn('крещенский', results)
        results = self.derivation.derive(word_b='поведение', pos_b='noun', pos_a='adj')
        self.assertIn('поведенческий', results)
        results = self.derivation.derive(word_b='канцелярия', pos_b='noun', pos_a='adj')
        self.assertIn('канцелярский', results)
        results = self.derivation.derive(word_b='гимназия', pos_b='noun', pos_a='adj')
        self.assertIn('гимназический', results)
        results = self.derivation.derive(word_b='Кахетия', pos_b='noun', pos_a='adj')
        self.assertIn('кахетинский', results)
        results = self.derivation.derive(word_b='пролетарий', pos_b='noun', pos_a='adj')
        self.assertIn('пролетарский', results)
        results = self.derivation.derive(word_b='евангелие', pos_b='noun', pos_a='adj')
        self.assertIn('евангельский', results)
        results = self.derivation.derive(word_b='амфибрахий', pos_b='noun', pos_a='adj')
        self.assertIn('амфибрахический', results)
        results = self.derivation.derive(word_b='Болонья', pos_b='noun', pos_a='adj')
        self.assertIn('болонский', results)
        results = self.derivation.derive(word_b='Севилья', pos_b='noun', pos_a='adj')
        self.assertIn('севильский', results)
        results = self.derivation.derive(word_b='Усолье', pos_b='noun', pos_a='adj')
        self.assertIn('усольский', results)
        results = self.derivation.derive(word_b='Щучье', pos_b='noun', pos_a='adj')
        self.assertIn('щучинский', results)
        results = self.derivation.derive(word_b='Заречье', pos_b='noun', pos_a='adj')
        self.assertIn('зареченский', results)
        results = self.derivation.derive(word_b='патриций', pos_b='noun', pos_a='adj')
        self.assertIn('патрицианский', results)

    def test_adj_632_21(self):
        results = self.derivation.derive(word_b='беженец', pos_b='noun', pos_a='adj')
        self.assertIn('беженский', results)
        results = self.derivation.derive(word_b='якобинец', pos_b='noun', pos_a='adj')
        self.assertIn('якобинский', results)
        results = self.derivation.derive(word_b='нанаец', pos_b='noun', pos_a='adj')
        self.assertIn('нанайский', results)

    def test_adj_632_22(self):
        results = self.derivation.derive(word_b='Дамаск', pos_b='noun', pos_a='adj')
        self.assertIn('дамасский', results)
        results = self.derivation.derive(word_b='этруски', pos_b='noun', pos_a='adj')
        self.assertIn('этрусский', results)
        results = self.derivation.derive(word_b='Сан-Франциско', pos_b='noun', pos_a='adj')
        self.assertIn('сан-францисский', results)

    def test_adj_632_23(self):
        results = self.derivation.derive(word_b='уравниловка', pos_b='noun', pos_a='adj')
        self.assertIn('уравниловский', results)
        results = self.derivation.derive(word_b='мальчишка', pos_b='noun', pos_a='adj')
        self.assertIn('мальчишеский', results)
        results = self.derivation.derive(word_b='Новогрудок', pos_b='noun', pos_a='adj')
        self.assertIn('новогрудский', results)

    def test_adj_632_24(self):
        results = self.derivation.derive(word_b='переводчик', pos_b='noun', pos_a='adj')
        self.assertIn('переводческий', results)

    def test_adj_632_25(self):
        results = self.derivation.derive(word_b='анахронизм', pos_b='noun', pos_a='adj')
        self.assertIn('анахронический', results)

    def test_adj_632_26(self):
        results = self.derivation.derive(word_b='космос', pos_b='noun', pos_a='adj')
        self.assertIn('космический', results)
        results = self.derivation.derive(word_b='синтаксис', pos_b='noun', pos_a='adj')
        self.assertIn('синтаксический', results)
        results = self.derivation.derive(word_b='апокалипсис', pos_b='noun', pos_a='adj')
        self.assertIn('апокалиптический', results)

    def test_adj_632_27(self):
        results = self.derivation.derive(word_b='женщина', pos_b='noun', pos_a='adj')
        self.assertIn('женский', results)
        results = self.derivation.derive(word_b='мужчина', pos_b='noun', pos_a='adj')
        self.assertIn('мужской', results)

    def test_adj_632_28(self):
        results = self.derivation.derive(word_b='свинья', pos_b='noun', pos_a='adj')
        self.assertIn('свинский', results)
        results = self.derivation.derive(word_b='каналья', pos_b='noun', pos_a='adj')
        self.assertIn('канальский', results)

    def test_adj_632_29(self):
        results = self.derivation.derive(word_b='Терек', pos_b='noun', pos_a='adj')
        self.assertIn('терский', results)
        results = self.derivation.derive(word_b='Польша', pos_b='noun', pos_a='adj')
        self.assertIn('польский', results)

    def test_adj_632_30(self):
        results = self.derivation.derive(word_b='язычник', pos_b='noun', pos_a='adj')
        self.assertIn('языческий', results)

    def test_adj_632_31(self):
        results = self.derivation.derive(word_b='господин', pos_b='noun', pos_a='adj')
        self.assertIn('господский', results)
        results = self.derivation.derive(word_b='татарин', pos_b='noun', pos_a='adj')
        self.assertIn('татарский', results)
        results = self.derivation.derive(word_b='крестьянин', pos_b='noun', pos_a='adj')
        self.assertIn('крестьянский', results)
        results = self.derivation.derive(word_b='хозяин', pos_b='noun', pos_a='adj')
        self.assertIn('хозяйский', results)

    def test_adj_632_32(self):
        results = self.derivation.derive(word_b='матерь', pos_b='noun', pos_a='adj')
        self.assertIn('материнский', results)
        results = self.derivation.derive(word_b='ребята', pos_b='noun', pos_a='adj')
        self.assertIn('ребяческий', results)

    def test_adj_632_33(self):
        results = self.derivation.derive(word_b='драма', pos_b='noun', pos_a='adj')
        self.assertIn('драматический', results)
        results = self.derivation.derive(word_b='симптом', pos_b='noun', pos_a='adj')
        self.assertIn('симптоматический', results)

    def test_adj_632_34(self):
        results = self.derivation.derive(word_b='арго', pos_b='noun', pos_a='adj')
        self.assertIn('арготический', results)

    def test_adj_632_35(self):
        results = self.derivation.derive(word_b='Неаполь', pos_b='noun', pos_a='adj')
        self.assertIn('неаполитанский', results)
        results = self.derivation.derive(word_b='негр', pos_b='noun', pos_a='adj')
        self.assertIn('негритянский', results)

    def test_adj_632_36(self):
        results = self.derivation.derive(word_b='персы', pos_b='noun', pos_a='adj')
        self.assertIn('персидский', results)

    def test_adj_632_37(self):
        results = self.derivation.derive(word_b='алгебра', pos_b='noun', pos_a='adj')
        self.assertIn('алгебраический', results)
        results = self.derivation.derive(word_b='проза', pos_b='noun', pos_a='adj')
        self.assertIn('прозаический', results)

    def test_adj_632_38(self):
        results = self.derivation.derive(word_b='захватчик', pos_b='noun', pos_a='adj')
        self.assertIn('захватнический', results)

    def test_adj_632_39(self):
        results = self.derivation.derive(word_b='турок', pos_b='noun', pos_a='adj')
        self.assertIn('турецкий', results)

    def test_adj_632_40(self):
        results = self.derivation.derive(word_b='депо', pos_b='noun', pos_a='adj')
        self.assertIn('деповский', results)
        results = self.derivation.derive(word_b='Пикассо', pos_b='noun', pos_a='adj')
        self.assertIn('пикассовский', results)
        results = self.derivation.derive(word_b='Гёте', pos_b='noun', pos_a='adj')
        self.assertIn('гётевский', results)
        results = self.derivation.derive(word_b='Лахти', pos_b='noun', pos_a='adj')
        self.assertIn('лахтинский', results)
        results = self.derivation.derive(word_b='Тольятти', pos_b='noun', pos_a='adj')
        self.assertIn('тольяттинский', results)
        results = self.derivation.derive(word_b='Гоа', pos_b='noun', pos_a='adj')
        self.assertIn('гоанский', results)
        results = self.derivation.derive(word_b='Никарагуа', pos_b='noun', pos_a='adj')
        self.assertIn('никарагуанский', results)
        results = self.derivation.derive(word_b='Чили', pos_b='noun', pos_a='adj')
        self.assertIn('чилийский', results)
        results = self.derivation.derive(word_b='Токио', pos_b='noun', pos_a='adj')
        self.assertIn('токийский', results)

    def test_adj_632_41(self):
        results = self.derivation.derive(word_b='Свердловск', pos_b='noun', pos_a='adj')
        self.assertIn('свердловский', results)
        results = self.derivation.derive(word_b='Донецк', pos_b='noun', pos_a='adj')
        self.assertIn('донецкий', results)
        results = self.derivation.derive(word_b='Белинский', pos_b='noun', pos_a='adj')
        self.assertIn('белинский', results)
        results = self.derivation.derive(word_b='Вешенская', pos_b='noun', pos_a='adj')
        self.assertIn('вешенский', results)

    def test_adj_632_42(self):
        results = self.derivation.derive(word_b='саксы', pos_b='noun', pos_a='adj')
        self.assertIn('сакский', results)
        results = self.derivation.derive(word_b='Прованс', pos_b='noun', pos_a='adj')
        self.assertIn('прованский', results)
        results = self.derivation.derive(word_b='Уэльс', pos_b='noun', pos_a='adj')
        self.assertIn('уэльский', results)
        results = self.derivation.derive(word_b='Пруссия', pos_b='noun', pos_a='adj')
        self.assertIn('прусский', results)
        results = self.derivation.derive(word_b='пруссы', pos_b='noun', pos_a='adj')
        self.assertIn('прусский', results)

    def test_adj_632_43(self):
        results = self.derivation.derive(word_b='ткач', pos_b='noun', pos_a='adj')
        self.assertIn('ткацкий', results)

    def test_adj_632_44(self):
        results = self.derivation.derive(word_b='чукчи', pos_b='noun', pos_a='adj')
        self.assertIn('чукотский', results)

    def test_adj_632_45(self):
        results = self.derivation.derive(word_b='ребята', pos_b='noun', pos_a='adj')
        self.assertIn('ребяческий', results)
        results = self.derivation.derive(word_b='студент', pos_b='noun', pos_a='adj')
        self.assertIn('студенческий', results)
        results = self.derivation.derive(word_b='метеорит', pos_b='noun', pos_a='adj')
        self.assertIn('метеорический', results)
        results = self.derivation.derive(word_b='князь', pos_b='noun', pos_a='adj')
        self.assertIn('княжеский', results)

    def test_adj_632_46(self):
        results = self.derivation.derive(word_b='Орда', pos_b='noun', pos_a='adj')
        self.assertIn('ордынский', results)

    def test_adj_632_47(self):
        results = self.derivation.derive(word_b='хаос', pos_b='noun', pos_a='adj')
        self.assertIn('хаотический', results)
        results = self.derivation.derive(word_b='анализ', pos_b='noun', pos_a='adj')
        self.assertIn('аналитический', results)
        results = self.derivation.derive(word_b='сарказм', pos_b='noun', pos_a='adj')
        self.assertIn('саркастический', results)
        results = self.derivation.derive(word_b='большевизм', pos_b='noun', pos_a='adj')
        self.assertIn('большевистский', results)

    def test_adj_632_48(self):
        results = self.derivation.derive(word_b='Флоренция', pos_b='noun', pos_a='adj')
        self.assertIn('флорентийский', results)
        results = self.derivation.derive(word_b='Далмация', pos_b='noun', pos_a='adj')
        self.assertIn('далматинский', results)

    def test_adj_632_49(self):
        results = self.derivation.derive(word_b='диагноз', pos_b='noun', pos_a='adj')
        self.assertIn('диагностический', results)
        results = self.derivation.derive(word_b='парафраз', pos_b='noun', pos_a='adj')
        self.assertIn('парафрастический', results)

    def test_adj_632_50(self):
        results = self.derivation.derive(word_b='юрист', pos_b='noun', pos_a='adj')
        self.assertIn('юридический', results)

    def test_adj_632_50(self):
        results = self.derivation.derive(word_b='деляга', pos_b='noun', pos_a='adj')
        self.assertIn('деляческий', results)

    def test_adj_632_51(self):
        results = self.derivation.derive(word_b='Дания', pos_b='noun', pos_a='adj')
        self.assertIn('датский', results)

    def test_adj_632_52(self):
        results = self.derivation.derive(word_b='деревня', pos_b='noun', pos_a='adj')
        self.assertIn('деревенский', results)
        results = self.derivation.derive(word_b='страдалец', pos_b='noun', pos_a='adj')
        self.assertIn('страдальческий', results)

    def test_adj_632_53(self):
        results = self.derivation.derive(word_b='отец', pos_b='noun', pos_a='adj')
        self.assertIn('отеческий', results)

    def test_adj_632_54(self):
        results = self.derivation.derive(word_b='министр', pos_b='noun', pos_a='adj')
        self.assertIn('министерский', results)
        results = self.derivation.derive(word_b='житьё', pos_b='noun', pos_a='adj')
        self.assertIn('житейский', results)
        results = self.derivation.derive(word_b='шляхта', pos_b='noun', pos_a='adj')
        self.assertIn('шляхетский', results)
        results = self.derivation.derive(word_b='Соловки', pos_b='noun', pos_a='adj')
        self.assertIn('соловецкий', results)
        results = self.derivation.derive(word_b='Венгрия', pos_b='noun', pos_a='adj')
        self.assertIn('венгерский', results)
        results = self.derivation.derive(word_b='чечня', pos_b='noun', pos_a='adj')
        self.assertIn('чеченский', results)

    def test_adj_632_55(self):
        results = self.derivation.derive(word_b='бургомистр', pos_b='noun', pos_a='adj')
        self.assertIn('бургомистерский', results)
        results = self.derivation.derive(word_b='магистр', pos_b='noun', pos_a='adj')
        self.assertIn('магистерский', results)
        results = self.derivation.derive(word_b='Коломна', pos_b='noun', pos_a='adj')
        self.assertIn('коломенский', results)
        results = self.derivation.derive(word_b='Вязьма', pos_b='noun', pos_a='adj')
        self.assertIn('вяземский', results)
        results = self.derivation.derive(word_b='Опочка', pos_b='noun', pos_a='adj')
        self.assertIn('опочецкий', results)
        results = self.derivation.derive(word_b='Песочня', pos_b='noun', pos_a='adj')
        self.assertIn('песоченский', results)

    def test_adj_632_56(self):
        results = self.derivation.derive(word_b='Москва', pos_b='noun', pos_a='adj')
        self.assertIn('московский', results)
        results = self.derivation.derive(word_b='Вологда', pos_b='noun', pos_a='adj')
        self.assertIn('вологодский', results)
        results = self.derivation.derive(word_b='Вытегра', pos_b='noun', pos_a='adj')
        self.assertIn('вытегорский', results)
        results = self.derivation.derive(word_b='Вычегда', pos_b='noun', pos_a='adj')
        self.assertIn('вычегодский', results)
        results = self.derivation.derive(word_b='Литва', pos_b='noun', pos_a='adj')
        self.assertIn('литовский', results)
        results = self.derivation.derive(word_b='мордва', pos_b='noun', pos_a='adj')
        self.assertIn('мордовский', results)
        results = self.derivation.derive(word_b='чухна', pos_b='noun', pos_a='adj')
        self.assertIn('чухонский', results)
        results = self.derivation.derive(word_b='угры', pos_b='noun', pos_a='adj')
        self.assertIn('угорский', results)
        results = self.derivation.derive(word_b='чукчи', pos_b='noun', pos_a='adj')
        self.assertIn('чукотский', results)

    def test_adj_632_57(self):
        results = self.derivation.derive(word_b='армия', pos_b='noun', pos_a='adj')
        self.assertIn('армейский', results)
        results = self.derivation.derive(word_b='библия', pos_b='noun', pos_a='adj')
        self.assertIn('библейский', results)
        results = self.derivation.derive(word_b='артиллерия', pos_b='noun', pos_a='adj')
        self.assertIn('артиллерийский', results)

    def test_adj_632_58(self):
        results = self.derivation.derive(word_b='Италия', pos_b='noun', pos_a='adj')
        self.assertIn('итальянский', results)

    def test_adj_636(self):
        results = self.derivation.derive(word_b='Кант', pos_b='noun', pos_a='adj')
        self.assertIn('кантианский', results)
        results = self.derivation.derive(word_b='Фейербах', pos_b='noun', pos_a='adj')
        self.assertIn('фейербахианский', results)
        results = self.derivation.derive(word_b='Ломброзо', pos_b='noun', pos_a='adj')
        self.assertIn('ломброзианский', results)

    def test_adj_636_2(self):
        results = self.derivation.derive(word_b='Мальтус', pos_b='noun', pos_a='adj')
        self.assertIn('мальтузианский', results)

    def test_adj_636_3(self):
        results = self.derivation.derive(word_b='Вольтер', pos_b='noun', pos_a='adj')
        self.assertIn('вольтерьянский', results)
        results = self.derivation.derive(word_b='Гегель', pos_b='noun', pos_a='adj')
        self.assertIn('гегельянский', results)
        results = self.derivation.derive(word_b='Фихте', pos_b='noun', pos_a='adj')
        self.assertIn('фихтеанский', results)
        results = self.derivation.derive(word_b='Ницше', pos_b='noun', pos_a='adj')
        self.assertIn('ницшеанский', results)
        results = self.derivation.derive(word_b='Конфуций', pos_b='noun', pos_a='adj')
        self.assertIn('конфуцианский', results)

    def test_adj_636_4(self):
        results = self.derivation.derive(word_b='Вакх', pos_b='noun', pos_a='adj')
        self.assertIn('вакхический', results)
        results = self.derivation.derive(word_b='Байрон', pos_b='noun', pos_a='adj')
        self.assertIn('байронический', results)

    def test_adj_636_5(self):
        results = self.derivation.derive(word_b='Будда', pos_b='noun', pos_a='adj')
        self.assertIn('буддийский', results)

    def test_adj_636_6(self):
        results = self.derivation.derive(word_b='Пифагор', pos_b='noun', pos_a='adj')
        self.assertIn('пифагорейский', results)

    def test_adj_637(self):
        results = self.derivation.derive(word_b='голова', pos_b='noun', pos_a='adj')
        self.assertIn('головастый', results)
        results = self.derivation.derive(word_b='лоб', pos_b='noun', pos_a='adj')
        self.assertIn('лобастый', results)
        results = self.derivation.derive(word_b='горло', pos_b='noun', pos_a='adj')
        self.assertIn('горластый', results)
        results = self.derivation.derive(word_b='ноздря', pos_b='noun', pos_a='adj')
        self.assertIn('ноздрястый', results)
        results = self.derivation.derive(word_b='щека', pos_b='noun', pos_a='adj')
        self.assertIn('щекастый', results)
        results = self.derivation.derive(word_b='язык', pos_b='noun', pos_a='adj')
        self.assertIn('языкастый', results)
        results = self.derivation.derive(word_b='ухо', pos_b='noun', pos_a='adj')
        self.assertIn('ушастый', results)
        results = self.derivation.derive(word_b='щель', pos_b='noun', pos_a='adj')
        self.assertIn('щелястый', results)
        results = self.derivation.derive(word_b='мышь', pos_b='noun', pos_a='adj')
        self.assertIn('мышастый', results)
        results = self.derivation.derive(word_b='очки', pos_b='noun', pos_a='adj')
        self.assertIn('очкастый', results)
        results = self.derivation.derive(word_b='грудь', pos_b='noun', pos_a='adj')
        self.assertIn('грудастый', results)

    def test_adj_637_2(self):
        results = self.derivation.derive(word_b='вихор', pos_b='noun', pos_a='adj')
        self.assertIn('вихрастый', results)
        results = self.derivation.derive(word_b='пенсне', pos_b='noun', pos_a='adj')
        self.assertIn('пенснястый', results)

    def test_adj_638(self):
        results = self.derivation.derive(word_b='зуб', pos_b='noun', pos_a='adj')
        self.assertIn('зубатый', results)
        results = self.derivation.derive(word_b='борода', pos_b='noun', pos_a='adj')
        self.assertIn('бородатый', results)
        results = self.derivation.derive(word_b='гор', pos_b='noun', pos_a='adj')
        self.assertIn('рогатый', results)
        results = self.derivation.derive(word_b='хохол', pos_b='noun', pos_a='adj')
        self.assertIn('хохлатый', results)
        results = self.derivation.derive(word_b='язык', pos_b='noun', pos_a='adj')
        self.assertIn('языкатый', results)
        results = self.derivation.derive(word_b='пузо', pos_b='noun', pos_a='adj')
        self.assertIn('пузатый', results)
        results = self.derivation.derive(word_b='брюхо', pos_b='noun', pos_a='adj')
        self.assertIn('брюхатый', results)

    def test_adj_638_2(self):
        results = self.derivation.derive(word_b='внук', pos_b='noun', pos_a='adj')
        self.assertIn('внучатый', results)

    def test_adj_638_3(self):
        results = self.derivation.derive(word_b='щербина', pos_b='noun', pos_a='adj')
        self.assertIn('щербатый', results)
        results = self.derivation.derive(word_b='желвак', pos_b='noun', pos_a='adj')
        self.assertIn('желватый', results)

    def test_adj_638_4(self):
        results = self.derivation.derive(word_b='перо', pos_b='noun', pos_a='adj')
        self.assertIn('пернатый', results)

    def test_adj_639(self):
        results = self.derivation.derive(word_b='свод', pos_b='noun', pos_a='adj')
        self.assertIn('сводчатый', results)
        results = self.derivation.derive(word_b='бахрома', pos_b='noun', pos_a='adj')
        self.assertIn('бахромчатый', results)
        results = self.derivation.derive(word_b='колено', pos_b='noun', pos_a='adj')
        self.assertIn('коленчатый', results)
        results = self.derivation.derive(word_b='материя', pos_b='noun', pos_a='adj')
        self.assertIn('матерчатый', results)
        results = self.derivation.derive(word_b='нить', pos_b='noun', pos_a='adj')
        self.assertIn('нитчатый', results)
        results = self.derivation.derive(word_b='бревно', pos_b='noun', pos_a='adj')
        self.assertIn('бревенчатый', results)
        results = self.derivation.derive(word_b='доска', pos_b='noun', pos_a='adj')
        self.assertIn('дощатый', results)
        results = self.derivation.derive(word_b='зубец', pos_b='noun', pos_a='adj')
        self.assertIn('зубчатый', results)
        results = self.derivation.derive(word_b='крупица', pos_b='noun', pos_a='adj')
        self.assertIn('крупчатый', results)
        results = self.derivation.derive(word_b='бугорок', pos_b='noun', pos_a='adj')
        self.assertIn('бугорчатый', results)
        results = self.derivation.derive(word_b='желёзка', pos_b='noun', pos_a='adj')
        self.assertIn('желёзчатый', results)
        results = self.derivation.derive(word_b='веснушки', pos_b='noun', pos_a='adj')
        self.assertIn('веснушчатый', results)
        results = self.derivation.derive(word_b='кубышка', pos_b='noun', pos_a='adj')
        self.assertIn('кубышчатый', results)

    def test_adj_639_2(self):
        results = self.derivation.derive(word_b='губка', pos_b='noun', pos_a='adj')
        self.assertIn('губчатый', results)
        results = self.derivation.derive(word_b='ресница', pos_b='noun', pos_a='adj')
        self.assertIn('реснитчатый', results)
        results = self.derivation.derive(word_b='вилы', pos_b='noun', pos_a='adj')
        self.assertIn('вильчатый', results)
        results = self.derivation.derive(word_b='стрелка', pos_b='noun', pos_a='adj')
        self.assertIn('стрельчатый', results)
        results = self.derivation.derive(word_b='угол', pos_b='noun', pos_a='adj')
        self.assertIn('угольчатый', results)
        results = self.derivation.derive(word_b='глазок', pos_b='noun', pos_a='adj')
        self.assertIn('глазчатый', results)
        results = self.derivation.derive(word_b='хлопья', pos_b='noun', pos_a='adj')
        self.assertIn('хлопчатый', results)

    def test_adj_639_3(self):
        results = self.derivation.derive(word_b='крапина', pos_b='noun', pos_a='adj')
        self.assertIn('крапчатый', results)

    def test_adj_640(self):
        results = self.derivation.derive(word_b='игла', pos_b='noun', pos_a='adj')
        self.assertIn('игловатый', results)
        results = self.derivation.derive(word_b='плут', pos_b='noun', pos_a='adj')
        self.assertIn('плутоватый', results)
        results = self.derivation.derive(word_b='стекло', pos_b='noun', pos_a='adj')
        self.assertIn('стекловатый', results)
        results = self.derivation.derive(word_b='щеголь', pos_b='noun', pos_a='adj')
        self.assertIn('щеголеватый', results)
        results = self.derivation.derive(word_b='кочка', pos_b='noun', pos_a='adj')
        self.assertIn('кочковатый', results)
        results = self.derivation.derive(word_b='мужик', pos_b='noun', pos_a='adj')
        self.assertIn('мужиковатый', results)
        results = self.derivation.derive(word_b='крючок', pos_b='noun', pos_a='adj')
        self.assertIn('крючковатый', results)
        results = self.derivation.derive(word_b='прыщ', pos_b='noun', pos_a='adj')
        self.assertIn('прыщеватый', results)
        results = self.derivation.derive(word_b='солнце', pos_b='noun', pos_a='adj')
        self.assertIn('солнцеватый', results)
        results = self.derivation.derive(word_b='молодец', pos_b='noun', pos_a='adj')
        self.assertIn('молодцеватый', results)
        results = self.derivation.derive(word_b='пыль', pos_b='noun', pos_a='adj')
        self.assertIn('пылеватый', results)
        results = self.derivation.derive(word_b='кудри', pos_b='noun', pos_a='adj')
        self.assertIn('кудреватый', results)

    def test_adj_640_2(self):
        results = self.derivation.derive(word_b='смола', pos_b='noun', pos_a='adj')
        self.assertIn('смолеватый', results)
        results = self.derivation.derive(word_b='зверь', pos_b='noun', pos_a='adj')
        self.assertIn('звероватый', results)

    def test_adj_640_3(self):
        results = self.derivation.derive(word_b='веснушки', pos_b='noun', pos_a='adj')
        self.assertIn('весноватый', results)

    def test_adj_640_4(self):
        results = self.derivation.derive(word_b='бес', pos_b='noun', pos_a='adj')
        self.assertIn('бесноватый', results)

    def test_adj_641(self):
        results = self.derivation.derive(word_b='дар', pos_b='noun', pos_a='adj')
        self.assertIn('даровитый', results)
        results = self.derivation.derive(word_b='башка', pos_b='noun', pos_a='adj')
        self.assertIn('башковитый', results)
        results = self.derivation.derive(word_b='пух', pos_b='noun', pos_a='adj')
        self.assertIn('пуховитый', results)
        results = self.derivation.derive(word_b='бочок', pos_b='noun', pos_a='adj')
        self.assertIn('бочковитый', results)
        results = self.derivation.derive(word_b='дкло', pos_b='noun', pos_a='adj')
        self.assertIn('деловитый', results)
        results = self.derivation.derive(word_b='глянец', pos_b='noun', pos_a='adj')
        self.assertIn('глянцевитый', results)

    def test_adj_642(self):
        results = self.derivation.derive(word_b='морщина', pos_b='noun', pos_a='adj')
        self.assertIn('морщинистый', results)
        results = self.derivation.derive(word_b='лёд', pos_b='noun', pos_a='adj')
        self.assertIn('льдистый', results)
        results = self.derivation.derive(word_b='дупло', pos_b='noun', pos_a='adj')
        self.assertIn('дуплистый', results)
        results = self.derivation.derive(word_b='коготь', pos_b='noun', pos_a='adj')
        self.assertIn('когтистый', results)
        results = self.derivation.derive(word_b='творог', pos_b='noun', pos_a='adj')
        self.assertIn('творожистый', results)
        results = self.derivation.derive(word_b='ёрш', pos_b='noun', pos_a='adj')
        self.assertIn('ершистый', results)
        results = self.derivation.derive(word_b='плечо', pos_b='noun', pos_a='adj')
        self.assertIn('плечистый', results)
        results = self.derivation.derive(word_b='змея', pos_b='noun', pos_a='adj')
        self.assertIn('змеистый', results)
        results = self.derivation.derive(word_b='слой', pos_b='noun', pos_a='adj')
        self.assertIn('слоистый', results)
        results = self.derivation.derive(word_b='тень', pos_b='noun', pos_a='adj')
        self.assertIn('тенистый', results)
        results = self.derivation.derive(word_b='мускулы', pos_b='noun', pos_a='adj')
        self.assertIn('мускулистый', results)
        results = self.derivation.derive(word_b='чутьё', pos_b='noun', pos_a='adj')
        self.assertIn('чутьистый', results)
        results = self.derivation.derive(word_b='суглинок', pos_b='noun', pos_a='adj')
        self.assertIn('суглинистый', results)
        results = self.derivation.derive(word_b='сноровка', pos_b='noun', pos_a='adj')
        self.assertIn('сноровистый', results)
        results = self.derivation.derive(word_b='терние', pos_b='noun', pos_a='adj')
        self.assertIn('тернистый', results)
        results = self.derivation.derive(word_b='кремний', pos_b='noun', pos_a='adj')
        self.assertIn('кремнистый', results)

    def test_adj_642_2(self):
        results = self.derivation.derive(word_b='седловина', pos_b='noun', pos_a='adj')
        self.assertIn('седлистый', results)
        results = self.derivation.derive(word_b='скважина', pos_b='noun', pos_a='adj')
        self.assertIn('скважистый', results)
        results = self.derivation.derive(word_b='щетина', pos_b='noun', pos_a='adj')
        self.assertIn('щетинистый', results)

    def test_adj_642_3(self):
        results = self.derivation.derive(word_b='ущелье', pos_b='noun', pos_a='adj')
        self.assertIn('ущелистый', results)
        results = self.derivation.derive(word_b='иней', pos_b='noun', pos_a='adj')
        self.assertIn('инистый', results)

    def test_adj_642_4(self):
        results = self.derivation.derive(word_b='шаг', pos_b='noun', pos_a='adj')
        self.assertIn('шагистый', results)

    def test_adj_642_5(self):
        results = self.derivation.derive(word_b='камень', pos_b='noun', pos_a='adj')
        self.assertIn('каменистый', results)

    def test_adj_643(self):
        results = self.derivation.derive(word_b='слеза', pos_b='noun', pos_a='adj')
        self.assertIn('слезливый', results)
        results = self.derivation.derive(word_b='плакса', pos_b='noun', pos_a='adj')
        self.assertIn('плаксивый', results)
        results = self.derivation.derive(word_b='талант', pos_b='noun', pos_a='adj')
        self.assertIn('талантливый', results)
        results = self.derivation.derive(word_b='сопля', pos_b='noun', pos_a='adj')
        self.assertIn('сопливый', results)
        results = self.derivation.derive(word_b='дождь', pos_b='noun', pos_a='adj')
        self.assertIn('дождливый', results)
        results = self.derivation.derive(word_b='засуха', pos_b='noun', pos_a='adj')
        self.assertIn('засушливый', results)
        results = self.derivation.derive(word_b='зяблик', pos_b='noun', pos_a='adj')
        self.assertIn('зябличивый', results)
        results = self.derivation.derive(word_b='добыча', pos_b='noun', pos_a='adj')
        self.assertIn('добычливый', results)
        results = self.derivation.derive(word_b='затея', pos_b='noun', pos_a='adj')
        self.assertIn('затейливый', results)
        results = self.derivation.derive(word_b='совесть', pos_b='noun', pos_a='adj')
        self.assertIn('совестливый', results)
        results = self.derivation.derive(word_b='фальшь', pos_b='noun', pos_a='adj')
        self.assertIn('фальшивый', results)
        results = self.derivation.derive(word_b='удой', pos_b='noun', pos_a='adj')
        self.assertIn('удойливый', results)
        results = self.derivation.derive(word_b='ложь', pos_b='noun', pos_a='adj')
        self.assertIn('лживый', results)
        results = self.derivation.derive(word_b='червь', pos_b='noun', pos_a='adj')
        self.assertIn('червивый', results)
        results = self.derivation.derive(word_b='противоречие', pos_b='noun', pos_a='adj')
        self.assertIn('противоречивый', results)
        results = self.derivation.derive(word_b='вша', pos_b='noun', pos_a='adj')
        self.assertIn('вшивый', results)

    def test_adj_643_2(self):
        results = self.derivation.derive(word_b='боязнь', pos_b='noun', pos_a='adj')
        self.assertIn('боязливый', results)

    def test_adj_643_3(self):
        results = self.derivation.derive(word_b='тоска', pos_b='noun', pos_a='adj')
        self.assertIn('тоскливый', results)
        results = self.derivation.derive(word_b='визг', pos_b='noun', pos_a='adj')
        self.assertIn('визгливый', results)
        results = self.derivation.derive(word_b='крик', pos_b='noun', pos_a='adj')
        self.assertIn('крикливый', results)

    def test_adj_643_4(self):
        results = self.derivation.derive(word_b='ребята', pos_b='noun', pos_a='adj')
        self.assertIn('ребячливый', results)

    def test_adj_643_5(self):
        results = self.derivation.derive(word_b='участие', pos_b='noun', pos_a='adj')
        self.assertIn('участливый', results)
        results = self.derivation.derive(word_b='счастье', pos_b='noun', pos_a='adj')
        self.assertIn('счастливый', results)
        results = self.derivation.derive(word_b='смётка', pos_b='noun', pos_a='adj')
        self.assertIn('сметливый', results)

    def test_adj_644(self):
        results = self.derivation.derive(word_b='ржа', pos_b='noun', pos_a='adj')
        self.assertIn('ржавый', results)
        results = self.derivation.derive(word_b='прыщ', pos_b='noun', pos_a='adj')
        self.assertIn('прыщавый', results)
        results = self.derivation.derive(word_b='слюна', pos_b='noun', pos_a='adj')
        self.assertIn('слюнявый', results)
        results = self.derivation.derive(word_b='кудри', pos_b='noun', pos_a='adj')
        self.assertIn('кудрявый', results)
        results = self.derivation.derive(word_b='писк', pos_b='noun', pos_a='adj')
        self.assertIn('писклявый', results)
        results = self.derivation.derive(word_b='труха', pos_b='noun', pos_a='adj')
        self.assertIn('трухлявый', results)
        results = self.derivation.derive(word_b='кости', pos_b='noun', pos_a='adj')
        self.assertIn('костлявый', results)
        results = self.derivation.derive(word_b='сучья', pos_b='noun', pos_a='adj')
        self.assertIn('сучлявый', results)

    def test_adj_644_2(self):
        results = self.derivation.derive(word_b='кровь', pos_b='noun', pos_a='adj')
        self.assertIn('кровавый', results)
        results = self.derivation.derive(word_b='дыра', pos_b='noun', pos_a='adj')
        self.assertIn('дырявый', results)

    def test_adj_644_3(self):
        results = self.derivation.derive(word_b='величие', pos_b='noun', pos_a='adj')
        self.assertIn('величавый', results)

    def test_adj_645_1(self):
        results = self.derivation.derive(word_b='жар', pos_b='noun', pos_a='adj')
        self.assertIn('жаркий', results)
        results = self.derivation.derive(word_b='жара', pos_b='noun', pos_a='adj')
        self.assertIn('жаркий', results)
        results = self.derivation.derive(word_b='зной', pos_b='noun', pos_a='adj')
        self.assertIn('знойкий', results)

    def test_adj_645_2(self):
        results = self.derivation.derive(word_b='зрение', pos_b='noun', pos_a='adj')
        self.assertIn('зоркий', results)

    def test_adj_645_3(self):
        results = self.derivation.derive(word_b='зрение', pos_b='noun', pos_a='adj')
        self.assertIn('зрячий', results)

    def test_adj_645_4(self):
        results = self.derivation.derive(word_b='зрение', pos_b='noun', pos_a='adj')
        self.assertIn('зримый', results)

    def test_adj_645_5(self):
        results = self.derivation.derive(word_b='круг', pos_b='noun', pos_a='adj')
        self.assertIn('круглый', results)
        results = self.derivation.derive(word_b='свет', pos_b='noun', pos_a='adj')
        self.assertIn('светлый', results)

    def test_adj_645_6(self):
        results = self.derivation.derive(word_b='год', pos_b='noun', pos_a='adj')
        self.assertIn('годовалый', results)

    def test_adj_645_7(self):
        results = self.derivation.derive(word_b='имя', pos_b='noun', pos_a='adj')
        self.assertIn('именитый', results)

    def test_adj_646(self):
        results = self.derivation.derive(word_b='болеть', pos_b='verb', pos_a='adj')
        self.assertIn('больной', results)
        results = self.derivation.derive(word_b='чваниться', pos_b='verb', pos_a='adj')
        self.assertIn('чванный', results)
        results = self.derivation.derive(word_b='склоняться', pos_b='verb', pos_a='adj')
        self.assertIn('склонный', results)
        results = self.derivation.derive(word_b='заметить', pos_b='verb', pos_a='adj')
        self.assertIn('заметный', results)
        results = self.derivation.derive(word_b='завидовать', pos_b='verb', pos_a='adj')
        self.assertIn('завидный', results)
        results = self.derivation.derive(word_b='связывать', pos_b='verb', pos_a='adj')
        self.assertIn('связной', results)
        results = self.derivation.derive(word_b='закраивать', pos_b='verb', pos_a='adj')
        self.assertIn('закройный', results)
        results = self.derivation.derive(word_b='доить', pos_b='verb', pos_a='adj')
        self.assertIn('дойный', results)
        results = self.derivation.derive(word_b='раздвигать', pos_b='verb', pos_a='adj')
        self.assertIn('раздвижной', results)
        results = self.derivation.derive(word_b='составить', pos_b='verb', pos_a='adj')
        self.assertIn('составной', results)
        results = self.derivation.derive(word_b='привыкнуть', pos_b='verb', pos_a='adj')
        self.assertIn('привычный', results)
        results = self.derivation.derive(word_b='напускать', pos_b='verb', pos_a='adj')
        self.assertIn('напускной', results)

    def test_adj_646_2(self):
        results = self.derivation.derive(word_b='действовать', pos_b='verb', pos_a='adj')
        self.assertIn('действенный', results)
        results = self.derivation.derive(word_b='прочувствовать', pos_b='verb', pos_a='adj')
        self.assertIn('прочувственный', results)
        results = self.derivation.derive(word_b='почитать', pos_b='verb', pos_a='adj')
        self.assertIn('почтенный', results)
        results = self.derivation.derive(word_b='согнуться', pos_b='verb', pos_a='adj')
        self.assertIn('согбенный', results)
        results = self.derivation.derive(word_b='проникнуть', pos_b='verb', pos_a='adj')
        self.assertIn('проникновенный', results)
        results = self.derivation.derive(word_b='дерзнуть', pos_b='verb', pos_a='adj')
        self.assertIn('дерзновенный', results)
        results = self.derivation.derive(word_b='открыться', pos_b='verb', pos_a='adj')
        self.assertIn('откровенный', results)

    def test_adj_646_3(self):
        results = self.derivation.derive(word_b='сбыться', pos_b='verb', pos_a='adj')
        self.assertIn('сбыточный', results)
        results = self.derivation.derive(word_b='раздать', pos_b='verb', pos_a='adj')
        self.assertIn('раздаточный', results)
        results = self.derivation.derive(word_b='достать', pos_b='verb', pos_a='adj')
        self.assertIn('достаточный', results)
        results = self.derivation.derive(word_b='распивать', pos_b='verb', pos_a='adj')
        self.assertIn('распивочный', results)

    def test_adj_646_4(self):
        results = self.derivation.derive(word_b='лечить', pos_b='verb', pos_a='adj')
        self.assertIn('лечебный', results)

    def test_adj_646_5(self):
        results = self.derivation.derive(word_b='съесть', pos_b='verb', pos_a='adj')
        self.assertIn('съедобный', results)

    def test_adj_646_6(self):
        results = self.derivation.derive(word_b='мешкать', pos_b='verb', pos_a='adj')
        self.assertIn('мешкотный', results)

    def test_adj_646_7(self):
        results = self.derivation.derive(word_b='шить', pos_b='verb', pos_a='adj')
        self.assertIn('швейный', results)
        results = self.derivation.derive(word_b='плести', pos_b='verb', pos_a='adj')
        self.assertIn('плетейный', results)

    def test_adj_646_8(self):
        results = self.derivation.derive(word_b='ответить', pos_b='verb', pos_a='adj')
        self.assertIn('ответственный', results)
        results = self.derivation.derive(word_b='благодарить', pos_b='verb', pos_a='adj')
        self.assertIn('благодарственный', results)

    def test_adj_646_9(self):
        results = self.derivation.derive(word_b='знать', pos_b='verb', pos_a='adj')
        self.assertIn('знатный', results)
        results = self.derivation.derive(word_b='слить', pos_b='verb', pos_a='adj')
        self.assertIn('слитный', results)

    def test_adj_646_10(self):
        results = self.derivation.derive(word_b='убить', pos_b='verb', pos_a='adj')
        self.assertIn('убойный', results)

    def test_adj_646_11(self):
        results = self.derivation.derive(word_b='покрыть', pos_b='verb', pos_a='adj')
        self.assertIn('покровный', results)

    def test_adj_646_12(self):
        results = self.derivation.derive(word_b='беречь', pos_b='verb', pos_a='adj')
        self.assertIn('бережный', results)
        results = self.derivation.derive(word_b='грести', pos_b='verb', pos_a='adj')
        self.assertIn('гребной', results)
        results = self.derivation.derive(word_b='надоесть', pos_b='verb', pos_a='adj')
        self.assertIn('надоедный', results)
        results = self.derivation.derive(word_b='вырасти', pos_b='verb', pos_a='adj')
        self.assertIn('выростной', results)
        results = self.derivation.derive(word_b='нажить', pos_b='verb', pos_a='adj')
        self.assertIn('наживной', results)
        results = self.derivation.derive(word_b='расстаться', pos_b='verb', pos_a='adj')
        self.assertIn('расстанный', results)

    def test_adj_646_13(self):
        results = self.derivation.derive(word_b='шить', pos_b='verb', pos_a='adj')
        self.assertIn('швейный', results)
        results = self.derivation.derive(word_b='посеять', pos_b='verb', pos_a='adj')
        self.assertIn('посевной', results)
        results = self.derivation.derive(word_b='надеяться', pos_b='verb', pos_a='adj')
        self.assertIn('надёжный', results)

    def test_adj_646_14(self):
        results = self.derivation.derive(word_b='отобрать', pos_b='verb', pos_a='adj')
        self.assertIn('отборный', results)
        results = self.derivation.derive(word_b='отбирать', pos_b='verb', pos_a='adj')
        self.assertIn('отборный', results)
        results = self.derivation.derive(word_b='упереться', pos_b='verb', pos_a='adj')
        self.assertIn('упорный', results)
        results = self.derivation.derive(word_b='упираться', pos_b='verb', pos_a='adj')
        self.assertIn('упорный', results)
        results = self.derivation.derive(word_b='обожраться', pos_b='verb', pos_a='adj')
        self.assertIn('обжорный', results)
        results = self.derivation.derive(word_b='обжираться', pos_b='verb', pos_a='adj')
        self.assertIn('обжорный', results)
        results = self.derivation.derive(word_b='счесть', pos_b='verb', pos_a='adj')
        self.assertIn('счётный', results)
        results = self.derivation.derive(word_b='считать', pos_b='verb', pos_a='adj')
        self.assertIn('счётный', results)

    def test_adj_646_15(self):
        results = self.derivation.derive(word_b='снять', pos_b='verb', pos_a='adj')
        self.assertIn('съёмный', results)
        results = self.derivation.derive(word_b='снимать', pos_b='verb', pos_a='adj')
        self.assertIn('съёмный', results)
        results = self.derivation.derive(word_b='притечь', pos_b='verb', pos_a='adj')
        self.assertIn('приточный', results)

    def test_adj_646_16(self):
        results = self.derivation.derive(word_b='почтить', pos_b='verb', pos_a='adj')
        self.assertIn('почтенный', results)
        results = self.derivation.derive(word_b='почитать', pos_b='verb', pos_a='adj')
        self.assertIn('почтенный', results)

    def test_adj_646_17(self):
        results = self.derivation.derive(word_b='проезжать', pos_b='verb', pos_a='adj')
        self.assertIn('проездной', results)

    def test_adj_651(self):
        results = self.derivation.derive(word_b='страдать', pos_b='verb', pos_a='adj')
        self.assertIn('страдальный', results)
        results = self.derivation.derive(word_b='рисовать', pos_b='verb', pos_a='adj')
        self.assertIn('рисовальный', results)
        results = self.derivation.derive(word_b='родить', pos_b='verb', pos_a='adj')
        self.assertIn('родильный', results)
        results = self.derivation.derive(word_b='вязать', pos_b='verb', pos_a='adj')
        self.assertIn('вязальный', results)
        results = self.derivation.derive(word_b='спать', pos_b='verb', pos_a='adj')
        self.assertIn('спальный', results)

    def test_adj_651_2(self):
        results = self.derivation.derive(word_b='трясти', pos_b='verb', pos_a='adj')
        self.assertIn('трясильный', results)
        results = self.derivation.derive(word_b='прясть', pos_b='verb', pos_a='adj')
        self.assertIn('прядильный', results)
        results = self.derivation.derive(word_b='плести', pos_b='verb', pos_a='adj')
        self.assertIn('плетельный', results)
        results = self.derivation.derive(word_b='лить', pos_b='verb', pos_a='adj')
        self.assertIn('льяльный', results)
        results = self.derivation.derive(word_b='тянуть', pos_b='verb', pos_a='adj')
        self.assertIn('тягальный', results)

    def test_adj_651_3(self):
        results = self.derivation.derive(word_b='молиться', pos_b='verb', pos_a='adj')
        self.assertIn('молельный', results)
        results = self.derivation.derive(word_b='складывать', pos_b='verb', pos_a='adj')
        self.assertIn('складальный', results)

    def test_adj_652_1(self):
        results = self.derivation.derive(word_b='удовлетворить', pos_b='verb', pos_a='adj')
        self.assertIn('удовлетворительный', results)
        results = self.derivation.derive(word_b='оправдать', pos_b='verb', pos_a='adj')
        self.assertIn('оправдательный', results)
        results = self.derivation.derive(word_b='желать', pos_b='verb', pos_a='adj')
        self.assertIn('желательный', results)
        results = self.derivation.derive(word_b='требовать', pos_b='verb', pos_a='adj')
        self.assertIn('требовательный', results)
        results = self.derivation.derive(word_b='владеть', pos_b='verb', pos_a='adj')
        self.assertIn('владетельный', results)
        results = self.derivation.derive(word_b='живить', pos_b='verb', pos_a='adj')
        self.assertIn('живительный', results)
        results = self.derivation.derive(word_b='воспалиться', pos_b='verb', pos_a='adj')
        self.assertIn('воспалительный', results)

    def test_adj_652_1_2(self):
        results = self.derivation.derive(word_b='окончить', pos_b='verb', pos_a='adj')
        self.assertIn('окончательный', results)
        results = self.derivation.derive(word_b='притягивать', pos_b='verb', pos_a='adj')
        self.assertIn('притягательный', results)
        results = self.derivation.derive(word_b='знаменовать', pos_b='verb', pos_a='adj')
        self.assertIn('знаменательный', results)
        results = self.derivation.derive(word_b='рекомендовать', pos_b='verb', pos_a='adj')
        self.assertIn('рекомендательный', results)
        results = self.derivation.derive(word_b='дышать', pos_b='verb', pos_a='adj')
        self.assertIn('дыхательный', results)

    def test_adj_652_2(self):
        results = self.derivation.derive(word_b='повелеть', pos_b='verb', pos_a='adj')
        self.assertIn('повелительный', results)
        results = self.derivation.derive(word_b='осмотреть', pos_b='verb', pos_a='adj')
        self.assertIn('осмотрительный', results)
        results = self.derivation.derive(word_b='спасти', pos_b='verb', pos_a='adj')
        self.assertIn('спасительный', results)
        results = self.derivation.derive(word_b='пренебречь', pos_b='verb', pos_a='adj')
        self.assertIn('пренебрежительный', results)
        results = self.derivation.derive(word_b='предпочесть', pos_b='verb', pos_a='adj')
        self.assertIn('предпочтительный', results)
        results = self.derivation.derive(word_b='расти', pos_b='verb', pos_a='adj')
        self.assertIn('растительный', results)
        results = self.derivation.derive(word_b='общаться', pos_b='verb', pos_a='adj')
        self.assertIn('общительный', results)
        results = self.derivation.derive(word_b='увольнять', pos_b='verb', pos_a='adj')
        self.assertIn('увольнительный', results)
        results = self.derivation.derive(word_b='действовать', pos_b='verb', pos_a='adj')
        self.assertIn('действительный', results)
        results = self.derivation.derive(word_b='подозревать', pos_b='verb', pos_a='adj')
        self.assertIn('подозрительный', results)

    def test_adj_653_1(self):
        results = self.derivation.derive(word_b='печатать', pos_b='verb', pos_a='adj')
        self.assertIn('печатабельный', results)
        results = self.derivation.derive(word_b='оперировать', pos_b='verb', pos_a='adj')
        self.assertIn('операбельный', results)

    def test_adj_653_2(self):
        results = self.derivation.derive(word_b='смотреть', pos_b='verb', pos_a='adj')
        self.assertIn('смотрибельный', results)

    def test_adj_654(self):
        results = self.derivation.derive(word_b='бросать', pos_b='verb', pos_a='adj')
        self.assertIn('бросовый', results)
        results = self.derivation.derive(word_b='скакать', pos_b='verb', pos_a='adj')
        self.assertIn('скаковой', results)
        results = self.derivation.derive(word_b='гулять', pos_b='verb', pos_a='adj')
        self.assertIn('гулевой', results)
        results = self.derivation.derive(word_b='ходить', pos_b='verb', pos_a='adj')
        self.assertIn('ходовой', results)
        results = self.derivation.derive(word_b='грызть', pos_b='verb', pos_a='adj')
        self.assertIn('грызовой', results)
        results = self.derivation.derive(word_b='плясать', pos_b='verb', pos_a='adj')
        self.assertIn('плясовой', results)
        results = self.derivation.derive(word_b='казать', pos_b='verb', pos_a='adj')
        self.assertIn('казовый', results)
        results = self.derivation.derive(word_b='искать', pos_b='verb', pos_a='adj')
        self.assertIn('исковой', results)
        results = self.derivation.derive(word_b='смотреть', pos_b='verb', pos_a='adj')
        self.assertIn('смотровой', results)
        results = self.derivation.derive(word_b='бурить', pos_b='verb', pos_a='adj')
        self.assertIn('буровой', results)
        results = self.derivation.derive(word_b='торговать', pos_b='verb', pos_a='adj')
        self.assertIn('торговый', results)
        results = self.derivation.derive(word_b='страховать', pos_b='verb', pos_a='adj')
        self.assertIn('страховой', results)
        results = self.derivation.derive(word_b='кочевать', pos_b='verb', pos_a='adj')
        self.assertIn('кочевой', results)
        results = self.derivation.derive(word_b='плевать', pos_b='verb', pos_a='adj')
        self.assertIn('плёвый', results)

    def test_adj_655_1(self):
        results = self.derivation.derive(word_b='колдовать', pos_b='verb', pos_a='adj')
        self.assertIn('колдовской', results)

    def test_adj_655_2(self):
        results = self.derivation.derive(word_b='бродяжничать', pos_b='verb', pos_a='adj')
        self.assertIn('бродяжнический', results)

    def test_adj_655_3(self):
        results = self.derivation.derive(word_b='издеваться', pos_b='verb', pos_a='adj')
        self.assertIn('издевательский', results)
        results = self.derivation.derive(word_b='наплевать', pos_b='verb', pos_a='adj')
        self.assertIn('наплевательский', results)

    def test_adj_656(self):
        results = self.derivation.derive(word_b='колоть', pos_b='verb', pos_a='adj')
        self.assertIn('колкий', results)
        results = self.derivation.derive(word_b='шатать', pos_b='verb', pos_a='adj')
        self.assertIn('шаткий', results)
        results = self.derivation.derive(word_b='есть', pos_b='verb', pos_a='adj')
        self.assertIn('едкий', results)
        results = self.derivation.derive(word_b='знобить', pos_b='verb', pos_a='adj')
        self.assertIn('знобкий', results)
        results = self.derivation.derive(word_b='трясти', pos_b='verb', pos_a='adj')
        self.assertIn('тряский', results)
        results = self.derivation.derive(word_b='хрустеть', pos_b='verb', pos_a='adj')
        self.assertIn('хрусткий', results)
        results = self.derivation.derive(word_b='садиться', pos_b='verb', pos_a='adj')
        self.assertIn('садкий', results)
        results = self.derivation.derive(word_b='зябнуть', pos_b='verb', pos_a='adj')
        self.assertIn('зябкий', results)

    def test_adj_656_2(self):
        results = self.derivation.derive(word_b='звенеть', pos_b='verb', pos_a='adj')
        self.assertIn('звонкий', results)
        results = self.derivation.derive(word_b='вертеться', pos_b='verb', pos_a='adj')
        self.assertIn('вёрткий', results)
        results = self.derivation.derive(word_b='гнать', pos_b='verb', pos_a='adj')
        self.assertIn('гонкий', results)
        results = self.derivation.derive(word_b='цепляться', pos_b='verb', pos_a='adj')
        self.assertIn('цепкий', results)
        results = self.derivation.derive(word_b='тонуть', pos_b='verb', pos_a='adj')
        self.assertIn('топкий', results)
        results = self.derivation.derive(word_b='гнуться', pos_b='verb', pos_a='adj')
        self.assertIn('гибкий', results)
        results = self.derivation.derive(word_b='гнуться', pos_b='verb', pos_a='adj')
        self.assertIn('гнуткий', results)
        results = self.derivation.derive(word_b='чуять', pos_b='verb', pos_a='adj')
        self.assertIn('чуткий', results)

    def test_adj_657(self):
        results = self.derivation.derive(word_b='ощутить', pos_b='verb', pos_a='adj')
        self.assertIn('ощутимый', results)
        results = self.derivation.derive(word_b='изменять', pos_b='verb', pos_a='adj')
        self.assertIn('изменяемый', results)
        results = self.derivation.derive(word_b='терпеть', pos_b='verb', pos_a='adj')
        self.assertIn('терпимый', results)
        results = self.derivation.derive(word_b='угрожать', pos_b='verb', pos_a='adj')
        self.assertIn('угрожаемый', results)
        results = self.derivation.derive(word_b='доказать', pos_b='verb', pos_a='adj')
        self.assertIn('доказуемый', results)
        results = self.derivation.derive(word_b='познавать', pos_b='verb', pos_a='adj')
        self.assertIn('познаваемый', results)
        results = self.derivation.derive(word_b='пренебречь', pos_b='verb', pos_a='adj')
        self.assertIn('пренебрежимый', results)
        results = self.derivation.derive(word_b='поправить', pos_b='verb', pos_a='adj')
        self.assertIn('поправимый', results)
        results = self.derivation.derive(word_b='преодолеть', pos_b='verb', pos_a='adj')
        self.assertIn('преодолимый', results)
        results = self.derivation.derive(word_b='опровергнуть', pos_b='verb', pos_a='adj')
        self.assertIn('опровержимый', results)
        results = self.derivation.derive(word_b='растянуть', pos_b='verb', pos_a='adj')
        self.assertIn('растяжимый', results)

    def test_adj_657_2(self):
        results = self.derivation.derive(word_b='принимать', pos_b='verb', pos_a='adj')
        self.assertIn('приемлемый', results)
        results = self.derivation.derive(word_b='весить', pos_b='verb', pos_a='adj')
        self.assertIn('весомый', results)
        results = self.derivation.derive(word_b='знать', pos_b='verb', pos_a='adj')
        self.assertIn('знакомый', results)

    def test_adj_658(self):
        results = self.derivation.derive(word_b='прерывать', pos_b='verb', pos_a='adj')
        self.assertIn('прерывистый', results)
        results = self.derivation.derive(word_b='поджарить', pos_b='verb', pos_a='adj')
        self.assertIn('поджаристый', results)
        results = self.derivation.derive(word_b='размахиваться', pos_b='verb', pos_a='adj')
        self.assertIn('размашистый', results)
        results = self.derivation.derive(word_b='размахнуться', pos_b='verb', pos_a='adj')
        self.assertIn('размашистый', results)
        results = self.derivation.derive(word_b='укладываться', pos_b='verb', pos_a='adj')
        self.assertIn('укладистый', results)
        results = self.derivation.derive(word_b='лаять', pos_b='verb', pos_a='adj')
        self.assertIn('лаистый', results)
        results = self.derivation.derive(word_b='загрести', pos_b='verb', pos_a='adj')
        self.assertIn('загрёбистый', results)

    def test_adj_658_2(self):
        results = self.derivation.derive(word_b='забрать', pos_b='verb', pos_a='adj')
        self.assertIn('забористый', results)
        results = self.derivation.derive(word_b='забирать', pos_b='verb', pos_a='adj')
        self.assertIn('забористый', results)
        results = self.derivation.derive(word_b='напереть', pos_b='verb', pos_a='adj')
        self.assertIn('напористый', results)
        results = self.derivation.derive(word_b='напирать', pos_b='verb', pos_a='adj')
        self.assertIn('напористый', results)
        results = self.derivation.derive(word_b='рассчитать', pos_b='verb', pos_a='adj')
        self.assertIn('расчётистый', results)
        results = self.derivation.derive(word_b='рассчитывать', pos_b='verb', pos_a='adj')
        self.assertIn('расчётистый', results)
        results = self.derivation.derive(word_b='поднять', pos_b='verb', pos_a='adj')
        self.assertIn('подъёмистый', results)
        results = self.derivation.derive(word_b='поднимать', pos_b='verb', pos_a='adj')
        self.assertIn('подъёмистый', results)
        results = self.derivation.derive(word_b='извернуться', pos_b='verb', pos_a='adj')
        self.assertIn('изворотистый', results)
        results = self.derivation.derive(word_b='изворачиваться', pos_b='verb', pos_a='adj')
        self.assertIn('изворотистый', results)
        results = self.derivation.derive(word_b='обернуться', pos_b='verb', pos_a='adj')
        self.assertIn('оборотистый', results)
        results = self.derivation.derive(word_b='оборачиваться', pos_b='verb', pos_a='adj')
        self.assertIn('оборотистый', results)

    def test_adj_659(self):
        results = self.derivation.derive(word_b='разрывать', pos_b='verb', pos_a='adj')
        self.assertIn('разрывчатый', results)

    def test_adj_660_1(self):
        results = self.derivation.derive(word_b='течь', pos_b='verb', pos_a='adj')
        self.assertIn('текучий', results)
        results = self.derivation.derive(word_b='жечь', pos_b='verb', pos_a='adj')
        self.assertIn('жгучий', results)
        results = self.derivation.derive(word_b='ползти', pos_b='verb', pos_a='adj')
        self.assertIn('ползучий', results)
        results = self.derivation.derive(word_b='лететь', pos_b='verb', pos_a='adj')
        self.assertIn('летучий', results)
        results = self.derivation.derive(word_b='линять', pos_b='verb', pos_a='adj')
        self.assertIn('линючий', results)
        results = self.derivation.derive(word_b='гореть', pos_b='verb', pos_a='adj')
        self.assertIn('горючий', results)
        results = self.derivation.derive(word_b='греметь', pos_b='verb', pos_a='adj')
        self.assertIn('гремучий', results)
        results = self.derivation.derive(word_b='плакать', pos_b='verb', pos_a='adj')
        self.assertIn('плакучий', results)
        results = self.derivation.derive(word_b='бить', pos_b='verb', pos_a='adj')
        self.assertIn('бьючий', results)
        results = self.derivation.derive(word_b='колоть', pos_b='verb', pos_a='adj')
        self.assertIn('колючий', results)
        results = self.derivation.derive(word_b='пахнуть', pos_b='verb', pos_a='adj')
        self.assertIn('пахучий', results)
        results = self.derivation.derive(word_b='плыть', pos_b='verb', pos_a='adj')
        self.assertIn('плывучий', results)
        results = self.derivation.derive(word_b='гнить', pos_b='verb', pos_a='adj')
        self.assertIn('гниючий', results)
        results = self.derivation.derive(word_b='жить', pos_b='verb', pos_a='adj')
        self.assertIn('живучий', results)
        results = self.derivation.derive(word_b='петь', pos_b='verb', pos_a='adj')
        self.assertIn('певучий', results)

    def test_adj_660_1_2(self):
        results = self.derivation.derive(word_b='есть', pos_b='verb', pos_a='adj')
        self.assertIn('едучий', results)

    def test_adj_660_1_3(self):
        results = self.derivation.derive(word_b='тянуться', pos_b='verb', pos_a='adj')
        self.assertIn('тягучий', results)
        results = self.derivation.derive(word_b='тянуться', pos_b='verb', pos_a='adj')
        self.assertIn('тянучий', results)

    def test_adj_660_1_4(self):
        results = self.derivation.derive(word_b='блестеть', pos_b='verb', pos_a='adj')
        self.assertIn('блескучий', results)

    def test_adj_660_1_5(self):
        results = self.derivation.derive(word_b='трещать', pos_b='verb', pos_a='adj')
        self.assertIn('трескучий', results)
        results = self.derivation.derive(word_b='визжать', pos_b='verb', pos_a='adj')
        self.assertIn('визгучий', results)

    def test_adj_660_2(self):
        results = self.derivation.derive(word_b='ходить', pos_b='verb', pos_a='adj')
        self.assertIn('ходячий', results)
        results = self.derivation.derive(word_b='висеть', pos_b='verb', pos_a='adj')
        self.assertIn('висячий', results)
        results = self.derivation.derive(word_b='лежать', pos_b='verb', pos_a='adj')
        self.assertIn('лежачий', results)
        results = self.derivation.derive(word_b='стоять', pos_b='verb', pos_a='adj')
        self.assertIn('стоячий', results)
        results = self.derivation.derive(word_b='кусать', pos_b='verb', pos_a='adj')
        self.assertIn('кусачий', results)

    def test_adj_661_1(self):
        results = self.derivation.derive(word_b='улыбаться', pos_b='verb', pos_a='adj')
        self.assertIn('улыбчивый', results)
        results = self.derivation.derive(word_b='доверять', pos_b='verb', pos_a='adj')
        self.assertIn('доверчивый', results)
        results = self.derivation.derive(word_b='вспылить', pos_b='verb', pos_a='adj')
        self.assertIn('вспыльчивый', results)
        results = self.derivation.derive(word_b='прилипнуть', pos_b='verb', pos_a='adj')
        self.assertIn('прилипчивый', results)
        results = self.derivation.derive(word_b='обидеться', pos_b='verb', pos_a='adj')
        self.assertIn('обидчивый', results)
        results = self.derivation.derive(word_b='устоять', pos_b='verb', pos_a='adj')
        self.assertIn('устойчивый', results)

    def test_adj_661_1_2(self):
        results = self.derivation.derive(word_b='перемётываться', pos_b='verb', pos_a='adj')
        self.assertIn('перемётчивый', results)
        results = self.derivation.derive(word_b='увёртываться', pos_b='verb', pos_a='adj')
        self.assertIn('увёртливый', results)

    def test_adj_661_2(self):
        results = self.derivation.derive(word_b='потеть', pos_b='verb', pos_a='adj')
        self.assertIn('потливый', results)
        results = self.derivation.derive(word_b='насмехаться', pos_b='verb', pos_a='adj')
        self.assertIn('насмешливый', results)
        results = self.derivation.derive(word_b='баловаться', pos_b='verb', pos_a='adj')
        self.assertIn('баловливый', results)
        results = self.derivation.derive(word_b='глумиться', pos_b='verb', pos_a='adj')
        self.assertIn('глумливый', results)
        results = self.derivation.derive(word_b='шуметь', pos_b='verb', pos_a='adj')
        self.assertIn('шумливый', results)
        results = self.derivation.derive(word_b='ворчать', pos_b='verb', pos_a='adj')
        self.assertIn('ворчливый', results)
        results = self.derivation.derive(word_b='кричать', pos_b='verb', pos_a='adj')
        self.assertIn('крикливый', results)
        results = self.derivation.derive(word_b='пищать', pos_b='verb', pos_a='adj')
        self.assertIn('пискливый', results)
        results = self.derivation.derive(word_b='визжать', pos_b='verb', pos_a='adj')
        self.assertIn('визгливый', results)
        results = self.derivation.derive(word_b='беречь', pos_b='verb', pos_a='adj')
        self.assertIn('бережливый', results)

    def test_adj_661_2_2(self):
        results = self.derivation.derive(word_b='молчать', pos_b='verb', pos_a='adj')
        self.assertIn('молчаливый', results)
        results = self.derivation.derive(word_b='терпеть', pos_b='verb', pos_a='adj')
        self.assertIn('терпеливый', results)

    def test_adj_661_2_3(self):
        results = self.derivation.derive(word_b='понять', pos_b='verb', pos_a='adj')
        self.assertIn('понятливый', results)
        results = self.derivation.derive(word_b='податься', pos_b='verb', pos_a='adj')
        self.assertIn('податливый', results)

    def test_adj_661_2_4(self):
        results = self.derivation.derive(word_b='разобраться', pos_b='verb', pos_a='adj')
        self.assertIn('разборчивый', results)
        results = self.derivation.derive(word_b='разбираться', pos_b='verb', pos_a='adj')
        self.assertIn('разборчивый', results)
        results = self.derivation.derive(word_b='перенять', pos_b='verb', pos_a='adj')
        self.assertIn('переимчивый', results)
        results = self.derivation.derive(word_b='извернуться', pos_b='verb', pos_a='adj')
        self.assertIn('изворотливый', results)
        results = self.derivation.derive(word_b='изворачиваться', pos_b='verb', pos_a='adj')
        self.assertIn('изворотливый', results)

    def test_adj_661_2_5(self):
        results = self.derivation.derive(word_b='дурачиться', pos_b='verb', pos_a='adj')
        self.assertIn('дурашливый', results)

    def test_adj_661_3(self):
        results = self.derivation.derive(word_b='играть', pos_b='verb', pos_a='adj')
        self.assertIn('игривый', results)
        results = self.derivation.derive(word_b='ревновать', pos_b='verb', pos_a='adj')
        self.assertIn('ревнивый', results)
        results = self.derivation.derive(word_b='лгать', pos_b='verb', pos_a='adj')
        self.assertIn('лживый', results)

    def test_adj_662(self):
        results = self.derivation.derive(word_b='устать', pos_b='verb', pos_a='adj')
        self.assertIn('усталый', results)
        results = self.derivation.derive(word_b='спеть', pos_b='verb', pos_a='adj')
        self.assertIn('спелый', results)
        results = self.derivation.derive(word_b='тухнуть', pos_b='verb', pos_a='adj')
        self.assertIn('тухлый', results)
        results = self.derivation.derive(word_b='служить', pos_b='verb', pos_a='adj')
        self.assertIn('служилый', results)
        results = self.derivation.derive(word_b='лежать', pos_b='verb', pos_a='adj')
        self.assertIn('лежалый', results)
        results = self.derivation.derive(word_b='впасть', pos_b='verb', pos_a='adj')
        self.assertIn('впалый', results)
        results = self.derivation.derive(word_b='цвести', pos_b='verb', pos_a='adj')
        self.assertIn('цвёлый', results)
        results = self.derivation.derive(word_b='впасть', pos_b='verb', pos_a='adj')
        self.assertIn('впалый', results)
        results = self.derivation.derive(word_b='отечь', pos_b='verb', pos_a='adj')
        self.assertIn('отёклый', results)
        results = self.derivation.derive(word_b='полечь', pos_b='verb', pos_a='adj')
        self.assertIn('полёглый', results)
        results = self.derivation.derive(word_b='гнить', pos_b='verb', pos_a='adj')
        self.assertIn('гнилой', results)
        results = self.derivation.derive(word_b='стыть', pos_b='verb', pos_a='adj')
        self.assertIn('стылый', results)
        results = self.derivation.derive(word_b='отстать', pos_b='verb', pos_a='adj')
        self.assertIn('отсталый', results)
        results = self.derivation.derive(word_b='жить', pos_b='verb', pos_a='adj')
        self.assertIn('жилой', results)

    def test_adj_662_2(self):
        results = self.derivation.derive(word_b='быть', pos_b='verb', pos_a='adj')
        self.assertIn('былой', results)
        results = self.derivation.derive(word_b='прийти', pos_b='verb', pos_a='adj')
        self.assertIn('пришлый', results)
        results = self.derivation.derive(word_b='таять', pos_b='verb', pos_a='adj')
        self.assertIn('талый', results)
        results = self.derivation.derive(word_b='бежать', pos_b='verb', pos_a='adj')
        self.assertIn('беглый', results)
        results = self.derivation.derive(word_b='осесть', pos_b='verb', pos_a='adj')
        self.assertIn('осёдлый', results)

    def test_adj_663_1(self):
        results = self.derivation.derive(word_b='тереть', pos_b='verb', pos_a='adj')
        self.assertIn('тертый', results)
        results = self.derivation.derive(word_b='колоть', pos_b='verb', pos_a='adj')
        self.assertIn('колотый', results)
        results = self.derivation.derive(word_b='молоть', pos_b='verb', pos_a='adj')
        self.assertIn('молотый', results)
        results = self.derivation.derive(word_b='бить', pos_b='verb', pos_a='adj')
        self.assertIn('битый', results)
        results = self.derivation.derive(word_b='крыть', pos_b='verb', pos_a='adj')
        self.assertIn('крытый', results)
        results = self.derivation.derive(word_b='дуть', pos_b='verb', pos_a='adj')
        self.assertIn('дутый', results)
        results = self.derivation.derive(word_b='мять', pos_b='verb', pos_a='adj')
        self.assertIn('мятый', results)
        results = self.derivation.derive(word_b='крыть', pos_b='verb', pos_a='adj')
        self.assertIn('крытый', results)

    def test_adj_663_2(self):
        # вернуться после 1585
        results = self.derivation.derive(word_b='делать', pos_b='verb', pos_a='adj')
        self.assertIn('деланый', results)
        results = self.derivation.derive(word_b='баловать', pos_b='verb', pos_a='adj')
        self.assertIn('балованный', results)
        results = self.derivation.derive(word_b='рвать', pos_b='verb', pos_a='adj')
        self.assertIn('рваный', results)

    def test_adj_663_3(self):
        results = self.derivation.derive(word_b='варить', pos_b='verb', pos_a='adj')
        self.assertIn('варёный', results)
        results = self.derivation.derive(word_b='морозить', pos_b='verb', pos_a='adj')
        self.assertIn('мороженый', results)
        results = self.derivation.derive(word_b='кипятить', pos_b='verb', pos_a='adj')
        self.assertIn('кипячёный', results)
        results = self.derivation.derive(word_b='лудить', pos_b='verb', pos_a='adj')
        self.assertIn('лужёный', results)
        results = self.derivation.derive(word_b='красить', pos_b='verb', pos_a='adj')
        self.assertIn('крашеный', results)
        results = self.derivation.derive(word_b='чистить', pos_b='verb', pos_a='adj')
        self.assertIn('чищеный', results)
        results = self.derivation.derive(word_b='ездить', pos_b='verb', pos_a='adj')
        self.assertIn('езженый', results)
        results = self.derivation.derive(word_b='долбить', pos_b='verb', pos_a='adj')
        self.assertIn('долблёный', results)
        results = self.derivation.derive(word_b='печь', pos_b='verb', pos_a='adj')
        self.assertIn('печёный', results)
        results = self.derivation.derive(word_b='жечь', pos_b='verb', pos_a='adj')
        self.assertIn('жжёный', results)
        results = self.derivation.derive(word_b='красть', pos_b='verb', pos_a='adj')
        self.assertIn('краденый', results)
        results = self.derivation.derive(word_b='плести', pos_b='verb', pos_a='adj')
        self.assertIn('плетёный', results)

    def test_adj_663_4(self):
        results = self.derivation.derive(word_b='клеймить', pos_b='verb', pos_a='adj')
        self.assertIn('клеймёный', results)
        results = self.derivation.derive(word_b='студить', pos_b='verb', pos_a='adj')
        self.assertIn('студёный', results)

    def test_adj_664(self):
        results = self.derivation.derive(word_b='растеряться', pos_b='verb', pos_a='adj')
        self.assertIn('растерянный', results)
        results = self.derivation.derive(word_b='протянуться', pos_b='verb', pos_a='adj')
        self.assertIn('протяжённый', results)
        results = self.derivation.derive(word_b='пересытиться', pos_b='verb', pos_a='adj')
        self.assertIn('пересыщенный', results)
        results = self.derivation.derive(word_b='убедиться', pos_b='verb', pos_a='adj')
        self.assertIn('убеждённый', results)
        results = self.derivation.derive(word_b='условиться', pos_b='verb', pos_a='adj')
        self.assertIn('условленный', results)
        results = self.derivation.derive(word_b='изнемочь', pos_b='verb', pos_a='adj')
        self.assertIn('изнеможённый', results)
        results = self.derivation.derive(word_b='изнемочь', pos_b='verb', pos_a='adj')
        self.assertIn('изнемождённый', results)

    def test_adj_664_2(self):
        results = self.derivation.derive(word_b='воздержаться', pos_b='verb', pos_a='adj')
        self.assertIn('воздержанный', results)

    def test_adj_665_1_1(self):
        results = self.derivation.derive(word_b='иметь', pos_b='verb', pos_a='adj')
        self.assertIn('имущий', results)
        results = self.derivation.derive(word_b='завидовать', pos_b='verb', pos_a='adj')
        self.assertIn('завидущий', results)
        results = self.derivation.derive(word_b='плодиться', pos_b='verb', pos_a='adj')
        self.assertIn('плодущий', results)

    def test_adj_665_1_2(self):
        results = self.derivation.derive(word_b='заваляться', pos_b='verb', pos_a='adj')
        self.assertIn('завалящий', results)
        results = self.derivation.derive(word_b='работать', pos_b='verb', pos_a='adj')
        self.assertIn('работящий', results)
        results = self.derivation.derive(word_b='пропасть', pos_b='verb', pos_a='adj')
        self.assertIn('пропащий', results)

    def test_adj_665_2(self):
        results = self.derivation.derive(word_b='рдеть', pos_b='verb', pos_a='adj')
        self.assertIn('рдяный', results)
        results = self.derivation.derive(word_b='пить', pos_b='verb', pos_a='adj')
        self.assertIn('пьяный', results)

    def test_adj_665_3(self):
        results = self.derivation.derive(word_b='гнусить', pos_b='verb', pos_a='adj')
        self.assertIn('гнусавый', results)
        results = self.derivation.derive(word_b='вихляться', pos_b='verb', pos_a='adj')
        self.assertIn('вихлявый', results)
        results = self.derivation.derive(word_b='вертеться', pos_b='verb', pos_a='adj')
        self.assertIn('вертлявый', results)

    def test_adj_665_4(self):
        results = self.derivation.derive(word_b='писать', pos_b='verb', pos_a='adj')
        self.assertIn('писчий', results)
        results = self.derivation.derive(word_b='товить', pos_b='verb', pos_a='adj')
        self.assertIn('ловчий', results)
        results = self.derivation.derive(word_b='купить', pos_b='verb', pos_a='adj')
        self.assertIn('купчий', results)
        results = self.derivation.derive(word_b='гнать', pos_b='verb', pos_a='adj')
        self.assertIn('гончий', results)
        results = self.derivation.derive(word_b='петь', pos_b='verb', pos_a='adj')
        self.assertIn('певчий', results)
        results = self.derivation.derive(word_b='косить', pos_b='verb', pos_a='adj')
        self.assertIn('косчий', results)

    def test_adj_665_5(self):
        results = self.derivation.derive(word_b='вихлять', pos_b='verb', pos_a='adj')
        self.assertIn('вихлястый', results)

    def test_adj_665_6(self):
        results = self.derivation.derive(word_b='сопеть', pos_b='verb', pos_a='adj')
        self.assertIn('сопатый', results)

    def test_adj_665_7(self):
        results = self.derivation.derive(word_b='сипеть', pos_b='verb', pos_a='adj')
        self.assertIn('сиповатый', results)

    def test_adj_666(self):
        results = self.derivation.derive(word_b='грязный', pos_b='adj', pos_a='adj')
        self.assertIn('грязноватый', results)
        results = self.derivation.derive(word_b='лиловый', pos_b='adj', pos_a='adj')
        self.assertIn('лиловатый', results)
        results = self.derivation.derive(word_b='оранжевый', pos_b='adj', pos_a='adj')
        self.assertIn('оранжеватый', results)
        results = self.derivation.derive(word_b='вязкий', pos_b='adj', pos_a='adj')
        self.assertIn('вязковатый', results)
        results = self.derivation.derive(word_b='рыжий', pos_b='adj', pos_a='adj')
        self.assertIn('рыжеватый', results)
        results = self.derivation.derive(word_b='куцый', pos_b='adj', pos_a='adj')
        self.assertIn('куцеватый', results)

    def test_adj_667(self):
        results = self.derivation.derive(word_b='умный', pos_b='adj', pos_a='adj')
        self.assertIn('умненький', results)
        results = self.derivation.derive(word_b='синий', pos_b='adj', pos_a='adj')
        self.assertIn('синенький', results)
        results = self.derivation.derive(word_b='сладкий', pos_b='adj', pos_a='adj')
        self.assertIn('сладенький', results)
        results = self.derivation.derive(word_b='высокий', pos_b='adj', pos_a='adj')
        self.assertIn('высоконький', results)
        results = self.derivation.derive(word_b='плохой', pos_b='adj', pos_a='adj')
        self.assertIn('плохенький', results)
        results = self.derivation.derive(word_b='свежий', pos_b='adj', pos_a='adj')
        self.assertIn('свеженький', results)

    def test_adj_667_2(self):
        results = self.derivation.derive(word_b='малый', pos_b='adj', pos_a='adj')
        self.assertIn('махонький', results)

    def test_adj_668(self):
        results = self.derivation.derive(word_b='слабый', pos_b='adj', pos_a='adj')
        self.assertIn('слабенек', results)
        results = self.derivation.derive(word_b='строгий', pos_b='adj', pos_a='adj')
        self.assertIn('строгонек', results)

    def test_adj_669(self):
        results = self.derivation.derive(word_b='полный', pos_b='adj', pos_a='adj')
        self.assertIn('полнёхонький', results)
        results = self.derivation.derive(word_b='синий', pos_b='adj', pos_a='adj')
        self.assertIn('синёхонький', results)
        results = self.derivation.derive(word_b='лёгкий', pos_b='adj', pos_a='adj')
        self.assertIn('лёгонький', results)

    def test_adj_670(self):
        results = self.derivation.derive(word_b='такой', pos_b='adj', pos_a='adj')
        self.assertIn('такусенький', results)
        results = self.derivation.derive(word_b='тонкий', pos_b='adj', pos_a='adj')
        self.assertIn('тонюсенький', results)

    def test_adj_671_1(self):
        results = self.derivation.derive(word_b='толстый', pos_b='adj', pos_a='adj')
        self.assertIn('толстущий', results)
        results = self.derivation.derive(word_b='толстый', pos_b='adj', pos_a='adj')
        self.assertIn('толстющий', results)
        results = self.derivation.derive(word_b='злой', pos_b='adj', pos_a='adj')
        self.assertIn('злющий', results)
        results = self.derivation.derive(word_b='большой', pos_b='adj', pos_a='adj')
        self.assertIn('большущий', results)

    def test_adj_671_2(self):
        results = self.derivation.derive(word_b='здоровый', pos_b='adj', pos_a='adj')
        self.assertIn('здоровенный', results)
        results = self.derivation.derive(word_b='страшный', pos_b='adj', pos_a='adj')
        self.assertIn('страшенный', results)
        results = self.derivation.derive(word_b='широкий', pos_b='adj', pos_a='adj')
        self.assertIn('широченный', results)

    def test_adj_671_3(self):
        results = self.derivation.derive(word_b='толстый', pos_b='adj', pos_a='adj')
        self.assertIn('толщенный', results)

    def test_adj_671_4(self):
        results = self.derivation.derive(word_b='добрый', pos_b='adj', pos_a='adj')
        self.assertIn('добреющий', results)

    def test_adj_671_5(self):
        results = self.derivation.derive(word_b='холодный', pos_b='adj', pos_a='adj')
        self.assertIn('холоднючий', results)

    def test_adj_672_1(self):
        results = self.derivation.derive(word_b='богатый', pos_b='adj', pos_a='adj')
        self.assertIn('богатейший', results)
        results = self.derivation.derive(word_b='свежий', pos_b='adj', pos_a='adj')
        self.assertIn('свежейший', results)
        results = self.derivation.derive(word_b='горячий', pos_b='adj', pos_a='adj')
        self.assertIn('горячейший', results)

    def test_adj_672_2(self):
        results = self.derivation.derive(word_b='жалкий', pos_b='adj', pos_a='adj')
        self.assertIn('жалчайший', results)
        results = self.derivation.derive(word_b='близкий', pos_b='adj', pos_a='adj')
        self.assertIn('ближайший', results)
        results = self.derivation.derive(word_b='мелкий', pos_b='adj', pos_a='adj')
        self.assertIn('мельчайший', results)
        results = self.derivation.derive(word_b='свежий', pos_b='adj', pos_a='adj')
        self.assertIn('свежайший', results)

    def test_adj_672_3(self):
        results = self.derivation.derive(word_b='высокий', pos_b='adj', pos_a='adj')
        self.assertIn('высший', results)
        results = self.derivation.derive(word_b='низкий', pos_b='adj', pos_a='adj')
        self.assertIn('низший', results)
        results = self.derivation.derive(word_b='худой', pos_b='adj', pos_a='adj')
        self.assertIn('худший', results)

    def test_adj_673(self):
        results = self.derivation.derive(word_b='песчаный', pos_b='adj', pos_a='adj')
        self.assertIn('песчанистый', results)
        results = self.derivation.derive(word_b='деревянный', pos_b='adj', pos_a='adj')
        self.assertIn('деревянистый', results)

    def test_adj_674(self):
        results = self.derivation.derive(word_b='черный', pos_b='adj', pos_a='adj')
        self.assertIn('черновой', results)
        results = self.derivation.derive(word_b='легкий', pos_b='adj', pos_a='adj')
        self.assertIn('легковой', results)
        results = self.derivation.derive(word_b='беж', pos_b='adj_color', pos_a='adj')
        self.assertIn('бежевый', results)
        results = self.derivation.derive(word_b='бордо', pos_b='adj_color', pos_a='adj')
        self.assertIn('бордовый', results)

    def test_adj_675_1(self):
        results = self.derivation.derive(word_b='простой', pos_b='adj', pos_a='adj')
        self.assertIn('простецкий', results)
        results = self.derivation.derive(word_b='важный', pos_b='adj', pos_a='adj')
        self.assertIn('важнецкий', results)

    def test_adj_675_2(self):
        results = self.derivation.derive(word_b='немудрёный', pos_b='adj', pos_a='adj')
        self.assertIn('немудрящий', results)
        results = self.derivation.derive(word_b='негодный', pos_b='adj', pos_a='adj')
        self.assertIn('негодящий', results)
        results = self.derivation.derive(word_b='непутёвый', pos_b='adj', pos_a='adj')
        self.assertIn('непутящий', results)

    def test_adj_675_3(self):
        results = self.derivation.derive(word_b='черный', pos_b='adj', pos_a='adj')
        self.assertIn('чернявый', results)
        results = self.derivation.derive(word_b='молодой', pos_b='adj', pos_a='adj')
        self.assertIn('моложавый', results)

    def test_adj_675_4(self):
        results = self.derivation.derive(word_b='худой', pos_b='adj', pos_a='adj')
        self.assertIn('худощавый', results)
        results = self.derivation.derive(word_b='сухой', pos_b='adj', pos_a='adj')
        self.assertIn('сухощавый', results)

    def test_adj_675_5(self):
        results = self.derivation.derive(word_b='сладкий', pos_b='adj', pos_a='adj')
        self.assertIn('слащавый', results)

    def test_adj_675_6(self):
        results = self.derivation.derive(word_b='первый', pos_b='?', pos_a='adj')
        self.assertIn('первичный', results)
        results = self.derivation.derive(word_b='второй', pos_b='?', pos_a='adj')
        self.assertIn('вторичный', results)
        results = self.derivation.derive(word_b='третий', pos_b='?', pos_a='adj')
        self.assertIn('третичный', results)
        results = self.derivation.derive(word_b='четвертый', pos_b='?', pos_a='adj')
        self.assertIn('четвертичный', results)

    def test_adj_675_7(self):
        results = self.derivation.derive(word_b='местный', pos_b='adj', pos_a='adj')
        self.assertIn('местнический', results)
        results = self.derivation.derive(word_b='областной', pos_b='adj', pos_a='adj')
        self.assertIn('областнический', results)

    def test_adj_675_8(self):
        results = self.derivation.derive(word_b='седой', pos_b='adj', pos_a='adj')
        self.assertIn('седатый', results)

    def test_adj_675_9(self):
        results = self.derivation.derive(word_b='щедрый', pos_b='adj', pos_a='adj')
        self.assertIn('щедровитый', results)

    def test_adj_675_10(self):
        results = self.derivation.derive(word_b='особый', pos_b='adj', pos_a='adj')
        self.assertIn('особливый', results)

    def test_adj_675_11(self):
        results = self.derivation.derive(word_b='гордый', pos_b='adj', pos_a='adj')
        self.assertIn('горделивый', results)

    def test_adj_675_12(self):
        results = self.derivation.derive(word_b='весь', pos_b='?', pos_a='adj')
        self.assertIn('всякий', results)

    def test_adj_675_13(self):
        results = self.derivation.derive(word_b='целый', pos_b='adj', pos_a='adj')
        self.assertIn('цельный', results)
        results = self.derivation.derive(word_b='ничей', pos_b='adj', pos_a='adj')
        self.assertIn('ничейный', results)

    def test_adj_675_14(self):
        results = self.derivation.derive(word_b='мертвый', pos_b='adj', pos_a='adj')
        self.assertIn('мертвенный', results)
        results = self.derivation.derive(word_b='трезвый', pos_b='adj', pos_a='adj')
        self.assertIn('трезвенный', results)

    def test_adj_675_15(self):
        results = self.derivation.derive(word_b='низкий', pos_b='adj', pos_a='adj')
        self.assertIn('низменный', results)

    def test_adj_675_16(self):
        results = self.derivation.derive(word_b='недурной', pos_b='adj', pos_a='adj')
        self.assertIn('недурственный', results)
        results = self.derivation.derive(word_b='приятный', pos_b='adj', pos_a='adj')
        self.assertIn('приятственный', results)
        results = self.derivation.derive(word_b='явный', pos_b='adj', pos_a='adj')
        self.assertIn('явственный', results)

    def test_adj_675_17(self):
        results = self.derivation.derive(word_b='свой', pos_b='?', pos_a='adj')
        self.assertIn('свойский', results)
        results = self.derivation.derive(word_b='всякий', pos_b='adj', pos_a='adj')
        self.assertIn('всяческий', results)
        results = self.derivation.derive(word_b='наш', pos_b='?', pos_a='adj')
        self.assertIn('нашенский', results)

    def test_adj_675_18(self):
        results = self.derivation.derive(word_b='третий', pos_b='?', pos_a='adj')
        self.assertIn('третейский', results)

    def test_adj_676_1(self):
        results = self.derivation.derive(word_b='трое', pos_b='?', pos_a='adj')
        self.assertIn('троичный', results)
        results = self.derivation.derive(word_b='десятеро', pos_b='?', pos_a='adj')
        self.assertIn('десятеричный', results)

    def test_adj_676_2(self):
        results = self.derivation.derive(word_b='двое', pos_b='?', pos_a='adj')
        self.assertIn('двоякий', results)

    def test_adj_676_3(self):
        results = self.derivation.derive(word_b='двое', pos_b='?', pos_a='adj')
        self.assertIn('двойчатый', results)

    def test_adj_676_4(self):
        results = self.derivation.derive(word_b='сорок', pos_b='num', pos_a='adj')
        self.assertIn('сороковой', results)

    def test_adj_676_5(self):
        results = self.derivation.derive(word_b='ничто', pos_b='?', pos_a='adj')
        self.assertIn('ничтожный', results)
        results = self.derivation.derive(word_b='оба', pos_b='?', pos_a='adj')
        self.assertIn('обоюдный', results)

    def test_adj_676_6(self):
        results = self.derivation.derive(word_b='трое', pos_b='?', pos_a='adj')
        self.assertIn('тройственный', results)
        results = self.derivation.derive(word_b='себя', pos_b='?', pos_a='adj')
        self.assertIn('собственный', results)

    def test_adj_677_1(self):
        results = self.derivation.derive(word_b='близ', pos_b='adv', pos_a='adj')
        self.assertIn('ближний', results)
        results = self.derivation.derive(word_b='здесь', pos_b='adv', pos_a='adj')
        self.assertIn('здешний', results)
        results = self.derivation.derive(word_b='среди', pos_b='adv', pos_a='adj')
        self.assertIn('средний', results)
        results = self.derivation.derive(word_b='рано', pos_b='adv', pos_a='adj')
        self.assertIn('ранний', results)
        results = self.derivation.derive(word_b='прежде', pos_b='adv', pos_a='adj')
        self.assertIn('прежний', results)
        results = self.derivation.derive(word_b='замуж', pos_b='adv', pos_a='adj')
        self.assertIn('замужний', results)
        results = self.derivation.derive(word_b='замужем', pos_b='adv', pos_a='adj')
        self.assertIn('замужний', results)

    def test_adj_677_2(self):
        results = self.derivation.derive(word_b='внутрь', pos_b='adv', pos_a='adj')
        self.assertIn('внутренний', results)
        results = self.derivation.derive(word_b='внутри', pos_b='adv', pos_a='adj')
        self.assertIn('внутренний', results)

    def test_adj_677_3(self):
        results = self.derivation.derive(word_b='вне', pos_b='adv', pos_a='adj')
        self.assertIn('внешний', results)
        results = self.derivation.derive(word_b='дома', pos_b='adv', pos_a='adj')
        self.assertIn('домашний', results)
        results = self.derivation.derive(word_b='всегда', pos_b='adv', pos_a='adj')
        self.assertIn('всегдашний', results)
        results = self.derivation.derive(word_b='тогда', pos_b='adv', pos_a='adj')
        self.assertIn('тогдашний', results)
        results = self.derivation.derive(word_b='вчера', pos_b='adv', pos_a='adj')
        self.assertIn('вчерашний', results)
        results = self.derivation.derive(word_b='завтра', pos_b='adv', pos_a='adj')
        self.assertIn('завтрашний', results)
        results = self.derivation.derive(word_b='сегодня', pos_b='adv', pos_a='adj')
        self.assertIn('сегодняшний', results)
        results = self.derivation.derive(word_b='намедни', pos_b='adv', pos_a='adj')
        self.assertIn('намеднишний', results)

    def test_adj_677_4(self):
        results = self.derivation.derive(word_b='взаправду', pos_b='adv', pos_a='adj')
        self.assertIn('взаправдашний', results)
        results = self.derivation.derive(word_b='там', pos_b='adv', pos_a='adj')
        self.assertIn('тамошний', results)
        results = self.derivation.derive(word_b='теперь', pos_b='adv', pos_a='adj')
        self.assertIn('теперешний', results)

    def test_adj_677_5(self):
        results = self.derivation.derive(word_b='давно', pos_b='adv', pos_a='adj')
        self.assertIn('давнишний', results)

    def test_adj_678_1(self):
        results = self.derivation.derive(word_b='против', pos_b='adv', pos_a='adj')
        self.assertIn('противный', results)
        results = self.derivation.derive(word_b='сплошь', pos_b='adv', pos_a='adj')
        self.assertIn('сплошной', results)
        results = self.derivation.derive(word_b='сквозь', pos_b='adv', pos_a='adj')
        self.assertIn('сквозной', results)
        results = self.derivation.derive(word_b='наружу', pos_b='adv', pos_a='adj')
        self.assertIn('наружный', results)
        results = self.derivation.derive(word_b='искони', pos_b='adv', pos_a='adj')
        self.assertIn('исконный', results)
        results = self.derivation.derive(word_b='априори', pos_b='adv', pos_a='adj')
        self.assertIn('априорный', results)
        results = self.derivation.derive(word_b='поперек', pos_b='adv', pos_a='adj')
        self.assertIn('поперечный', results)
        results = self.derivation.derive(word_b='акапела', pos_b='adv', pos_a='adj')
        self.assertIn('акапельный', results)
        results = self.derivation.derive(word_b='огулом', pos_b='adv', pos_a='adj')
        self.assertIn('огульный', results)
        results = self.derivation.derive(word_b='чуточку', pos_b='adv', pos_a='adj')
        self.assertIn('чуточный', results)

    def test_adj_678_2(self):
        results = self.derivation.derive(word_b='зря', pos_b='adv', pos_a='adj')
        self.assertIn('зряшный', results)

    def test_adj_678_3(self):
        results = self.derivation.derive(word_b='взаправду', pos_b='adv', pos_a='adj')
        self.assertIn('взаправдашный', results)

    def test_adj_678_4(self):
        results = self.derivation.derive(word_b='близ', pos_b='adv', pos_a='adj')
        self.assertIn('близкий', results)

    def test_adj_679(self):
        results = self.derivation.derive(word_b='пять', pos_b='num', pos_a='adj')
        self.assertIn('пятый', results)
        results = self.derivation.derive(word_b='восемь', pos_b='num', pos_a='adj')
        self.assertIn('восьмой', results)
        results = self.derivation.derive(word_b='триста', pos_b='num', pos_a='adj')
        self.assertIn('трехсотый', results)
        results = self.derivation.derive(word_b='тысяча', pos_b='num', pos_a='adj')
        self.assertIn('тысячный', results)
        results = self.derivation.derive(word_b='четыре', pos_b='num', pos_a='adj')
        self.assertIn('четвертый', results)
        results = self.derivation.derive(word_b='один', pos_b='num', pos_a='adj')
        self.assertIn('первый', results)
        results = self.derivation.derive(word_b='два', pos_b='num', pos_a='adj')
        self.assertIn('второй', results)

    def test_adj_680(self):
        results = self.derivation.derive(word_b='больше', pos_b='comp', pos_a='adj')
        self.assertIn('больший', results)
        results = self.derivation.derive(word_b='лучше', pos_b='comp', pos_a='adj')
        self.assertIn('лучший', results)

    def test_adj_681(self):
        results = self.derivation.derive(word_b='входить', pos_b='verb', pos_a='adj')
        self.assertIn('вхожий', results)
        results = self.derivation.derive(word_b='сходиться', pos_b='verb', pos_a='adj')
        self.assertIn('схожий', results)
        results = self.derivation.derive(word_b='приезжать', pos_b='verb', pos_a='adj')
        self.assertIn('приезжий', results)
        results = self.derivation.derive(word_b='походить', pos_b='verb', pos_a='adj')
        self.assertIn('похожий', results)
        results = self.derivation.derive(word_b='расходовать', pos_b='verb', pos_a='adj')
        self.assertIn('расхожий', results)
        results = self.derivation.derive(word_b='хворать', pos_b='verb', pos_a='adj')
        self.assertIn('хворый', results)
        results = self.derivation.derive(word_b='жить', pos_b='verb', pos_a='adj')
        self.assertIn('живой', results)
        results = self.derivation.derive(word_b='любить', pos_b='verb', pos_a='adj')
        self.assertIn('любый', results)
        results = self.derivation.derive(word_b='тошнить', pos_b='verb', pos_a='adj')
        self.assertIn('тошный', results)

    def test_adj_682(self):
        results = self.derivation.derive(word_b='будни', pos_b='noun', pos_a='adj')
        self.assertIn('будний', results)
        results = self.derivation.derive(word_b='весна', pos_b='noun', pos_a='adj')
        self.assertIn('вешний', results)
        results = self.derivation.derive(word_b='золото', pos_b='noun', pos_a='adj')
        self.assertIn('золотой', results)
        results = self.derivation.derive(word_b='работа', pos_b='noun', pos_a='adj')
        self.assertIn('рабочий', results)
        results = self.derivation.derive(word_b='охота', pos_b='noun', pos_a='adj')
        self.assertIn('охочий', results)
        results = self.derivation.derive(word_b='погода', pos_b='noun', pos_a='adj')
        self.assertIn('погожий', results)
        results = self.derivation.derive(word_b='болезнь', pos_b='noun', pos_a='adj')
        self.assertIn('болезный', results)
        results = self.derivation.derive(word_b='досуг', pos_b='noun', pos_a='adj')
        self.assertIn('досужий', results)
        results = self.derivation.derive(word_b='покат', pos_b='noun', pos_a='adj')
        self.assertIn('покатый', results)
        results = self.derivation.derive(word_b='свинья', pos_b='noun', pos_a='adj')
        self.assertIn('свиной', results)
        results = self.derivation.derive(word_b='жеребёнок', pos_b='noun', pos_a='adj')
        self.assertIn('жерёбой', results)
        results = self.derivation.derive(word_b='отец', pos_b='noun', pos_a='adj')
        self.assertIn('отчий', results)
        results = self.derivation.derive(word_b='орёл', pos_b='noun', pos_a='adj')
        self.assertIn('орлий', results)
        results = self.derivation.derive(word_b='патриарх', pos_b='noun', pos_a='adj')
        self.assertIn('патриарший', results)
        results = self.derivation.derive(word_b='князь', pos_b='noun', pos_a='adj')
        self.assertIn('княжой', results)

    def test_adj_683(self):
        results = self.derivation.derive(word_b='ритмичный', pos_b='adj', pos_a='adj')
        self.assertIn('аритмичный', results)

    def test_adj_684(self):
        results = self.derivation.derive(word_b='санитарный', pos_b='adj', pos_a='adj')
        self.assertIn('антисанитарный', results)

    def test_adj_685(self):
        results = self.derivation.derive(word_b='опасный', pos_b='adj', pos_a='adj')
        self.assertIn('архиопасный', results)

    def test_adj_686(self):
        results = self.derivation.derive(word_b='болезненный', pos_b='adj', pos_a='adj')
        self.assertIn('безболезненный', results)
        results = self.derivation.derive(word_b='искусный', pos_b='adj', pos_a='adj')
        self.assertIn('безыскусный', results)
        results = self.derivation.derive(word_b='подобный', pos_b='adj', pos_a='adj')
        self.assertIn('бесподобный', results)

    def test_adj_687(self):
        results = self.derivation.derive(word_b='плановый', pos_b='adj', pos_a='adj')
        self.assertIn('внеплановый', results)

    def test_adj_688(self):
        results = self.derivation.derive(word_b='отраслевой', pos_b='adj', pos_a='adj')
        self.assertIn('внутриотраслевой', results)

    def test_adj_689(self):
        results = self.derivation.derive(word_b='звуковой', pos_b='adj', pos_a='adj')
        self.assertIn('гиперзвуковой', results)

    def test_adj_690(self):
        results = self.derivation.derive(word_b='военный', pos_b='adj', pos_a='adj')
        self.assertIn('довоенный', results)

    def test_adj_691(self):
        results = self.derivation.derive(word_b='облачный', pos_b='adj', pos_a='adj')
        self.assertIn('заоблачный', results)

    def test_adj_692_1(self):
        results = self.derivation.derive(word_b='материальный', pos_b='adj', pos_a='adj')
        self.assertIn('имматериальный', results)

    def test_adj_692_2(self):
        results = self.derivation.derive(word_b='рациональный', pos_b='adj', pos_a='adj')
        self.assertIn('иррациональный', results)

    def test_adj_693(self):
        results = self.derivation.derive(word_b='национальный', pos_b='adj', pos_a='adj')
        self.assertIn('интернациональный', results)

    def test_adj_694(self):
        results = self.derivation.derive(word_b='бригадный', pos_b='adj', pos_a='adj')
        self.assertIn('межбригадный', results)
        results = self.derivation.derive(word_b='видовой', pos_b='adj', pos_a='adj')
        self.assertIn('междувидовой', results)

    def test_adj_695(self):
        results = self.derivation.derive(word_b='классовый', pos_b='adj', pos_a='adj')
        self.assertIn('надклассовый', results)

    def test_adj_696(self):
        results = self.derivation.derive(word_b='высший', pos_b='adj', pos_a='adj')
        self.assertIn('наивысший', results)
        results = self.derivation.derive(word_b='большой', pos_b='adj', pos_a='adj')
        self.assertIn('наибольший', results)
        results = self.derivation.derive(word_b='отважный', pos_b='adj', pos_a='adj')
        self.assertIn('наиотважный', results)

    def test_adj_697(self):
        results = self.derivation.derive(word_b='научный', pos_b='adj', pos_a='adj')
        self.assertIn('ненаучный', results)
        results = self.derivation.derive(word_b='обитаемый', pos_b='adj', pos_a='adj')
        self.assertIn('необитаемый', results)

    def test_adj_698(self):
        results = self.derivation.derive(word_b='опасный', pos_b='adj', pos_a='adj')
        self.assertIn('небезопасный', results)
        results = self.derivation.derive(word_b='известный', pos_b='adj', pos_a='adj')
        self.assertIn('небезызвестный', results)
        results = self.derivation.derive(word_b='корыстный', pos_b='adj', pos_a='adj')
        self.assertIn('небескорыстный', results)

    def test_adj_699(self):
        results = self.derivation.derive(word_b='солнечный', pos_b='adj', pos_a='adj')
        self.assertIn('околосолнечный', results)

    def test_adj_700(self):
        results = self.derivation.derive(word_b='тертый', pos_b='adj', pos_a='adj')
        self.assertIn('перетертый', results)

    def test_adj_701(self):
        results = self.derivation.derive(word_b='волжский', pos_b='adj', pos_a='adj')
        self.assertIn('поволжский', results)

    def test_adj_702(self):
        results = self.derivation.derive(word_b='интереснее', pos_b='comp', pos_a='comp')
        self.assertIn('поинтереснее', results)

    def test_adj_703(self):
        results = self.derivation.derive(word_b='крановый', pos_b='adj', pos_a='adj')
        self.assertIn('подкрановый', results)

    def test_adj_704(self):
        results = self.derivation.derive(word_b='октябрьский', pos_b='adj', pos_a='adj')
        self.assertIn('послеоктябрьский', results)

    def test_adj_705(self):
        results = self.derivation.derive(word_b='инфекционный', pos_b='adj', pos_a='adj')
        self.assertIn('постинфекционный', results)

    def test_adj_706(self):
        results = self.derivation.derive(word_b='скучный', pos_b='adj', pos_a='adj')
        self.assertIn('прескучный', results)

    def test_adj_707(self):
        results = self.derivation.derive(word_b='последний', pos_b='adj', pos_a='adj')
        self.assertIn('предпоследний', results)

    def test_adj_707_2(self):
        results = self.derivation.derive(word_b='рассветный', pos_b='adj', pos_a='adj')
        self.assertIn('передрассветный', results)

    def test_adj_708(self):
        results = self.derivation.derive(word_b='вокзальный', pos_b='adj', pos_a='adj')
        self.assertIn('привокзальный', results)

    def test_adj_709(self):
        results = self.derivation.derive(word_b='американский', pos_b='adj', pos_a='adj')
        self.assertIn('проамериканский', results)

    def test_adj_710(self):
        results = self.derivation.derive(word_b='законный', pos_b='adj', pos_a='adj')
        self.assertIn('противозаконный', results)

    def test_adj_711(self):
        results = self.derivation.derive(word_b='веселый', pos_b='adj', pos_a='adj')
        self.assertIn('развеселый', results)
        results = self.derivation.derive(word_b='кудрявый', pos_b='adj', pos_a='adj')
        self.assertIn('раскудрявый', results)

    def test_adj_712(self):
        results = self.derivation.derive(word_b='низкий', pos_b='adj', pos_a='adj')
        self.assertIn('сверхнизкий', results)

    def test_adj_713(self):
        results = self.derivation.derive(word_b='предельный', pos_b='adj', pos_a='adj')
        self.assertIn('сопредельный', results)

    def test_adj_714(self):
        results = self.derivation.derive(word_b='антарктический', pos_b='adj', pos_a='adj')
        self.assertIn('субантарктический', results)

    def test_adj_715(self):
        results = self.derivation.derive(word_b='эластичный', pos_b='adj', pos_a='adj')
        self.assertIn('суперэластичный', results)

    def test_adj_716(self):
        results = self.derivation.derive(word_b='континентальный', pos_b='adj', pos_a='adj')
        self.assertIn('трансконтинентальный', results)
        results = self.derivation.derive(word_b='европейский', pos_b='adj', pos_a='adj')
        self.assertIn('трансъевропейский', results)

    def test_adj_717(self):
        results = self.derivation.derive(word_b='современный', pos_b='adj', pos_a='adj')
        self.assertIn('ультрасовременный', results)

    def test_adj_718(self):
        results = self.derivation.derive(word_b='ординарный', pos_b='adj', pos_a='adj')
        self.assertIn('экстраординарный', results)

    def test_adj_719_1(self):
        results = self.derivation.derive(word_b='начальный', pos_b='adj', pos_a='adj')
        self.assertIn('изначальный', results)

    def test_adj_719_2(self):
        results = self.derivation.derive(word_b='прошлый', pos_b='adj', pos_a='adj')
        self.assertIn('позапрошлый', results)

    def test_adj_719_3(self):
        results = self.derivation.derive(word_b='территориальный', pos_b='adj', pos_a='adj')
        self.assertIn('экстерриториальный', results)

    def test_adj_723(self):
        results = self.derivation.derive(word_b='вина', pos_b='noun', pos_a='adj')
        self.assertIn('безвинный', results)
        results = self.derivation.derive(word_b='дар', pos_b='noun', pos_a='adj')
        self.assertIn('бездарный', results)
        results = self.derivation.derive(word_b='воля', pos_b='noun', pos_a='adj')
        self.assertIn('безвольный', results)
        results = self.derivation.derive(word_b='дождь', pos_b='noun', pos_a='adj')
        self.assertIn('бездождный', results)
        results = self.derivation.derive(word_b='дети', pos_b='noun', pos_a='adj')
        self.assertIn('бездетный', results)
        results = self.derivation.derive(word_b='рассудок', pos_b='noun', pos_a='adj')
        self.assertIn('безрассудный', results)
        results = self.derivation.derive(word_b='герой', pos_b='noun', pos_a='adj')
        self.assertIn('безгеройный', results)

    def test_adj_723_2(self):
        results = self.derivation.derive(word_b='талант', pos_b='noun', pos_a='adj')
        self.assertIn('бесталанный', results)
        results = self.derivation.derive(word_b='хозяин', pos_b='noun', pos_a='adj')
        self.assertIn('бесхозный', results)
        results = self.derivation.derive(word_b='хозяин', pos_b='noun', pos_a='adj')
        self.assertIn('бесхозяйный', results)

    def test_adj_723_3(self):
        results = self.derivation.derive(word_b='смысл', pos_b='noun', pos_a='adj')
        self.assertIn('бессмысленный', results)

    def test_adj_724(self):
        results = self.derivation.derive(word_b='вена', pos_b='noun', pos_a='adj')
        self.assertIn('внутривенный', results)
        results = self.derivation.derive(word_b='ряд', pos_b='noun', pos_a='adj')
        self.assertIn('внерядный', results)
        results = self.derivation.derive(word_b='зерно', pos_b='noun', pos_a='adj')
        self.assertIn('внутризеренный', results)

    def test_adj_724_2(self):
        results = self.derivation.derive(word_b='завод', pos_b='noun', pos_a='adj')
        self.assertIn('внутризаводский', results)

    def test_adj_725(self):
        results = self.derivation.derive(word_b='лес', pos_b='noun', pos_a='adj')
        self.assertIn('залесный', results)
        results = self.derivation.derive(word_b='стол', pos_b='noun', pos_a='adj')
        self.assertIn('застольный', results)
        results = self.derivation.derive(word_b='река', pos_b='noun', pos_a='adj')
        self.assertIn('заречный', results)
        results = self.derivation.derive(word_b='ухо', pos_b='noun', pos_a='adj')
        self.assertIn('заушный', results)
        results = self.derivation.derive(word_b='плечо', pos_b='noun', pos_a='adj')
        self.assertIn('заплечный', results)
        results = self.derivation.derive(word_b='граница', pos_b='noun', pos_a='adj')
        self.assertIn('заграничный', results)
        results = self.derivation.derive(word_b='печь', pos_b='noun', pos_a='adj')
        self.assertIn('запечный', results)

    def test_adj_725_2(self):
        results = self.derivation.derive(word_b='дон', pos_b='noun', pos_a='adj')
        self.assertIn('задонский', results)
        results = self.derivation.derive(word_b='море', pos_b='noun', pos_a='adj')
        self.assertIn('заморский', results)
        results = self.derivation.derive(word_b='волга', pos_b='noun', pos_a='adj')
        self.assertIn('заволжский', results)

    def test_adj_726(self):
        results = self.derivation.derive(word_b='луна', pos_b='noun', pos_a='adj')
        self.assertIn('залуненный', results)
        results = self.derivation.derive(word_b='лес', pos_b='noun', pos_a='adj')
        self.assertIn('залесенный', results)

    def test_adj_726_2(self):
        results = self.derivation.derive(word_b='кустарник', pos_b='noun', pos_a='adj')
        self.assertIn('закустаренный', results)

    def test_adj_726_3(self):
        results = self.derivation.derive(word_b='камыш', pos_b='noun', pos_a='adj')
        self.assertIn('закамышованный', results)

    def test_adj_727_1(self):
        results = self.derivation.derive(word_b='ряд', pos_b='noun', pos_a='adj')
        self.assertIn('междурядный', results)
        results = self.derivation.derive(word_b='кость', pos_b='noun', pos_a='adj')
        self.assertIn('межкостный', results)

    def test_adj_727_2(self):
        results = self.derivation.derive(word_b='клетка', pos_b='noun', pos_a='adj')
        self.assertIn('межклетный', results)

    def test_adj_727_3(self):
        results = self.derivation.derive(word_b='завод', pos_b='noun', pos_a='adj')
        self.assertIn('межзаводский', results)

    def test_adj_728_1(self):
        results = self.derivation.derive(word_b='бедро', pos_b='noun', pos_a='adj')
        self.assertIn('набедренный', results)

    def test_adj_728_2(self):
        results = self.derivation.derive(word_b='рука', pos_b='noun', pos_a='adj')
        self.assertIn('наручный', results)
        results = self.derivation.derive(word_b='лоб', pos_b='noun', pos_a='adj')
        self.assertIn('налобный', results)
        results = self.derivation.derive(word_b='плечо', pos_b='noun', pos_a='adj')
        self.assertIn('наплечный', results)
        results = self.derivation.derive(word_b='земля', pos_b='noun', pos_a='adj')
        self.assertIn('наземный', results)
        results = self.derivation.derive(word_b='стол', pos_b='noun', pos_a='adj')
        self.assertIn('настольный', results)
        results = self.derivation.derive(word_b='стена', pos_b='noun', pos_a='adj')
        self.assertIn('настенный', results)
        results = self.derivation.derive(word_b='скала', pos_b='noun', pos_a='adj')
        self.assertIn('наскальный', results)
        results = self.derivation.derive(word_b='поле', pos_b='noun', pos_a='adj')
        self.assertIn('напольный', results)

    def test_adj_729(self):
        results = self.derivation.derive(word_b='бровь', pos_b='noun', pos_a='adj')
        self.assertIn('надбровный', results)
        results = self.derivation.derive(word_b='лоб', pos_b='noun', pos_a='adj')
        self.assertIn('надлобный', results)
        results = self.derivation.derive(word_b='земля', pos_b='noun', pos_a='adj')
        self.assertIn('надземный', results)

    def test_adj_730(self):
        results = self.derivation.derive(word_b='вина', pos_b='noun', pos_a='adj')
        self.assertIn('невинный', results)
        results = self.derivation.derive(word_b='исход', pos_b='noun', pos_a='adj')
        self.assertIn('неисходный', results)
        results = self.derivation.derive(word_b='счастье', pos_b='noun', pos_a='adj')
        self.assertIn('несчастный', results)
        results = self.derivation.derive(word_b='забвение', pos_b='noun', pos_a='adj')
        self.assertIn('незабвенный', results)

    def test_adj_731(self):
        results = self.derivation.derive(word_b='ухо', pos_b='noun', pos_a='adj')
        self.assertIn('околоушный', results)
        results = self.derivation.derive(word_b='плод', pos_b='noun', pos_a='adj')
        self.assertIn('околоплодный', results)
        results = self.derivation.derive(word_b='земля', pos_b='noun', pos_a='adj')
        self.assertIn('околоземный', results)
        results = self.derivation.derive(word_b='луна', pos_b='noun', pos_a='adj')
        self.assertIn('окололунный', results)

    def test_adj_732(self):
        results = self.derivation.derive(word_b='глагол', pos_b='noun', pos_a='adj')
        self.assertIn('отглагольный', results)
        results = self.derivation.derive(word_b='имя', pos_b='noun', pos_a='adj')
        self.assertIn('отымённый', results)
        results = self.derivation.derive(word_b='наречие', pos_b='noun', pos_a='adj')
        self.assertIn('отнаречный', results)
        results = self.derivation.derive(word_b='предлог', pos_b='noun', pos_a='adj')
        self.assertIn('отпредложный', results)

    def test_adj_733_1(self):
        results = self.derivation.derive(word_b='море', pos_b='noun', pos_a='adj')
        self.assertIn('поморский', results)
        results = self.derivation.derive(word_b='волга', pos_b='noun', pos_a='adj')
        self.assertIn('поволжский', results)

    def test_adj_733_2(self):
        results = self.derivation.derive(word_b='сила', pos_b='noun', pos_a='adj')
        self.assertIn('посильный', results)
        results = self.derivation.derive(word_b='квартал', pos_b='noun', pos_a='adj')
        self.assertIn('поквартальный', results)
        results = self.derivation.derive(word_b='колено', pos_b='noun', pos_a='adj')
        self.assertIn('поколенный', results)
        results = self.derivation.derive(word_b='день', pos_b='noun', pos_a='adj')
        self.assertIn('поденный', results)
        results = self.derivation.derive(word_b='берег', pos_b='noun', pos_a='adj')
        self.assertIn('побережный', results)
        results = self.derivation.derive(word_b='река', pos_b='noun', pos_a='adj')
        self.assertIn('поречный', results)

    def test_adj_734_1(self):
        results = self.derivation.derive(word_b='голова', pos_b='noun', pos_a='adj')
        self.assertIn('подголовный', results)
        results = self.derivation.derive(word_b='глаз', pos_b='noun', pos_a='adj')
        self.assertIn('подглазный', results)
        results = self.derivation.derive(word_b='начало', pos_b='noun', pos_a='adj')
        self.assertIn('подначальный', results)
        results = self.derivation.derive(word_b='река', pos_b='noun', pos_a='adj')
        self.assertIn('подречный', results)
        results = self.derivation.derive(word_b='язык', pos_b='noun', pos_a='adj')
        self.assertIn('подъязычный', results)
        results = self.derivation.derive(word_b='кожа', pos_b='noun', pos_a='adj')
        self.assertIn('подкожный', results)
        results = self.derivation.derive(word_b='власть', pos_b='noun', pos_a='adj')
        self.assertIn('подвластный', results)

    def test_adj_734_2(self):
        results = self.derivation.derive(word_b='лепесток', pos_b='noun', pos_a='adj')
        self.assertIn('подлепестный', results)
        results = self.derivation.derive(word_b='москва', pos_b='noun', pos_a='adj')
        self.assertIn('подмосковный', results)

    def test_adj_735(self):
        results = self.derivation.derive(word_b='мост', pos_b='noun', pos_a='adj')
        self.assertIn('предмостный', results)
        results = self.derivation.derive(word_b='пахота', pos_b='noun', pos_a='adj')
        self.assertIn('предпахотный', results)

    def test_adj_736(self):
        results = self.derivation.derive(word_b='двор', pos_b='noun', pos_a='adj')
        self.assertIn('придворный', results)
        results = self.derivation.derive(word_b='река', pos_b='noun', pos_a='adj')
        self.assertIn('приречный', results)

    def test_adj_736_2(self):
        results = self.derivation.derive(word_b='ферма', pos_b='noun', pos_a='adj')
        self.assertIn('прифермский', results)
        results = self.derivation.derive(word_b='дон', pos_b='noun', pos_a='adj')
        self.assertIn('придонский', results)
        results = self.derivation.derive(word_b='море', pos_b='noun', pos_a='adj')
        self.assertIn('приморский', results)

    def test_adj_737(self):
        results = self.derivation.derive(word_b='время', pos_b='noun', pos_a='adj')
        self.assertIn('современный', results)
        results = self.derivation.derive(word_b='звук', pos_b='noun', pos_a='adj')
        self.assertIn('созвучный', results)
        results = self.derivation.derive(word_b='чувство', pos_b='noun', pos_a='adj')
        self.assertIn('сочувственный', results)

    def test_adj_738(self):
        results = self.derivation.derive(word_b='земля', pos_b='noun', pos_a='adj')
        self.assertIn('средиземный', results)
        results = self.derivation.derive(word_b='день', pos_b='noun', pos_a='adj')
        self.assertIn('средидневный', results)
        results = self.derivation.derive(word_b='сезон', pos_b='noun', pos_a='adj')
        self.assertIn('средисезонный', results)

    def test_adj_739(self):
        results = self.derivation.derive(word_b='седло', pos_b='noun', pos_a='adj')
        self.assertIn('чересседельный', results)
        results = self.derivation.derive(word_b='подушка', pos_b='noun', pos_a='adj')
        self.assertIn('чересподушечный', results)
        results = self.derivation.derive(word_b='подъем', pos_b='noun', pos_a='adj')
        self.assertIn('чересподъемный', results)
        results = self.derivation.derive(word_b='плечо', pos_b='noun', pos_a='adj')
        self.assertIn('чересплечный', results)
        results = self.derivation.derive(word_b='полоса', pos_b='noun', pos_a='adj')
        self.assertIn('чересполосный', results)
        results = self.derivation.derive(word_b='борозда', pos_b='noun', pos_a='adj')
        self.assertIn('черезбороздный', results)
        results = self.derivation.derive(word_b='ряд', pos_b='noun', pos_a='adj')
        self.assertIn('черезрядный', results)

    def test_adj_740(self):
        results = self.derivation.derive(word_b='мера', pos_b='noun', pos_a='adj')
        self.assertIn('чрезмерный', results)

    def test_adj_740_2(self):
        results = self.derivation.derive(word_b='слово', pos_b='noun', pos_a='adj')
        self.assertIn('дословный', results)

    def test_adj_740_3(self):
        results = self.derivation.derive(word_b='ряд', pos_b='noun', pos_a='adj')
        self.assertIn('вдольрядный', results)

    def test_adj_740_4(self):
        results = self.derivation.derive(word_b='злоба', pos_b='noun', pos_a='adj')
        self.assertIn('незлобивый', results)

    def test_adj_740_5(self):
        results = self.derivation.derive(word_b='люд', pos_b='noun', pos_a='adj')
        self.assertIn('нелюдимый', results)

    def test_adj_740_6(self):
        results = self.derivation.derive(word_b='земля', pos_b='noun', pos_a='adj')
        self.assertIn('приземистый', results)

    def test_adj_740_7(self):
        results = self.derivation.derive(word_b='лапа', pos_b='noun', pos_a='adj')
        self.assertIn('разлапистый', results)

    def test_adj_743(self):
        results = self.derivation.derive(word_b='разделять', pos_b='verb', pos_a='adj')
        self.assertIn('безраздельный', results)
        results = self.derivation.derive(word_b='упрекать', pos_b='verb', pos_a='adj')
        self.assertIn('безупречный', results)
        results = self.derivation.derive(word_b='оглядываться', pos_b='verb', pos_a='adj')
        self.assertIn('безоглядный', results)
        results = self.derivation.derive(word_b='пробудить', pos_b='verb', pos_a='adj')
        self.assertIn('беспробудный', results)
        results = self.derivation.derive(word_b='печься', pos_b='verb', pos_a='adj')
        self.assertIn('беспечный', results)

    def test_adj_743_2(self):
        results = self.derivation.derive(word_b='вылезти', pos_b='verb', pos_a='adj')
        self.assertIn('безвылазный', results)
        results = self.derivation.derive(word_b='перестать', pos_b='verb', pos_a='adj')
        self.assertIn('беспрестанный', results)
        results = self.derivation.derive(word_b='надеяться', pos_b='verb', pos_a='adj')
        self.assertIn('безнадёжный', results)

    def test_adj_744(self):
        results = self.derivation.derive(word_b='возвратить', pos_b='verb', pos_a='adj')
        self.assertIn('невозвратный', results)
        results = self.derivation.derive(word_b='избежать', pos_b='verb', pos_a='adj')
        self.assertIn('неизбежный', results)
        results = self.derivation.derive(word_b='проглядывать', pos_b='verb', pos_a='adj')
        self.assertIn('непроглядный', results)
        results = self.derivation.derive(word_b='постигнуть', pos_b='verb', pos_a='adj')
        self.assertIn('непостижный', results)
        results = self.derivation.derive(word_b='умолкать', pos_b='verb', pos_a='adj')
        self.assertIn('неумолчный', results)

    def test_adj_744_2(self):
        results = self.derivation.derive(word_b='проезжать', pos_b='verb', pos_a='adj')
        self.assertIn('непроездный', results)

    def test_adj_744_3(self):
        results = self.derivation.derive(word_b='счесть', pos_b='verb', pos_a='adj')
        self.assertIn('несчётный', results)
        results = self.derivation.derive(word_b='считать', pos_b='verb', pos_a='adj')
        self.assertIn('несчётный', results)
        results = self.derivation.derive(word_b='поднять', pos_b='verb', pos_a='adj')
        self.assertIn('неподъёмный', results)
        results = self.derivation.derive(word_b='поднимать', pos_b='verb', pos_a='adj')
        self.assertIn('неподъёмный', results)
        results = self.derivation.derive(word_b='уснуть', pos_b='verb', pos_a='adj')
        self.assertIn('неусыпный', results)
        results = self.derivation.derive(word_b='вылезти', pos_b='verb', pos_a='adj')
        self.assertIn('невылазный', results)
        results = self.derivation.derive(word_b='вылезать', pos_b='verb', pos_a='adj')
        self.assertIn('невылазный', results)
        results = self.derivation.derive(word_b='объять', pos_b='verb', pos_a='adj')
        self.assertIn('необъятный', results)
        results = self.derivation.derive(word_b='устать', pos_b='verb', pos_a='adj')
        self.assertIn('неустанный', results)

    def test_adj_745(self):
        results = self.derivation.derive(word_b='зыбнуть', pos_b='verb', pos_a='adj')
        self.assertIn('незыблемый', results)
        results = self.derivation.derive(word_b='умолкать', pos_b='verb', pos_a='adj')
        self.assertIn('неумолкаемый', results)
        results = self.derivation.derive(word_b='минуть', pos_b='verb', pos_a='adj')
        self.assertIn('неминуемый', results)
        results = self.derivation.derive(word_b='передавать', pos_b='verb', pos_a='adj')
        self.assertIn('непередаваемый', results)
        results = self.derivation.derive(word_b='забывать', pos_b='verb', pos_a='adj')
        self.assertIn('незабываемый', results)
        results = self.derivation.derive(word_b='узнавать', pos_b='verb', pos_a='adj')
        self.assertIn('неузнаваемый', results)

    def test_adj_745_2(self):
        results = self.derivation.derive(word_b='делить', pos_b='verb', pos_a='adj')
        self.assertIn('неделимый', results)
        results = self.derivation.derive(word_b='удержать', pos_b='verb', pos_a='adj')
        self.assertIn('неудержимый', results)
        results = self.derivation.derive(word_b='одолеть', pos_b='verb', pos_a='adj')
        self.assertIn('неодолимый', results)
        results = self.derivation.derive(word_b='опровергнуть', pos_b='verb', pos_a='adj')
        self.assertIn('неопровержимый', results)
        results = self.derivation.derive(word_b='колебать', pos_b='verb', pos_a='adj')
        self.assertIn('неколебимый', results)
        results = self.derivation.derive(word_b='превзойти', pos_b='verb', pos_a='adj')
        self.assertIn('непревзойдимо', results)

    def test_adj_745_3(self):
        results = self.derivation.derive(word_b='описать', pos_b='verb', pos_a='adj')
        self.assertIn('неописуемый', results)

    def test_adj_746(self):
        results = self.derivation.derive(word_b='относить', pos_b='verb', pos_a='adj')
        self.assertIn('безотносительный', results)
        results = self.derivation.derive(word_b='доказать', pos_b='verb', pos_a='adj')
        self.assertIn('бездоказательный', results)

    def test_adj_746_2(self):
        results = self.derivation.derive(word_b='замедлить', pos_b='verb', pos_a='adj')
        self.assertIn('незамедлительный', results)

    def test_adj_746_3(self):
        results = self.derivation.derive(word_b='сказать', pos_b='verb', pos_a='adj')
        self.assertIn('несказанный', results)
        results = self.derivation.derive(word_b='ждать', pos_b='verb', pos_a='adj')
        self.assertIn('нежданный', results)
        results = self.derivation.derive(word_b='ожидать', pos_b='verb', pos_a='adj')
        self.assertIn('неожиданный', results)

    def test_adj_746_4(self):
        results = self.derivation.derive(word_b='наказать', pos_b='verb', pos_a='adj')
        self.assertIn('безнаказанный', results)

    def test_adj_747(self):
        results = self.derivation.derive(word_b='спать', pos_b='verb', pos_a='adj')
        self.assertIn('заспанный', results)
        results = self.derivation.derive(word_b='плакать', pos_b='verb', pos_a='adj')
        self.assertIn('заплаканный', results)
        results = self.derivation.derive(word_b='реветь', pos_b='verb', pos_a='adj')
        self.assertIn('зареванный', results)

    def test_adj_748(self):
        results = self.derivation.derive(word_b='миновать', pos_b='verb', pos_a='adj')
        self.assertIn('неминучий', results)

    def test_adj_748_2(self):
        results = self.derivation.derive(word_b='радеть', pos_b='verb', pos_a='adj')
        self.assertIn('нерадивый', results)

    def test_adj_748_3(self):
        results = self.derivation.derive(word_b='отвязаться', pos_b='verb', pos_a='adj')
        self.assertIn('неотвязчивый', results)

    def test_adj_748_4(self):
        results = self.derivation.derive(word_b='бороть', pos_b='verb', pos_a='adj')
        self.assertIn('необоримый', results)

    def test_adj_748_5(self):
        results = self.derivation.derive(word_b='бороть', pos_b='verb', pos_a='adj')
        self.assertIn('непреоборимый', results)

    def test_adj_748_6(self):
        results = self.derivation.derive(word_b='унывать', pos_b='verb', pos_a='adj')
        self.assertIn('заунывный', results)

    def test_adj_748_7(self):
        results = self.derivation.derive(word_b='торопиться', pos_b='verb', pos_a='adj')
        self.assertIn('расторопный', results)

    def test_adj_748_8(self):
        results = self.derivation.derive(word_b='глядеть', pos_b='verb', pos_a='adj')
        self.assertIn('наглядный', results)

    def test_adj_748_9(self):
        results = self.derivation.derive(word_b='жрать', pos_b='verb', pos_a='adj')
        self.assertIn('прожорливый', results)

    def test_adj_748_10(self):
        results = self.derivation.derive(word_b='зачать', pos_b='verb', pos_a='adj')
        self.assertIn('противозачаточный', results)

    def test_adj_750(self):
        results = self.derivation.derive(word_b='кислый', pos_b='adj', pos_a='adj')
        self.assertIn('закисленный', results)
        results = self.derivation.derive(word_b='бытовой', pos_b='adj', pos_a='adj')
        self.assertIn('забытовлённый', results)

    def test_adj_751(self):
        results = self.derivation.derive(word_b='голый', pos_b='adj', pos_a='adj')
        self.assertIn('нагольный', results)

    def test_adj_751_2(self):
        results = self.derivation.derive(word_b='широкий', pos_b='adj', pos_a='adj')
        self.assertIn('обширный', results)

    def test_adj_751_3(self):
        results = self.derivation.derive(word_b='слепой', pos_b='adj', pos_a='adj')
        self.assertIn('подслеповатый', results)

    def test_adj_751_4(self):
        results = self.derivation.derive(word_b='долгий', pos_b='adj', pos_a='adj')
        self.assertIn('продолговатый', results)

    def test_adj_751_5(self):
        results = self.derivation.derive(word_b='вместе', pos_b='adv', pos_a='adj')
        self.assertIn('совместный', results)

    def test_adj_752(self):
        results = self.derivation.derive(word_b='язык', pos_b='noun', pos_a='adj')
        self.assertIn('безъязыкий', results)
        results = self.derivation.derive(word_b='нога', pos_b='noun', pos_a='adj')
        self.assertIn('безногий', results)
        results = self.derivation.derive(word_b='зуб', pos_b='noun', pos_a='adj')
        self.assertIn('беззубый', results)
        results = self.derivation.derive(word_b='крыло', pos_b='noun', pos_a='adj')
        self.assertIn('бескрылый', results)
        results = self.derivation.derive(word_b='бровь', pos_b='noun', pos_a='adj')
        self.assertIn('безбровый', results)
        results = self.derivation.derive(word_b='палец', pos_b='noun', pos_a='adj')
        self.assertIn('беспалый', results)
        results = self.derivation.derive(word_b='кудри', pos_b='noun', pos_a='adj')
        self.assertIn('бескудрая', results)
        results = self.derivation.derive(word_b='грош', pos_b='noun', pos_a='adj')
        self.assertIn('безгроший', results)
        results = self.derivation.derive(word_b='крыша', pos_b='noun', pos_a='adj')
        self.assertIn('бескрыший', results)

    def test_adj_752_2(self):
        results = self.derivation.derive(word_b='стыд', pos_b='noun', pos_a='adj')
        self.assertIn('бесстыжий', results)

    def test_adj_752_3(self):
        results = self.derivation.derive(word_b='мозг', pos_b='noun', pos_a='adj')
        self.assertIn('безмозглый', results)

    def test_adj_753(self):
        results = self.derivation.derive(word_b='поросенок', pos_b='noun', pos_a='adj')
        self.assertIn('супоросая', results)
        results = self.derivation.derive(word_b='ягненок', pos_b='noun', pos_a='adj')
        self.assertIn('суягная', results)

    def test_adj_753_2(self):
        results = self.derivation.derive(word_b='зима', pos_b='noun', pos_a='adj')
        self.assertIn('озимый', results)

    def test_adj_753_3(self):
        results = self.derivation.derive(word_b='лапа', pos_b='noun', pos_a='adj')
        self.assertIn('разлапый', results)

    def test_adj_753_4(self):
        results = self.derivation.derive(word_b='глубокий', pos_b='adj', pos_a='adj')
        self.assertIn('приглубый', results)

    def test_adj_753_5(self):
        results = self.derivation.derive(word_b='слепой', pos_b='adj', pos_a='adj')
        self.assertIn('подслепый', results)

if __name__ == '__main__':
    unittest.main(verbosity=2)
