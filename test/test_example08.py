import unittest
from ddt import ddt, data


@ddt
class FooTestCase(unittest.TestCase):

    @data("a", "_", "B", "1")
    @data("b", "*", "X", "2", "")
    def test_decorated(self, a, b):
        self.assertEqual((a + b).lower(), a.lower() + b.lower())
