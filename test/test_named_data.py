import ddt
import unittest


@ddt.ddt
class TestNamedData(unittest.TestCase):
    class NonTrivialClass(object):
        pass

    @ddt.named_data(
        ['Single', 0, 1]
    )
    def test_single_named_value(self, value1, value2):
        self.assertGreater(value2, value1)

    @ddt.named_data(
        ['1st', 1, 2],
        ('2nd', 3, 4)
    )
    def test_multiple_named_value_seqs(self, value1, value2):
        self.assertGreater(value2, value1)

    @ddt.named_data(
        dict(name='1st', value2=1, value1=0),
        {'name': '2nd', 'value2': 1, 'value1': 0}
    )
    def test_multiple_named_value_dicts(self, value1, value2):
        self.assertGreater(value2, value1)

    @ddt.named_data(
        dict(name='1st', value2=1, value1=0),
        ('2nd', 0, 1)
    )
    def test_multiple_named_value_mixed(self, value1, value2):
        self.assertGreater(value2, value1)

    @ddt.named_data(
        ['Passes', NonTrivialClass(), True],
        ('Fails', 1, False)
    )
    def test_seq_with_nontrivial_type(self, value, passes):
        if passes:
            self.assertIsInstance(value, self.NonTrivialClass)
        else:
            self.assertNotIsInstance(value, self.NonTrivialClass)

    @ddt.named_data(
        {'name': 'Passes', 'value': NonTrivialClass(), 'passes': True},
        {'name': 'Fails', 'value': 1, 'passes': False}
    )
    def test_dict_with_nontrivial_type(self, value, passes):
        if passes:
            self.assertIsInstance(value, self.NonTrivialClass)
        else:
            self.assertNotIsInstance(value, self.NonTrivialClass)

    def test_missing_name_dict(self):
        with self.assertRaises(KeyError):
            @ddt.named_data(
                {'not_a_name': 'oops', 'value': 1}
            )
            def _internal_test(value):
                pass
