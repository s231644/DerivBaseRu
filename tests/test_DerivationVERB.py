import unittest

from src.Derivation import Derivation


class TestDerivation(unittest.TestCase):
    def setUp(self):
        self.derivation = Derivation()

    def tearDown(self):
        del self.derivation

    def test_verb_794(self):
        results = self.derivation.derive(word_b='лиса', pos_b='noun', pos_a='verb')
        self.assertIn('лисить', results)
        results = self.derivation.derive(word_b='партизан', pos_b='noun', pos_a='verb')
        self.assertIn('партизанить', results)
        results = self.derivation.derive(word_b='козёл', pos_b='noun', pos_a='verb')
        self.assertIn('козлить', results)
        results = self.derivation.derive(word_b='решето', pos_b='noun', pos_a='verb')
        self.assertIn('решетить', results)
        results = self.derivation.derive(word_b='слесарь', pos_b='noun', pos_a='verb')
        self.assertIn('слесарить', results)
        results = self.derivation.derive(word_b='вьюга', pos_b='noun', pos_a='verb')
        self.assertIn('вьюжить', results)
        results = self.derivation.derive(word_b='куртизанка', pos_b='noun', pos_a='verb')
        self.assertIn('куртзанить', results)
        results = self.derivation.derive(word_b='лоск', pos_b='noun', pos_a='verb')
        self.assertIn('лощить', results)
        results = self.derivation.derive(word_b='снег', pos_b='noun', pos_a='verb')
        self.assertIn('снежить', results)
        results = self.derivation.derive(word_b='потрох', pos_b='noun', pos_a='verb')
        self.assertIn('потрошить', results)
        results = self.derivation.derive(word_b='паузок', pos_b='noun', pos_a='verb')
        self.assertIn('паузить', results)
        results = self.derivation.derive(word_b='воща', pos_b='noun', pos_a='verb')
        self.assertIn('вощить', results)
        results = self.derivation.derive(word_b='сторож', pos_b='noun', pos_a='verb')
        self.assertIn('сторожить', results)
        results = self.derivation.derive(word_b='перец', pos_b='noun', pos_a='verb')
        self.assertIn('перчить', results)
        results = self.derivation.derive(word_b='рой', pos_b='noun', pos_a='verb')
        self.assertIn('роить', results)
        results = self.derivation.derive(word_b='лицемерие', pos_b='noun', pos_a='verb')
        self.assertIn('лицемерить', results)
        results = self.derivation.derive(word_b='соль', pos_b='noun', pos_a='verb')
        self.assertIn('солить', results)
        results = self.derivation.derive(word_b='время', pos_b='noun', pos_a='verb')
        self.assertIn('временить', results)

    def test_verb_794_1(self):
        results = self.derivation.derive(word_b='нянька', pos_b='noun', pos_a='verb')
        self.assertIn('нянчить', results)
        results = self.derivation.derive(word_b='песок', pos_b='noun', pos_a='verb')
        self.assertIn('песочить', results)
        results = self.derivation.derive(word_b='убыток', pos_b='noun', pos_a='verb')
        self.assertIn('убыточить', results)

    def test_verb_794_2(self):
        results = self.derivation.derive(word_b='дневалить', pos_b='noun', pos_a='verb')
        self.assertIn('дневальный', results)

    def test_verb_795(self):
        results = self.derivation.derive(word_b='глупый', pos_b='adj', pos_a='verb')
        self.assertIn('глупить', results)
        results = self.derivation.derive(word_b='бодрый', pos_b='adj', pos_a='verb')
        self.assertIn('бодрить', results)
        results = self.derivation.derive(word_b='грязный', pos_b='adj', pos_a='verb')
        self.assertIn('грязнить', results)
        results = self.derivation.derive(word_b='грустный', pos_b='adj', pos_a='verb')
        self.assertIn('грустить', results)
        results = self.derivation.derive(word_b='гладкий', pos_b='adj', pos_a='verb')
        self.assertIn('гладить', results)
        results = self.derivation.derive(word_b='горький', pos_b='adj', pos_a='verb')
        self.assertIn('горчить', results)
        results = self.derivation.derive(word_b='свинячий', pos_b='adj', pos_a='verb')
        self.assertIn('свинячить', results)

    def test_verb_795_1(self):
        results = self.derivation.derive(word_b='ледяной', pos_b='adj', pos_a='verb')
        self.assertIn('леденить', results)

    def test_verb_795_2(self):
        results = self.derivation.derive(word_b='бесславный', pos_b='adj', pos_a='verb')
        self.assertIn('бесславить', results)
        results = self.derivation.derive(word_b='широкий', pos_b='adj', pos_a='verb')
        self.assertIn('ширить', results)
        results = self.derivation.derive(word_b='мокрый', pos_b='adj', pos_a='verb')
        self.assertIn('мочить', results)
        results = self.derivation.derive(word_b='сердитый', pos_b='adj', pos_a='verb')
        self.assertIn('сердить', results)

    def test_verb_795_3(self):
        results = self.derivation.derive(word_b='темнее', pos_b='comp', pos_a='verb')
        self.assertIn('темнить', results)
        results = self.derivation.derive(word_b='разнообразнее', pos_b='comp', pos_a='verb')
        self.assertIn('разнообразить', results)
        results = self.derivation.derive(word_b='мельче', pos_b='comp', pos_a='verb')
        self.assertIn('мельчить', results)
        results = self.derivation.derive(word_b='крепче', pos_b='comp', pos_a='verb')
        self.assertIn('крепить', results)

    def test_verb_798(self):
        results = self.derivation.derive(word_b='двое', pos_b='num', pos_a='verb')
        self.assertIn('двоить', results)
        results = self.derivation.derive(word_b='четверо', pos_b='num', pos_a='verb')
        self.assertIn('четверить', results)

    def test_verb_799(self):
        results = self.derivation.derive(word_b='князь', pos_b='noun', pos_a='verb')
        self.assertIn('княжить', results)
        results = self.derivation.derive(word_b='скорняк', pos_b='noun', pos_a='verb')
        self.assertIn('скорняжить', results)
        results = self.derivation.derive(word_b='тяжкий', pos_b='noun', pos_a='verb')
        self.assertIn('тягчить', results)
        results = self.derivation.derive(word_b='мелкий', pos_b='noun', pos_a='verb')
        self.assertIn('мельчить', results)

    def test_verb_799_1(self):
        results = self.derivation.derive(word_b='багор', pos_b='noun', pos_a='verb')
        self.assertIn('багрить', results)
        results = self.derivation.derive(word_b='коготь', pos_b='noun', pos_a='verb')
        self.assertIn('когтить', results)
        results = self.derivation.derive(word_b='мох', pos_b='noun', pos_a='verb')
        self.assertIn('мшить', results)

    def test_verb_799_2(self):
        results = self.derivation.derive(word_b='пепел', pos_b='noun', pos_a='verb')
        self.assertIn('пепелить', results)
        results = self.derivation.derive(word_b='щебень', pos_b='noun', pos_a='verb')
        self.assertIn('щебенить', results)
        results = self.derivation.derive(word_b='песок', pos_b='noun', pos_a='verb')
        self.assertIn('песочить', results)
        results = self.derivation.derive(word_b='убыток', pos_b='noun', pos_a='verb')
        self.assertIn('убыточить', results)

    def test_verb_799_3(self):
        results = self.derivation.derive(word_b='копоть', pos_b='noun', pos_a='verb')
        self.assertIn('коптить', results)
        results = self.derivation.derive(word_b='шабер', pos_b='noun', pos_a='verb')
        self.assertIn('шабрить', results)

    def test_verb_805(self):
        results = self.derivation.derive(word_b='полоса', pos_b='noun', pos_a='verb')
        self.assertIn('полосовать', results)
        results = self.derivation.derive(word_b='плут', pos_b='noun', pos_a='verb')
        self.assertIn('плутовать', results)
        results = self.derivation.derive(word_b='шпиль', pos_b='noun', pos_a='verb')
        self.assertIn('шпилевать', results)
        results = self.derivation.derive(word_b='день', pos_b='noun', pos_a='verb')
        self.assertIn('дневать', results)
        results = self.derivation.derive(word_b='цикля', pos_b='noun', pos_a='verb')
        self.assertIn('циклевать', results)
        results = self.derivation.derive(word_b='критика', pos_b='noun', pos_a='verb')
        self.assertIn('критиковать', results)
        results = self.derivation.derive(word_b='праздник', pos_b='noun', pos_a='verb')
        self.assertIn('праздновать', results)
        results = self.derivation.derive(word_b='шприц', pos_b='noun', pos_a='verb')
        self.assertIn('шприцевать', results)
        results = self.derivation.derive(word_b='комиссия', pos_b='noun', pos_a='verb')
        self.assertIn('комиссовать', results)
        results = self.derivation.derive(word_b='глазурь', pos_b='noun', pos_a='verb')
        self.assertIn('глазуровать', results)

    def test_verb_805_1(self):
        results = self.derivation.derive(word_b='резюме', pos_b='noun', pos_a='verb')
        self.assertIn('резюмировать', results)
        results = self.derivation.derive(word_b='интервью', pos_b='noun', pos_a='verb')
        self.assertIn('интервьюировать', results)
        results = self.derivation.derive(word_b='табу', pos_b='noun', pos_a='verb')
        self.assertIn('табуировать', results)
        results = self.derivation.derive(word_b='цитата', pos_b='noun', pos_a='verb')
        self.assertIn('цитировать', results)
        results = self.derivation.derive(word_b='травма', pos_b='noun', pos_a='verb')
        self.assertIn('травмировать', results)
        results = self.derivation.derive(word_b='бюрократ', pos_b='noun', pos_a='verb')
        self.assertIn('бюрократизировать', results)
        results = self.derivation.derive(word_b='брикет', pos_b='noun', pos_a='verb')
        self.assertIn('брикетировать', results)
        results = self.derivation.derive(word_b='асфальт', pos_b='noun', pos_a='verb')
        self.assertIn('асфальтировать', results)
        results = self.derivation.derive(word_b='лорнет', pos_b='noun', pos_a='verb')
        self.assertIn('лорнировать', results)
        results = self.derivation.derive(word_b='финансы', pos_b='noun', pos_a='verb')
        self.assertIn('финансировать', results)
        results = self.derivation.derive(word_b='никель', pos_b='noun', pos_a='verb')
        self.assertIn('никелировать', results)
        results = self.derivation.derive(word_b='субсидия', pos_b='noun', pos_a='verb')
        self.assertIn('субсидировать', results)
        results = self.derivation.derive(word_b='алюминий', pos_b='noun', pos_a='verb')
        self.assertIn('алюминировать', results)
        results = self.derivation.derive(word_b='капель', pos_b='noun', pos_a='verb')
        self.assertIn('капелировать', results)

    def test_verb_805_2(self):
        results = self.derivation.derive(word_b='алгебра', pos_b='noun', pos_a='verb')
        self.assertIn('алгебраизировать', results)
        results = self.derivation.derive(word_b='тонус', pos_b='noun', pos_a='verb')
        self.assertIn('тонизировать', results)
        results = self.derivation.derive(word_b='фокус', pos_b='noun', pos_a='verb')
        self.assertIn('фокусировать', results)
        results = self.derivation.derive(word_b='бутон', pos_b='noun', pos_a='verb')
        self.assertIn('бутонизировать', results)
        results = self.derivation.derive(word_b='иммунитет', pos_b='noun', pos_a='verb')
        self.assertIn('иммунизировать', results)
        results = self.derivation.derive(word_b='математика', pos_b='noun', pos_a='verb')
        self.assertIn('математизировать', results)
        results = self.derivation.derive(word_b='герой', pos_b='noun', pos_a='verb')
        self.assertIn('героизировать', results)
        results = self.derivation.derive(word_b='аммоний', pos_b='noun', pos_a='verb')
        self.assertIn('аммонизировать', results)

    def test_verb_805_3(self):
        results = self.derivation.derive(word_b='кристалл', pos_b='noun', pos_a='verb')
        self.assertIn('кристаллизовать', results)
        results = self.derivation.derive(word_b='паралич', pos_b='noun', pos_a='verb')
        self.assertIn('парализовать', results)
        results = self.derivation.derive(word_b='колония', pos_b='noun', pos_a='verb')
        self.assertIn('колонизовать', results)

    def test_verb_805_4(self):
        results = self.derivation.derive(word_b='транскрипция', pos_b='noun', pos_a='verb')
        self.assertIn('транскрибировать', results)
        results = self.derivation.derive(word_b='интонация', pos_b='noun', pos_a='verb')
        self.assertIn('интонировать', results)

    def test_verb_807(self):
        results = self.derivation.derive(word_b='лютый', pos_b='adj', pos_a='verb')
        self.assertIn('лютовать', results)
        results = self.derivation.derive(word_b='озорный', pos_b='adj', pos_a='verb')
        self.assertIn('озоровать', results)
        results = self.derivation.derive(word_b='схематичный', pos_b='adj', pos_a='verb')
        self.assertIn('схематизировать', results)
        results = self.derivation.derive(word_b='оптимальный', pos_b='adj', pos_a='verb')
        self.assertIn('оптимизировать', results)
        results = self.derivation.derive(word_b='индивидуальный', pos_b='adj', pos_a='verb')
        self.assertIn('индивидуализировать', results)
        results = self.derivation.derive(word_b='латинский', pos_b='adj', pos_a='verb')
        self.assertIn('латинизировать', results)
        results = self.derivation.derive(word_b='фашистский', pos_b='adj', pos_a='verb')
        self.assertIn('фашизировать', results)
        results = self.derivation.derive(word_b='герметический', pos_b='adj', pos_a='verb')
        self.assertIn('герметизировать', results)

    def test_verb_807_1(self):
        results = self.derivation.derive(word_b='стабильнее', pos_b='comp', pos_a='verb')
        self.assertIn('стабилизировать', results)

    def test_verb_807_2(self):
        results = self.derivation.derive(word_b='гипноз', pos_b='noun', pos_a='verb')
        self.assertIn('гипнотизировать', results)
        results = self.derivation.derive(word_b='наркоз', pos_b='noun', pos_a='verb')
        self.assertIn('наркотизировать', results)
        results = self.derivation.derive(word_b='рефлекс', pos_b='noun', pos_a='verb')
        self.assertIn('рефлектировать', results)
        results = self.derivation.derive(word_b='рефлекс', pos_b='noun', pos_a='verb')
        self.assertIn('рефлексировать', results)
        results = self.derivation.derive(word_b='флексия', pos_b='noun', pos_a='verb')
        self.assertIn('флектировать', results)
        results = self.derivation.derive(word_b='флексия', pos_b='noun', pos_a='verb')
        self.assertIn('флексировать', results)

    def test_verb_807_3(self):
        results = self.derivation.derive(word_b='фланг', pos_b='noun', pos_a='verb')
        self.assertIn('фланкировать', results)
        results = self.derivation.derive(word_b='суспензия', pos_b='noun', pos_a='verb')
        self.assertIn('суспендировать', results)
        results = self.derivation.derive(word_b='суспензия', pos_b='noun', pos_a='verb')
        self.assertIn('суспензировать', results)
        results = self.derivation.derive(word_b='эрозия', pos_b='noun', pos_a='verb')
        self.assertIn('эродировать', results)
        results = self.derivation.derive(word_b='депозит', pos_b='noun', pos_a='verb')
        self.assertIn('депонировать', results)
        results = self.derivation.derive(word_b='музыка', pos_b='noun', pos_a='verb')
        self.assertIn('музицировать', results)
        results = self.derivation.derive(word_b='эмульсия', pos_b='noun', pos_a='verb')
        self.assertIn('эмульгировать', results)
        results = self.derivation.derive(word_b='эмульсия', pos_b='noun', pos_a='verb')
        self.assertIn('эмульсировать', results)

    def test_verb_807_4(self):
        results = self.derivation.derive(word_b='глянец', pos_b='noun', pos_a='verb')
        self.assertIn('глянцевать', results)
        results = self.derivation.derive(word_b='день', pos_b='noun', pos_a='verb')
        self.assertIn('дневать', results)
        results = self.derivation.derive(word_b='пасынок', pos_b='noun', pos_a='verb')
        self.assertIn('пасынковать', results)

    def test_verb_807_5(self):
        results = self.derivation.derive(word_b='мебель', pos_b='noun', pos_a='verb')
        self.assertIn('меблировать', results)
        results = self.derivation.derive(word_b='шабер', pos_b='noun', pos_a='verb')
        self.assertIn('шабровать', results)

    def test_verb_812(self):
        results = self.derivation.derive(word_b='столяр', pos_b='noun', pos_a='verb')
        self.assertIn('столярничать', results)
        results = self.derivation.derive(word_b='нахал', pos_b='noun', pos_a='verb')
        self.assertIn('нахальничать', results)
        results = self.derivation.derive(word_b='слесарь', pos_b='noun', pos_a='verb')
        self.assertIn('слесарничать', results)
        results = self.derivation.derive(word_b='сапожник', pos_b='noun', pos_a='verb')
        self.assertIn('сапожничать', results)
        results = self.derivation.derive(word_b='острог', pos_b='noun', pos_a='verb')
        self.assertIn('острожничать', results)
        results = self.derivation.derive(word_b='сумерки', pos_b='noun', pos_a='verb')
        self.assertIn('сумерничать', results)
        results = self.derivation.derive(word_b='баклуша', pos_b='noun', pos_a='verb')
        self.assertIn('баклушничать', results)
        results = self.derivation.derive(word_b='тунеядец', pos_b='noun', pos_a='verb')
        self.assertIn('тунеядничать', results)
        results = self.derivation.derive(word_b='трофей', pos_b='noun', pos_a='verb')
        self.assertIn('трофейничать', results)
        results = self.derivation.derive(word_b='малодушие', pos_b='noun', pos_a='verb')
        self.assertIn('малодушничать', results)
        results = self.derivation.derive(word_b='роскошь', pos_b='noun', pos_a='verb')
        self.assertIn('роскошничать', results)

    def test_verb_812_1(self):
        results = self.derivation.derive(word_b='жулик', pos_b='noun', pos_a='verb')
        self.assertIn('жульничать', results)
        results = self.derivation.derive(word_b='ямщик', pos_b='noun', pos_a='verb')
        self.assertIn('ямщичничать', results)
        results = self.derivation.derive(word_b='лазутчик', pos_b='noun', pos_a='verb')
        self.assertIn('лазутничать', results)
        results = self.derivation.derive(word_b='водопроводчик', pos_b='noun', pos_a='verb')
        self.assertIn('водопроводничать', results)
        results = self.derivation.derive(word_b='кокетка', pos_b='noun', pos_a='verb')
        self.assertIn('кокетничать', results)
        results = self.derivation.derive(word_b='подголосок', pos_b='noun', pos_a='verb')
        self.assertIn('подголосничать', results)
        results = self.derivation.derive(word_b='молотобоец', pos_b='noun', pos_a='verb')
        self.assertIn('молотобойничать', results)
        results = self.derivation.derive(word_b='кузнец', pos_b='noun', pos_a='verb')
        self.assertIn('кузнечничать', results)
        results = self.derivation.derive(word_b='прихвостень', pos_b='noun', pos_a='verb')
        self.assertIn('прихвостничать', results)

    def test_verb_814(self):
        results = self.derivation.derive(word_b='жадный', pos_b='adj', pos_a='verb')
        self.assertIn('жадничать', results)
        results = self.derivation.derive(word_b='озорной', pos_b='adj', pos_a='verb')
        self.assertIn('озорничать', results)
        results = self.derivation.derive(word_b='искренний', pos_b='adj', pos_a='verb')
        self.assertIn('искренничать', results)
        results = self.derivation.derive(word_b='дерзкий', pos_b='adj', pos_a='verb')
        self.assertIn('дерзничать', results)

    def test_verb_817(self):
        results = self.derivation.derive(word_b='злоба', pos_b='noun', pos_a='verb')
        self.assertIn('злобствовать', results)
        results = self.derivation.derive(word_b='тиран', pos_b='noun', pos_a='verb')
        self.assertIn('тиранствовать', results)
        results = self.derivation.derive(word_b='генерал', pos_b='noun', pos_a='verb')
        self.assertIn('генеральствовать', results)
        results = self.derivation.derive(word_b='упрямство', pos_b='noun', pos_a='verb')
        self.assertIn('упрямствовать', results)
        results = self.derivation.derive(word_b='шинкарь', pos_b='noun', pos_a='verb')
        self.assertIn('шинкарствовать', results)
        results = self.derivation.derive(word_b='учитель', pos_b='noun', pos_a='verb')
        self.assertIn('учительствовать', results)
        results = self.derivation.derive(word_b='владыка', pos_b='noun', pos_a='verb')
        self.assertIn('владычествовать', results)
        results = self.derivation.derive(word_b='пророк', pos_b='noun', pos_a='verb')
        self.assertIn('пророчествовать', results)
        results = self.derivation.derive(word_b='идолопоклонник', pos_b='noun', pos_a='verb')
        self.assertIn('идолопоклонствовать', results)
        results = self.derivation.derive(word_b='снохач', pos_b='noun', pos_a='verb')
        self.assertIn('снохачествовать', results)
        results = self.derivation.derive(word_b='молодец', pos_b='noun', pos_a='verb')
        self.assertIn('молодечествовать', results)
        results = self.derivation.derive(word_b='герой', pos_b='noun', pos_a='verb')
        self.assertIn('геройствовать', results)
        results = self.derivation.derive(word_b='малодушие', pos_b='noun', pos_a='verb')
        self.assertIn('малодушествовать', results)
        results = self.derivation.derive(word_b='усердие', pos_b='noun', pos_a='verb')
        self.assertIn('усердствовать', results)

    def test_verb_817_1(self):
        results = self.derivation.derive(word_b='вития', pos_b='noun', pos_a='verb')
        self.assertIn('витийствовать', results)
        results = self.derivation.derive(word_b='барин', pos_b='noun', pos_a='verb')
        self.assertIn('барствовать', results)
        results = self.derivation.derive(word_b='тунеядец', pos_b='noun', pos_a='verb')
        self.assertIn('тунеядствовать', results)
        results = self.derivation.derive(word_b='кокетка', pos_b='noun', pos_a='verb')
        self.assertIn('кокетствовать', results)
        results = self.derivation.derive(word_b='меньшевик', pos_b='noun', pos_a='verb')
        self.assertIn('меньшевиствовать', results)
        results = self.derivation.derive(word_b='начальник', pos_b='noun', pos_a='verb')
        self.assertIn('начальствовать', results)
        results = self.derivation.derive(word_b='соперник', pos_b='noun', pos_a='verb')
        self.assertIn('соперничествовать', results)

    def test_verb_817_2(self):
        results = self.derivation.derive(word_b='любопытство', pos_b='noun', pos_a='verb')
        self.assertIn('любопытствовать', results)
        results = self.derivation.derive(word_b='соответствие', pos_b='noun', pos_a='verb')
        self.assertIn('соответствовать', results)
        results = self.derivation.derive(word_b='власть', pos_b='noun', pos_a='verb')
        self.assertIn('властвовать', results)
        results = self.derivation.derive(word_b='фашист', pos_b='noun', pos_a='verb')
        self.assertIn('фашистовать', results)

    def test_verb_817_3(self):
        results = self.derivation.derive(word_b='юродивый', pos_b='noun?', pos_a='verb')
        self.assertIn('юродствовать', results)
        results = self.derivation.derive(word_b='лесничий', pos_b='noun?', pos_a='verb')
        self.assertIn('лесничествовать', results)

    def test_verb_820(self):
        results = self.derivation.derive(word_b='благоприятный', pos_b='adj', pos_a='verb')
        self.assertIn('благоприятствовать', results)

    def test_verb_824(self):
        results = self.derivation.derive(word_b='хомут', pos_b='noun', pos_a='verb')
        self.assertIn('хомутать', results)
        results = self.derivation.derive(word_b='пятно', pos_b='noun', pos_a='verb')
        self.assertIn('пятнать', results)
        results = self.derivation.derive(word_b='костыль', pos_b='noun', pos_a='verb')
        self.assertIn('костылять', results)
        results = self.derivation.derive(word_b='петля', pos_b='noun', pos_a='verb')
        self.assertIn('петлять', results)
        results = self.derivation.derive(word_b='пеленка', pos_b='noun', pos_a='verb')
        self.assertIn('пеленать', results)
        results = self.derivation.derive(word_b='козырек', pos_b='noun', pos_a='verb')
        self.assertIn('козырять', results)
        results = self.derivation.derive(word_b='венок', pos_b='noun', pos_a='verb')
        self.assertIn('венчать', results)
        results = self.derivation.derive(word_b='восторг', pos_b='noun', pos_a='verb')
        self.assertIn('восторгать', results)
        results = self.derivation.derive(word_b='страх', pos_b='noun', pos_a='verb')
        self.assertIn('стращать', results)
        results = self.derivation.derive(word_b='долг', pos_b='noun', pos_a='verb')
        self.assertIn('должать', results)
        results = self.derivation.derive(word_b='завтрак', pos_b='noun', pos_a='verb')
        self.assertIn('завтракать', results)

    def test_verb_824_1(self):
        results = self.derivation.derive(word_b='промысел', pos_b='noun', pos_a='verb')
        self.assertIn('промышлять', results)

    def test_verb_826(self):
        results = self.derivation.derive(word_b='ветхий', pos_b='adj', pos_a='verb')
        self.assertIn('ветшать', results)
        results = self.derivation.derive(word_b='дикий', pos_b='adj', pos_a='verb')
        self.assertIn('дичать', results)
        results = self.derivation.derive(word_b='нищий', pos_b='adj', pos_a='verb')
        self.assertIn('нищать', results)
        results = self.derivation.derive(word_b='ровный', pos_b='adj', pos_a='verb')
        self.assertIn('ровнять', results)
        results = self.derivation.derive(word_b='хромой', pos_b='adj', pos_a='verb')
        self.assertIn('хромать', results)

    def test_verb_826_1(self):
        results = self.derivation.derive(word_b='ровнее', pos_b='comp', pos_a='verb')
        self.assertIn('ровнять', results)
        results = self.derivation.derive(word_b='дороже', pos_b='comp', pos_a='verb')
        self.assertIn('дорожать', results)

    def test_verb_828(self):
        results = self.derivation.derive(word_b='ах', pos_b='?', pos_a='verb')
        self.assertIn('ахать', results)
        results = self.derivation.derive(word_b='вы', pos_b='?', pos_a='verb')
        self.assertIn('выкать', results)
        results = self.derivation.derive(word_b='ты', pos_b='?', pos_a='verb')
        self.assertIn('тыкать', results)
        results = self.derivation.derive(word_b='о', pos_b='?', pos_a='verb')
        self.assertIn('окать', results)
        results = self.derivation.derive(word_b='ванька', pos_b='?', pos_a='verb')
        self.assertIn('ванькать', results)
        results = self.derivation.derive(word_b='спасибо', pos_b='?', pos_a='verb')
        self.assertIn('спасибкать', results)
        results = self.derivation.derive(word_b='баю', pos_b='?', pos_a='verb')
        self.assertIn('баюкать', results)
        results = self.derivation.derive(word_b='да', pos_b='?', pos_a='verb')
        self.assertIn('дакать', results)
        results = self.derivation.derive(word_b='бац', pos_b='?', pos_a='verb')
        self.assertIn('бацать', results)
        results = self.derivation.derive(word_b='кукареку', pos_b='?', pos_a='verb')
        self.assertIn('кукарекать', results)
        results = self.derivation.derive(word_b='тик', pos_b='?', pos_a='verb')
        self.assertIn('тикать', results)

    def test_verb_830(self):
        results = self.derivation.derive(word_b='белый', pos_b='adj', pos_a='verb')
        self.assertIn('белеть', results)
        results = self.derivation.derive(word_b='влажный', pos_b='adj', pos_a='verb')
        self.assertIn('влажнеть', results)
        results = self.derivation.derive(word_b='голубой', pos_b='adj', pos_a='verb')
        self.assertIn('голубеть', results)
        results = self.derivation.derive(word_b='ледяной', pos_b='adj', pos_a='verb')
        self.assertIn('леденеть', results)
        results = self.derivation.derive(word_b='редкий', pos_b='adj', pos_a='verb')
        self.assertIn('редеть', results)
        results = self.derivation.derive(word_b='мягкий', pos_b='adj', pos_a='verb')
        self.assertIn('мягчеть', results)
        results = self.derivation.derive(word_b='убогий', pos_b='adj', pos_a='verb')
        self.assertIn('убожеть', results)
        results = self.derivation.derive(word_b='русский', pos_b='adj', pos_a='verb')
        self.assertIn('русеть', results)
        results = self.derivation.derive(word_b='бессильный', pos_b='adj', pos_a='verb')
        self.assertIn('бессилеть', results)

    def test_verb_830_1(self):
        results = self.derivation.derive(word_b='светлее', pos_b='comp', pos_a='verb')
        self.assertIn('светлеть', results)

    def test_verb_832(self):
        results = self.derivation.derive(word_b='сирота', pos_b='noun', pos_a='verb')
        self.assertIn('сиротеть', results)
        results = self.derivation.derive(word_b='золото', pos_b='noun', pos_a='verb')
        self.assertIn('золотеть', results)
        results = self.derivation.derive(word_b='студень', pos_b='noun', pos_a='verb')
        self.assertIn('студенеть', results)
        results = self.derivation.derive(word_b='пламя', pos_b='noun', pos_a='verb')
        self.assertIn('пламенеть', results)

    def test_verb_832_1(self):
        results = self.derivation.derive(word_b='тусклый', pos_b='noun', pos_a='verb')
        self.assertIn('тускнеть', results)
        results = self.derivation.derive(word_b='тусклый', pos_b='noun', pos_a='verb')
        self.assertIn('тусклеть', results)

    def test_verb_832_2(self):
        results = self.derivation.derive(word_b='иней', pos_b='noun', pos_a='verb')
        self.assertIn('индеветь', results)

    def test_verb_832_3(self):
        results = self.derivation.derive(word_b='столб', pos_b='noun', pos_a='verb')
        self.assertIn('столбенеть', results)

    def test_verb_835(self):
        results = self.derivation.derive(word_b='слепой', pos_b='adj', pos_a='verb')
        self.assertIn('слепнуть', results)
        results = self.derivation.derive(word_b='мокрый', pos_b='adj', pos_a='verb')
        self.assertIn('мокнуть', results)
        results = self.derivation.derive(word_b='глухой', pos_b='adj', pos_a='verb')
        self.assertIn('глохнуть', results)
        results = self.derivation.derive(word_b='сухой', pos_b='adj', pos_a='verb')
        self.assertIn('сохнуть', results)
        results = self.derivation.derive(word_b='крепкий', pos_b='adj', pos_a='verb')
        self.assertIn('крепнуть', results)
        results = self.derivation.derive(word_b='горький', pos_b='adj', pos_a='verb')
        self.assertIn('горкнуть', results)

    def test_verb_835_1(self):
        results = self.derivation.derive(word_b='крепче', pos_b='comp', pos_a='verb')
        self.assertIn('крепнуть', results)

    def test_verb_835_2(self):
        results = self.derivation.derive(word_b='слабее', pos_b='comp', pos_a='verb')
        self.assertIn('слабнуть', results)

    def test_verb_836(self):
        results = self.derivation.derive(word_b='толкать', pos_b='verb', pos_a='verb')
        self.assertIn('толкнуть', results)
        results = self.derivation.derive(word_b='брызгать', pos_b='verb', pos_a='verb')
        self.assertIn('брызнуть', results)
        results = self.derivation.derive(word_b='полосовать', pos_b='verb', pos_a='verb')
        self.assertIn('полоснуть', results)
        results = self.derivation.derive(word_b='спекулировать', pos_b='verb', pos_a='verb')
        self.assertIn('спекульнуть', results)
        results = self.derivation.derive(word_b='тормозить', pos_b='verb', pos_a='verb')
        self.assertIn('тормознуть', results)
        results = self.derivation.derive(word_b='палить', pos_b='verb', pos_a='verb')
        self.assertIn('пальнуть', results)
        results = self.derivation.derive(word_b='скрипеть', pos_b='verb', pos_a='verb')
        self.assertIn('скрипнуть', results)
        results = self.derivation.derive(word_b='кричать', pos_b='verb', pos_a='verb')
        self.assertIn('крикнуть', results)
        results = self.derivation.derive(word_b='махать', pos_b='verb', pos_a='verb')
        self.assertIn('махнуть', results)
        results = self.derivation.derive(word_b='лаять', pos_b='verb', pos_a='verb')
        self.assertIn('лайнуть', results)
        results = self.derivation.derive(word_b='трясти', pos_b='verb', pos_a='verb')
        self.assertIn('трахнуть', results)
        results = self.derivation.derive(word_b='грызть', pos_b='verb', pos_a='verb')
        self.assertIn('грызнуть', results)
        results = self.derivation.derive(word_b='грести', pos_b='verb', pos_a='verb')
        self.assertIn('гребнуть', results)
        results = self.derivation.derive(word_b='колоть', pos_b='verb', pos_a='verb')
        self.assertIn('кольнуть', results)
        results = self.derivation.derive(word_b='лить', pos_b='verb', pos_a='verb')
        self.assertIn('линуть', results)
        results = self.derivation.derive(word_b='дуть', pos_b='verb', pos_a='verb')
        self.assertIn('дунуть', results)

    def test_verb_840(self):
        results = self.derivation.derive(word_b='сказать', pos_b='verb', pos_a='verb')
        self.assertIn('сказануть', results)
        results = self.derivation.derive(word_b='стегать', pos_b='verb', pos_a='verb')
        self.assertIn('стегануть', results)
        results = self.derivation.derive(word_b='хлестать', pos_b='verb', pos_a='verb')
        self.assertIn('хлестануть', results)
        results = self.derivation.derive(word_b='резать', pos_b='verb', pos_a='verb')
        self.assertIn('резануть', results)
        results = self.derivation.derive(word_b='газовать', pos_b='verb', pos_a='verb')
        self.assertIn('газануть', results)
        results = self.derivation.derive(word_b='толкать', pos_b='verb', pos_a='verb')
        self.assertIn('толкануть', results)
        results = self.derivation.derive(word_b='мазать', pos_b='verb', pos_a='verb')
        self.assertIn('мазануть', results)
        results = self.derivation.derive(word_b='сечь', pos_b='verb', pos_a='verb')
        self.assertIn('секануть', results)
        results = self.derivation.derive(word_b='трясти', pos_b='verb', pos_a='verb')
        self.assertIn('тряхануть', results)
        results = self.derivation.derive(word_b='крутить', pos_b='verb', pos_a='verb')
        self.assertIn('крутануть', results)
        results = self.derivation.derive(word_b='храпеть', pos_b='verb', pos_a='verb')
        self.assertIn('храпануть', results)
        results = self.derivation.derive(word_b='стучать', pos_b='verb', pos_a='verb')
        self.assertIn('стукануть', results)
        results = self.derivation.derive(word_b='лить', pos_b='verb', pos_a='verb')
        self.assertIn('ливануть', results)

    def test_verb_842(self):
        results = self.derivation.derive(word_b='заболеть', pos_b='verb', pos_a='verb')
        self.assertIn('заболевать', results)
        results = self.derivation.derive(word_b='затеять', pos_b='verb', pos_a='verb')
        self.assertIn('затевать', results)
        results = self.derivation.derive(word_b='зашить', pos_b='verb', pos_a='verb')
        self.assertIn('зашивать', results)
        results = self.derivation.derive(word_b='раздуть', pos_b='verb', pos_a='verb')
        self.assertIn('раздувать', results)
        results = self.derivation.derive(word_b='петь', pos_b='verb', pos_a='verb')
        self.assertIn('певать', results)
        results = self.derivation.derive(word_b='зашить', pos_b='verb', pos_a='verb')
        self.assertIn('зашивать', results)
        results = self.derivation.derive(word_b='раздуть', pos_b='verb', pos_a='verb')
        self.assertIn('раздувать', results)
        results = self.derivation.derive(word_b='засеять', pos_b='verb', pos_a='verb')
        self.assertIn('засевать', results)
        results = self.derivation.derive(word_b='затеять', pos_b='verb', pos_a='verb')
        self.assertIn('затевать', results)
        results = self.derivation.derive(word_b='обуять', pos_b='verb', pos_a='verb')
        self.assertIn('обуевать', results)
        results = self.derivation.derive(word_b='затмить', pos_b='verb', pos_a='verb')
        self.assertIn('затмевать', results)
        results = self.derivation.derive(word_b='продлить', pos_b='verb', pos_a='verb')
        self.assertIn('продлевать', results)
        results = self.derivation.derive(word_b='дать', pos_b='verb', pos_a='verb')
        self.assertIn('давать', results)
        results = self.derivation.derive(word_b='узнать', pos_b='verb', pos_a='verb')
        self.assertIn('узнавать', results)
        results = self.derivation.derive(word_b='встать', pos_b='verb', pos_a='verb')
        self.assertIn('вставать', results)
        results = self.derivation.derive(word_b='забыть', pos_b='verb', pos_a='verb')
        self.assertIn('забывать', results)
        results = self.derivation.derive(word_b='отважиться', pos_b='verb', pos_a='verb')
        self.assertIn('отваживаться', results)
        results = self.derivation.derive(word_b='осмелиться', pos_b='verb', pos_a='verb')
        self.assertIn('осмеливаться', results)
        results = self.derivation.derive(word_b='раздуть', pos_b='verb', pos_a='verb')
        self.assertIn('раздувать', results)
        results = self.derivation.derive(word_b='загнить', pos_b='verb', pos_a='verb')
        self.assertIn('загнивать', results)
        results = self.derivation.derive(word_b='задуть', pos_b='verb', pos_a='verb')
        self.assertIn('задувать', results)
        results = self.derivation.derive(word_b='вбить', pos_b='verb', pos_a='verb')
        self.assertIn('вбивать', results)
        results = self.derivation.derive(word_b='засеять', pos_b='verb', pos_a='verb')
        self.assertIn('засевать', results)
        results = self.derivation.derive(word_b='дожить', pos_b='verb', pos_a='verb')
        self.assertIn('доживать', results)
        results = self.derivation.derive(word_b='застрять', pos_b='verb', pos_a='verb')
        self.assertIn('застревать', results)
        results = self.derivation.derive(word_b='затмить', pos_b='verb', pos_a='verb')
        self.assertIn('затмевать', results)
        results = self.derivation.derive(word_b='претерпеть', pos_b='verb', pos_a='verb')
        self.assertIn('претерпевать', results)
        results = self.derivation.derive(word_b='добыть', pos_b='verb', pos_a='verb')
        self.assertIn('добывать', results)
        results = self.derivation.derive(word_b='отдать', pos_b='verb', pos_a='verb')
        self.assertIn('отдавать', results)

    def test_verb_842_1(self):
        results = self.derivation.derive(word_b='выгнуть', pos_b='verb', pos_a='verb')
        self.assertIn('выгибать', results)
        results = self.derivation.derive(word_b='освежить', pos_b='verb', pos_a='verb')
        self.assertIn('освежать', results)
        results = self.derivation.derive(word_b='загореть', pos_b='verb', pos_a='verb')
        self.assertIn('загорать', results)
        results = self.derivation.derive(word_b='заплести', pos_b='verb', pos_a='verb')
        self.assertIn('заплетать', results)
        results = self.derivation.derive(word_b='рассечь', pos_b='verb', pos_a='verb')
        self.assertIn('рассекать', results)
        results = self.derivation.derive(word_b='оповестить', pos_b='verb', pos_a='verb')
        self.assertIn('оповещать', results)
        results = self.derivation.derive(word_b='воскликнуть', pos_b='verb', pos_a='verb')
        self.assertIn('восклицать', results)
        results = self.derivation.derive(word_b='устранить', pos_b='verb', pos_a='verb')
        self.assertIn('устранять', results)
        results = self.derivation.derive(word_b='обидеть', pos_b='verb', pos_a='verb')
        self.assertIn('обижать', results)
        results = self.derivation.derive(word_b='вырубить', pos_b='verb', pos_a='verb')
        self.assertIn('вырубать', results)
        results = self.derivation.derive(word_b='вгрызться', pos_b='verb', pos_a='verb')
        self.assertIn('вгрызаться', results)
        results = self.derivation.derive(word_b='пленить', pos_b='verb', pos_a='verb')
        self.assertIn('пленять', results)
        results = self.derivation.derive(word_b='огрызнуться', pos_b='verb', pos_a='verb')
        self.assertIn('огрызаться', results)
        results = self.derivation.derive(word_b='натыкать', pos_b='verb', pos_a='verb')
        self.assertIn('натыкать', results)
        results = self.derivation.derive(word_b='вздохнуть', pos_b='verb', pos_a='verb')
        self.assertIn('вздыхать', results)
        results = self.derivation.derive(word_b='ввергнуть', pos_b='verb', pos_a='verb')
        self.assertIn('ввергать', results)
        results = self.derivation.derive(word_b='засыпать', pos_b='verb', pos_a='verb')
        self.assertIn('засыпать', results)
        results = self.derivation.derive(word_b='отослать', pos_b='verb', pos_a='verb')
        self.assertIn('отсылать', results)
        results = self.derivation.derive(word_b='переждать', pos_b='verb', pos_a='verb')
        self.assertIn('пережидать', results)
        results = self.derivation.derive(word_b='забрать', pos_b='verb', pos_a='verb')
        self.assertIn('забирать', results)
        results = self.derivation.derive(word_b='запрячь', pos_b='verb', pos_a='verb')
        self.assertIn('запрягать', results)
        results = self.derivation.derive(word_b='выскрести', pos_b='verb', pos_a='verb')
        self.assertIn('выскребать', results)
        results = self.derivation.derive(word_b='ушибить', pos_b='verb', pos_a='verb')
        self.assertIn('ушибать', results)
        results = self.derivation.derive(word_b='вырасти', pos_b='verb', pos_a='verb')
        self.assertIn('вырастать', results)
        results = self.derivation.derive(word_b='подмести', pos_b='verb', pos_a='verb')
        self.assertIn('подметать', results)
        results = self.derivation.derive(word_b='отпасть', pos_b='verb', pos_a='verb')
        self.assertIn('отпадать', results)
        results = self.derivation.derive(word_b='проклясть', pos_b='verb', pos_a='verb')
        self.assertIn('проклинать', results)
        results = self.derivation.derive(word_b='распять', pos_b='verb', pos_a='verb')
        self.assertIn('распинать', results)
        results = self.derivation.derive(word_b='внять', pos_b='verb', pos_a='verb')
        self.assertIn('внимать', results)
        results = self.derivation.derive(word_b='бросить', pos_b='verb', pos_a='verb')
        self.assertIn('бросать', results)
        results = self.derivation.derive(word_b='закипеть', pos_b='verb', pos_a='verb')
        self.assertIn('закипать', results)
        results = self.derivation.derive(word_b='прогнать', pos_b='verb', pos_a='verb')
        self.assertIn('прогонять', results)
        results = self.derivation.derive(word_b='выехать', pos_b='verb', pos_a='verb')
        self.assertIn('выезжать', results)
        results = self.derivation.derive(word_b='добежать', pos_b='verb', pos_a='verb')
        self.assertIn('добегать', results)
        results = self.derivation.derive(word_b='почтить', pos_b='verb', pos_a='verb')
        self.assertIn('почитать', results)
        results = self.derivation.derive(word_b='съесть', pos_b='verb', pos_a='verb')
        self.assertIn('съедать', results)

    def test_verb_842_3(self):
        results = self.derivation.derive(word_b='доиграть', pos_b='verb', pos_a='verb')
        self.assertIn('доигрывать', results)
        results = self.derivation.derive(word_b='изжевать', pos_b='verb', pos_a='verb')
        self.assertIn('изжевывать', results)
        results = self.derivation.derive(word_b='взмахнуть', pos_b='verb', pos_a='verb')
        self.assertIn('взмахивать', results)
        results = self.derivation.derive(word_b='выдернуть', pos_b='verb', pos_a='verb')
        self.assertIn('выдергивать', results)
        results = self.derivation.derive(word_b='скосить', pos_b='verb', pos_a='verb')
        self.assertIn('скашивать', results)
        results = self.derivation.derive(word_b='проследить', pos_b='verb', pos_a='verb')
        self.assertIn('прослеживать', results)
        results = self.derivation.derive(word_b='простоять', pos_b='verb', pos_a='verb')
        self.assertIn('простаивать', results)
        results = self.derivation.derive(word_b='писать', pos_b='verb', pos_a='verb')
        self.assertIn('писывать', results)
        results = self.derivation.derive(word_b='высмеять', pos_b='verb', pos_a='verb')
        self.assertIn('высмеивать', results)
        results = self.derivation.derive(word_b='отколоть', pos_b='verb', pos_a='verb')
        self.assertIn('откалывать', results)
        results = self.derivation.derive(word_b='выплюнуть', pos_b='verb', pos_a='verb')
        self.assertIn('выплевывать', results)
        results = self.derivation.derive(word_b='пропахнуть', pos_b='verb', pos_a='verb')
        self.assertIn('пропахивать', results)
        results = self.derivation.derive(word_b='отсосать', pos_b='verb', pos_a='verb')
        self.assertIn('отсасывать', results)
        results = self.derivation.derive(word_b='взреветь', pos_b='verb', pos_a='verb')
        self.assertIn('взревывать', results)
        results = self.derivation.derive(word_b='отволочь', pos_b='verb', pos_a='verb')
        self.assertIn('отволакивать', results)
        results = self.derivation.derive(word_b='выскрести', pos_b='verb', pos_a='verb')
        self.assertIn('выскребывать', results)
        results = self.derivation.derive(word_b='выкрасть', pos_b='verb', pos_a='verb')
        self.assertIn('выкрадывать', results)
        results = self.derivation.derive(word_b='учесть', pos_b='verb', pos_a='verb')
        self.assertIn('учитывать', results)
        results = self.derivation.derive(word_b='гасить', pos_b='verb', pos_a='verb')
        self.assertIn('гащивать', results)
        results = self.derivation.derive(word_b='простучать', pos_b='verb', pos_a='verb')
        self.assertIn('простукивать', results)
        results = self.derivation.derive(word_b='говорить', pos_b='verb', pos_a='verb')
        self.assertIn('говаривать', results)
        results = self.derivation.derive(word_b='обуржуазить', pos_b='verb', pos_a='verb')
        self.assertIn('обуржуазивать', results)
        results = self.derivation.derive(word_b='обезлесить', pos_b='verb', pos_a='verb')
        self.assertIn('обезлесивать', results)
        results = self.derivation.derive(word_b='вдавить', pos_b='verb', pos_a='verb')
        self.assertIn('вдавливать', results)
        results = self.derivation.derive(word_b='прихворнуть', pos_b='verb', pos_a='verb')
        self.assertIn('прихварывать', results)
        results = self.derivation.derive(word_b='заглядеться', pos_b='verb', pos_a='verb')
        self.assertIn('заглядываться', results)
        results = self.derivation.derive(word_b='организовать', pos_b='verb', pos_a='verb')
        self.assertIn('организовывать', results)

    def test_verb_842_5(self):
        results = self.derivation.derive(word_b='выкрасть', pos_b='verb', pos_a='verb')
        self.assertIn('выкрадывать', results)
        results = self.derivation.derive(word_b='учесть', pos_b='verb', pos_a='verb')
        self.assertIn('учитывать', results)
        results = self.derivation.derive(word_b='усесться', pos_b='verb', pos_a='verb')
        self.assertIn('усаживаться', results)
        results = self.derivation.derive(word_b='помочь', pos_b='verb', pos_a='verb')
        self.assertIn('помогать', results)
        results = self.derivation.derive(word_b='облечь', pos_b='verb', pos_a='verb')
        self.assertIn('облекать', results)
        results = self.derivation.derive(word_b='забрести', pos_b='verb', pos_a='verb')
        self.assertIn('забредать', results)
        results = self.derivation.derive(word_b='проклясть', pos_b='verb', pos_a='verb')
        self.assertIn('проклинать', results)
        results = self.derivation.derive(word_b='обрести', pos_b='verb', pos_a='verb')
        self.assertIn('обретать', results)
        results = self.derivation.derive(word_b='нажать', pos_b='verb', pos_a='verb')
        self.assertIn('нажимать', results)
        results = self.derivation.derive(word_b='размять', pos_b='verb', pos_a='verb')
        self.assertIn('разминать', results)

    def test_verb_842_6(self):
        results = self.derivation.derive(word_b='обокрасть', pos_b='verb', pos_a='verb')
        self.assertIn('обкрадывать', results)
        results = self.derivation.derive(word_b='отобрать', pos_b='verb', pos_a='verb')
        self.assertIn('отбирать', results)
        results = self.derivation.derive(word_b='оторвать', pos_b='verb', pos_a='verb')
        self.assertIn('отрывать', results)
        results = self.derivation.derive(word_b='подзывать', pos_b='verb', pos_a='verb')
        self.assertIn('подозвать', results)
        results = self.derivation.derive(word_b='собрать', pos_b='verb', pos_a='verb')
        self.assertIn('собирать', results)
        results = self.derivation.derive(word_b='созвать', pos_b='verb', pos_a='verb')
        self.assertIn('созывать', results)

    def test_verb_842_7(self):
        results = self.derivation.derive(word_b='ночевать', pos_b='verb', pos_a='verb')
        self.assertIn('ночевывать', results)
        results = self.derivation.derive(word_b='обедать', pos_b='verb', pos_a='verb')
        self.assertIn('обедывать', results)
        results = self.derivation.derive(word_b='мочить', pos_b='verb', pos_a='verb')
        self.assertIn('мачивать', results)
        results = self.derivation.derive(word_b='болеть', pos_b='verb', pos_a='verb')
        self.assertIn('баливать', results)
        results = self.derivation.derive(word_b='брить', pos_b='verb', pos_a='verb')
        self.assertIn('бривать', results)
        results = self.derivation.derive(word_b='тянуть', pos_b='verb', pos_a='verb')
        self.assertIn('тягивать', results)
        results = self.derivation.derive(word_b='таять', pos_b='verb', pos_a='verb')
        self.assertIn('таивать', results)
        results = self.derivation.derive(word_b='драть', pos_b='verb', pos_a='verb')
        self.assertIn('дирать', results)
        results = self.derivation.derive(word_b='жить', pos_b='verb', pos_a='verb')
        self.assertIn('живать', results)
        results = self.derivation.derive(word_b='жать', pos_b='verb', pos_a='verb')
        self.assertIn('жинать', results)
        results = self.derivation.derive(word_b='носить', pos_b='verb', pos_a='verb')
        self.assertIn('нашивать', results)
        results = self.derivation.derive(word_b='поить', pos_b='verb', pos_a='verb')
        self.assertIn('паивать', results)
        results = self.derivation.derive(word_b='видеть', pos_b='verb', pos_a='verb')
        self.assertIn('видывать', results)
        results = self.derivation.derive(word_b='слышать', pos_b='verb', pos_a='verb')
        self.assertIn('слыхивать', results)
        results = self.derivation.derive(word_b='есть', pos_b='verb', pos_a='verb')
        self.assertIn('едать', results)

    def test_verb_842_9(self):
        results = self.derivation.derive(word_b='всадить', pos_b='verb', pos_a='verb')
        self.assertIn('всаживать', results)
        results = self.derivation.derive(word_b='ездить', pos_b='verb', pos_a='verb')
        self.assertIn('езживать', results)
        results = self.derivation.derive(word_b='нарядить', pos_b='verb', pos_a='verb')
        self.assertIn('наряжать', results)

    def test_verb_842_10(self):
        results = self.derivation.derive(word_b='взвинтить', pos_b='verb', pos_a='verb')
        self.assertIn('взвинчивать', results)
        results = self.derivation.derive(word_b='платить', pos_b='verb', pos_a='verb')
        self.assertIn('плачивать', results)
        results = self.derivation.derive(word_b='ответить', pos_b='verb', pos_a='verb')
        self.assertIn('отвечать', results)

    def test_verb_842_11(self):
        results = self.derivation.derive(word_b='заморозить', pos_b='verb', pos_a='verb')
        self.assertIn('замораживать', results)
        results = self.derivation.derive(word_b='возить', pos_b='verb', pos_a='verb')
        self.assertIn('важивать', results)
        results = self.derivation.derive(word_b='исказить', pos_b='verb', pos_a='verb')
        self.assertIn('искажать', results)
        results = self.derivation.derive(word_b='обуржуазить', pos_b='verb', pos_a='verb')
        self.assertIn('обуржуазивать', results)

    def test_verb_842_12(self):
        results = self.derivation.derive(word_b='взвесить', pos_b='verb', pos_a='verb')
        self.assertIn('взвешивать', results)
        results = self.derivation.derive(word_b='носить', pos_b='verb', pos_a='verb')
        self.assertIn('нашивать', results)
        results = self.derivation.derive(word_b='украсить', pos_b='verb', pos_a='verb')
        self.assertIn('украшать', results)
        results = self.derivation.derive(word_b='обезлесить', pos_b='verb', pos_a='verb')
        self.assertIn('обезлесивать', results)

    def test_verb_842_13(self):
        results = self.derivation.derive(word_b='победить', pos_b='verb', pos_a='verb')
        self.assertIn('побеждать', results)
        results = self.derivation.derive(word_b='смутить', pos_b='verb', pos_a='verb')
        self.assertIn('смущать', results)
        results = self.derivation.derive(word_b='ездить', pos_b='verb', pos_a='verb')
        self.assertIn('езжать', results)
        results = self.derivation.derive(word_b='загромоздить', pos_b='verb', pos_a='verb')
        self.assertIn('загромождать', results)

    def test_verb_842_14(self):
        results = self.derivation.derive(word_b='замыслить', pos_b='verb', pos_a='verb')
        self.assertIn('замышлять', results)
        results = self.derivation.derive(word_b='умертвить', pos_b='verb', pos_a='verb')
        self.assertIn('умерщвлять', results)

    def test_verb_842_15(self):
        results = self.derivation.derive(word_b='вырастить', pos_b='verb', pos_a='verb')
        self.assertIn('выращивать', results)
        results = self.derivation.derive(word_b='гостить', pos_b='verb', pos_a='verb')
        self.assertIn('гащивать', results)
        results = self.derivation.derive(word_b='сгустить', pos_b='verb', pos_a='verb')
        self.assertIn('сгущать', results)

    def test_verb_842_16(self):
        results = self.derivation.derive(word_b='вбежать', pos_b='verb', pos_a='verb')
        self.assertIn('вбегать', results)
        results = self.derivation.derive(word_b='вложить', pos_b='verb', pos_a='verb')
        self.assertIn('влагать', results)
        results = self.derivation.derive(word_b='вскочить', pos_b='verb', pos_a='verb')
        self.assertIn('вскакивать', results)
        results = self.derivation.derive(word_b='слышать', pos_b='verb', pos_a='verb')
        self.assertIn('слыхивать', results)
        results = self.derivation.derive(word_b='втащить', pos_b='verb', pos_a='verb')
        self.assertIn('втаскивать', results)

    def test_verb_842_17(self):
        results = self.derivation.derive(word_b='выплюнуть', pos_b='verb', pos_a='verb')
        self.assertIn('выплевывать', results)
        results = self.derivation.derive(word_b='высунуть', pos_b='verb', pos_a='verb')
        self.assertIn('высовывать', results)

    def test_verb_842_18(self):
        results = self.derivation.derive(word_b='увянуть', pos_b='verb', pos_a='verb')
        self.assertIn('увядать', results)
        results = self.derivation.derive(word_b='утонуть', pos_b='verb', pos_a='verb')
        self.assertIn('утопать', results)
        results = self.derivation.derive(word_b='согнуть', pos_b='verb', pos_a='verb')
        self.assertIn('сгибать', results)
        results = self.derivation.derive(word_b='занять', pos_b='verb', pos_a='verb')
        self.assertIn('занимать', results)
        results = self.derivation.derive(word_b='выдернуть', pos_b='verb', pos_a='verb')
        self.assertIn('выдергивать', results)
        results = self.derivation.derive(word_b='закинуть', pos_b='verb', pos_a='verb')
        self.assertIn('закидывать', results)
        results = self.derivation.derive(word_b='втиснуть', pos_b='verb', pos_a='verb')
        self.assertIn('втискивать', results)
        results = self.derivation.derive(word_b='выдвинуть', pos_b='verb', pos_a='verb')
        self.assertIn('выдвигать', results)
        results = self.derivation.derive(word_b='заснуть', pos_b='verb', pos_a='verb')
        self.assertIn('засыпать', results)
        results = self.derivation.derive(word_b='повернуть', pos_b='verb', pos_a='verb')
        self.assertIn('повертывать', results)
        results = self.derivation.derive(word_b='повернуть', pos_b='verb', pos_a='verb')
        self.assertIn('поворачивать', results)

    def test_verb_842_19(self):
        results = self.derivation.derive(word_b='пустить', pos_b='verb', pos_a='verb')
        self.assertIn('пускать', results)
        results = self.derivation.derive(word_b='воскликнуть', pos_b='verb', pos_a='verb')
        self.assertIn('восклицать', results)

    def test_verb_842_20(self):
        results = self.derivation.derive(word_b='выдрать', pos_b='verb', pos_a='verb')
        self.assertIn('выдирать', results)
        results = self.derivation.derive(word_b='забрать', pos_b='verb', pos_a='verb')
        self.assertIn('забирать', results)
        results = self.derivation.derive(word_b='настлать', pos_b='verb', pos_a='verb')
        self.assertIn('настилать', results)
        results = self.derivation.derive(word_b='попрать', pos_b='verb', pos_a='verb')
        self.assertIn('попирать', results)
        results = self.derivation.derive(word_b='приврать', pos_b='verb', pos_a='verb')
        self.assertIn('привирать', results)
        results = self.derivation.derive(word_b='согнуть', pos_b='verb', pos_a='verb')
        self.assertIn('сгибать', results)
        results = self.derivation.derive(word_b='удрать', pos_b='verb', pos_a='verb')
        self.assertIn('удирать', results)

    def test_verb_842_21(self):
        results = self.derivation.derive(word_b='вырвать', pos_b='verb', pos_a='verb')
        self.assertIn('вырывать', results)
        results = self.derivation.derive(word_b='переслать', pos_b='verb', pos_a='verb')
        self.assertIn('пересылать', results)
        results = self.derivation.derive(word_b='призвать', pos_b='verb', pos_a='verb')
        self.assertIn('призывать', results)
        results = self.derivation.derive(word_b='примкнуть', pos_b='verb', pos_a='verb')
        self.assertIn('примыкать', results)
        results = self.derivation.derive(word_b='проспать', pos_b='verb', pos_a='verb')
        self.assertIn('просыпать', results)
        results = self.derivation.derive(word_b='заснуть', pos_b='verb', pos_a='verb')
        self.assertIn('засыпать', results)
        results = self.derivation.derive(word_b='проткнуть', pos_b='verb', pos_a='verb')
        self.assertIn('протыкать', results)
        results = self.derivation.derive(word_b='оболгать', pos_b='verb', pos_a='verb')
        self.assertIn('облыгать', results)
        results = self.derivation.derive(word_b='прилгнуть', pos_b='verb', pos_a='verb')
        self.assertIn('прилыгать', results)

    def test_verb_842_22(self):
        results = self.derivation.derive(word_b='накопить', pos_b='verb', pos_a='verb')
        self.assertIn('накапливать', results)
        results = self.derivation.derive(word_b='отработать', pos_b='verb', pos_a='verb')
        self.assertIn('отрабатывать', results)
        results = self.derivation.derive(word_b='поить', pos_b='verb', pos_a='verb')
        self.assertIn('паивать', results)

    def test_verb_842_23(self):
        results = self.derivation.derive(word_b='причесать', pos_b='verb', pos_a='verb')
        self.assertIn('причесывать', results)
        results = self.derivation.derive(word_b='растрепать', pos_b='verb', pos_a='verb')
        self.assertIn('растрепывать', results)

    def test_verb_842_24(self):
        results = self.derivation.derive(word_b='зачесть', pos_b='verb', pos_a='verb')
        self.assertIn('зачитывать', results)
        results = self.derivation.derive(word_b='учесть', pos_b='verb', pos_a='verb')
        self.assertIn('учитывать', results)

    def test_verb_842_25(self):
        results = self.derivation.derive(word_b='вздохнуть', pos_b='verb', pos_a='verb')
        self.assertIn('вздыхать', results)
        results = self.derivation.derive(word_b='засохнуть', pos_b='verb', pos_a='verb')
        self.assertIn('засыхать', results)
        results = self.derivation.derive(word_b='натереть', pos_b='verb', pos_a='verb')
        self.assertIn('натирать', results)

    def test_verb_842_26(self):
        results = self.derivation.derive(word_b='помянуть', pos_b='verb', pos_a='verb')
        self.assertIn('поминать', results)

    def test_verb_842_27(self):
        results = self.derivation.derive(word_b='забрать', pos_b='verb', pos_a='verb')
        self.assertIn('забирать', results)
        results = self.derivation.derive(word_b='ободрать', pos_b='verb', pos_a='verb')
        self.assertIn('обдирать', results)
        results = self.derivation.derive(word_b='отозвать', pos_b='verb', pos_a='verb')
        self.assertIn('отзывать', results)
        results = self.derivation.derive(word_b='оторвать', pos_b='verb', pos_a='verb')
        self.assertIn('отрывать', results)
        results = self.derivation.derive(word_b='отомкнуть', pos_b='verb', pos_a='verb')
        self.assertIn('отмыкать', results)
        results = self.derivation.derive(word_b='подостлать', pos_b='verb', pos_a='verb')
        self.assertIn('подстилать', results)
        results = self.derivation.derive(word_b='послать', pos_b='verb', pos_a='verb')
        self.assertIn('посылать', results)
        results = self.derivation.derive(word_b='проспать', pos_b='verb', pos_a='verb')
        self.assertIn('просыпать', results)
        results = self.derivation.derive(word_b='удрать', pos_b='verb', pos_a='verb')
        self.assertIn('удирать', results)
        results = self.derivation.derive(word_b='напомнить', pos_b='verb', pos_a='verb')
        self.assertIn('напоминать', results)

    def test_verb_842_28(self):
        results = self.derivation.derive(word_b='загнать', pos_b='verb', pos_a='verb')
        self.assertIn('загонять', results)

    def test_verb_846(self):
        results = self.derivation.derive(word_b='воскреснуть', pos_b='verb', pos_a='verb')
        self.assertIn('воскресить', results)
        results = self.derivation.derive(word_b='гаснуть', pos_b='verb', pos_a='verb')
        self.assertIn('гасить', results)

    def test_verb_846_1(self):
        results = self.derivation.derive(word_b='гнить', pos_b='verb', pos_a='verb')
        self.assertIn('гноить', results)
        results = self.derivation.derive(word_b='пить', pos_b='verb', pos_a='verb')
        self.assertIn('поить', results)

    def test_verb_846_2(self):
        results = self.derivation.derive(word_b='гибнуть', pos_b='verb', pos_a='verb')
        self.assertIn('губить', results)

    def test_verb_846_3(self):
        results = self.derivation.derive(word_b='зажить', pos_b='verb', pos_a='verb')
        self.assertIn('заживить', results)

    def test_verb_846_4(self):
        results = self.derivation.derive(word_b='звенеть', pos_b='verb', pos_a='verb')
        self.assertIn('звонить', results)

    def test_verb_846_5(self):
        results = self.derivation.derive(word_b='кипеть', pos_b='verb', pos_a='verb')
        self.assertIn('кипятить', results)

    def test_verb_846_6(self):
        results = self.derivation.derive(word_b='липнуть', pos_b='verb', pos_a='verb')
        self.assertIn('лепить', results)

    def test_verb_846_7(self):
        results = self.derivation.derive(word_b='мереть', pos_b='verb', pos_a='verb')
        self.assertIn('морить', results)

    def test_verb_846_8(self):
        results = self.derivation.derive(word_b='мерзнуть', pos_b='verb', pos_a='verb')
        self.assertIn('морозить', results)

    def test_verb_846_9(self):
        results = self.derivation.derive(word_b='плыть', pos_b='verb', pos_a='verb')
        self.assertIn('плавить', results)

    def test_verb_846_10(self):
        results = self.derivation.derive(word_b='расти', pos_b='verb', pos_a='verb')
        self.assertIn('растить', results)

    def test_verb_846_11(self):
        results = self.derivation.derive(word_b='рухнуть', pos_b='verb', pos_a='verb')
        self.assertIn('рушить', results)

    def test_verb_846_12(self):
        results = self.derivation.derive(word_b='смеяться', pos_b='verb', pos_a='verb')
        self.assertIn('смешить', results)

    def test_verb_846_13(self):
        results = self.derivation.derive(word_b='стынуть', pos_b='verb', pos_a='verb')
        self.assertIn('студить', results)

    def test_verb_846_14(self):
        results = self.derivation.derive(word_b='тлеть', pos_b='verb', pos_a='verb')
        self.assertIn('тлить', results)

    def test_verb_846_15(self):
        results = self.derivation.derive(word_b='тонуть', pos_b='verb', pos_a='verb')
        self.assertIn('топить', results)

    def test_verb_846_16(self):
        results = self.derivation.derive(word_b='течь', pos_b='verb', pos_a='verb')
        self.assertIn('точить', results)

    def test_verb_846_17(self):
        results = self.derivation.derive(word_b='тухнуть', pos_b='verb', pos_a='verb')
        self.assertIn('тушить', results)

    def test_verb_846_18(self):
        results = self.derivation.derive(word_b='уснуть', pos_b='verb', pos_a='verb')
        self.assertIn('усыпить', results)

    def test_verb_846_19(self):
        results = self.derivation.derive(word_b='цепенеть', pos_b='verb', pos_a='verb')
        self.assertIn('цепенить', results)
        results = self.derivation.derive(word_b='коченеть', pos_b='verb', pos_a='verb')
        self.assertIn('коченить', results)

    def test_verb_846_20(self):
        results = self.derivation.derive(word_b='стать', pos_b='verb', pos_a='verb')
        self.assertIn('ставить', results)

    def test_verb_846_21(self):
        results = self.derivation.derive(word_b='стоять', pos_b='verb', pos_a='verb')
        self.assertIn('ставить', results)

    def test_verb_846_22(self):
        results = self.derivation.derive(word_b='перелечь', pos_b='verb', pos_a='verb')
        self.assertIn('переложить', results)

    def test_verb_846_23(self):
        results = self.derivation.derive(word_b='завязнуть', pos_b='verb', pos_a='verb')
        self.assertIn('завязить', results)
        results = self.derivation.derive(word_b='увязнуть', pos_b='verb', pos_a='verb')
        self.assertIn('увязить', results)

    def test_verb_847(self):
        results = self.derivation.derive(word_b='сесть', pos_b='verb', pos_a='verb')
        self.assertIn('сажать', results)
        results = self.derivation.derive(word_b='сидеть', pos_b='verb', pos_a='verb')
        self.assertIn('сажать', results)
        results = self.derivation.derive(word_b='виснуть', pos_b='verb', pos_a='verb')
        self.assertIn('вешать', results)
        results = self.derivation.derive(word_b='висеть', pos_b='verb', pos_a='verb')
        self.assertIn('вешать', results)
        results = self.derivation.derive(word_b='слышать', pos_b='verb', pos_a='verb')
        self.assertIn('слушать', results)

    def test_verb_848(self):
        results = self.derivation.derive(word_b='везти', pos_b='verb', pos_a='verb')
        self.assertIn('возить', results)
        results = self.derivation.derive(word_b='нести', pos_b='verb', pos_a='verb')
        self.assertIn('носить', results)
        results = self.derivation.derive(word_b='лезть', pos_b='verb', pos_a='verb')
        self.assertIn('лазить', results)
        results = self.derivation.derive(word_b='брести', pos_b='verb', pos_a='verb')
        self.assertIn('бродить', results)
        results = self.derivation.derive(word_b='вести', pos_b='verb', pos_a='verb')
        self.assertIn('водить', results)
        results = self.derivation.derive(word_b='ехать', pos_b='verb', pos_a='verb')
        self.assertIn('ездить', results)

    def test_verb_849(self):
        results = self.derivation.derive(word_b='бежать', pos_b='verb', pos_a='verb')
        self.assertIn('бегать', results)
        results = self.derivation.derive(word_b='гнать', pos_b='verb', pos_a='verb')
        self.assertIn('гонять', results)
        results = self.derivation.derive(word_b='катить', pos_b='verb', pos_a='verb')
        self.assertIn('катать', results)
        results = self.derivation.derive(word_b='лезть', pos_b='verb', pos_a='verb')
        self.assertIn('лазать', results)
        results = self.derivation.derive(word_b='лететь', pos_b='verb', pos_a='verb')
        self.assertIn('летать', results)
        results = self.derivation.derive(word_b='плыть', pos_b='verb', pos_a='verb')
        self.assertIn('плавать', results)
        results = self.derivation.derive(word_b='ползти', pos_b='verb', pos_a='verb')
        self.assertIn('ползать', results)
        results = self.derivation.derive(word_b='тащить', pos_b='verb', pos_a='verb')
        self.assertIn('таскать', results)

    def test_verb_854(self):
        results = self.derivation.derive(word_b='катить', pos_b='verb', pos_a='verb')
        self.assertIn('вкатить', results)
        results = self.derivation.derive(word_b='ползти', pos_b='verb', pos_a='verb')
        self.assertIn('вползти', results)
        results = self.derivation.derive(word_b='ткнуть', pos_b='verb', pos_a='verb')
        self.assertIn('воткнуть', results)
        results = self.derivation.derive(word_b='ехать', pos_b='verb', pos_a='verb')
        self.assertIn('въехать', results)

    def test_verb_854_1(self):
        results = self.derivation.derive(word_b='идти', pos_b='verb', pos_a='verb')
        self.assertIn('войти', results)

    def test_verb_855(self):
        results = self.derivation.derive(word_b='лететь', pos_b='verb', pos_a='verb')
        self.assertIn('взлететь', results)
        results = self.derivation.derive(word_b='коробить', pos_b='verb', pos_a='verb')
        self.assertIn('вскоробить', results)
        results = self.derivation.derive(word_b='ехать', pos_b='verb', pos_a='verb')
        self.assertIn('взъехать', results)
        results = self.derivation.derive(word_b='играть', pos_b='verb', pos_a='verb')
        self.assertIn('взыграть', results)

    def test_verb_855_1(self):
        results = self.derivation.derive(word_b='идти', pos_b='verb', pos_a='verb')
        self.assertIn('взойти', results)

    def test_verb_856(self):
        results = self.derivation.derive(word_b='вести', pos_b='verb', pos_a='verb')
        self.assertIn('возвести', results)
        results = self.derivation.derive(word_b='парить', pos_b='verb', pos_a='verb')
        self.assertIn('воспарить', results)
        results = self.derivation.derive(word_b='создать', pos_b='verb', pos_a='verb')
        self.assertIn('воссоздать', results)

    def test_verb_856_1(self):
        results = self.derivation.derive(word_b='идти', pos_b='verb', pos_a='verb')
        self.assertIn('возойти', results)

    def test_verb_857(self):
        results = self.derivation.derive(word_b='везти', pos_b='verb', pos_a='verb')
        self.assertIn('вывезти', results)
        results = self.derivation.derive(word_b='ехать', pos_b='verb', pos_a='verb')
        self.assertIn('выехать', results)
        results = self.derivation.derive(word_b='играть', pos_b='verb', pos_a='verb')
        self.assertIn('выиграть', results)

    def test_verb_858(self):
        results = self.derivation.derive(word_b='мобилизовать', pos_b='verb', pos_a='verb')
        self.assertIn('демобилизовать', results)
        results = self.derivation.derive(word_b='ориентировать', pos_b='verb', pos_a='verb')
        self.assertIn('дезориентировать', results)
        results = self.derivation.derive(word_b='стабилизировать', pos_b='verb', pos_a='verb')
        self.assertIn('дестабилизировать', results)

    def test_verb_859(self):
        results = self.derivation.derive(word_b='квалифицировать', pos_b='verb', pos_a='verb')
        self.assertIn('дисквалифицировать', results)
        results = self.derivation.derive(word_b='гармонировать', pos_b='verb', pos_a='verb')
        self.assertIn('дисгармонировать', results)

    def test_verb_860(self):
        results = self.derivation.derive(word_b='сидеть', pos_b='verb', pos_a='verb')
        self.assertIn('досидеть', results)
        results = self.derivation.derive(word_b='играть', pos_b='verb', pos_a='verb')
        self.assertIn('доиграть', results)

    def test_verb_861(self):
        results = self.derivation.derive(word_b='плыть', pos_b='verb', pos_a='verb')
        self.assertIn('заплыть', results)
        results = self.derivation.derive(word_b='асфальтировать', pos_b='verb', pos_a='verb')
        self.assertIn('заасфальтировать', results)
        results = self.derivation.derive(word_b='играть', pos_b='verb', pos_a='verb')
        self.assertIn('заиграть', results)
        results = self.derivation.derive(word_b='ездить', pos_b='verb', pos_a='verb')
        self.assertIn('заездить', results)

    def test_verb_861_1(self):
        results = self.derivation.derive(word_b='ехать', pos_b='verb', pos_a='verb')
        self.assertIn('заехать', results)
        results = self.derivation.derive(word_b='идти', pos_b='verb', pos_a='verb')
        self.assertIn('зайти', results)

    def test_verb_862(self):
        results = self.derivation.derive(word_b='лить', pos_b='verb', pos_a='verb')
        self.assertIn('излить', results)
        results = self.derivation.derive(word_b='течь', pos_b='verb', pos_a='verb')
        self.assertIn('истечь', results)
        results = self.derivation.derive(word_b='ездить', pos_b='verb', pos_a='verb')
        self.assertIn('изъездить', results)

    def test_verb_863(self):
        results = self.derivation.derive(word_b='греть', pos_b='verb', pos_a='verb')
        self.assertIn('нагреть', results)
        results = self.derivation.derive(word_b='течь', pos_b='verb', pos_a='verb')
        self.assertIn('натечь', results)
        results = self.derivation.derive(word_b='ездить', pos_b='verb', pos_a='verb')
        self.assertIn('наездить', results)

    def test_verb_863_1(self):
        results = self.derivation.derive(word_b='ехать', pos_b='verb', pos_a='verb')
        self.assertIn('наехать', results)
        results = self.derivation.derive(word_b='идти', pos_b='verb', pos_a='verb')
        self.assertIn('найти', results)

    def test_verb_864(self):
        results = self.derivation.derive(word_b='строить', pos_b='verb', pos_a='verb')
        self.assertIn('надстроить', results)
        results = self.derivation.derive(word_b='рвать', pos_b='verb', pos_a='verb')
        self.assertIn('надорвать', results)

    def test_verb_865(self):
        results = self.derivation.derive(word_b='грузить', pos_b='verb', pos_a='verb')
        self.assertIn('недогрузить', results)
        results = self.derivation.derive(word_b='оценить', pos_b='verb', pos_a='verb')
        self.assertIn('недооценить', results)

    def test_verb_865_1(self):
        results = self.derivation.derive(word_b='дать', pos_b='verb', pos_a='verb')
        self.assertIn('недодать', results)
        results = self.derivation.derive(word_b='есть', pos_b='verb', pos_a='verb')
        self.assertIn('недоесть', results)

    def test_verb_866(self):
        results = self.derivation.derive(word_b='вести', pos_b='verb', pos_a='verb')
        self.assertIn('низвести', results)
        results = self.derivation.derive(word_b='ринуться', pos_b='verb', pos_a='verb')
        self.assertIn('низринуться', results)
        results = self.derivation.derive(word_b='пасть', pos_b='verb', pos_a='verb')
        self.assertIn('ниспасть', results)

    def test_verb_866_1(self):
        results = self.derivation.derive(word_b='идти', pos_b='verb', pos_a='verb')
        self.assertIn('низойти', results)

    def test_verb_867(self):
        results = self.derivation.derive(word_b='бежать', pos_b='verb', pos_a='verb')
        self.assertIn('обежать', results)

    def test_verb_868(self):
        results = self.derivation.derive(word_b='драть', pos_b='verb', pos_a='verb')
        self.assertIn('ободрать', results)
        results = self.derivation.derive(word_b='садить', pos_b='verb', pos_a='verb')
        self.assertIn('обсадить', results)

    def test_verb_868_1(self):
        results = self.derivation.derive(word_b='идти', pos_b='verb', pos_a='verb')
        self.assertIn('обойти', results)
        results = self.derivation.derive(word_b='ехать', pos_b='verb', pos_a='verb')
        self.assertIn('объехать', results)

    def test_verb_869(self):
        results = self.derivation.derive(word_b='катить', pos_b='verb', pos_a='verb')
        self.assertIn('откатить', results)
        results = self.derivation.derive(word_b='двинуть', pos_b='verb', pos_a='verb')
        self.assertIn('отодвинуть', results)
        results = self.derivation.derive(word_b='мстить', pos_b='verb', pos_a='verb')
        self.assertIn('отомстить', results)

    def test_verb_869_1(self):
        results = self.derivation.derive(word_b='идти', pos_b='verb', pos_a='verb')
        self.assertIn('отойти', results)

    def test_verb_870(self):
        results = self.derivation.derive(word_b='рубить', pos_b='verb', pos_a='verb')
        self.assertIn('перерубить', results)
        results = self.derivation.derive(word_b='играть', pos_b='verb', pos_a='verb')
        self.assertIn('переиграть', results)

    def test_verb_871(self):
        results = self.derivation.derive(word_b='обсохнуть', pos_b='verb', pos_a='verb')
        self.assertIn('пообсохнуть', results)
        results = self.derivation.derive(word_b='износиться', pos_b='verb', pos_a='verb')
        self.assertIn('поизноситься', results)
        results = self.derivation.derive(word_b='привыкнуть', pos_b='verb', pos_a='verb')
        self.assertIn('попривыкнуть', results)

    def test_verb_872(self):
        results = self.derivation.derive(word_b='брать', pos_b='verb', pos_a='verb')
        self.assertIn('подобрать', results)
        results = self.derivation.derive(word_b='ставить', pos_b='verb', pos_a='verb')
        self.assertIn('подставить', results)
        results = self.derivation.derive(word_b='дернуть', pos_b='verb', pos_a='verb')
        self.assertIn('поддернуть', results)
        results = self.derivation.derive(word_b='играть', pos_b='verb', pos_a='verb')
        self.assertIn('поодыграть', results)
        results = self.derivation.derive(word_b='езжать', pos_b='verb', pos_a='verb')
        self.assertIn('подъезжать', results)

    def test_verb_873(self):
        results = self.derivation.derive(word_b='исполнить', pos_b='verb', pos_a='verb')
        self.assertIn('преисполнить', results)
        results = self.derivation.derive(word_b='уменьшить', pos_b='verb', pos_a='verb')
        self.assertIn('преуменьшить', results)

    def test_verb_874(self):
        results = self.derivation.derive(word_b='возвестить', pos_b='verb', pos_a='verb')
        self.assertIn('предвозвестить', results)
        results = self.derivation.derive(word_b='определить', pos_b='verb', pos_a='verb')
        self.assertIn('предопределить', results)
        results = self.derivation.derive(word_b='хранить', pos_b='verb', pos_a='verb')
        self.assertIn('предохранить', results)

    def test_verb_875(self):
        results = self.derivation.derive(word_b='плести', pos_b='verb', pos_a='verb')
        self.assertIn('приплести', results)
        results = self.derivation.derive(word_b='рисовать', pos_b='verb', pos_a='verb')
        self.assertIn('пририсовать', results)

    def test_verb_876(self):
        results = self.derivation.derive(word_b='дымить', pos_b='verb', pos_a='verb')
        self.assertIn('продымить', results)
        results = self.derivation.derive(word_b='ездить', pos_b='verb', pos_a='verb')
        self.assertIn('проездить', results)
        results = self.derivation.derive(word_b='играть', pos_b='verb', pos_a='verb')
        self.assertIn('проиграть', results)

    def test_verb_877(self):
        results = self.derivation.derive(word_b='злить', pos_b='verb', pos_a='verb')
        self.assertIn('разозлить', results)
        results = self.derivation.derive(word_b='слать', pos_b='verb', pos_a='verb')
        self.assertIn('разослать', results)
        results = self.derivation.derive(word_b='дернуть', pos_b='verb', pos_a='verb')
        self.assertIn('раздернуть', results)
        results = self.derivation.derive(word_b='играть', pos_b='verb', pos_a='verb')
        self.assertIn('разыграть', results)
        results = self.derivation.derive(word_b='ездить', pos_b='verb', pos_a='verb')
        self.assertIn('разъездить', results)

    def test_verb_878(self):
        results = self.derivation.derive(word_b='эвакуировать', pos_b='verb', pos_a='verb')
        self.assertIn('реэвакуировать', results)
        results = self.derivation.derive(word_b='милитаризировать', pos_b='verb', pos_a='verb')
        self.assertIn('ремилитаризировать', results)
        results = self.derivation.derive(word_b='интерпретировать', pos_b='verb', pos_a='verb')
        self.assertIn('реинтерпретировать', results)

    def test_verb_879(self):
        results = self.derivation.derive(word_b='грести', pos_b='verb', pos_a='verb')
        self.assertIn('сгрести', results)
        results = self.derivation.derive(word_b='звать', pos_b='verb', pos_a='verb')
        self.assertIn('созвать', results)
        results = self.derivation.derive(word_b='имитировать', pos_b='verb', pos_a='verb')
        self.assertIn('сымитировать', results)

    def test_verb_880(self):
        results = self.derivation.derive(word_b='наследовать', pos_b='verb', pos_a='verb')
        self.assertIn('сонаследовать', results)

    def test_verb_881(self):
        results = self.derivation.derive(word_b='катить', pos_b='verb', pos_a='verb')
        self.assertIn('укатить', results)

    def test_verb_887(self):
        results = self.derivation.derive(word_b='прямой', pos_b='adj', pos_a='verb')
        self.assertIn('выпрямить', results)
        results = self.derivation.derive(word_b='явный', pos_b='adj', pos_a='verb')
        self.assertIn('выявить', results)
        results = self.derivation.derive(word_b='ясный', pos_b='adj', pos_a='verb')
        self.assertIn('выяснить', results)

    def test_verb_888(self):
        results = self.derivation.derive(word_b='штора', pos_b='noun', pos_a='verb')
        self.assertIn('зашторить', results)
        results = self.derivation.derive(word_b='хлам', pos_b='noun', pos_a='verb')
        self.assertIn('захламить', results)
        results = self.derivation.derive(word_b='болото', pos_b='noun', pos_a='verb')
        self.assertIn('заболотить', results)
        results = self.derivation.derive(word_b='сургут', pos_b='noun', pos_a='verb')
        self.assertIn('засургутить', results)
        results = self.derivation.derive(word_b='слуга', pos_b='noun', pos_a='verb')
        self.assertIn('заслужить', results)
        results = self.derivation.derive(word_b='тень', pos_b='noun', pos_a='verb')
        self.assertIn('затенить', results)

    def test_verb_888_2(self):
        results = self.derivation.derive(word_b='трудный', pos_b='adj', pos_a='verb')
        self.assertIn('затруднить', results)
        results = self.derivation.derive(word_b='высокий', pos_b='adj', pos_a='verb')
        self.assertIn('завысить', results)
        results = self.derivation.derive(word_b='низкий', pos_b='adj', pos_a='verb')
        self.assertIn('занизить', results)

    def test_verb_888_3(self):
        results = self.derivation.derive(word_b='труднее', pos_b='comp', pos_a='verb')
        self.assertIn('затруднить', results)

    def test_verb_889(self):
        results = self.derivation.derive(word_b='крест', pos_b='noun', pos_a='verb')
        self.assertIn('искрестить', results)
        results = self.derivation.derive(word_b='узор', pos_b='noun', pos_a='verb')
        self.assertIn('изузорить', results)
        results = self.derivation.derive(word_b='язва', pos_b='noun', pos_a='verb')
        self.assertIn('изъязвить', results)

    def test_verb_889_1(self):
        results = self.derivation.derive(word_b='тонкий', pos_b='adj', pos_a='verb')
        self.assertIn('истончить', results)
        results = self.derivation.derive(word_b='редкий', pos_b='adj', pos_a='verb')
        self.assertIn('изредить', results)
        results = self.derivation.derive(word_b='пошлый', pos_b='adj', pos_a='verb')
        self.assertIn('испошлить', results)

    def test_verb_890(self):
        results = self.derivation.derive(word_b='сытый', pos_b='adj', pos_a='verb')
        self.assertIn('насытить', results)
        results = self.derivation.derive(word_b='полный', pos_b='adj', pos_a='verb')
        self.assertIn('наполнить', results)

    def test_verb_891(self):
        results = self.derivation.derive(word_b='цепь', pos_b='noun', pos_a='verb')
        self.assertIn('оцепить', results)
        results = self.derivation.derive(word_b='кайма', pos_b='noun', pos_a='verb')
        self.assertIn('окаймить', results)
        results = self.derivation.derive(word_b='куча', pos_b='noun', pos_a='verb')
        self.assertIn('окучить', results)
        results = self.derivation.derive(word_b='пух', pos_b='noun', pos_a='verb')
        self.assertIn('опушить', results)
        results = self.derivation.derive(word_b='контур', pos_b='noun', pos_a='verb')
        self.assertIn('оконтурить', results)
        results = self.derivation.derive(word_b='заглавие', pos_b='noun', pos_a='verb')
        self.assertIn('озаглавить', results)
        results = self.derivation.derive(word_b='стекло', pos_b='noun', pos_a='verb')
        self.assertIn('остеклить', results)

    def test_verb_891_1(self):
        results = self.derivation.derive(word_b='благородный', pos_b='adj', pos_a='verb')
        self.assertIn('облагородить', results)
        results = self.derivation.derive(word_b='короткий', pos_b='adj', pos_a='verb')
        self.assertIn('окоротить', results)
        results = self.derivation.derive(word_b='порожный', pos_b='adj', pos_a='verb')
        self.assertIn('опорожнить', results)

    def test_verb_891_2(self):
        results = self.derivation.derive(word_b='сложнее', pos_b='comp', pos_a='verb')
        self.assertIn('осложнить', results)

    def test_verb_892(self):
        results = self.derivation.derive(word_b='дерн', pos_b='noun', pos_a='verb')
        self.assertIn('обдернить', results)
        results = self.derivation.derive(word_b='мель', pos_b='noun', pos_a='verb')
        self.assertIn('обмелить', results)
        results = self.derivation.derive(word_b='семя', pos_b='noun', pos_a='verb')
        self.assertIn('обсеменить', results)
        results = self.derivation.derive(word_b='литература', pos_b='noun', pos_a='verb')
        self.assertIn('облитературить', results)
        results = self.derivation.derive(word_b='инженерный', pos_b='noun', pos_a='verb')
        self.assertIn('обынженерить', results)

    def test_verb_892_1(self):
        results = self.derivation.derive(word_b='легкий', pos_b='adj', pos_a='verb')
        self.assertIn('облегчить', results)
        results = self.derivation.derive(word_b='короткий', pos_b='adj', pos_a='verb')
        self.assertIn('обкоротить', results)
        results = self.derivation.derive(word_b='общий', pos_b='adj', pos_a='verb')
        self.assertIn('обобщить', results)

    def test_verb_892_2(self):
        results = self.derivation.derive(word_b='легче', pos_b='comp', pos_a='verb')
        self.assertIn('облегчить', results)

    def test_verb_893(self):
        results = self.derivation.derive(word_b='жир', pos_b='noun', pos_a='verb')
        self.assertIn('обезжирить', results)
        results = self.derivation.derive(word_b='зараза', pos_b='noun', pos_a='verb')
        self.assertIn('обеззаразить', results)
        results = self.derivation.derive(word_b='крыло', pos_b='noun', pos_a='verb')
        self.assertIn('обескрылить', results)
        results = self.derivation.derive(word_b='соль', pos_b='noun', pos_a='verb')
        self.assertIn('обессолить', results)
        results = self.derivation.derive(word_b='ток', pos_b='noun', pos_a='verb')
        self.assertIn('обесточить', results)

    def test_verb_893_1(self):
        results = self.derivation.derive(word_b='движение', pos_b='noun', pos_a='verb')
        self.assertIn('обездвижить', results)

    def test_verb_894(self):
        results = self.derivation.derive(word_b='щепка', pos_b='noun', pos_a='verb')
        self.assertIn('отщепить', results)
        results = self.derivation.derive(word_b='граница', pos_b='noun', pos_a='verb')
        self.assertIn('отграничить', results)

    def test_verb_895(self):
        results = self.derivation.derive(word_b='горький', pos_b='adj', pos_a='verb')
        self.assertIn('перегорчить', results)
        results = self.derivation.derive(word_b='кислый', pos_b='adj', pos_a='verb')
        self.assertIn('перекислить', results)
        results = self.derivation.derive(word_b='тонкий', pos_b='adj', pos_a='verb')
        self.assertIn('перетончить', results)
        results = self.derivation.derive(word_b='злой', pos_b='adj', pos_a='verb')
        self.assertIn('перезлить', results)

    def test_verb_895_1(self):
        results = self.derivation.derive(word_b='сильный', pos_b='adj', pos_a='verb')
        self.assertIn('пересилить', results)
        results = self.derivation.derive(word_b='упрямый', pos_b='adj', pos_a='verb')
        self.assertIn('переупрямить', results)
        results = self.derivation.derive(word_b='изящный', pos_b='adj', pos_a='verb')
        self.assertIn('переизящнить', results)

    def test_verb_895_2(self):
        results = self.derivation.derive(word_b='нахал', pos_b='noun', pos_a='verb')
        self.assertIn('перенахалить', results)
        results = self.derivation.derive(word_b='зинаида', pos_b='noun', pos_a='verb')
        self.assertIn('перезинаидить', results)

    def test_verb_896(self):
        results = self.derivation.derive(word_b='высокий', pos_b='adj', pos_a='verb')
        self.assertIn('повысить', results)
        results = self.derivation.derive(word_b='низкий', pos_b='adj', pos_a='verb')
        self.assertIn('понизить', results)
        results = self.derivation.derive(word_b='ясный', pos_b='adj', pos_a='verb')
        self.assertIn('пояснить', results)

    def test_verb_897(self):
        results = self.derivation.derive(word_b='домкрат', pos_b='noun', pos_a='verb')
        self.assertIn('поддомкратить', results)
        results = self.derivation.derive(word_b='пружина', pos_b='noun', pos_a='verb')
        self.assertIn('подпружинить', results)

    def test_verb_897_1(self):
        results = self.derivation.derive(word_b='короткий', pos_b='adj', pos_a='verb')
        self.assertIn('подкоротить', results)
        results = self.derivation.derive(word_b='кислый', pos_b='adj', pos_a='verb')
        self.assertIn('подкислить', results)

    def test_verb_898(self):
        results = self.derivation.derive(word_b='губа', pos_b='noun', pos_a='verb')
        self.assertIn('пригубить', results)
        results = self.derivation.derive(word_b='земля', pos_b='noun', pos_a='verb')
        self.assertIn('приземлить', results)
        results = self.derivation.derive(word_b='клюв', pos_b='noun', pos_a='verb')
        self.assertIn('приклювить', results)
        results = self.derivation.derive(word_b='страсть', pos_b='noun', pos_a='verb')
        self.assertIn('пристрастить', results)
        results = self.derivation.derive(word_b='кнопка', pos_b='noun', pos_a='verb')
        self.assertIn('прикнопить', results)

    def test_verb_899(self):
        results = self.derivation.derive(word_b='резина', pos_b='noun', pos_a='verb')
        self.assertIn('прорезинить', results)
        results = self.derivation.derive(word_b='олиф', pos_b='noun', pos_a='verb')
        self.assertIn('проолифить', results)
        results = self.derivation.derive(word_b='табак', pos_b='noun', pos_a='verb')
        self.assertIn('протабачить', results)

    def test_verb_899_1(self):
        results = self.derivation.derive(word_b='ясный', pos_b='adj', pos_a='verb')
        self.assertIn('прояснить', results)
        results = self.derivation.derive(word_b='редкий', pos_b='adj', pos_a='verb')
        self.assertIn('проредить', results)
        results = self.derivation.derive(word_b='свежий', pos_b='adj', pos_a='verb')
        self.assertIn('просвежить', results)

    def test_verb_900(self):
        results = self.derivation.derive(word_b='пыль', pos_b='noun', pos_a='verb')
        self.assertIn('распылить', results)
        results = self.derivation.derive(word_b='крыло', pos_b='noun', pos_a='verb')
        self.assertIn('раскрылить', results)
        results = self.derivation.derive(word_b='щебень', pos_b='noun', pos_a='verb')
        self.assertIn('расщебенить', results)
        results = self.derivation.derive(word_b='щепка', pos_b='noun', pos_a='verb')
        self.assertIn('расщепить', results)
        results = self.derivation.derive(word_b='охота', pos_b='noun', pos_a='verb')
        self.assertIn('разохотить', results)
        results = self.derivation.derive(word_b='оружие', pos_b='noun', pos_a='verb')
        self.assertIn('разоружить', results)
        results = self.derivation.derive(word_b='чехол', pos_b='noun', pos_a='verb')
        self.assertIn('расчехлить', results)
        results = self.derivation.derive(word_b='воздух', pos_b='noun', pos_a='verb')
        self.assertIn('развоздушить', results)

    def test_verb_900_1(self):
        results = self.derivation.derive(word_b='ярость', pos_b='noun', pos_a='verb')
        self.assertIn('разъярить', results)

    def test_verb_900_2(self):
        results = self.derivation.derive(word_b='жидкий', pos_b='adj', pos_a='verb')
        self.assertIn('разжидить', results)
        results = self.derivation.derive(word_b='ясный', pos_b='adj', pos_a='verb')
        self.assertIn('разъяснить', results)

    def test_verb_900_3(self):
        results = self.derivation.derive(word_b='реже', pos_b='comp', pos_a='verb')
        self.assertIn('разредить', results)

    def test_verb_900_4(self):
        results = self.derivation.derive(word_b='секретный', pos_b='adj', pos_a='verb')
        self.assertIn('рассекретить', results)
        results = self.derivation.derive(word_b='общий', pos_b='adj', pos_a='verb')
        self.assertIn('разобщить', results)

    def test_verb_901(self):
        results = self.derivation.derive(word_b='куча', pos_b='noun', pos_a='verb')
        self.assertIn('скучить', results)
        results = self.derivation.derive(word_b='клок', pos_b='noun', pos_a='verb')
        self.assertIn('склочить', results)
        results = self.derivation.derive(word_b='толпа', pos_b='noun', pos_a='verb')
        self.assertIn('столпить', results)
        results = self.derivation.derive(word_b='сбор', pos_b='noun', pos_a='verb')
        self.assertIn('сосборить', results)
        results = self.derivation.derive(word_b='петля', pos_b='noun', pos_a='verb')
        self.assertIn('спетлить', results)

    def test_verb_901_1(self):
        results = self.derivation.derive(word_b='жидкий', pos_b='adj', pos_a='verb')
        self.assertIn('сжидить', results)
        results = self.derivation.derive(word_b='кособокий', pos_b='adj', pos_a='verb')
        self.assertIn('скособочить', results)
        results = self.derivation.derive(word_b='низкий', pos_b='adj', pos_a='verb')
        self.assertIn('снизить', results)

    def test_verb_901_2(self):
        results = self.derivation.derive(word_b='двое', pos_b='num', pos_a='verb')
        self.assertIn('сдвоить', results)
        results = self.derivation.derive(word_b='четверо', pos_b='num', pos_a='verb')
        self.assertIn('счетверить', results)

    def test_verb_902(self):
        results = self.derivation.derive(word_b='равновесие', pos_b='noun', pos_a='verb')
        self.assertIn('уравновесить', results)
        results = self.derivation.derive(word_b='покоить', pos_b='noun', pos_a='verb')
        self.assertIn('упокоить', results)
        results = self.derivation.derive(word_b='порядок', pos_b='noun', pos_a='verb')
        self.assertIn('упорядочить', results)

    def test_verb_902_1(self):
        results = self.derivation.derive(word_b='сын', pos_b='noun', pos_a='verb')
        self.assertIn('усыновить', results)
        results = self.derivation.derive(word_b='дочь', pos_b='noun', pos_a='verb')
        self.assertIn('удочерить', results)
        results = self.derivation.derive(word_b='внук', pos_b='noun', pos_a='verb')
        self.assertIn('увнучить', results)
        results = self.derivation.derive(word_b='щенок', pos_b='noun', pos_a='verb')
        self.assertIn('ущенить', results)

    def test_verb_902_2(self):
        results = self.derivation.derive(word_b='влажный', pos_b='adj', pos_a='verb')
        self.assertIn('увлажнить', results)
        results = self.derivation.derive(word_b='глубокий', pos_b='adj', pos_a='verb')
        self.assertIn('углубить', results)
        results = self.derivation.derive(word_b='длинный', pos_b='adj', pos_a='verb')
        self.assertIn('удлинить', results)
        results = self.derivation.derive(word_b='короткий', pos_b='adj', pos_a='verb')
        self.assertIn('укоротить', results)

    def test_verb_902_3(self):
        results = self.derivation.derive(word_b='короче', pos_b='comp', pos_a='verb')
        self.assertIn('укоротить', results)
        results = self.derivation.derive(word_b='меньше', pos_b='comp', pos_a='verb')
        self.assertIn('уменьшить', results)
        results = self.derivation.derive(word_b='ярче', pos_b='comp', pos_a='verb')
        self.assertIn('уярчить', results)

    def test_verb_902_4(self):
        results = self.derivation.derive(word_b='десятеро', pos_b='num', pos_a='verb')
        self.assertIn('удесятерить', results)
        results = self.derivation.derive(word_b='двое', pos_b='num', pos_a='verb')
        self.assertIn('удвоить', results)

    def test_verb_905(self):
        results = self.derivation.derive(word_b='полоумный', pos_b='adj', pos_a='verb')
        self.assertIn('ополоуметь', results)
        results = self.derivation.derive(word_b='роговой', pos_b='adj', pos_a='verb')
        self.assertIn('ороговеть', results)
        results = self.derivation.derive(word_b='голый', pos_b='adj', pos_a='verb')
        self.assertIn('оголеть', results)
        results = self.derivation.derive(word_b='длинный', pos_b='adj', pos_a='verb')
        self.assertIn('одлинеть', results)

    def test_verb_906(self):
        results = self.derivation.derive(word_b='мох', pos_b='noun', pos_a='verb')
        self.assertIn('обомшеть', results)
        results = self.derivation.derive(word_b='листва', pos_b='noun', pos_a='verb')
        self.assertIn('облистветь', results)
        results = self.derivation.derive(word_b='мозоль', pos_b='noun', pos_a='verb')
        self.assertIn('обмозолить', results)

    def test_verb_907(self):
        results = self.derivation.derive(word_b='память', pos_b='noun', pos_a='verb')
        self.assertIn('обеспамятеть', results)
        results = self.derivation.derive(word_b='деньги', pos_b='noun', pos_a='verb')
        self.assertIn('обезденежеть', results)
        results = self.derivation.derive(word_b='раба', pos_b='noun', pos_a='verb')
        self.assertIn('обезрыбеть', results)
        results = self.derivation.derive(word_b='живот', pos_b='noun', pos_a='verb')
        self.assertIn('обезживотеть', results)
        results = self.derivation.derive(word_b='ночь', pos_b='noun', pos_a='verb')
        self.assertIn('обезночеть', results)
        results = self.derivation.derive(word_b='крыло', pos_b='noun', pos_a='verb')
        self.assertIn('обескрылеть', results)
        results = self.derivation.derive(word_b='мужик', pos_b='noun', pos_a='verb')
        self.assertIn('обезмужичеть', results)

    def test_verb_908(self):
        results = self.derivation.derive(word_b='серьезный', pos_b='adj', pos_a='verb')
        self.assertIn('посерьезнеть', results)
        results = self.derivation.derive(word_b='широкий', pos_b='adj', pos_a='verb')
        self.assertIn('поширеть', results)

    def test_verb_908_1(self):
        results = self.derivation.derive(word_b='лучше', pos_b='comp', pos_a='verb')
        self.assertIn('получшеть', results)
        results = self.derivation.derive(word_b='строже', pos_b='comp', pos_a='verb')
        self.assertIn('построжеть', results)

    def test_verb_909(self):
        results = self.derivation.derive(word_b='звезда', pos_b='noun', pos_a='verb')
        self.assertIn('вызвездеть', results)
        results = self.derivation.derive(word_b='толстый', pos_b='adj', pos_a='verb')
        self.assertIn('вытолщеть', results)
        results = self.derivation.derive(word_b='дырявый', pos_b='adj', pos_a='verb')
        self.assertIn('издыряветь', results)
        results = self.derivation.derive(word_b='смирный', pos_b='adj', pos_a='verb')
        self.assertIn('присмиреть', results)
        results = self.derivation.derive(word_b='соль', pos_b='noun', pos_a='verb')
        self.assertIn('просолеть', results)
        results = self.derivation.derive(word_b='целый', pos_b='adj', pos_a='verb')
        self.assertIn('уцелеть', results)
        results = self.derivation.derive(word_b='пот', pos_b='noun', pos_a='verb')
        self.assertIn('употеть', results)

    def test_verb_909_1(self):
        results = self.derivation.derive(word_b='лед', pos_b='noun', pos_a='verb')
        self.assertIn('нальдеть', results)
        results = self.derivation.derive(word_b='живой', pos_b='adj', pos_a='verb')
        self.assertIn('отживеть', results)
        results = self.derivation.derive(word_b='жара', pos_b='noun', pos_a='verb')
        self.assertIn('сжареть', results)

    def test_verb_911(self):
        results = self.derivation.derive(word_b='народ', pos_b='noun', pos_a='verb')
        self.assertIn('обнародовать', results)
        results = self.derivation.derive(word_b='ярмо', pos_b='noun', pos_a='verb')
        self.assertIn('объярмовать', results)

    def test_verb_911_1(self):
        results = self.derivation.derive(word_b='фраза', pos_b='noun', pos_a='verb')
        self.assertIn('перефразировать', results)

    def test_verb_911_2(self):
        results = self.derivation.derive(word_b='вожжа', pos_b='noun', pos_a='verb')
        self.assertIn('завожжать', results)
        results = self.derivation.derive(word_b='поздний', pos_b='sdj', pos_a='verb')
        self.assertIn('запоздать', results)

    def test_verb_911_3(self):
        results = self.derivation.derive(word_b='поздний', pos_b='sdj', pos_a='verb')
        self.assertIn('опоздать', results)
        results = self.derivation.derive(word_b='бедный', pos_b='sdj', pos_a='verb')
        self.assertIn('обеднять', results)

    def test_verb_911_4(self):
        results = self.derivation.derive(word_b='узда', pos_b='noun', pos_a='verb')
        self.assertIn('обуздать', results)

    def test_verb_911_5(self):
        results = self.derivation.derive(word_b='лучше', pos_b='comp', pos_a='verb')
        self.assertIn('получшать', results)
        results = self.derivation.derive(word_b='тоньше', pos_b='comp', pos_a='verb')
        self.assertIn('потоньшать', results)
        results = self.derivation.derive(word_b='строже', pos_b='comp', pos_a='verb')
        self.assertIn('построжать', results)

    def test_verb_911_6(self):
        results = self.derivation.derive(word_b='тоньше', pos_b='comp', pos_a='verb')
        self.assertIn('утоньшать', results)

    def test_verb_911_7(self):
        results = self.derivation.derive(word_b='пояс', pos_b='noun', pos_a='verb')
        self.assertIn('опоясать', results)
        results = self.derivation.derive(word_b='пояс', pos_b='noun', pos_a='verb')
        self.assertIn('перепоясать', results)
        results = self.derivation.derive(word_b='пояс', pos_b='noun', pos_a='verb')
        self.assertIn('подпоясать', results)
        results = self.derivation.derive(word_b='пояс', pos_b='noun', pos_a='verb')
        self.assertIn('распоясать', results)

    def test_verb_914(self):
        results = self.derivation.derive(word_b='танцевать', pos_b='verb', pos_a='verb')
        self.assertIn('вытанцовывать', results)
        results = self.derivation.derive(word_b='звонить', pos_b='verb', pos_a='verb')
        self.assertIn('вызванивать', results)
        results = self.derivation.derive(word_b='плясать', pos_b='verb', pos_a='verb')
        self.assertIn('выплясывать', results)
        results = self.derivation.derive(word_b='свистеть', pos_b='verb', pos_a='verb')
        self.assertIn('высвистывать', results)
        results = self.derivation.derive(word_b='щелкать', pos_b='verb', pos_a='verb')
        self.assertIn('выщелкивать', results)

    def test_verb_915(self):
        results = self.derivation.derive(word_b='звонить', pos_b='verb', pos_a='verb')
        self.assertIn('названивать', results)
        results = self.derivation.derive(word_b='крутить', pos_b='verb', pos_a='verb')
        self.assertIn('накручивать', results)
        results = self.derivation.derive(word_b='плясать', pos_b='verb', pos_a='verb')
        self.assertIn('наплясывать', results)
        results = self.derivation.derive(word_b='рисовать', pos_b='verb', pos_a='verb')
        self.assertIn('нарисовывать', results)
        results = self.derivation.derive(word_b='свистеть', pos_b='verb', pos_a='verb')
        self.assertIn('насвистывать', results)
        results = self.derivation.derive(word_b='петь', pos_b='verb', pos_a='verb')
        self.assertIn('напевать', results)

    def test_verb_916(self):
        results = self.derivation.derive(word_b='плясать', pos_b='verb', pos_a='verb')
        self.assertIn('отплясывать', results)
        results = self.derivation.derive(word_b='стучать', pos_b='verb', pos_a='verb')
        self.assertIn('отстукивать', results)
        results = self.derivation.derive(word_b='щелкать', pos_b='verb', pos_a='verb')
        self.assertIn('отщелкивать', results)
        results = self.derivation.derive(word_b='блестеть', pos_b='verb', pos_a='verb')
        self.assertIn('отблескивать', results)
        results = self.derivation.derive(word_b='светить', pos_b='verb', pos_a='verb')
        self.assertIn('отсвечивать', results)
        results = self.derivation.derive(word_b='сверкать', pos_b='verb', pos_a='verb')
        self.assertIn('отсверкивать', results)

    def test_verb_917(self):
        results = self.derivation.derive(word_b='звонить', pos_b='verb', pos_a='verb')
        self.assertIn('перезванивать', results)
        results = self.derivation.derive(word_b='стучать', pos_b='verb', pos_a='verb')
        self.assertIn('перестукивать', results)

    def test_verb_918(self):
        results = self.derivation.derive(word_b='болеть', pos_b='verb', pos_a='verb')
        self.assertIn('побаливать', results)
        results = self.derivation.derive(word_b='визжать', pos_b='verb', pos_a='verb')
        self.assertIn('повизгивать', results)
        results = self.derivation.derive(word_b='дергать', pos_b='verb', pos_a='verb')
        self.assertIn('подергивать', results)
        results = self.derivation.derive(word_b='драть', pos_b='verb', pos_a='verb')
        self.assertIn('подирать', results)
        results = self.derivation.derive(word_b='дремать', pos_b='verb', pos_a='verb')
        self.assertIn('подремывать', results)
        results = self.derivation.derive(word_b='дуть', pos_b='verb', pos_a='verb')
        self.assertIn('подувать', results)
        results = self.derivation.derive(word_b='ежиться', pos_b='verb', pos_a='verb')
        self.assertIn('поеживаться', results)
        results = self.derivation.derive(word_b='кашлять', pos_b='verb', pos_a='verb')
        self.assertIn('покашливать', results)
        results = self.derivation.derive(word_b='ругать', pos_b='verb', pos_a='verb')
        self.assertIn('поругивать', results)
        results = self.derivation.derive(word_b='тереть', pos_b='verb', pos_a='verb')
        self.assertIn('потирать', results)
        results = self.derivation.derive(word_b='воевать', pos_b='verb', pos_a='verb')
        self.assertIn('повоевывать', results)

    def test_verb_919(self):
        results = self.derivation.derive(word_b='пахать', pos_b='verb', pos_a='verb')
        self.assertIn('подпахивать', results)
        results = self.derivation.derive(word_b='врать', pos_b='verb', pos_a='verb')
        self.assertIn('подвирать', results)
        results = self.derivation.derive(word_b='дразнить', pos_b='verb', pos_a='verb')
        self.assertIn('поддразнивать', results)
        results = self.derivation.derive(word_b='дуть', pos_b='verb', pos_a='verb')
        self.assertIn('поддувать', results)
        results = self.derivation.derive(word_b='кашлять', pos_b='verb', pos_a='verb')
        self.assertIn('подкашливать', results)
        results = self.derivation.derive(word_b='храпеть', pos_b='verb', pos_a='verb')
        self.assertIn('подхрапывать', results)
        results = self.derivation.derive(word_b='голодать', pos_b='verb', pos_a='verb')
        self.assertIn('подголадывать', results)
        results = self.derivation.derive(word_b='ныть', pos_b='verb', pos_a='verb')
        self.assertIn('поднывать', results)

    def test_verb_920(self):
        results = self.derivation.derive(word_b='петь', pos_b='verb', pos_a='verb')
        self.assertIn('припевать', results)
        results = self.derivation.derive(word_b='говорить', pos_b='verb', pos_a='verb')
        self.assertIn('приговаривать', results)
        results = self.derivation.derive(word_b='крякать', pos_b='verb', pos_a='verb')
        self.assertIn('прикрякивать', results)
        results = self.derivation.derive(word_b='свистеть', pos_b='verb', pos_a='verb')
        self.assertIn('присвистывать', results)
        results = self.derivation.derive(word_b='хлопать', pos_b='verb', pos_a='verb')
        self.assertIn('прихлопывать', results)
        results = self.derivation.derive(word_b='шлепать', pos_b='verb', pos_a='verb')
        self.assertIn('пришептывать', results)
        results = self.derivation.derive(word_b='хромать', pos_b='verb', pos_a='verb')
        self.assertIn('прихрамывать', results)
        results = self.derivation.derive(word_b='пахать', pos_b='verb', pos_a='verb')
        self.assertIn('припахивать', results)
        results = self.derivation.derive(word_b='хворать', pos_b='verb', pos_a='verb')
        self.assertIn('прихварывать', results)
        results = self.derivation.derive(word_b='хлебать', pos_b='verb', pos_a='verb')
        self.assertIn('прихлебывать', results)

    def test_verb_921(self):
        results = self.derivation.derive(word_b='пить', pos_b='verb', pos_a='verb')
        self.assertIn('распивать', results)
        results = self.derivation.derive(word_b='думать', pos_b='verb', pos_a='verb')
        self.assertIn('раздумывать', results)
        results = self.derivation.derive(word_b='курить', pos_b='verb', pos_a='verb')
        self.assertIn('раскуривать', results)
        results = self.derivation.derive(word_b='ходить', pos_b='verb', pos_a='verb')
        self.assertIn('расхаживать', results)
        results = self.derivation.derive(word_b='гулять', pos_b='verb', pos_a='verb')
        self.assertIn('разгуливать', results)
        results = self.derivation.derive(word_b='ездить', pos_b='verb', pos_a='verb')
        self.assertIn('разъезжать', results)

    def test_verb_923(self):
        results = self.derivation.derive(word_b='плакать', pos_b='verb', pos_a='verb')
        self.assertIn('всплакнуть', results)
        results = self.derivation.derive(word_b='грустить', pos_b='verb', pos_a='verb')
        self.assertIn('взгрустнуть', results)
        results = self.derivation.derive(word_b='дрермать', pos_b='verb', pos_a='verb')
        self.assertIn('вздремнуть', results)
        results = self.derivation.derive(word_b='полоскать', pos_b='verb', pos_a='verb')
        self.assertIn('всполоснуть', results)
        results = self.derivation.derive(word_b='храпеть', pos_b='verb', pos_a='verb')
        self.assertIn('всхрапнуть', results)

    def test_verb_924(self):
        results = self.derivation.derive(word_b='хворать', pos_b='verb', pos_a='verb')
        self.assertIn('прихворнуть', results)
        results = self.derivation.derive(word_b='дремать', pos_b='verb', pos_a='verb')
        self.assertIn('придремнуть', results)
        results = self.derivation.derive(word_b='лгать', pos_b='verb', pos_a='verb')
        self.assertIn('прилгнуть', results)
        results = self.derivation.derive(word_b='хвастать', pos_b='verb', pos_a='verb')
        self.assertIn('прихвастнуть', results)

    def test_verb_925(self):
        results = self.derivation.derive(word_b='болтать', pos_b='verb', pos_a='verb')
        self.assertIn('сболтнуть', results)
        results = self.derivation.derive(word_b='грустить', pos_b='verb', pos_a='verb')
        self.assertIn('сгрустнуть', results)
        results = self.derivation.derive(word_b='полоскать', pos_b='verb', pos_a='verb')
        self.assertIn('сполоснуть', results)
        results = self.derivation.derive(word_b='брехать', pos_b='verb', pos_a='verb')
        self.assertIn('сбрехнуть', results)
        results = self.derivation.derive(word_b='спать', pos_b='verb', pos_a='verb')
        self.assertIn('соснуть', results)
        results = self.derivation.derive(word_b='стирать', pos_b='verb', pos_a='verb')
        self.assertIn('состирнуть', results)

    def test_verb_926_1(self):
        results = self.derivation.derive(word_b='спать', pos_b='verb', pos_a='verb')
        self.assertIn('заснуть', results)

    def test_verb_926_2(self):
        results = self.derivation.derive(word_b='полоскать', pos_b='verb', pos_a='verb')
        self.assertIn('ополоснуть', results)

    def test_verb_926_3(self):
        results = self.derivation.derive(word_b='стирать', pos_b='verb', pos_a='verb')
        self.assertIn('простирнуть', results)

    def test_verb_926_4(self):
        results = self.derivation.derive(word_b='спать', pos_b='verb', pos_a='verb')
        self.assertIn('уснуть', results)
        results = self.derivation.derive(word_b='смеяться', pos_b='verb', pos_a='verb')
        self.assertIn('усмехнуться', results)

    def test_verb_928(self):
        results = self.derivation.derive(word_b='вешать', pos_b='verb', pos_a='verb')
        self.assertIn('взвесить', results)
        results = self.derivation.derive(word_b='вешать', pos_b='verb', pos_a='verb')
        self.assertIn('довесить', results)
        results = self.derivation.derive(word_b='вешать', pos_b='verb', pos_a='verb')
        self.assertIn('недовесить', results)
        results = self.derivation.derive(word_b='вешать', pos_b='verb', pos_a='verb')
        self.assertIn('обвесить', results)
        results = self.derivation.derive(word_b='вешать', pos_b='verb', pos_a='verb')
        self.assertIn('отвесить', results)
        results = self.derivation.derive(word_b='вешать', pos_b='verb', pos_a='verb')
        self.assertIn('перевесить', results)
        results = self.derivation.derive(word_b='вешать', pos_b='verb', pos_a='verb')
        self.assertIn('привесить', results)
        results = self.derivation.derive(word_b='вешать', pos_b='verb', pos_a='verb')
        self.assertIn('провесить', results)
        results = self.derivation.derive(word_b='вешать', pos_b='verb', pos_a='verb')
        self.assertIn('развесить', results)

    def test_verb_928_1(self):
        results = self.derivation.derive(word_b='вешать', pos_b='verb', pos_a='verb')
        self.assertIn('вывесить', results)
        results = self.derivation.derive(word_b='вешать', pos_b='verb', pos_a='verb')
        self.assertIn('завесить', results)
        results = self.derivation.derive(word_b='вешать', pos_b='verb', pos_a='verb')
        self.assertIn('навесить', results)
        results = self.derivation.derive(word_b='вешать', pos_b='verb', pos_a='verb')
        self.assertIn('обвесить', results)
        results = self.derivation.derive(word_b='вешать', pos_b='verb', pos_a='verb')
        self.assertIn('перевесить', results)
        results = self.derivation.derive(word_b='вешать', pos_b='verb', pos_a='verb')
        self.assertIn('повесить', results)
        results = self.derivation.derive(word_b='вешать', pos_b='verb', pos_a='verb')
        self.assertIn('подвесить', results)
        results = self.derivation.derive(word_b='вешать', pos_b='verb', pos_a='verb')
        self.assertIn('провесить', results)
        results = self.derivation.derive(word_b='вешать', pos_b='verb', pos_a='verb')
        self.assertIn('развесить', results)
        results = self.derivation.derive(word_b='вешать', pos_b='verb', pos_a='verb')
        self.assertIn('свесить', results)
        results = self.derivation.derive(word_b='вешать', pos_b='verb', pos_a='verb')
        self.assertIn('увесить', results)

    def test_verb_928_2(self):
        results = self.derivation.derive(word_b='ворочать', pos_b='verb', pos_a='verb')
        self.assertIn('выворотить', results)
        results = self.derivation.derive(word_b='ворочать', pos_b='verb', pos_a='verb')
        self.assertIn('отворотить', results)
        results = self.derivation.derive(word_b='ворочать', pos_b='verb', pos_a='verb')
        self.assertIn('поворотить', results)
        results = self.derivation.derive(word_b='ворочать', pos_b='verb', pos_a='verb')
        self.assertIn('своротить', results)

    def test_verb_928_3(self):
        results = self.derivation.derive(word_b='глотать', pos_b='verb', pos_a='verb')
        self.assertIn('поглотить', results)
        results = self.derivation.derive(word_b='глотать', pos_b='verb', pos_a='verb')
        self.assertIn('проглотить', results)

    def test_verb_928_4(self):
        results = self.derivation.derive(word_b='кланяться', pos_b='verb', pos_a='verb')
        self.assertIn('поклониться', results)

    def test_verb_928_5(self):
        results = self.derivation.derive(word_b='кусать', pos_b='verb', pos_a='verb')
        self.assertIn('закусить', results)
        results = self.derivation.derive(word_b='кусать', pos_b='verb', pos_a='verb')
        self.assertIn('надкусить', results)
        results = self.derivation.derive(word_b='кусать', pos_b='verb', pos_a='verb')
        self.assertIn('откусить', results)
        results = self.derivation.derive(word_b='кусать', pos_b='verb', pos_a='verb')
        self.assertIn('перекусить', results)
        results = self.derivation.derive(word_b='кусать', pos_b='verb', pos_a='verb')
        self.assertIn('прикусить', results)
        results = self.derivation.derive(word_b='кусать', pos_b='verb', pos_a='verb')
        self.assertIn('прокусить', results)
        results = self.derivation.derive(word_b='кусать', pos_b='verb', pos_a='verb')
        self.assertIn('раскусить', results)
        results = self.derivation.derive(word_b='кусать', pos_b='verb', pos_a='verb')
        self.assertIn('укусить', results)

    def test_verb_928_6(self):
        results = self.derivation.derive(word_b='кушать', pos_b='verb', pos_a='verb')
        self.assertIn('закусить', results)
        results = self.derivation.derive(word_b='кушать', pos_b='verb', pos_a='verb')
        self.assertIn('перекусить', results)

    def test_verb_928_7(self):
        results = self.derivation.derive(word_b='менять', pos_b='verb', pos_a='verb')
        self.assertIn('заменить', results)
        results = self.derivation.derive(word_b='менять', pos_b='verb', pos_a='verb')
        self.assertIn('изменить', results)
        results = self.derivation.derive(word_b='менять', pos_b='verb', pos_a='verb')
        self.assertIn('обменить', results)
        results = self.derivation.derive(word_b='менять', pos_b='verb', pos_a='verb')
        self.assertIn('отменить', results)
        results = self.derivation.derive(word_b='менять', pos_b='verb', pos_a='verb')
        self.assertIn('переменить', results)
        results = self.derivation.derive(word_b='менять', pos_b='verb', pos_a='verb')
        self.assertIn('подменить', results)
        results = self.derivation.derive(word_b='менять', pos_b='verb', pos_a='verb')
        self.assertIn('сменить', results)

    def test_verb_928_8(self):
        results = self.derivation.derive(word_b='подозревать', pos_b='verb', pos_a='verb')
        self.assertIn('заподозрить', results)

    def test_verb_928_9(self):
        results = self.derivation.derive(word_b='ронять', pos_b='verb', pos_a='verb')
        self.assertIn('выронить', results)
        results = self.derivation.derive(word_b='ронять', pos_b='verb', pos_a='verb')
        self.assertIn('заронить', results)
        results = self.derivation.derive(word_b='ронять', pos_b='verb', pos_a='verb')
        self.assertIn('обронить', results)
        results = self.derivation.derive(word_b='ронять', pos_b='verb', pos_a='verb')
        self.assertIn('проронить', results)
        results = self.derivation.derive(word_b='ронять', pos_b='verb', pos_a='verb')
        self.assertIn('сронить', results)
        results = self.derivation.derive(word_b='ронять', pos_b='verb', pos_a='verb')
        self.assertIn('уронить', results)

    def test_verb_928_10(self):
        results = self.derivation.derive(word_b='ручаться', pos_b='verb', pos_a='verb')
        self.assertIn('поручиться', results)

    def test_verb_928_11(self):
        results = self.derivation.derive(word_b='сажать', pos_b='verb', pos_a='verb')
        self.assertIn('высадить', results)
        results = self.derivation.derive(word_b='сажать', pos_b='verb', pos_a='verb')
        self.assertIn('досадить', results)
        results = self.derivation.derive(word_b='сажать', pos_b='verb', pos_a='verb')
        self.assertIn('засадить', results)
        results = self.derivation.derive(word_b='сажать', pos_b='verb', pos_a='verb')
        self.assertIn('насадить', results)
        results = self.derivation.derive(word_b='сажать', pos_b='verb', pos_a='verb')
        self.assertIn('обсадить', results)
        results = self.derivation.derive(word_b='сажать', pos_b='verb', pos_a='verb')
        self.assertIn('отсадить', results)
        results = self.derivation.derive(word_b='сажать', pos_b='verb', pos_a='verb')
        self.assertIn('пересадить', results)
        results = self.derivation.derive(word_b='сажать', pos_b='verb', pos_a='verb')
        self.assertIn('подсадить', results)
        results = self.derivation.derive(word_b='сажать', pos_b='verb', pos_a='verb')
        self.assertIn('посадить', results)
        results = self.derivation.derive(word_b='сажать', pos_b='verb', pos_a='verb')
        self.assertIn('присадить', results)
        results = self.derivation.derive(word_b='сажать', pos_b='verb', pos_a='verb')
        self.assertIn('рассадить', results)

    def test_verb_928_12(self):
        results = self.derivation.derive(word_b='сажать', pos_b='verb', pos_a='verb')
        self.assertIn('высадить', results)
        results = self.derivation.derive(word_b='сажать', pos_b='verb', pos_a='verb')
        self.assertIn('досадить', results)
        results = self.derivation.derive(word_b='сажать', pos_b='verb', pos_a='verb')
        self.assertIn('засадить', results)
        results = self.derivation.derive(word_b='сажать', pos_b='verb', pos_a='verb')
        self.assertIn('насадить', results)
        results = self.derivation.derive(word_b='сажать', pos_b='verb', pos_a='verb')
        self.assertIn('отсадить', results)
        results = self.derivation.derive(word_b='сажать', pos_b='verb', pos_a='verb')
        self.assertIn('пересадить', results)
        results = self.derivation.derive(word_b='сажать', pos_b='verb', pos_a='verb')
        self.assertIn('подсадить', results)
        results = self.derivation.derive(word_b='сажать', pos_b='verb', pos_a='verb')
        self.assertIn('посадить', results)
        results = self.derivation.derive(word_b='сажать', pos_b='verb', pos_a='verb')
        self.assertIn('рассадить', results)
        results = self.derivation.derive(word_b='сажать', pos_b='verb', pos_a='verb')
        self.assertIn('ссадить', results)
        results = self.derivation.derive(word_b='сажать', pos_b='verb', pos_a='verb')
        self.assertIn('усадить', results)

    def test_verb_928_13(self):
        results = self.derivation.derive(word_b='скакать', pos_b='verb', pos_a='verb')
        self.assertIn('вскочить', results)
        results = self.derivation.derive(word_b='скакать', pos_b='verb', pos_a='verb')
        self.assertIn('выскочить', results)
        results = self.derivation.derive(word_b='скакать', pos_b='verb', pos_a='verb')
        self.assertIn('заскочить', results)
        results = self.derivation.derive(word_b='скакать', pos_b='verb', pos_a='verb')
        self.assertIn('наскочить', results)
        results = self.derivation.derive(word_b='скакать', pos_b='verb', pos_a='verb')
        self.assertIn('отскочить', results)
        results = self.derivation.derive(word_b='скакать', pos_b='verb', pos_a='verb')
        self.assertIn('перескочить', results)
        results = self.derivation.derive(word_b='скакать', pos_b='verb', pos_a='verb')
        self.assertIn('подскочить', results)
        results = self.derivation.derive(word_b='скакать', pos_b='verb', pos_a='verb')
        self.assertIn('проскочить', results)
        results = self.derivation.derive(word_b='скакать', pos_b='verb', pos_a='verb')
        self.assertIn('соскочить', results)

    def test_verb_928_14(self):
        results = self.derivation.derive(word_b='сомневаться', pos_b='verb', pos_a='verb')
        self.assertIn('усомниться', results)

    def test_verb_928_15(self):
        results = self.derivation.derive(word_b='стрелять', pos_b='verb', pos_a='verb')
        self.assertIn('выстрелить', results)
        results = self.derivation.derive(word_b='стрелять', pos_b='verb', pos_a='verb')
        self.assertIn('застрелить', results)
        results = self.derivation.derive(word_b='стрелять', pos_b='verb', pos_a='verb')
        self.assertIn('отстрелить', results)
        results = self.derivation.derive(word_b='стрелять', pos_b='verb', pos_a='verb')
        self.assertIn('подстрелить', results)
        results = self.derivation.derive(word_b='стрелять', pos_b='verb', pos_a='verb')
        self.assertIn('пристрелить', results)
        results = self.derivation.derive(word_b='стрелять', pos_b='verb', pos_a='verb')
        self.assertIn('прострелить', results)

    def test_verb_928_16(self):
        results = self.derivation.derive(word_b='хватать', pos_b='verb', pos_a='verb')
        self.assertIn('выхватить', results)
        results = self.derivation.derive(word_b='хватать', pos_b='verb', pos_a='verb')
        self.assertIn('захватить', results)
        results = self.derivation.derive(word_b='хватать', pos_b='verb', pos_a='verb')
        self.assertIn('охватить', results)
        results = self.derivation.derive(word_b='хватать', pos_b='verb', pos_a='verb')
        self.assertIn('обхватить', results)
        results = self.derivation.derive(word_b='хватать', pos_b='verb', pos_a='verb')
        self.assertIn('отхватить', results)
        results = self.derivation.derive(word_b='хватать', pos_b='verb', pos_a='verb')
        self.assertIn('перехватить', results)
        results = self.derivation.derive(word_b='хватать', pos_b='verb', pos_a='verb')
        self.assertIn('подхватить', results)
        results = self.derivation.derive(word_b='хватать', pos_b='verb', pos_a='verb')
        self.assertIn('прихватить', results)
        results = self.derivation.derive(word_b='хватать', pos_b='verb', pos_a='verb')
        self.assertIn('схватить', results)
        results = self.derivation.derive(word_b='хватать', pos_b='verb', pos_a='verb')
        self.assertIn('ухватить', results)

    def test_verb_928_17(self):
        results = self.derivation.derive(word_b='цеплять', pos_b='verb', pos_a='verb')
        self.assertIn('зацепить', results)
        results = self.derivation.derive(word_b='цеплять', pos_b='verb', pos_a='verb')
        self.assertIn('нацепить', results)
        results = self.derivation.derive(word_b='цеплять', pos_b='verb', pos_a='verb')
        self.assertIn('отцепить', results)
        results = self.derivation.derive(word_b='цеплять', pos_b='verb', pos_a='verb')
        self.assertIn('перецепить', results)
        results = self.derivation.derive(word_b='цеплять', pos_b='verb', pos_a='verb')
        self.assertIn('подцепить', results)
        results = self.derivation.derive(word_b='цеплять', pos_b='verb', pos_a='verb')
        self.assertIn('прицепить', results)
        results = self.derivation.derive(word_b='цеплять', pos_b='verb', pos_a='verb')
        self.assertIn('расцепить', results)
        results = self.derivation.derive(word_b='цеплять', pos_b='verb', pos_a='verb')
        self.assertIn('сцепить', results)
        results = self.derivation.derive(word_b='цеплять', pos_b='verb', pos_a='verb')
        self.assertIn('уцепить', results)

    def test_verb_928_18(self):
        results = self.derivation.derive(word_b='щепать', pos_b='verb', pos_a='verb')
        self.assertIn('отщепить', results)
        results = self.derivation.derive(word_b='щепать', pos_b='verb', pos_a='verb')
        self.assertIn('прищепить', results)
        results = self.derivation.derive(word_b='щепать', pos_b='verb', pos_a='verb')
        self.assertIn('расщепить', results)

    def test_verb_930(self):
        results = self.derivation.derive(word_b='мыть', pos_b='verb', pos_a='verb')
        self.assertIn('мыться', results)
        results = self.derivation.derive(word_b='белеть', pos_b='verb', pos_a='verb')
        self.assertIn('белеться', results)
        results = self.derivation.derive(word_b='дуть', pos_b='verb', pos_a='verb')
        self.assertIn('дуться', results)
        results = self.derivation.derive(word_b='рисовать', pos_b='verb', pos_a='verb')
        self.assertIn('рисоваться', results)
        results = self.derivation.derive(word_b='вести', pos_b='verb', pos_a='verb')
        self.assertIn('вестись', results)
        results = self.derivation.derive(word_b='давать', pos_b='verb', pos_a='verb')
        self.assertIn('даваться', results)
        results = self.derivation.derive(word_b='нанять', pos_b='verb', pos_a='verb')
        self.assertIn('наняться', results)

    def test_verb_932(self):
        results = self.derivation.derive(word_b='невеста', pos_b='noun', pos_a='verb')
        self.assertIn('невеститься', results)
        results = self.derivation.derive(word_b='петух', pos_b='noun', pos_a='verb')
        self.assertIn('петушиться', results)
        results = self.derivation.derive(word_b='фосфор', pos_b='noun', pos_a='verb')
        self.assertIn('фосфориться', results)
        results = self.derivation.derive(word_b='уголь', pos_b='noun', pos_a='verb')
        self.assertIn('углиться', results)
        results = self.derivation.derive(word_b='толпа', pos_b='noun', pos_a='verb')
        self.assertIn('толпиться', results)
        results = self.derivation.derive(word_b='ветвь', pos_b='noun', pos_a='verb')
        self.assertIn('ветвиться', results)
        results = self.derivation.derive(word_b='тщеславие', pos_b='noun', pos_a='verb')
        self.assertIn('тщеславиться', results)
        results = self.derivation.derive(word_b='щенок', pos_b='noun', pos_a='verb')
        self.assertIn('щениться', results)
        results = self.derivation.derive(word_b='ягненок', pos_b='noun', pos_a='verb')
        self.assertIn('ягниться', results)
        results = self.derivation.derive(word_b='сосулька', pos_b='noun', pos_a='verb')
        self.assertIn('сосулиться', results)

    def test_verb_933(self):
        results = self.derivation.derive(word_b='дикий', pos_b='adj', pos_a='verb')
        self.assertIn('дичиться', results)
        results = self.derivation.derive(word_b='скупой', pos_b='adj', pos_a='verb')
        self.assertIn('скупиться', results)
        results = self.derivation.derive(word_b='угрюмый', pos_b='adj', pos_a='verb')
        self.assertIn('угрюмиться', results)
        results = self.derivation.derive(word_b='жеманный', pos_b='adj', pos_a='verb')
        self.assertIn('жеманиться', results)
        results = self.derivation.derive(word_b='разный', pos_b='adj', pos_a='verb')
        self.assertIn('разниться', results)
        results = self.derivation.derive(word_b='высокий', pos_b='adj', pos_a='verb')
        self.assertIn('выситься', results)

    def test_verb_935(self):
        results = self.derivation.derive(word_b='почка', pos_b='noun', pos_a='verb')
        self.assertIn('почковаться', results)
        results = self.derivation.derive(word_b='рубец', pos_b='noun', pos_a='verb')
        self.assertIn('рубцеваться', results)
        results = self.derivation.derive(word_b='стол', pos_b='noun', pos_a='verb')
        self.assertIn('столоваться', results)

    def test_verb_935_1(self):
        results = self.derivation.derive(word_b='брат', pos_b='noun', pos_a='verb')
        self.assertIn('брататься', results)
        results = self.derivation.derive(word_b='жених', pos_b='noun', pos_a='verb')
        self.assertIn('женихаться', results)
        results = self.derivation.derive(word_b='нужда', pos_b='noun', pos_a='verb')
        self.assertIn('нуждаться', results)

    def test_verb_935_2(self):
        results = self.derivation.derive(word_b='видный', pos_b='adj', pos_a='verb')
        self.assertIn('виднеться', results)

    def test_verb_937(self):
        results = self.derivation.derive(word_b='думать', pos_b='verb', pos_a='verb')
        self.assertIn('вдуматься', results)
        results = self.derivation.derive(word_b='смотреть', pos_b='verb', pos_a='verb')
        self.assertIn('всмотреться', results)
        results = self.derivation.derive(word_b='петь', pos_b='verb', pos_a='verb')
        self.assertIn('впеться', results)
        results = self.derivation.derive(word_b='играть', pos_b='verb', pos_a='verb')
        self.assertIn('выграться', results)

    def test_verb_937_1(self):
        results = self.derivation.derive(word_b='ахать', pos_b='verb', pos_a='verb')
        self.assertIn('взахаться', results)
        results = self.derivation.derive(word_b='дурить', pos_b='verb', pos_a='verb')
        self.assertIn('вздуриться', results)
        results = self.derivation.derive(word_b='плакать', pos_b='verb', pos_a='verb')
        self.assertIn('всплакаться', results)
        results = self.derivation.derive(word_b='бушевать', pos_b='verb', pos_a='verb')
        self.assertIn('взбушеваться', results)

    def test_verb_937_2(self):
        results = self.derivation.derive(word_b='бегать', pos_b='verb', pos_a='verb')
        self.assertIn('выбегаться', results)
        results = self.derivation.derive(word_b='говорить', pos_b='verb', pos_a='verb')
        self.assertIn('выговориться', results)

    def test_verb_937_3(self):
        results = self.derivation.derive(word_b='рыть', pos_b='verb', pos_a='verb')
        self.assertIn('дорыться', results)
        results = self.derivation.derive(word_b='черппать', pos_b='verb', pos_a='verb')
        self.assertIn('дочерпаться', results)

    def test_verb_937_4(self):
        results = self.derivation.derive(word_b='будить', pos_b='verb', pos_a='verb')
        self.assertIn('добудиться', results)
        results = self.derivation.derive(word_b='думать', pos_b='verb', pos_a='verb')
        self.assertIn('додуматься', results)
        results = self.derivation.derive(word_b='ждать', pos_b='verb', pos_a='verb')
        self.assertIn('дождаться', results)

    def test_verb_937_5(self):
        results = self.derivation.derive(word_b='работать', pos_b='verb', pos_a='verb')
        self.assertIn('доработаться', results)
        results = self.derivation.derive(word_b='воевать', pos_b='verb', pos_a='verb')
        self.assertIn('довоеваться', results)
        results = self.derivation.derive(word_b='курить', pos_b='verb', pos_a='verb')
        self.assertIn('докуриться', results)

    def test_verb_937_6(self):
        results = self.derivation.derive(word_b='бегать', pos_b='verb', pos_a='verb')
        self.assertIn('забегаться', results)
        results = self.derivation.derive(word_b='смотреть', pos_b='verb', pos_a='verb')
        self.assertIn('засмотреться', results)

    def test_verb_937_7(self):
        results = self.derivation.derive(word_b='лгать', pos_b='verb', pos_a='verb')
        self.assertIn('изолгаться', results)
        results = self.derivation.derive(word_b='нервничать', pos_b='verb', pos_a='verb')
        self.assertIn('изнервничаться', results)
        results = self.derivation.derive(word_b='страдать', pos_b='verb', pos_a='verb')
        self.assertIn('исстрадаться', results)

    def test_verb_937_8(self):
        results = self.derivation.derive(word_b='бегать', pos_b='verb', pos_a='verb')
        self.assertIn('набегаться', results)
        results = self.derivation.derive(word_b='терпеть', pos_b='verb', pos_a='verb')
        self.assertIn('натерпеться', results)
        results = self.derivation.derive(word_b='вставать', pos_b='verb', pos_a='verb')
        self.assertIn('навставаться', results)

    def test_verb_937_9(self):
        results = self.derivation.derive(word_b='есть', pos_b='verb', pos_a='verb')
        self.assertIn('наесться', results)

    def test_verb_937_10(self):
        results = self.derivation.derive(word_b='слышать', pos_b='verb', pos_a='verb')
        self.assertIn('ослышаться', results)
        results = self.derivation.derive(word_b='думать', pos_b='verb', pos_a='verb')
        self.assertIn('одуматься', results)

    def test_verb_937_11(self):
        results = self.derivation.derive(word_b='считать', pos_b='verb', pos_a='verb')
        self.assertIn('обсчитаться', results)
        results = self.derivation.derive(word_b='искать', pos_b='verb', pos_a='verb')
        self.assertIn('обыскаться', results)

    def test_verb_937_12(self):
        results = self.derivation.derive(word_b='сеять', pos_b='verb', pos_a='verb')
        self.assertIn('отсеяться', results)
        results = self.derivation.derive(word_b='воевать', pos_b='verb', pos_a='verb')
        self.assertIn('отвоеваться', results)
        results = self.derivation.derive(word_b='ездить', pos_b='verb', pos_a='verb')
        self.assertIn('отъездиться', results)

    def test_verb_937_13(self):
        results = self.derivation.derive(word_b='льстить', pos_b='verb', pos_a='verb')
        self.assertIn('подольститься', results)
        results = self.derivation.derive(word_b='лизать', pos_b='verb', pos_a='verb')
        self.assertIn('подлизаться', results)

    def test_verb_937_14(self):
        results = self.derivation.derive(word_b='слушать', pos_b='verb', pos_a='verb')
        self.assertIn('прислушаться', results)
        results = self.derivation.derive(word_b='тронуть', pos_b='verb', pos_a='verb')
        self.assertIn('притронуться', results)

    def test_verb_937_15(self):
        results = self.derivation.derive(word_b='есть', pos_b='verb', pos_a='verb')
        self.assertIn('приесться', results)

    def test_verb_937_16(self):
        results = self.derivation.derive(word_b='говорить', pos_b='verb', pos_a='verb')
        self.assertIn('проговориться', results)

    def test_verb_937_17(self):
        results = self.derivation.derive(word_b='ехать', pos_b='verb', pos_a='verb')
        self.assertIn('проехаться', results)
        results = self.derivation.derive(word_b='идти', pos_b='verb', pos_a='verb')
        self.assertIn('пройтись', results)

    def test_verb_937_18(self):
        results = self.derivation.derive(word_b='бежать', pos_b='verb', pos_a='verb')
        self.assertIn('разбежаться', results)
        results = self.derivation.derive(word_b='сохнуть', pos_b='verb', pos_a='verb')
        self.assertIn('рассохнуться', results)

    def test_verb_937_19(self):
        results = self.derivation.derive(word_b='идти', pos_b='verb', pos_a='verb')
        self.assertIn('разойтись', results)

    def test_verb_937_20(self):
        results = self.derivation.derive(word_b='бежать', pos_b='verb', pos_a='verb')
        self.assertIn('сбежаться', results)
        results = self.derivation.derive(word_b='ползти', pos_b='verb', pos_a='verb')
        self.assertIn('сползтись', results)
        results = self.derivation.derive(word_b='плыть', pos_b='verb', pos_a='verb')
        self.assertIn('сплыться', results)
        results = self.derivation.derive(word_b='течь', pos_b='verb', pos_a='verb')
        self.assertIn('стечься', results)
        results = self.derivation.derive(word_b='брести', pos_b='verb', pos_a='verb')
        self.assertIn('сбрестись', results)
        results = self.derivation.derive(word_b='липнуть', pos_b='verb', pos_a='verb')
        self.assertIn('слипнуться', results)

    def test_verb_937_21(self):
        results = self.derivation.derive(word_b='ездить', pos_b='verb', pos_a='verb')
        self.assertIn('уездиться', results)
        results = self.derivation.derive(word_b='прыгать', pos_b='verb', pos_a='verb')
        self.assertIn('упрыгаться', results)

    def test_verb_956(self):
        results = self.derivation.derive(word_b='банкрот', pos_b='noun', pos_a='verb')
        self.assertIn('обанкротиться', results)
        results = self.derivation.derive(word_b='мужик', pos_b='noun', pos_a='verb')
        self.assertIn('омужичиться', results)
        results = self.derivation.derive(word_b='баба', pos_b='noun', pos_a='verb')
        self.assertIn('обабиться', results)

    def test_verb_956_1(self):
        results = self.derivation.derive(word_b='смелый', pos_b='adj', pos_a='verb')
        self.assertIn('осмелиться', results)

    def test_verb_956_2(self):
        results = self.derivation.derive(word_b='интеллигент', pos_b='noun', pos_a='verb')
        self.assertIn('обынтеллигентиться', results)
        results = self.derivation.derive(word_b='якут', pos_b='noun', pos_a='verb')
        self.assertIn('объякутиться', results)

    def test_verb_956_3(self):
        results = self.derivation.derive(word_b='культурный', pos_b='adj', pos_a='verb')
        self.assertIn('обкультуриться', results)

    def test_verb_956_4(self):
        results = self.derivation.derive(word_b='ил', pos_b='noun', pos_a='verb')
        self.assertIn('заилиться', results)
        results = self.derivation.derive(word_b='паутина', pos_b='noun', pos_a='verb')
        self.assertIn('запаутиниться', results)

    def test_verb_956_5(self):
        results = self.derivation.derive(word_b='ловкий', pos_b='adj', pos_a='verb')
        self.assertIn('изловчиться', results)
        results = self.derivation.derive(word_b='несчастье', pos_b='noun', pos_a='verb')
        self.assertIn('изнесчаститься', results)

    def test_verb_956_6(self):
        results = self.derivation.derive(word_b='ловкий', pos_b='adj', pos_a='verb')
        self.assertIn('наловчиться', results)
        results = self.derivation.derive(word_b='коготь', pos_b='noun', pos_a='verb')
        self.assertIn('накогтиться', results)
        results = self.derivation.derive(word_b='коршун', pos_b='noun', pos_a='verb')
        self.assertIn('накоршуниться', results)

    def test_verb_956_7(self):
        results = self.derivation.derive(word_b='счастливый', pos_b='adj', pos_a='verb')
        self.assertIn('посчастливиться', results)
        results = self.derivation.derive(word_b='витамин', pos_b='noun', pos_a='verb')
        self.assertIn('повитаминиться', results)

    def test_verb_956_8(self):
        results = self.derivation.derive(word_b='поздний', pos_b='adj', pos_a='verb')
        self.assertIn('припоздниться', results)
        results = self.derivation.derive(word_b='луна', pos_b='noun', pos_a='verb')
        self.assertIn('прилуниться', results)
        results = self.derivation.derive(word_b='осанка', pos_b='noun', pos_a='verb')
        self.assertIn('приосаниться', results)

    def test_verb_956_9(self):
        results = self.derivation.derive(word_b='слеза', pos_b='noun', pos_a='verb')
        self.assertIn('прослезиться', results)
        results = self.derivation.derive(word_b='штраф', pos_b='noun', pos_a='verb')
        self.assertIn('проштрафиться', results)

    def test_verb_956_11(self):
        results = self.derivation.derive(word_b='кошель', pos_b='noun', pos_a='verb')
        self.assertIn('раскошелиться', results)
        results = self.derivation.derive(word_b='щедрый', pos_b='adj', pos_a='verb')
        self.assertIn('расщедриться', results)
        results = self.derivation.derive(word_b='погода', pos_b='noun', pos_a='verb')
        self.assertIn('распогодиться', results)
        results = self.derivation.derive(word_b='обезьяна', pos_b='noun', pos_a='verb')
        self.assertIn('разобезьяниться', results)

    def test_verb_956_12(self):
        results = self.derivation.derive(word_b='милостивый', pos_b='adj', pos_a='verb')
        self.assertIn('смилостивиться', results)
        results = self.derivation.derive(word_b='капут', pos_b='noun', pos_a='verb')
        self.assertIn('скапутиться', results)
        results = self.derivation.derive(word_b='копыто', pos_b='noun', pos_a='verb')
        self.assertIn('скопытиться', results)
        results = self.derivation.derive(word_b='петля', pos_b='noun', pos_a='verb')
        self.assertIn('спетлиться', results)

    def test_verb_956_13(self):
        results = self.derivation.derive(word_b='летучий', pos_b='adj', pos_a='verb')
        self.assertIn('улетучиться', results)
        results = self.derivation.derive(word_b='хитрый', pos_b='adj', pos_a='verb')
        self.assertIn('ухитриться', results)

    def test_verb_956_15(self):
        results = self.derivation.derive(word_b='шутить', pos_b='verb', pos_a='verb')
        self.assertIn('перешучиваться', results)
        results = self.derivation.derive(word_b='говорить', pos_b='verb', pos_a='verb')
        self.assertIn('переговариваться', results)
        results = self.derivation.derive(word_b='звонить', pos_b='verb', pos_a='verb')
        self.assertIn('перезваниваться', results)
        results = self.derivation.derive(word_b='кричать', pos_b='verb', pos_a='verb')
        self.assertIn('перекрикиваться', results)
        results = self.derivation.derive(word_b='свистеть', pos_b='verb', pos_a='verb')
        self.assertIn('пересвистываться', results)

    def test_verb_956_17(self):
        results = self.derivation.derive(word_b='дурить', pos_b='verb', pos_a='verb')
        self.assertIn('придуриваться', results)

    def test_verb_956_18(self):
        results = self.derivation.derive(word_b='цеплять', pos_b='verb', pos_a='verb')
        self.assertIn('вцепиться', results)

    def test_verb_956_19(self):
        results = self.derivation.derive(word_b='блуждать', pos_b='verb', pos_a='verb')
        self.assertIn('заблудиться', results)

    def test_verb_956_20(self):
        results = self.derivation.derive(word_b='жалеть', pos_b='verb', pos_a='verb')
        self.assertIn('сжалиться', results)

    def test_verb_956_21(self):
        results = self.derivation.derive(word_b='спать', pos_b='verb', pos_a='verb')
        self.assertIn('проснуться', results)

    def test_verb_956_22(self):
        results = self.derivation.derive(word_b='трепетать', pos_b='verb', pos_a='verb')
        self.assertIn('встрепенуться', results)















if __name__ == '__main__':
    unittest.main(verbosity=2)
