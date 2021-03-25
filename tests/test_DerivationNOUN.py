import unittest

from src.Derivation import Derivation


class TestDerivation(unittest.TestCase):
    def setUp(self):
        self.derivation = Derivation()

    def tearDown(self):
        del self.derivation


if __name__ == '__main__':
    unittest.main(verbosity=2)
