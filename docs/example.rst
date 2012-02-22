Example usage
=============

DDT consists of a class decorator ``ddt`` (for your ``TestCase`` subclass)
and a method decorator ``data`` (for your tests that want to be multiplied).

This allows you to write your tests as:

.. code-block:: python

    # tests.py
    import unittest
    from ddt import ddt, data
    from mycode import larger_than_two

    @ddt
    class FooTestCase(unittest.TestCase):

        @data(3, 4, 12, 23)
        def test_larger_than_two(self, value):
            self.assertTrue(larger_than_two(value))

        @data(1, -3, 2, 0)
        def test_not_larger_than_two(self, value):
            self.assertFalse(larger_than_two(value))

And then run them with::

    % nosetests tests.py
    ........
    ----------------------------------------------------------------------
    Ran 8 tests in 0.002s

    OK

2 test methods + some *magic* decorators = 8 test cases.
