import unittest
from ddt import ddt, data, file_data, unpack
from test.mycode import larger_than_two, has_three_elements, is_a_greeting


class Mylist(list):
    pass


def annotated(a, b):
    r = Mylist([a, b])
    setattr(r, "__name__", "test_%d_greater_than_%d" % (a, b))
    return r


@ddt
class FooTestCase(unittest.TestCase):
    def test_undecorated(self):
        self.assertTrue(larger_than_two(24))

    @data(3, 4, 12, 23)
    def test_larger_than_two(self, value):
        self.assertTrue(larger_than_two(value))

    @data(1, -3, 2, 0)
    def test_not_larger_than_two(self, value):
        self.assertFalse(larger_than_two(value))

    @data(annotated(2, 1), annotated(10, 5))
    def test_greater(self, value):
        a, b = value
        self.assertGreater(a, b)

    @file_data('test_data_dict.json')
    def test_file_data_dict(self, value):
        self.assertTrue(has_three_elements(value))

    @file_data('test_data_list.json')
    def test_file_data_list(self, value):
        self.assertTrue(is_a_greeting(value))

    @data((3, 2), (4, 3), (5, 3))
    @unpack
    def test_tuples_extracted_into_arguments(self, first_value, second_value):
        self.assertTrue(first_value > second_value)

    @data([3, 2], [4, 3], [5, 3])
    @unpack
    def test_list_extracted_into_arguments(self, first_value, second_value):
        self.assertTrue(first_value > second_value)

    @unpack
    @data({'first': 1, 'second': 3, 'third': 2},
          {'first': 4, 'second': 6, 'third': 5})
    def test_dicts_extracted_into_kwargs(self, first, second, third):
        self.assertTrue(first < third < second)

    @data(1, 2, 3)
    @data(4, 5, 6)
    @data(7, 8, 9)
    def test_products(self, first_value, second_value, third_value):
        self.assertTrue(first_value < second_value < third_value)

    @unpack
    @data({'first': 1}, {'first': 2}, {'first': 3})
    @data(
        {'second': 4, 'third': 5},
        {'second': 5, 'third': 6},
        {'second': 6, 'third': 7}
    )
    def test_dict_products(self, first, second, third):
        self.assertTrue(first < second < third)

    @unpack
    @data([1], [2], [3])
    @data((4, 5), (5, 6), (6, 7))
    def test_list_products(self, first, second, third):
        self.assertTrue(first < second < third)

    @data(u'ascii', u'non-ascii-\N{SNOWMAN}')
    def test_unicode(self, value):
        self.assertIn(value, (u'ascii', u'non-ascii-\N{SNOWMAN}'))
