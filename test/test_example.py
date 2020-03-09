import unittest

from ddt import ddt, data, file_data, unpack
from test.mycode import larger_than_two, has_three_elements, is_a_greeting

try:
    import yaml
except ImportError:  # pragma: no cover
    have_yaml_support = False
else:
    have_yaml_support = True

# A good-looking decorator
needs_yaml = unittest.skipUnless(
    have_yaml_support, "Need YAML to run this test"
)


class Mylist(list):
    pass


class MyClass:
    def __init__(self, **kwargs):
        for field, value in kwargs.items():
            setattr(self, field, value)

    def __eq__(self, other):
        return isinstance(other, dict) and vars(self) == other or \
               isinstance(other, MyClass) and vars(self) == vars(other)

    def __str__(self):
        return "TestObject %s" % vars(self)


def annotated(a, b):
    r = Mylist([a, b])
    setattr(r, "__name__", "test_%d_greater_than_%d" % (a, b))
    return r


def annotated2(listIn, name, docstring):
    r = Mylist(listIn)
    setattr(r, "__name__", name)
    setattr(r, "__doc__", docstring)
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

    @data(annotated2([2, 1], 'Test_case_1', """Test docstring 1"""),
          annotated2([10, 5], 'Test_case_2', """Test docstring 2"""))
    def test_greater_with_name_docstring(self, value):
        a, b = value
        self.assertGreater(a, b)
        self.assertIsNotNone(getattr(value, "__name__"))
        self.assertIsNotNone(getattr(value, "__doc__"))

    @file_data('data/test_data_dict_dict.json')
    def test_file_data_json_dict_dict(self, start, end, value):
        self.assertLess(start, end)
        self.assertLess(value, end)
        self.assertGreater(value, start)

    @file_data('data/test_data_dict.json')
    def test_file_data_json_dict(self, value):
        self.assertTrue(has_three_elements(value))

    @file_data('data/test_data_list.json')
    def test_file_data_json_list(self, value):
        self.assertTrue(is_a_greeting(value))

    @needs_yaml
    @file_data('data/test_data_dict_dict.yaml')
    def test_file_data_yaml_dict_dict(self, start, end, value):
        self.assertLess(start, end)
        self.assertLess(value, end)
        self.assertGreater(value, start)

    @needs_yaml
    @file_data('data/test_data_dict.yaml')
    def test_file_data_yaml_dict(self, value):
        self.assertTrue(has_three_elements(value))

    @needs_yaml
    @file_data('data/test_data_list.yaml')
    def test_file_data_yaml_list(self, value):
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

    @data(u'ascii', u'non-ascii-\N{SNOWMAN}')
    def test_unicode(self, value):
        self.assertIn(value, (u'ascii', u'non-ascii-\N{SNOWMAN}'))

    @data(3, 4, 12, 23)
    def test_larger_than_two_with_doc(self, value):
        """Larger than two with value {0}"""
        self.assertTrue(larger_than_two(value))

    @data(3, 4, 12, 23)
    def test_doc_missing_args(self, value):
        """Missing args with value {0} and {1}"""
        self.assertTrue(larger_than_two(value))

    @data(3, 4, 12, 23)
    def test_doc_missing_kargs(self, value):
        """Missing kargs with value {value} {value2}"""
        self.assertTrue(larger_than_two(value))

    @data([3, 2], [4, 3], [5, 3])
    @unpack
    def test_list_extracted_with_doc(self, first_value, second_value):
        """Extract into args with first value {} and second value {}"""
        self.assertTrue(first_value > second_value)


if have_yaml_support:
    # This test will only succeed if the execution context is from the ddt
    # directory. pyyaml cannot locate test.test_example.MyClass otherwise!

    @ddt
    class YamlOnlyTestCase(unittest.TestCase):
        @file_data('data/test_custom_yaml_loader.yaml', yaml.FullLoader)
        def test_custom_yaml_loader(self, instance, expected):
            """Test with yaml tags to create specific classes to compare"""
            self.assertEqual(expected, instance)
