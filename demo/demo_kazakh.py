from derivbase_ru.derivation import Derivation, TagGuesserWrapper

guesser = TagGuesserWrapper(lang="kaz")
derivation = Derivation(lang="kaz", guesser=guesser)

# g = guesser.guess(word="жазу", pos="verb")
# print(g)

res = derivation.derive(word_b="аласа", pos_b="adj", is_extended=True)
for k, vs in res.items():
    print(k, vs)
