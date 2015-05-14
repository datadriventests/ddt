
import unittest
from ddt import ddt, data, unpack
from test.mycode import larger_than_two


@ddt
class FooTestCase(unittest.TestCase):

    @unpack
    @unpack
    @data(
        base2_10=[[False, "10"], {"base": 2}],
        base3_10=[[True, "10"], {"base": 3}],
        base10_10=[[True, "10"], {"base": 10}],
        default_10=[[True, "10"], {}],
    )
    def test_decorated(self, result, value, **kwargs):
        self.assertEqual(larger_than_two(value, **kwargs), result)
