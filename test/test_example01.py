import unittest
from test.mycode import larger_than_two


class FooTestCase(unittest.TestCase):

    def test_manual_neg1(self):
        self.assertFalse(larger_than_two(-1))

    def test_manual_zero(self):
        self.assertFalse(larger_than_two(0))

    def test_manual_pos2(self):
        self.assertFalse(larger_than_two(2))

    def test_manual_pos3(self):
        self.assertTrue(larger_than_two(3))
