
import unittest
from ddt import ddt, data, unpack
from test.mycode import larger_than_two


@ddt
class FooTestCase(unittest.TestCase):

    @unpack
    @data(
        neg1={"value": -1, "result": False},
        zero={"value": 0, "result": False},
        pos2={"value": 2, "result": False},
        pos3={"value": 3, "result": True},
    )
    def test_decorated(self, value, result):
        self.assertEqual(larger_than_two(value), result)
