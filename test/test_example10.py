import unittest
from ddt import ddt, data, unpackall


@ddt
class FooTestCase(unittest.TestCase):

    @unpackall
    @data(
        empty_string=[[], ""],
        only_spaces=[[], "   "],
        two_words=[["ab", "cd"], "  ab  cd  "],
        three_words=[["ab", "cd", "ef"], "ab  cd ef"],
    )
    @data(
        no_options=[],
        with_sep_None=[None],
        with_sep_None_maxsplit_neg1=[None, -1],
    )
    def test_decorated(self, result, value, *args):
        self.assertEqual(value.split(*args), result)
