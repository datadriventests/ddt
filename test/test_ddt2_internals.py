
from unittest import TestCase

import ddt


class TestMakeParamsName(TestCase):

    def test__unnamed_int(self):
        self.assertEqual(ddt.make_params_name(3, None, 4), '3_4')

    def test__named_int(self):
        self.assertEqual(ddt.make_params_name(3, 'myint', 4), '3_myint')

    def test__unnamed_string(self):
        self.assertEqual(ddt.make_params_name(3, None, 'a'), '3_a')

    def test__named_string(self):
        self.assertEqual(
            ddt.make_params_name(3, 'mystring', 'a'),
            '3_mystring'
        )

    def test__unnamed_array_of_strings(self):
        self.assertEqual(ddt.make_params_name(3, None, ['a', 'b']), '3_a_b')

    def test__named_array_of_strings(self):
        self.assertEqual(
            ddt.make_params_name(3, 'myarray', ['a', 'b']),
            '3_myarray'
        )

    def test__unnamed_complex_type(self):
        if ddt.is_hash_randomized():
            self.assertEqual(ddt.make_params_name(3, None, Exception()), '3')
        else:
            self.assertEqual(ddt.make_params_name(3, None, Exception()), '3_')

    def test__unnamed_value_with__name__attribute(self):
        class SampleInt(int):
            pass

        v = SampleInt(1)
        v.__name__ = 'custom name'

        self.assertEqual(ddt.make_params_name(3, None, v), '3_custom_name')

    def test__named_value_with__name__attribute(self):
        class SampleInt(int):
            pass

        v = SampleInt(1)
        v.__name__ = 'custom name'

        self.assertEqual(ddt.make_params_name(3, 'myint', v), '3_myint')
