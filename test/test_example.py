import unittest
from ddt import ddt, data, file_data
from .mycode import larger_than_two, has_three_elements, is_a_greeting


class mylist(list):
    pass


def annotated(a, b):
    r = mylist([a, b])
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
