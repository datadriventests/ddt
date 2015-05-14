
import unittest
from ddt import ddt, data
from test.mycode import larger_than_two


@ddt
class FooTestCase(unittest.TestCase):

    @data(
        [-1, False],
        [0, False],
        [2, False],
        [3, True]
    )
    def test_decorated(self, data):
        self.assertEqual(larger_than_two(data[0]), data[1])
