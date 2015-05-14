
import unittest
from ddt import ddt, file_data, unpack
from test.mycode import larger_than_two


@ddt
class FooTestCase(unittest.TestCase):

    @unpack
    @unpack
    @file_data("json_list.json", encoding="ascii")
    def test_with_json_list(self, result, value, **kwargs):
        self.assertEqual(larger_than_two(value, **kwargs), result)

    @unpack
    @unpack
    @file_data("json_dict.json")
    def test_with_json_dict(self, result, value, **kwargs):
        self.assertEqual(larger_than_two(value, **kwargs), result)
