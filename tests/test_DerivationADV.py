import unittest

from src.Derivation import Derivation


class TestDerivation(unittest.TestCase):
    def setUp(self):
        self.derivation = Derivation()

    def tearDown(self):
        del self.derivation

    def test_adv_977(self):
        results = self.derivation.derive(word_b='быстрый', pos_b='adj', pos_a='adv')
        self.assertIn('быстро', results)
        results = self.derivation.derive(word_b='искренний', pos_b='adj', pos_a='adv')
        self.assertIn('искренне', results)
        results = self.derivation.derive(word_b='двоякий', pos_b='adj', pos_a='adv')
        self.assertIn('двояко', results)
        results = self.derivation.derive(word_b='певучий', pos_b='adj', pos_a='adv')
        self.assertIn('певуче', results)
        results = self.derivation.derive(word_b='свежий', pos_b='adj', pos_a='adv')
        self.assertIn('свежо', results)

    def test_adv_977_2(self):
        results = self.derivation.derive(word_b='броский', pos_b='adj', pos_a='adv')
        self.assertIn('броско', results)
        results = self.derivation.derive(word_b='веский', pos_b='adj', pos_a='adv')
        self.assertIn('веско', results)
    

    def test_adv_979(self):
        """ Проверка правила 979. """
        results = self.derivation.derive(word_b='всяческий', pos_b='adj', pos_a='adv')
        self.assertIn('всячески', results)
        results = self.derivation.derive(word_b='воровской', pos_b='adj', pos_a='adv')
        self.assertIn('воровски', results)

    def test_adv_979_2(self):
        """ Проверка правила 979. """
        results = self.derivation.derive(word_b='медвежий', pos_b='adj', pos_a='adv')
        self.assertIn('медвежьи', results)
        results = self.derivation.derive(word_b='бабий', pos_b='adj', pos_a='adv')
        self.assertIn('бабьи', results)


    @unittest.skip
    def test_adv_980(self):
        """ Проверка правила 979. """
        results = self.derivation.derive(word_b='пеший', pos_b='adj', pos_a='adv')
        self.assertIn('пешком', results)
        results = self.derivation.derive(word_b='тихий', pos_b='adj', pos_a='adv')
        self.assertIn('тишком', results)
        results = self.derivation.derive(word_b='тайный', pos_b='adj', pos_a='adv')
        self.assertIn('тайком', results)

    @unittest.skip
    def test_adv_980_2(self):
        """ Проверка правила 979. """
        results = self.derivation.derive(word_b='босой', pos_b='adj', pos_a='adv')
        self.assertIn('босиком', results)
        results = self.derivation.derive(word_b='целый', pos_b='adj', pos_a='adv')
        self.assertIn('целиком', results)
        results = self.derivation.derive(word_b='прямой', pos_b='adj', pos_a='adv')
        self.assertIn('прямиком', results)

    @unittest.skip
    def test_adv_980_3(self):
        """ Проверка правила 979. """
        results = self.derivation.derive(word_b='пеший', pos_b='adj', pos_a='adv')
        self.assertIn('пёхом', results)

    @unittest.skip
    def test_adv_980_4(self):
        """ Проверка правила 979. """
        results = self.derivation.derive(word_b='живой', pos_b='adj', pos_a='adv')
        self.assertIn('живьём', results)
        results = self.derivation.derive(word_b='голый', pos_b='adj', pos_a='adv')
        self.assertIn('гольём', results)

    @unittest.skip
    def test_adv_980_5(self):
        """ Проверка правила 979. """
        results = self.derivation.derive(word_b='особый', pos_b='adj', pos_a='adv')
        self.assertIn('особняком', results)

    @unittest.skip
    def test_adv_980_6(self):
        """ Проверка правила 979. """
        results = self.derivation.derive(word_b='нагой', pos_b='adj', pos_a='adv')
        self.assertIn('нагишом', results)

    
    @unittest.skip
    def test_adv_981_1(self):
        """ Проверка правила 979. """
        results = self.derivation.derive(word_b='белый', pos_b='adj', pos_a='adv')
        self.assertIn('белым', results)
        results = self.derivation.derive(word_b='давний', pos_b='adj', pos_a='adv')
        self.assertIn('давным', results)

    @unittest.skip
    def test_adv_981_2(self):
        """ Проверка правила 979. """
        results = self.derivation.derive(word_b='полный', pos_b='adj', pos_a='adv')
        self.assertIn('полностью', results)

    def test_adv_982(self):
        results = self.derivation.derive(word_b='зима', pos_b='noun', pos_a='adv')
        self.assertIn('зимой', results)
        results = self.derivation.derive(word_b='воля', pos_b='noun', pos_a='adv')
        self.assertIn('волей', results)
        results = self.derivation.derive(word_b='рысь', pos_b='noun', pos_a='adv')
        self.assertIn('рысью', results)
        results = self.derivation.derive(word_b='день', pos_b='noun', pos_a='adv')
        self.assertIn('днем', results)
        results = self.derivation.derive(word_b='волчок', pos_b='noun', pos_a='adv')
        self.assertIn('волчком', results)
        results = self.derivation.derive(word_b='наскок', pos_b='noun', pos_a='adv')
        self.assertIn('наскоком', results)
        results = self.derivation.derive(word_b='молодец', pos_b='noun', pos_a='adv')
        self.assertIn('молодцом', results)
        results = self.derivation.derive(word_b='утро', pos_b='noun', pos_a='adv')
        self.assertIn('утром', results)
        results = self.derivation.derive(word_b='дни', pos_b='noun', pos_a='adv')
        self.assertIn('днями', results)
        results = self.derivation.derive(word_b='времена', pos_b='noun', pos_a='adv')
        self.assertIn('временами', results)
    
    @unittest.skip
    def test_adv_982_2(self):
        results = self.derivation.derive(word_b='дом', pos_b='noun', pos_a='adv')
        self.assertIn('дома', results)

    @unittest.skip
    def test_adv_982_3(self):
        results = self.derivation.derive(word_b='сила', pos_b='noun', pos_a='adv')
        self.assertIn('силком', results)
        results = self.derivation.derive(word_b='гусь', pos_b='noun', pos_a='adv')
        self.assertIn('гуськом', results)

    @unittest.skip
    def test_adv_982_4(self):
        results = self.derivation.derive(word_b='сила', pos_b='noun', pos_a='adv')
        self.assertIn('силом', results)

    @unittest.skip
    def test_adv_983(self):
        results = self.derivation.derive(word_b='шесть', pos_b='num', pos_a='adv')
        self.assertIn('шестью', results)

    @unittest.skip
    def test_adv_984(self):
        results = self.derivation.derive(word_b='два', pos_b='num', pos_a='adv')
        self.assertIn('дважды', results)
        results = self.derivation.derive(word_b='три', pos_b='num', pos_a='adv')
        self.assertIn('трижды', results)
        results = self.derivation.derive(word_b='четыре', pos_b='num', pos_a='adv')
        self.assertIn('четырежды', results)

    @unittest.skip
    def test_adv_984_2(self):
        results = self.derivation.derive(word_b='один', pos_b='num', pos_a='adv')
        self.assertIn('однажды', results)
        results = self.derivation.derive(word_b='много', pos_b='num', pos_a='adv')
        self.assertIn('многажды', results)

    @unittest.skip
    def test_adv_984_3(self):
        results = self.derivation.derive(word_b='один', pos_b='num', pos_a='adv')
        self.assertIn('единожды', results)



    def test_adv_985(self):
        results = self.derivation.derive(word_b='стоять', pos_b='verb', pos_a='adv')
        self.assertIn('стоймя', results)
        results = self.derivation.derive(word_b='сидеть', pos_b='verb', pos_a='adv')
        self.assertIn('сидмя', results)
        results = self.derivation.derive(word_b='хлестать', pos_b='verb', pos_a='adv')
        self.assertIn('хлестмя', results)
        results = self.derivation.derive(word_b='валить', pos_b='verb', pos_a='adv')
        self.assertIn('вальмя', results)
        results = self.derivation.derive(word_b='жить', pos_b='verb', pos_a='adv')
        self.assertIn('живмя', results)
        results = self.derivation.derive(word_b='лить', pos_b='verb', pos_a='adv')
        self.assertIn('ливмя', results)
        # results = self.derivation.derive(word_b='пластать', pos_b='verb', pos_a='adv')
        # self.assertIn('плашмя', results)

    
    @unittest.skip
    def test_adv_986(self):
        results = self.derivation.derive(word_b='кувыркаться', pos_b='verb', pos_a='adv')
        self.assertIn('кувырком', results)
        results = self.derivation.derive(word_b='волочь', pos_b='verb', pos_a='adv')
        self.assertIn('волоком', results)
        results = self.derivation.derive(word_b='дыбиться', pos_b='verb', pos_a='adv')
        self.assertIn('дыбом', results)
        results = self.derivation.derive(word_b='насыпать', pos_b='verb', pos_a='adv')
        self.assertIn('насыпом', results)
        results = self.derivation.derive(word_b='наезжать', pos_b='verb', pos_a='adv')
        self.assertIn('наездом', results)

    @unittest.skip
    def test_adv_986_2(self):
        results = self.derivation.derive(word_b='ползти', pos_b='verb', pos_a='adv')
        self.assertIn('ползком', results)
        results = self.derivation.derive(word_b='молчать', pos_b='verb', pos_a='adv')
        self.assertIn('молчком', results)
        results = self.derivation.derive(word_b='щипать', pos_b='verb', pos_a='adv')
        self.assertIn('щипком', results)
        results = self.derivation.derive(word_b='стоять', pos_b='verb', pos_a='adv')
        self.assertIn('стойком', results)
        results = self.derivation.derive(word_b='трусить', pos_b='verb', pos_a='adv')
        self.assertIn('труском', results)

    @unittest.skip
    def test_adv_986_3(self):
        results = self.derivation.derive(word_b='рвать', pos_b='verb', pos_a='adv')
        self.assertIn('рывом', results)

    @unittest.skip
    def test_adv_986_4(self):
        results = self.derivation.derive(word_b='набиться', pos_b='verb', pos_a='adv')
        self.assertIn('битком', results)

    @unittest.skip
    def test_adv_986_5(self):
        results = self.derivation.derive(word_b='ходить', pos_b='verb', pos_a='adv')
        self.assertIn('ходуном', results)

    @unittest.skip
    def test_adv_987_1(self):
        results = self.derivation.derive(word_b='ощупать', pos_b='verb', pos_a='adv')
        self.assertIn('ощупью', results)
        results = self.derivation.derive(word_b='насыпать', pos_b='verb', pos_a='adv')
        self.assertIn('насыпью', results)

    @unittest.skip
    def test_adv_987_2(self):
        results = self.derivation.derive(word_b='сторожить', pos_b='verb', pos_a='adv')
        self.assertIn('настороже', results)

    @unittest.skip
    def test_adv_987_3(self):
        results = self.derivation.derive(word_b='урывать', pos_b='verb', pos_a='adv')
        self.assertIn('урывками', results)

    @unittest.skip
    def test_adv_987_4(self):
        results = self.derivation.derive(word_b='мочь', pos_b='verb', pos_a='adv')
        self.assertIn('можно', results)
        results = self.derivation.derive(word_b='жалеть', pos_b='verb', pos_a='adv')
        self.assertIn('жаль', results)

    def test_adv_987_5(self):
        results = self.derivation.derive(word_b='уметь', pos_b='verb', pos_a='adv')
        self.assertIn('умеючи', results)

    def test_adv_988(self):
        results = self.derivation.derive(word_b='рано', pos_b='adv', pos_a='adv')
        self.assertIn('рановато', results)

    def test_adv_989(self):
        results = self.derivation.derive(word_b='трудно', pos_b='adv', pos_a='adv')
        self.assertIn('трудненько', results)
        results = self.derivation.derive(word_b='хорошо', pos_b='adv', pos_a='adv')
        self.assertIn('хорошенько', results)
        results = self.derivation.derive(word_b='тихо', pos_b='adv', pos_a='adv')
        self.assertIn('тихонько', results)
        results = self.derivation.derive(word_b='высоко', pos_b='adv', pos_a='adv')
        self.assertIn('высоконько', results)

    def test_adv_990(self):
        results = self.derivation.derive(word_b='рано', pos_b='adv', pos_a='adv')
        self.assertIn('ранёхонько', results)
        results = self.derivation.derive(word_b='рано', pos_b='adv', pos_a='adv')
        self.assertIn('ранёшенько', results)
        results = self.derivation.derive(word_b='тихо', pos_b='adv', pos_a='adv')
        self.assertIn('тихохонько', results)
        results = self.derivation.derive(word_b='близко', pos_b='adv', pos_a='adv')
        self.assertIn('близёхонько', results)


    def test_adv_991(self):
        results = self.derivation.derive(word_b='боком', pos_b='adv', pos_a='adv')
        self.assertIn('бочком', results)
        results = self.derivation.derive(word_b='пешком', pos_b='adv', pos_a='adv')
        self.assertIn('пешочком', results)
        results = self.derivation.derive(word_b='босиком', pos_b='adv', pos_a='adv')
        self.assertIn('босичком', results)

    def test_adv_991_2(self):
        results = self.derivation.derive(word_b='стороной', pos_b='adv', pos_a='adv')
        self.assertIn('сторонкой', results)
        results = self.derivation.derive(word_b='украдкой', pos_b='adv', pos_a='adv')
        self.assertIn('украдочкой', results)

    def test_adv_991_3(self):
        results = self.derivation.derive(word_b='вразвалку', pos_b='adv', pos_a='adv')
        self.assertIn('вразвалочку', results)
        results = self.derivation.derive(word_b='потихоньку', pos_b='adv', pos_a='adv')
        self.assertIn('потихонечку', results)

    def test_adv_991_4(self):
        results = self.derivation.derive(word_b='хорошенько', pos_b='adv', pos_a='adv')
        self.assertIn('хорошенечко', results)


    @unittest.skip
    def test_adv_991_5(self):
        results = self.derivation.derive(word_b='рядом', pos_b='adv', pos_a='adv')
        self.assertIn('рядышком', results)

    def test_adv_992(self):
        results = self.derivation.derive(word_b='вдалеке', pos_b='adv', pos_a='adv')
        self.assertIn('невдалеке', results)
        results = self.derivation.derive(word_b='хотя', pos_b='tgr', pos_a='adv')
        self.assertIn('нехотя', results)

    @unittest.skip
    def test_adv_993(self):
        results = self.derivation.derive(word_b='вне', pos_b='adv', pos_a='adv')
        self.assertIn('вовне', results)

    @unittest.skip
    def test_adv_993_2(self):
        results = self.derivation.derive(word_b='светло', pos_b='adv', pos_a='adv')
        self.assertIn('засветло', results)

    @unittest.skip
    def test_adv_993_3(self):
        results = self.derivation.derive(word_b='сюда', pos_b='adv', pos_a='adv')
        self.assertIn('досюда', results)

    @unittest.skip
    def test_adv_993_4(self):
        results = self.derivation.derive(word_b='всегда', pos_b='adv', pos_a='adv')
        self.assertIn('навсегда', results)

    @unittest.skip
    def test_adv_993_5(self):
        results = self.derivation.derive(word_b='всюду', pos_b='adv', pos_a='adv')
        self.assertIn('повсюду', results)

    @unittest.skip
    def test_adv_993_6(self):
        results = self.derivation.derive(word_b='куда', pos_b='adv', pos_a='adv')
        self.assertIn('откуда', results)
        results = self.derivation.derive(word_b='всюду', pos_b='adv', pos_a='adv')
        self.assertIn('отовсюду', results)

    @unittest.skip
    def test_adv_993_7(self):
        results = self.derivation.derive(word_b='даром', pos_b='adv', pos_a='adv')
        self.assertIn('задаром', results)

    @unittest.skip
    def test_adv_993_8(self):
        results = self.derivation.derive(word_b='завтра', pos_b='adv', pos_a='adv')
        self.assertIn('назавтра', results)

    @unittest.skip
    def test_adv_993_9(self):
        results = self.derivation.derive(word_b='вне', pos_b='adv', pos_a='adv')
        self.assertIn('извне', results)

    @unittest.skip
    def test_adv_993_10(self):
        results = self.derivation.derive(word_b='выше', pos_b='adv', pos_a='adv')
        self.assertIn('свыше', results)

    @unittest.skip
    def test_adv_993_11(self):
        results = self.derivation.derive(word_b='завтра', pos_b='adv', pos_a='adv')
        self.assertIn('послезавтра', results)

    @unittest.skip
    def test_adv_993_12(self):
        results = self.derivation.derive(word_b='вчера', pos_b='adv', pos_a='adv')
        self.assertIn('позавчера', results)
    def test_adv_994_1(self):
        results = self.derivation.derive(word_b='прежний', pos_b='adj', pos_a='adv')
        self.assertIn('по-прежнему', results)
        results = self.derivation.derive(word_b='деловой', pos_b='adj', pos_a='adv')
        self.assertIn('по-деловому', results)
        results = self.derivation.derive(word_b='хороший', pos_b='adj', pos_a='adv')
        self.assertIn('по-хорошему', results)

    def test_adv_994_2(self):
        results = self.derivation.derive(word_b='птичий', pos_b='adj', pos_a='adv')
        self.assertIn('по-птичьему', results)

    def test_adv_994_3(self):
        results = self.derivation.derive(word_b='мамин', pos_b='adj1', pos_a='adv')
        self.assertIn('по-маминому', results)
        results = self.derivation.derive(word_b='наш', pos_b='adj1', pos_a='adv')
        self.assertIn('по-нашему', results)
        results = self.derivation.derive(word_b='твой', pos_b='adj1', pos_a='adv')
        self.assertIn('по-твоему', results)

    @unittest.skip
    def test_adv_994_4(self):
        results = self.derivation.derive(word_b='его', pos_b='adj3', pos_a='adv')
        self.assertIn('по-его', results)
        results = self.derivation.derive(word_b='ее', pos_b='adj3', pos_a='adv')
        self.assertIn('по-ее', results)


    def test_adv_995(self):
        results = self.derivation.derive(word_b='дружеский', pos_b='adj', pos_a='adv')
        self.assertIn('по-дружески', results)
        results = self.derivation.derive(word_b='бабий', pos_b='adj', pos_a='adv')
        self.assertIn('по-бабьи', results)
        results = self.derivation.derive(word_b='охотничий', pos_b='adj', pos_a='adv')
        self.assertIn('по-охотничьи', results)
        results = self.derivation.derive(word_b='свойский', pos_b='adj', pos_a='adv')
        self.assertIn('по-свойски', results)

    @unittest.skip
    def test_adv_996(self):
        results = self.derivation.derive(word_b='напрасный', pos_b='adj', pos_a='adv')
        self.assertIn('понапрасну', results)
        results = self.derivation.derive(word_b='сухой', pos_b='adj', pos_a='adv')
        self.assertIn('посуху', results)

    @unittest.skip
    def test_adv_997(self):
        results = self.derivation.derive(word_b='маленький', pos_b='adj', pos_a='adv')
        self.assertIn('помаленьку', results)
        results = self.derivation.derive(word_b='легонький', pos_b='adj', pos_a='adv')
        self.assertIn('полегоньку', results)
        results = self.derivation.derive(word_b='тихонький', pos_b='adj', pos_a='adv')
        self.assertIn('потихоньку', results)

    def test_adv_998(self):
        results = self.derivation.derive(word_b='новый', pos_b='adj', pos_a='adv')
        self.assertIn('по-новой', results)

    def test_adv_999(self):
        results = self.derivation.derive(word_b='плотный', pos_b='adj', pos_a='adv')
        self.assertIn('вплотную', results)
        results = self.derivation.derive(word_b='пеший', pos_b='adj', pos_a='adv')
        self.assertIn('впешую', results)
  

    @unittest.skip
    def test_adv_1000(self):
        results = self.derivation.derive(word_b='живой', pos_b='adj', pos_a='adv')
        self.assertIn('вживе', results)
        results = self.derivation.derive(word_b='краткий', pos_b='adj', pos_a='adv')
        self.assertIn('вкратце', results)
        results = self.derivation.derive(word_b='явный', pos_b='adj', pos_a='adv')
        self.assertIn('въяве', results)
        results = self.derivation.derive(word_b='общий', pos_b='adj', pos_a='adv')
        self.assertIn('вообще', results)

    @unittest.skip
    def test_adv_1000_2(self):
        results = self.derivation.derive(word_b='близкий', pos_b='adj', pos_a='adv')
        self.assertIn('вблизи', results)
        results = self.derivation.derive(word_b='запертый', pos_b='adj', pos_a='adv')
        self.assertIn('взаперти', results)

    @unittest.skip
    def test_adv_1000_3(self):
        results = self.derivation.derive(word_b='правый', pos_b='adj', pos_a='adv')
        self.assertIn('вправо', results)
        results = self.derivation.derive(word_b='левый', pos_b='adj', pos_a='adv')
        self.assertIn('влево', results)

    @unittest.skip
    def test_adv_1000_4(self):
        results = self.derivation.derive(word_b='третий', pos_b='adj4', pos_a='adv')
        self.assertIn('в-третьих', results)
        results = self.derivation.derive(word_b='десятый', pos_b='adj4', pos_a='adv')
        self.assertIn('в-десятых', results)

    @unittest.skip
    def test_adv_1000_5(self):
        results = self.derivation.derive(word_b='второй', pos_b='adj4', pos_a='adv')
        self.assertIn('во-вторых', results)
        results = self.derivation.derive(word_b='первый', pos_b='adj4', pos_a='adv')
        self.assertIn('во-первых', results)

    def test_adv_1001(self):
        results = self.derivation.derive(word_b='белый', pos_b='adj', pos_a='adv')
        self.assertIn('добела', results)
        results = self.derivation.derive(word_b='сухой', pos_b='adj', pos_a='adv')
        self.assertIn('досуха', results)
        results = self.derivation.derive(word_b='синий', pos_b='adj', pos_a='adv')
        self.assertIn('досиня', results)

    @unittest.skip
    def test_adv_1002(self):
        results = self.derivation.derive(word_b='живой', pos_b='adj', pos_a='adv')
        self.assertIn('заживо', results)
        results = self.derivation.derive(word_b='единый', pos_b='adj', pos_a='adv')
        self.assertIn('заодно', results)


    def test_adv_1003(self):
        results = self.derivation.derive(word_b='желтый', pos_b='adj', pos_a='adv')
        self.assertIn('изжелта', results)
        results = self.derivation.derive(word_b='синий', pos_b='adj', pos_a='adv')
        self.assertIn('иссиня', results)
        results = self.derivation.derive(word_b='чужой', pos_b='adj', pos_a='adv')
        self.assertIn('исчужа', results)
        results = self.derivation.derive(word_b='далекий', pos_b='adj', pos_a='adv')
        self.assertIn('издалека', results)

    def test_adv_1004(self):
        results = self.derivation.derive(word_b='грубый', pos_b='adj', pos_a='adv')
        self.assertIn('нагрубо', results)
        results = self.derivation.derive(word_b='глухой', pos_b='adj', pos_a='adv')
        self.assertIn('наглухо', results)
        results = self.derivation.derive(word_b='долгий', pos_b='adj', pos_a='adv')
        self.assertIn('надолго', results)

    
    @unittest.skip
    def test_adv_1005(self):
        results = self.derivation.derive(word_b='веселый', pos_b='adj', pos_a='adv')
        self.assertIn('навеселе', results)

    @unittest.skip
    def test_adv_1005_2(self):
        results = self.derivation.derive(word_b='чистый', pos_b='adj', pos_a='adv')
        self.assertIn('начистую', results)

    @unittest.skip
    def test_adv_1006(self):
        results = self.derivation.derive(word_b='полный', pos_b='adj', pos_a='adv')
        self.assertIn('сполна', results)
        results = self.derivation.derive(word_b='легкий', pos_b='adj', pos_a='adv')
        self.assertIn('слегка', results)
        results = self.derivation.derive(word_b='!общий', pos_b='adj', pos_a='adv')
        self.assertIn('сообща', results)
        results = self.derivation.derive(word_b='горячий', pos_b='adj', pos_a='adv')
        self.assertIn('сгоряча', results)

    @unittest.skip
    def test_adv_1006_2(self):
        results = self.derivation.derive(word_b='молодой', pos_b='adj', pos_a='adv')
        self.assertIn('смолоду', results)
        results = self.derivation.derive(word_b='дурной', pos_b='adj', pos_a='adv')
        self.assertIn('сдуру', results)
        results = self.derivation.derive(word_b='слепой', pos_b='adj', pos_a='adv')
        self.assertIn('сослепу', results)

    @unittest.skip
    def test_adv_1007(self):
        results = self.derivation.derive(word_b='новый', pos_b='adj', pos_a='adv')
        self.assertIn('сызнова', results)
        results = self.derivation.derive(word_b='давний', pos_b='adj', pos_a='adv')
        self.assertIn('сыздавна', results)

    @unittest.skip
    def test_adv_1008_1(self):
        results = self.derivation.derive(word_b='горячий', pos_b='adj', pos_a='adv')
        self.assertIn('вгорячах', results)

    @unittest.skip
    def test_adv_1008_2(self):
        results = self.derivation.derive(word_b='первый', pos_b='adj4', pos_a='adv')
        self.assertIn('впервой', results)

    @unittest.skip
    def test_adv_1008_3(self):
        results = self.derivation.derive(word_b='первый', pos_b='adj4', pos_a='adv')
        self.assertIn('впервые', results)

    @unittest.skip
    def test_adv_1008_4(self):
        results = self.derivation.derive(word_b='единый', pos_b='adj', pos_a='adv')
        self.assertIn('воедино', results)

    @unittest.skip
    def test_adv_1008_5(self):
        results = self.derivation.derive(word_b='частый', pos_b='adj', pos_a='adv')
        self.assertIn('зачастую', results)

    @unittest.skip
    def test_adv_1008_6(self):
        results = self.derivation.derive(word_b='панибратский', pos_b='adj', pos_a='adv')
        self.assertIn('запанибрата', results)

    @unittest.skip
    def test_adv_1008_7(self):
        results = self.derivation.derive(word_b='древлий', pos_b='adj', pos_a='adv')
        self.assertIn('издревле', results)

    @unittest.skip
    def test_adv_1008_8(self):
        results = self.derivation.derive(word_b='старый', pos_b='adj', pos_a='adv')
        self.assertIn('исстари', results)

    @unittest.skip
    def test_adv_1008_9(self):
        results = self.derivation.derive(word_b='верный', pos_b='adj', pos_a='adv')
        self.assertIn('наверное', results)

    @unittest.skip
    def test_adv_1008_10(self):
        results = self.derivation.derive(word_b='верный', pos_b='adj', pos_a='adv')
        self.assertIn('наверняка', results)

    @unittest.skip
    def test_adv_1008_11(self):
        results = self.derivation.derive(word_b='прямой', pos_b='adj', pos_a='adv')
        self.assertIn('напрямик', results)
        results = self.derivation.derive(word_b='косой', pos_b='adj', pos_a='adv')
        self.assertIn('наискосок', results)

    @unittest.skip
    def test_adv_1008_12(self):
        results = self.derivation.derive(word_b='прямой', pos_b='adj', pos_a='adv')
        self.assertIn('напрямки', results)
        results = self.derivation.derive(word_b='косой', pos_b='adj', pos_a='adv')
        self.assertIn('наискоски', results)

    @unittest.skip
    def test_adv_1008_13(self):
        results = self.derivation.derive(word_b='далекий', pos_b='adj', pos_a='adv')
        self.assertIn('неподалёку', results)

    @unittest.skip
    def test_adv_1008_14(self):
        results = self.derivation.derive(word_b='чистый', pos_b='adj', pos_a='adv')
        self.assertIn('подчистую', results)

    @unittest.skip
    def test_adv_1008_15(self):
        results = self.derivation.derive(word_b='малый', pos_b='adj', pos_a='adv')
        self.assertIn('сызмальства', results)

    @unittest.skip
    def test_adv_1008_16(self):
        results = self.derivation.derive(word_b='тихий', pos_b='adj', pos_a='adv')
        self.assertIn('исподтишка', results)

    def test_adv_1009(self):
        results = self.derivation.derive(word_b='низ', pos_b='noun', pos_a='adv')
        self.assertIn('вниз', results)
        results = self.derivation.derive(word_b='даль', pos_b='noun', pos_a='adv')
        self.assertIn('вдаль', results)
        results = self.derivation.derive(word_b='разнобой', pos_b='noun', pos_a='adv')
        self.assertIn('вразнобой', results)
        results = self.derivation.derive(word_b='правда', pos_b='noun', pos_a='adv')
        self.assertIn('вправду', results)
        results = self.derivation.derive(word_b='ничья', pos_b='noun', pos_a='adv')
        self.assertIn('вничью', results)
        results = self.derivation.derive(word_b='истина', pos_b='noun', pos_a='adv')
        self.assertIn('воистину', results)
        results = self.derivation.derive(word_b='век', pos_b='noun', pos_a='adv')
        self.assertIn('вовек', results)
        results = self.derivation.derive(word_b='круг', pos_b='noun', pos_a='adv')
        self.assertIn('вокруг', results)


    def test_adv_1010(self):

        results = self.derivation.derive(word_b='верх', pos_b='noun', pos_a='adv')
        self.assertIn('наверх', results)
        results = self.derivation.derive(word_b='встреча', pos_b='noun', pos_a='adv')
        self.assertIn('навстречу', results)
        results = self.derivation.derive(word_b='конец', pos_b='noun', pos_a='adv')
        self.assertIn('наконец', results)

    @unittest.skip
    def test_adv_1011(self):

        results = self.derivation.derive(word_b='верх', pos_b='noun', pos_a='adv')
        self.assertIn('вверху', results)
        results = self.derivation.derive(word_b='начало', pos_b='noun', pos_a='adv')
        self.assertIn('вначале', results)
        results = self.derivation.derive(word_b='право', pos_b='noun', pos_a='adv')
        self.assertIn('вправе', results)
        results = self.derivation.derive(word_b='даль', pos_b='noun', pos_a='adv')
        self.assertIn('вдали', results)
        results = self.derivation.derive(word_b='последствие', pos_b='noun', pos_a='adv')
        self.assertIn('впоследствии', results)

    @unittest.skip
    def test_adv_1011_2(self):

        results = self.derivation.derive(word_b='заем', pos_b='noun', pos_a='adv')
        self.assertIn('взаймы', results)
        results = self.derivation.derive(word_b='наем', pos_b='noun', pos_a='adv')
        self.assertIn('внаймы', results)

    @unittest.skip
    def test_adv_1012(self):

        results = self.derivation.derive(word_b='верх', pos_b='noun', pos_a='adv')
        self.assertIn('наверху', results)
        results = self.derivation.derive(word_b='дни', pos_b='noun', pos_a='adv')
        self.assertIn('на днях', results)


    @unittest.skip
    def test_adv_1013(self):

        results = self.derivation.derive(word_b='утро', pos_b='noun', pos_a='adv')
        self.assertIn('поутру', results)
        results = self.derivation.derive(word_b='середина', pos_b='noun', pos_a='adv')
        self.assertIn('посредине', results)
        results = self.derivation.derive(word_b='близость', pos_b='noun', pos_a='adv')
        self.assertIn('поблизости', results)

    @unittest.skip
    def test_adv_1014(self):

        results = self.derivation.derive(word_b='низ', pos_b='noun', pos_a='adv')
        self.assertIn('донизу', results)
        results = self.derivation.derive(word_b='зарез', pos_b='noun', pos_a='adv')
        self.assertIn('до зарезу', results)

    @unittest.skip
    def test_adv_1015_1(self):

        results = self.derivation.derive(word_b='бок', pos_b='noun', pos_a='adv')
        self.assertIn('сбоку', results)

    @unittest.skip
    def test_adv_1015_2(self):

        results = self.derivation.derive(word_b='разбег', pos_b='noun', pos_a='adv')
        self.assertIn('с разбегу', results)
        results = self.derivation.derive(word_b='поворот', pos_b='noun', pos_a='adv')
        self.assertIn('с поворота', results)

    @unittest.skip
    def test_adv_1015_3(self):

        results = self.derivation.derive(word_b='перед', pos_b='noun', pos_a='adv')
        self.assertIn('спереди', results)
        results = self.derivation.derive(word_b='зад', pos_b='noun', pos_a='adv')
        self.assertIn('сзади', results)

    @unittest.skip
    def test_adv_1016_1(self):
        results = self.derivation.derive(word_b='верх', pos_b='noun', pos_a='adv')
        self.assertIn('кверху', results)
        results = self.derivation.derive(word_b='низ', pos_b='noun', pos_a='adv')
        self.assertIn('книзу', results)

    @unittest.skip
    def test_adv_1016_2(self):
        results = self.derivation.derive(word_b='перед', pos_b='noun', pos_a='adv')
        self.assertIn('впереди', results)

    @unittest.skip
    def test_adv_1016_3(self):
        results = self.derivation.derive(word_b='зад', pos_b='noun', pos_a='adv')
        self.assertIn('позади', results)

    @unittest.skip
    def test_adv_1016_4(self):
        results = self.derivation.derive(word_b='даль', pos_b='noun', pos_a='adv')
        self.assertIn('издали', results)

    @unittest.skip
    def test_adv_1016_5(self):
        results = self.derivation.derive(word_b='часть', pos_b='noun', pos_a='adv')
        self.assertIn('отчасти', results)

    @unittest.skip
    def test_adv_1016_6(self):
        results = self.derivation.derive(word_b='утро', pos_b='noun', pos_a='adv')
        self.assertIn('наутро', results)

    @unittest.skip
    def test_adv_1016_7(self):
        results = self.derivation.derive(word_b='муж', pos_b='noun', pos_a='adv')
        self.assertIn('замужем', results)

    @unittest.skip
    def test_adv_1016_8(self):
        results = self.derivation.derive(word_b='детство', pos_b='noun', pos_a='adv')
        self.assertIn('сыздетства', results)

    @unittest.skip
    def test_adv_1017(self):
        results = self.derivation.derive(word_b='двое', pos_b='num1', pos_a='adv')
        self.assertIn('вдвоём', results)
        results = self.derivation.derive(word_b='четверо', pos_b='num1', pos_a='adv')
        self.assertIn('вчетвером', results)

    @unittest.skip
    def test_adv_1018(self):
        results = self.derivation.derive(word_b='двое', pos_b='num1', pos_a='adv')
        self.assertIn('вдвое', results)
        results = self.derivation.derive(word_b='пятеро', pos_b='num1', pos_a='adv')
        self.assertIn('впятеро', results)

    @unittest.skip
    def test_adv_1019(self):
        results = self.derivation.derive(word_b='двое', pos_b='num1', pos_a='adv')
        self.assertIn('надвое', results)
        results = self.derivation.derive(word_b='трое', pos_b='num1', pos_a='adv')
        self.assertIn('натрое', results)

    @unittest.skip
    def test_adv_1019_2(self):
        results = self.derivation.derive(word_b='сколько', pos_b='num', pos_a='adv')
        self.assertIn('насколько', results)
        results = self.derivation.derive(word_b='много', pos_b='num', pos_a='adv')
        self.assertIn('намного', results)

    def test_adv_1020(self):
        results = self.derivation.derive(word_b='догонять', pos_b='verb', pos_a='adv')
        self.assertIn('вдогонку', results)
        results = self.derivation.derive(word_b='приглядывать', pos_b='verb', pos_a='adv')
        self.assertIn('вприглядку', results)
        results = self.derivation.derive(word_b='распахивать', pos_b='verb', pos_a='adv')
        self.assertIn('нараспашку', results)

    @unittest.skip
    def test_adv_1021_1(self):
        results = self.derivation.derive(word_b='торопиться', pos_b='verb', pos_a='adv')
        self.assertIn('второпях', results)
        results = self.derivation.derive(word_b='бегать', pos_b='verb', pos_a='adv')
        self.assertIn('в бегах', results)

    @unittest.skip
    def test_adv_1021_2(self):
        results = self.derivation.derive(word_b='висеть', pos_b='verb', pos_a='adv')
        self.assertIn('на весу', results)

    @unittest.skip
    def test_adv_1021_3(self):
        results = self.derivation.derive(word_b='просыпаться', pos_b='verb', pos_a='adv')
        self.assertIn('без просыпу', results)

    @unittest.skip
    def test_adv_1021_4(self):
        results = self.derivation.derive(word_b='упасть', pos_b='verb', pos_a='adv')
        self.assertIn('доупаду', results)
        results = self.derivation.derive(word_b='отвалиться', pos_b='verb', pos_a='adv')
        self.assertIn('до отвала', results)

    @unittest.skip
    def test_adv_1021_5(self):
        results = self.derivation.derive(word_b='родиться', pos_b='verb', pos_a='adv')
        self.assertIn('сроду', results)
        results = self.derivation.derive(word_b='рвать', pos_b='verb', pos_a='adv')
        self.assertIn('срыву', results)

    @unittest.skip
    def test_adv_1021_6(self):
        results = self.derivation.derive(word_b='родиться', pos_b='verb', pos_a='adv')
        self.assertIn('отроду', results)

    @unittest.skip
    def test_adv_1021_7(self):
        results = self.derivation.derive(word_b='перегонять', pos_b='verb', pos_a='adv')
        self.assertIn('вперегонки', results)

    @unittest.skip
    def test_adv_1021_8(self):
        results = self.derivation.derive(word_b='перегонять', pos_b='verb', pos_a='adv')
        self.assertIn('наперегонки', results)

    @unittest.skip
    def test_adv_1021_9(self):
        results = self.derivation.derive(word_b='проснуться', pos_b='verb', pos_a='adv')
        self.assertIn('впросонках', results)

    @unittest.skip
    def test_adv_1021_10(self):
        results = self.derivation.derive(word_b='проснуться', pos_b='verb', pos_a='adv')
        self.assertIn('спросонок', results)

    @unittest.skip
    def test_adv_1021_11(self):
        results = self.derivation.derive(word_b='проснуться', pos_b='verb', pos_a='adv')
        self.assertIn('спросонья', results)

    @unittest.skip
    def test_adv_1021_12(self):
        results = self.derivation.derive(word_b='мочь', pos_b='verb', pos_a='adv')
        self.assertIn('невмоготу', results)

    @unittest.skip
    def test_adv_1021_13(self):
        results = self.derivation.derive(word_b='удаться', pos_b='verb', pos_a='adv')
        self.assertIn('наудалую', results)

    @unittest.skip
    def test_adv_1021_14(self):
        results = self.derivation.derive(word_b='перекосить', pos_b='verb', pos_a='adv')
        self.assertIn('наперекосяк', results)

    @unittest.skip
    def test_adv_1022(self):
        results = self.derivation.derive(word_b='долгий', pos_b='adj', pos_a='adv')
        self.assertIn('подолгу', results)

    @unittest.skip
    def test_adv_1022_2(self):
        results = self.derivation.derive(word_b='нарочно', pos_b='adv', pos_a='adv')
        self.assertIn('понарошку', results)

    @unittest.skip
    def test_adv_1023(self):
        results = self.derivation.derive(word_b='косой', pos_b='adj', pos_a='adv')
        self.assertIn('вкось', results)
        results = self.derivation.derive(word_b='довольный', pos_b='adj', pos_a='adv')
        self.assertIn('вдоволь', results)
        results = self.derivation.derive(word_b='ровный', pos_b='adj', pos_a='adv')
        self.assertIn('вровень', results)

    def test_adv_1024(self):
        results = self.derivation.derive(word_b='догонять', pos_b='verb', pos_a='adv')
        self.assertIn('вдогон', results)
        # results = self.derivation.derive(word_b='перебивать', pos_b='verb', pos_a='adv')
        # self.assertIn('вперебой', results)
        results = self.derivation.derive(word_b='плавать', pos_b='verb', pos_a='adv')
        self.assertIn('вплавь', results)
        results = self.derivation.derive(word_b='скакать', pos_b='verb', pos_a='adv')
        self.assertIn('вскачь', results)

    @unittest.skip
    def test_adv_1024_2(self):
        results = self.derivation.derive(word_b='перечесть', pos_b='verb', pos_a='adv')
        self.assertIn('наперечет', results)
        results = self.derivation.derive(word_b='прерывать', pos_b='verb', pos_a='adv')
        self.assertIn('наперерыв', results)
        results = self.derivation.derive(word_b='выворачивать', pos_b='verb', pos_a='adv')
        self.assertIn('навыворот', results)
        results = self.derivation.derive(word_b='ощупать', pos_b='verb', pos_a='adv')
        self.assertIn('наощупь', results)

    @unittest.skip
    def test_adv_1025_1(self):
        results = self.derivation.derive(word_b='проворачивать', pos_b='verb', pos_a='adv')
        self.assertIn('невпроворот', results)
        results = self.derivation.derive(word_b='догадываться', pos_b='verb', pos_a='adv')
        self.assertIn('невдогад', results)

    @unittest.skip
    def test_adv_1025_2(self):
        results = self.derivation.derive(word_b='терпеть', pos_b='verb', pos_a='adv')
        self.assertIn('невтерпёж', results)
        results = self.derivation.derive(word_b='мочь', pos_b='verb', pos_a='adv')
        self.assertIn('невмочь', results)

    @unittest.skip
    def test_adv_1025_3(self):
        results = self.derivation.derive(word_b='голодать', pos_b='verb', pos_a='adv')
        self.assertIn('впроголодь', results)

    @unittest.skip
    def test_adv_1025_4(self):
        results = self.derivation.derive(word_b='отиахиваться', pos_b='verb', pos_a='adv')
        self.assertIn('наотмашь', results)

    @unittest.skip
    def test_adv_1025_5(self):
        results = self.derivation.derive(word_b='косить', pos_b='verb', pos_a='adv')
        self.assertIn('наискось', results)

    @unittest.skip
    def test_adv_1025_6(self):
        results = self.derivation.derive(word_b='земля', pos_b='noun', pos_a='adv')
        self.assertIn('наземь', results)

    @unittest.skip
    def test_adv_1025_7(self):
        results = self.derivation.derive(word_b='муж', pos_b='noun', pos_a='adv')
        self.assertIn('замуж', results)
        results = self.derivation.derive(word_b='раз', pos_b='noun', pos_a='adv')
        self.assertIn('зараз', results)

    @unittest.skip
    def test_adv_1025_8(self):
        results = self.derivation.derive(word_b='бок', pos_b='noun', pos_a='adv')
        self.assertIn('обок', results)

    @unittest.skip
    def test_adv_1025_9(self):
        results = self.derivation.derive(word_b='верх', pos_b='noun', pos_a='adv')
        self.assertIn('поверх', results)

    @unittest.skip
    def test_adv_1025_10(self):
        results = self.derivation.derive(word_b='зарезать', pos_b='verb', pos_a='adv')
        self.assertIn('позарез', results)

    @unittest.skip
    def test_adv_1025_11(self):
        results = self.derivation.derive(word_b='запас', pos_b='noun', pos_a='adv')
        self.assertIn('про запас', results)


if __name__ == '__main__':
    unittest.main(verbosity=2)
