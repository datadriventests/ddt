
from unittest import TestCase

import six

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


class TestParams(TestCase):

    def test__Params_has_name_attribute(self):
        p = ddt.Params('sample_parameters', [], {})
        self.assertEqual(p.name, 'sample_parameters')

    def test__Params_has_args_attribute(self):
        p = ddt.Params('p', ['a', 'b', 'c'], {})
        self.assertEqual(p.args, ['a', 'b', 'c'])

    def test__Params_has_kwargs_attribute(self):
        p = ddt.Params('p', [], dict(a=1, b=2, c=3))
        self.assertEqual(p.kwargs, dict(a=1, b=2, c=3))

    def test__ParamsFailure_has_name_attribute(self):
        reason = Exception()
        p = ddt.ParamsFailure('error', reason)
        self.assertEqual(p.name, 'error')

    def test__ParamsFailure_has_reason_attribute(self):
        reason = Exception()
        p = ddt.ParamsFailure('error', reason)
        self.assertEqual(p.reason, reason)

    def test__Params_unpack_unpacks_lists_in_args(self):
        p = ddt.Params('p', [['a', 'b'], ['c']], {})
        p.unpack()
        self.assertEqual(p.args, ['a', 'b', 'c'])

    def test__Params_unpack_unpacks_tuples_in_args(self):
        p = ddt.Params('p', [('a', 'b'), ('c',)], {})
        p.unpack()
        self.assertEqual(p.args, ['a', 'b', 'c'])

    def test__Params_unpack_unpacks_dicts_in_args(self):
        p = ddt.Params('p', [dict(a=1, b=1), dict(a=2, c=2)], dict(b=0, d=0))
        p.unpack()
        self.assertEqual(p.kwargs, dict(a=2, b=1, c=2, d=0))

    def test__Params_unpack_treats_scalars_in_args_as_singletons(self):
        p = ddt.Params(
            'p',
            [['a', 'b'], 'c', dict(b=1, c=1), dict(c=2, d=2)],
            dict(a=0, b=0)
        )
        p.unpack()
        self.assertEqual(p.args, ['a', 'b', 'c'])
        self.assertEqual(p.kwargs, dict(a=0, b=1, c=2, d=2))

    def test__Params_unpack_does_nothing_with_argument_0(self):
        p = ddt.Params(
            'p',
            [['a', 'b'], 'c', dict(b=1, c=1), dict(c=2, d=2)],
            dict(a=0, b=0)
        )
        p.unpack(0)

        self.assertEqual(
            p.args,
            [['a', 'b'], 'c', dict(b=1, c=1), dict(c=2, d=2)]
        )
        self.assertEqual(p.kwargs, dict(a=0, b=0))

    def test__Params_unpack_unpacks_two_levels_with_argument_2(self):
        p = ddt.Params(
            'p',
            [[['a', 'b']], [dict(b=1, c=1)], [[dict(c=2, d=2)]]],
            dict(a=0, b=0)
        )
        p.unpack(2)

        self.assertEqual(p.args, ['a', 'b', dict(c=2, d=2)])
        self.assertEqual(p.kwargs, dict(a=0, b=1, c=1))

    def test_Params_unpack_returns_self(self):
        p = ddt.Params('p', ['a', 'b'], dict(a=0, b=0))
        p1 = p.unpack()
        self.assertEqual(p, p1)

    def test__ParamsFailure_unpack_does_nothing(self):
        reason = Exception()
        p = ddt.ParamsFailure('error', reason)
        p.unpack()
        self.assertEqual(p.name, 'error')
        self.assertEqual(p.reason, reason)

    def test_ParamsFailure_unpack_returns_self(self):
        reason = Exception()
        p = ddt.ParamsFailure('error', reason)
        p1 = p.unpack()
        self.assertEqual(p, p1)

    def test__ParamsA_plus_ParamsB_is_ParamsAB(self):
        p1 = ddt.Params('p1', ['a', 'b'], dict(x=0, y=0))
        p2 = ddt.Params('p2', ['c', 'd'], dict(y=1, z=1))
        p = p1 + p2
        self.assertIsInstance(p, ddt.Params)
        self.assertEqual(p.name, 'p1__p2')
        self.assertEqual(p.args, ['a', 'b', 'c', 'd'])
        self.assertEqual(p.kwargs, dict(x=0, y=1, z=1))

    def test__Params_plus_ParamsFailure_is_ParamsFailure(self):
        reason = Exception()
        p1 = ddt.Params('p1', ['a', 'b'], dict(x=0, y=0))
        p2 = ddt.ParamsFailure('error', reason)
        p = p1 + p2
        self.assertIsInstance(p, ddt.ParamsFailure)
        self.assertEqual(p.name, 'p1__error')
        self.assertEqual(p.reason, reason)

    def test__ParamsFailure_plus_Params_is_ParamsFailure(self):
        reason = Exception()
        p1 = ddt.ParamsFailure('error', reason)
        p2 = ddt.Params('p2', ['a', 'b'], dict(x=0, y=0))
        p = p1 + p2
        self.assertIsInstance(p, ddt.ParamsFailure)
        self.assertEqual(p.name, 'error__p2')
        self.assertEqual(p.reason, reason)

    def test__ParamsFailureA_plus_ParamsFailureB_is_ParamsFailureA(self):
        reason1 = Exception("Reason 1")
        reason2 = Exception("Reason 2")
        p1 = ddt.ParamsFailure('error1', reason1)
        p2 = ddt.ParamsFailure('error2', reason2)
        p = p1 + p2
        self.assertIsInstance(p, ddt.ParamsFailure)
        self.assertEqual(p.name, 'error1__error2')
        self.assertEqual(p.reason, reason1)

    def test__combine_names__None_None(self):
        self.assertEqual(ddt.combine_names(None, None), None)

    def test__combine_names__None_value(self):
        self.assertEqual(ddt.combine_names(None, 'name2'), 'name2')

    def test__combine_names__value_None(self):
        self.assertEqual(ddt.combine_names('name1', None), 'name1')

    def test__combine_names__value_value(self):
        self.assertEqual(ddt.combine_names('name1', 'name2'), 'name1__name2')


class TestParamsSet(TestCase):

    def test__InlineParamsSet_generates_unnamed_and_named_Params(self):
        ps = ddt.InlineParamsSet('b', 'a', z='c', y='d')

        params = list(ps)
        names = ['0_b', '1_a', '2_y', '3_z']
        values = [['b'], ['a'], ['d'], ['c']]

        self.assertEqual(len(values), 4)
        for p, n, v in zip(params, names, values):
            self.assertIsInstance(p, ddt.Params)
            self.assertEqual(p.name, n)
            self.assertEqual(p.args, v)
            self.assertEqual(p.kwargs, {})

    def test__FileParamsSet_generates_unnamed_Params_from_list(self):
        ps = ddt.FileParamsSet('test_data_list.json')
        ps.use_class(self.__class__)

        params = list(ps)
        names = ['0_Hello', '1_Goodbye']
        values = [['Hello'], ['Goodbye']]

        self.assertEqual(len(values), 2)
        for p, n, v in zip(params, names, values):
            self.assertIsInstance(p, ddt.Params)
            self.assertEqual(p.name, n)
            self.assertEqual(p.args, v)
            self.assertEqual(p.kwargs, {})

    def test__FileParamsSet_generates_named_Params_from_dict(self):
        ps = ddt.FileParamsSet('test_data_dict.json')
        ps.use_class(self.__class__)

        params = list(ps)
        names = ['0_sorted_list', '1_unsorted_list']
        values = [[[15, 12, 50]], [[10, 12, 15]]]

        self.assertEqual(len(values), 2)
        for p, n, v in zip(params, names, values):
            self.assertIsInstance(p, ddt.Params)
            self.assertEqual(p.name, n)
            self.assertEqual(p.args, v)
            self.assertEqual(p.kwargs, {})

    def test__FileParamsSet_generates_ParamsFailure_if_file_not_found(self):
        ps = ddt.FileParamsSet('test_no_such_file.json')
        ps.use_class(self.__class__)

        params = list(ps)

        self.assertEqual(len(params), 1)
        self.assertIsInstance(params[0], ddt.ParamsFailure)
        if six.PY2:
            self.assertEqual(params[0].name, 'IOError')
            self.assertIsInstance(params[0].reason, IOError)
        if six.PY3:
            self.assertEqual(params[0].name, 'FileNotFoundError')
            self.assertIsInstance(params[0].reason, FileNotFoundError)
        self.assertIn("No such file or directory", str(params[0].reason))

    def test__FileParamsSet_generates_ParamsFailure_on_invalid_JSON(self):
        ps = ddt.FileParamsSet('test_data_invalid.json')
        ps.use_class(self.__class__)

        params = list(ps)

        self.assertEqual(len(params), 1)
        self.assertIsInstance(params[0], ddt.ParamsFailure)
        self.assertEqual(params[0].name, 'ValueError')
        self.assertIsInstance(params[0].reason, ValueError)
        self.assertIn(
            "Invalid control character at: line 2 column 11",
            str(params[0].reason)
        )
