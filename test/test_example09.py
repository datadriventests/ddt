import unittest
from ddt import ddt, data, unpack


@ddt
class FooTestCase(unittest.TestCase):

    @unpack
    @data(
        no_options=[[]],
        with_sep_None=[[None]],
        with_sep_None_maxsplit_neg1=[[None, -1]],
    )
    @unpack
    @unpack
    @data(
        empty_string=[[""], {"result": []}],
        only_spaces=[["   "], {"result": []}],
        two_words=[["  ab  cd  "], {"result": ["ab", "cd"]}],
        three_words=[["ab  cd ef"], {"result": ["ab", "cd", "ef"]}],
    )
    def test_decorated(self, args, value, result=None):
        self.assertEqual(value.split(*args), result)
