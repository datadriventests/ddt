
import unittest
from ddt import ddt, data
from test.mycode import larger_than_two


@ddt
class FooTestCase(unittest.TestCase):

    @data(
        neg1=[-1, False],
        zero=[0, False],
        pos2=[2, False],
        pos3=[3, True],
    )
    def test_decorated(self, data):
        self.assertEqual(larger_than_two(data[0]), data[1])
