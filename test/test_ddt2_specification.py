
from unittest import TestCase

import gc
import warnings
import six

import ddt


class TestDecorators(TestCase):

    def test__data_decor_adds_derived_tests_for_unnamed_values(self):

        @ddt.ddt
        class SampleTestCase(object):
            @ddt.data('a', 'b')
            def test(self, *args, **kwargs):
                return args, kwargs

        tc = SampleTestCase()

        args, kwargs = tc.test__0_a()
        self.assertEqual(args, ('a',))
        self.assertEqual(kwargs, {})

        args, kwargs = tc.test__1_b()
        self.assertEqual(args, ('b',))
        self.assertEqual(kwargs, {})

    def test__data_decor_adds_derived_tests_for_named_values(self):

        @ddt.ddt
        class SampleTestCase(object):
            @ddt.data(x='a', y='b')
            def test(self, *args, **kwargs):
                return args, kwargs

        tc = SampleTestCase()

        args, kwargs = tc.test__0_x()
        self.assertEqual(args, ('a',))
        self.assertEqual(kwargs, {})

        args, kwargs = tc.test__1_y()
        self.assertEqual(args, ('b',))
        self.assertEqual(kwargs, {})

    def test__data_decor_adds_derived_tests_for_combined_values(self):

        @ddt.ddt
        class SampleTestCase(object):
            @ddt.data('A', x='B')
            def test(self, *args, **kwargs):
                return args, kwargs

        tc = SampleTestCase()

        args, kwargs = tc.test__0_A()
        self.assertEqual(args, ('A',))
        self.assertEqual(kwargs, {})

        args, kwargs = tc.test__1_x()
        self.assertEqual(args, ('B',))
        self.assertEqual(kwargs, {})

    def test__unpack_unpacks_list_in_single_value_set(self):

        @ddt.ddt
        class SampleTestCase(object):
            @ddt.unpack
            @ddt.data(a=['A', 'B'])
            def test(self, *args, **kwargs):
                return args, kwargs

        tc = SampleTestCase()

        args, kwargs = tc.test__0_a()
        self.assertEqual(args, ('A', 'B'))
        self.assertEqual(kwargs, {})

    def test__unpack_unpacks_tuple_in_single_value_set(self):

        @ddt.ddt
        class SampleTestCase(object):
            @ddt.unpack
            @ddt.data(a=('A', 'B'))
            def test(self, *args, **kwargs):
                return args, kwargs

        tc = SampleTestCase()

        args, kwargs = tc.test__0_a()
        self.assertEqual(args, ('A', 'B'))
        self.assertEqual(kwargs, {})

    def test__unpack_preserves_scalar_in_single_value_set(self):

        @ddt.ddt
        class SampleTestCase(object):
            @ddt.unpack
            @ddt.data(a='A')
            def test(self, *args, **kwargs):
                return args, kwargs

        tc = SampleTestCase()

        args, kwargs = tc.test__0_a()
        self.assertEqual(args, ('A',))
        self.assertEqual(kwargs, {})

    def test__unpack_converts_dict_to_kwargs_in_single_value_set(self):

        @ddt.ddt
        class SampleTestCase(object):
            @ddt.unpack
            @ddt.data(a=dict(y='A', x='B'))
            def test(self, *args, **kwargs):
                return args, kwargs

        tc = SampleTestCase()

        args, kwargs = tc.test__0_a()
        self.assertEqual(args, ())
        self.assertEqual(kwargs, dict(x='B', y='A'))

    def test__nested_data_decorators_produce_cartesian_product(self):

        @ddt.ddt
        class SampleTestCase(object):
            @ddt.data('a', 'b')
            @ddt.data('c', 'd')
            @ddt.data('e')
            def test(self, *args, **kwargs):
                return args, kwargs

        tc = SampleTestCase()

        args, kwargs = tc.test__0_a__0_c__0_e()
        self.assertEqual(args, ('a', 'c', 'e'))
        self.assertEqual(kwargs, {})

        args, kwargs = tc.test__0_a__1_d__0_e()
        self.assertEqual(args, ('a', 'd', 'e'))
        self.assertEqual(kwargs, {})

        args, kwargs = tc.test__1_b__0_c__0_e()
        self.assertEqual(args, ('b', 'c', 'e'))
        self.assertEqual(kwargs, {})

        args, kwargs = tc.test__1_b__1_d__0_e()
        self.assertEqual(args, ('b', 'd', 'e'))
        self.assertEqual(kwargs, {})

    def test__unpack_unpacks_only_the_next_data_decorator(self):

        @ddt.ddt
        class SampleTestCase(object):
            @ddt.data(A=['a', 'b'])
            @ddt.unpack
            @ddt.data(B=['c', 'd'])
            @ddt.data(C=dict(x='e', y='f'))
            def test(self, *args, **kwargs):
                return args, kwargs

        tc = SampleTestCase()

        args, kwargs = tc.test__0_A__0_B__0_C()
        self.assertEqual(args, (['a', 'b'], 'c', 'd', dict(x='e', y='f')))
        self.assertEqual(kwargs, {})

    def test__multiple_unpack_decorators_unpack_nested_lists(self):

        @ddt.ddt
        class SampleTestCase(object):
            @ddt.data(A=['a', 'b'])
            @ddt.unpack
            @ddt.unpack
            @ddt.data(B=[('c', 'd')])
            @ddt.data(C=dict(x='e', y='f'))
            def test(self, *args, **kwargs):
                return args, kwargs

        tc = SampleTestCase()

        args, kwargs = tc.test__0_A__0_B__0_C()
        self.assertEqual(args, (['a', 'b'], 'c', 'd', dict(x='e', y='f')))
        self.assertEqual(kwargs, {})

    def test__multiple_unpack_decorators_are_idempotent_on_dicts(self):

        @ddt.ddt
        class SampleTestCase(object):
            @ddt.data(A=['a', 'b'])
            @ddt.unpack
            @ddt.unpack
            @ddt.data(B=dict(r='c', s='d'))
            @ddt.data(C=dict(x='e', y='f'))
            def test(self, *args, **kwargs):
                return args, kwargs

        tc = SampleTestCase()

        args, kwargs = tc.test__0_A__0_B__0_C()
        self.assertEqual(args, (['a', 'b'], dict(x='e', y='f')))
        self.assertEqual(kwargs, dict(r='c', s='d'))

    def test__multiple_unpacked_dicts_are_combined(self):

        @ddt.ddt
        class SampleTestCase(object):
            @ddt.data(A=dict(a=0, b=0))
            @ddt.unpack
            @ddt.data(B=dict(b=1, c=1))
            @ddt.unpack
            @ddt.unpack
            @ddt.data(C=[dict(c=2, d=2)])
            def test(self, *args, **kwargs):
                return args, kwargs

        tc = SampleTestCase()

        args, kwargs = tc.test__0_A__0_B__0_C()
        self.assertEqual(args, (dict(a=0, b=0),))
        self.assertEqual(kwargs, dict(b=1, c=2, d=2))

    def test__unpackall_unpacks_data_from_all_decorators(self):

        @ddt.ddt
        class SampleTestCase(object):
            @ddt.unpackall
            @ddt.data(A=['a', 'b'])
            @ddt.data(B=dict(a=0, b=0))
            @ddt.data(C=[dict(b=1, c=1)])
            @ddt.data(D=[['c', 'd']])
            def test(self, *args, **kwargs):
                return args, kwargs

        tc = SampleTestCase()

        args, kwargs = tc.test__0_A__0_B__0_C__0_D()
        self.assertEqual(args, ('a', 'b', dict(b=1, c=1), ['c', 'd']))
        self.assertEqual(kwargs, dict(a=0, b=0))

    def test__position_of_unpackall_does_not_matter(self):

        @ddt.ddt
        class SampleTestCase(object):
            @ddt.data(A=['a', 'b'])
            @ddt.data(B=dict(a=0, b=0))
            @ddt.data(C=[dict(b=1, c=1)])
            @ddt.data(D=[['c', 'd']])
            @ddt.unpackall
            def test(self, *args, **kwargs):
                return args, kwargs

        tc = SampleTestCase()

        args, kwargs = tc.test__0_A__0_B__0_C__0_D()
        self.assertEqual(args, ('a', 'b', dict(b=1, c=1), ['c', 'd']))
        self.assertEqual(kwargs, dict(a=0, b=0))

    def test__multiple_unpackall_decorators_unpack_nested_lists(self):

        @ddt.ddt
        class SampleTestCase(object):
            @ddt.unpackall
            @ddt.data(A=['a', 'b'])
            @ddt.data(B=dict(a=0, b=0))
            @ddt.data(C=[dict(b=1, c=1)])
            @ddt.data(D=[['c', 'd']])
            @ddt.unpackall
            def test(self, *args, **kwargs):
                return args, kwargs

        tc = SampleTestCase()

        args, kwargs = tc.test__0_A__0_B__0_C__0_D()
        self.assertEqual(args, ('a', 'b', 'c', 'd'))
        self.assertEqual(kwargs, dict(a=0, b=1, c=1))

    def test__unpack_and_unpackall_decorators_combine_as_expected(self):

        @ddt.ddt
        class SampleTestCase(object):
            @ddt.unpackall
            @ddt.data(A=[['a', 'b']])
            @ddt.data(B=[dict(a=0, b=0)])
            @ddt.unpack
            @ddt.data(C=[dict(b=1, c=1)])
            @ddt.unpack
            @ddt.data(D=[['c', 'd']])
            def test(self, *args, **kwargs):
                return args, kwargs

        tc = SampleTestCase()

        args, kwargs = tc.test__0_A__0_B__0_C__0_D()
        self.assertEqual(args, (['a', 'b'], dict(a=0, b=0), 'c', 'd'))
        self.assertEqual(kwargs, dict(b=1, c=1))

    def test__names_for_complex_values_are_generated_correctly(self):

        @ddt.ddt
        class SampleTestCase(object):
            @ddt.data(dict(a=0, b=0))
            def test(self, *args, **kwargs):
                return args, kwargs

        tc = SampleTestCase()

        if ddt.is_hash_randomized():
            args, kwargs = tc.test__0()
        else:
            try:
                args, kwargs = tc.test__0_a_0_b_0()
            except AttributeError:
                args, kwargs = tc.test__0_b_0_a_0()

        self.assertEqual(args, (dict(a=0, b=0),))
        self.assertEqual(kwargs, {})

    def test__test_name_uses__name__attribute_if_complex_value_has_it(self):

        class SampleInt(int):
            pass

        d1 = SampleInt(1)
        d1.__name__ = 'custom name'

        d2 = SampleInt(2)

        @ddt.ddt
        class SampleTestCase(object):
            @ddt.data(d1, d2)
            def test(self, *args, **kwargs):
                return args, kwargs

        tc = SampleTestCase()

        args, kwargs = tc.test__0_custom_name()
        self.assertEqual(args, (1,))
        self.assertEqual(kwargs, {})

        args, kwargs = tc.test__1_2()
        self.assertEqual(args, (2,))
        self.assertEqual(kwargs, {})

    def test__sequences_of_underscores_in_test_names_are_reduced_to_one(self):

        @ddt.ddt
        class SampleTestCase(object):
            @ddt.data(['a', 'b'])
            @ddt.data((1, 2))
            def test(self, *args, **kwargs):
                return args, kwargs

        tc = SampleTestCase()

        args, kwargs = tc.test__0_a_b__0_1_2()
        self.assertEqual(args, (['a', 'b'], (1, 2)))
        self.assertEqual(kwargs, {})

    def test__file_data_decor_adds_derived_tests_with_unnamed_values(self):

        @ddt.ddt
        class SampleTestCase(object):
            @ddt.file_data('test_data_list.json')
            def test(self, *args, **kwargs):
                return args, kwargs

        tc = SampleTestCase()

        args, kwargs = tc.test__0_Hello()
        self.assertEqual(args, ('Hello',))
        self.assertEqual(kwargs, {})

        args, kwargs = tc.test__1_Goodbye()
        self.assertEqual(args, ('Goodbye',))
        self.assertEqual(kwargs, {})

    def test__file_data_decor_adds_derived_tests_for_named_values(self):

        @ddt.ddt
        class SampleTestCase(object):
            @ddt.file_data('test_data_dict.json')
            def test(self, *args, **kwargs):
                return args, kwargs

        tc = SampleTestCase()

        args, kwargs = tc.test__0_sorted_list()
        self.assertEqual(args, ([15, 12, 50],))
        self.assertEqual(kwargs, {})

        args, kwargs = tc.test__1_unsorted_list()
        self.assertEqual(args, ([10, 12, 15],))
        self.assertEqual(kwargs, {})

    def test__unpack_works_for_file_data_decor_too(self):

        @ddt.ddt
        class SampleTestCase(object):
            @ddt.unpack
            @ddt.file_data('test_data_dict.json')
            def test(self, *args, **kwargs):
                return args, kwargs

        tc = SampleTestCase()

        args, kwargs = tc.test__0_sorted_list()
        self.assertEqual(args, (15, 12, 50))
        self.assertEqual(kwargs, {})

        args, kwargs = tc.test__1_unsorted_list()
        self.assertEqual(args, (10, 12, 15))
        self.assertEqual(kwargs, {})

    def test__file_data_decor_does_not_cause_resource_warning(self):
        # ResourceWarning does not exist in Python 2 (?)
        if six.PY3:
            # let's violate priniciples of PEP8 to become pep8-compliant :-(
            # works around F821 in Python2
            resource_warning = eval('ResourceWarning')
            with warnings.catch_warnings(record=True) as w:

                warnings.resetwarnings()  # clear all filters
                warnings.simplefilter('ignore')  # ignore all
                warnings.simplefilter('always', resource_warning)  # add filter

                @ddt.ddt
                class SampleTestCase(object):
                    @ddt.unpack
                    @ddt.file_data('test_data_dict.json')
                    def test(self, *args, **kwargs):
                        return args, kwargs

                tc = SampleTestCase()
                del tc

                gc.collect()

            self.assertEqual(list(w), [])

    def test__tests_with_file_data_raise_exceptions_on_file_not_found(self):
        @ddt.ddt
        class SampleTestCase(object):
            @ddt.file_data('test_no_such_file.json')
            @ddt.data('a', 'b')
            def test(self, *args, **kwargs):
                return args, kwargs

        tc = SampleTestCase()

        if six.PY2:
            with self.assertRaises(IOError):
                tc.test__IOError__0_a()

            with self.assertRaises(IOError):
                tc.test__IOError__1_b()

        if six.PY3:
            with self.assertRaises(IOError):
                tc.test__FileNotFoundError__0_a()

            with self.assertRaises(IOError):
                tc.test__FileNotFoundError__1_b()

    def test__tests_with_file_data_raise_exceptions_on_invalid_json(self):
        @ddt.ddt
        class SampleTestCase(object):
            @ddt.file_data('test_data_invalid.json')
            @ddt.data('a', 'b')
            def test(self, *args, **kwargs):
                return args, kwargs

        tc = SampleTestCase()

        with self.assertRaises(ValueError):
            tc.test__ValueError__0_a()

        with self.assertRaises(ValueError):
            tc.test__ValueError__1_b()

    def test__unpacking_is_safe_even_if_loading_file_data_fails(self):
        @ddt.ddt
        class SampleTestCase(object):
            @ddt.unpack
            @ddt.file_data('test_data_invalid.json')
            @ddt.data('a', 'b')
            @ddt.unpackall
            def test(self, *args, **kwargs):
                return args, kwargs

        tc = SampleTestCase()

        with self.assertRaises(ValueError):
            tc.test__ValueError__0_a()

        with self.assertRaises(ValueError):
            tc.test__ValueError__1_b()

    def test__file_data_supports_file_encoding(self):

        @ddt.ddt
        class SampleTestCase(object):
            @ddt.file_data('test_data_utf8sig.json', encoding='utf-8-sig')
            def test(self, *args, **kwargs):
                return args, kwargs

        tc = SampleTestCase()

        method_name = 'test__0_u0158' if six.PY2 else 'test__0_\u0158'
        self.assertTrue(hasattr(tc, method_name))
