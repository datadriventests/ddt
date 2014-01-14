Example usage
=============

DDT consists of a class decorator ``ddt`` (for your ``TestCase`` subclass)
and two method decorators (for your tests that want to be multiplied):

* ``data``: contains as many arguments as values you want to feed to the test.
* ``file_data``: will load test data from a JSON file.

This allows you to write your tests as:

.. literalinclude:: ../test/test_example.py
   :language: python

Where ``test_data_dict.json``:

.. literalinclude:: ../test/test_data_dict.json
   :language: javascript

and ``test_data_list.json``:

.. literalinclude:: ../test/test_data_list.json
   :language: javascript

And then run them with::

    $ nosetests -v test/test_example.py
    test_file_data_dict_sorted_list (test.test_example.FooTestCase) ... ok
    test_file_data_dict_unsorted_list (test.test_example.FooTestCase) ... ok
    test_file_data_list_Goodbye (test.test_example.FooTestCase) ... ok
    test_file_data_list_Hello (test.test_example.FooTestCase) ... ok
    test_greater_test_10_greater_than_5 (test.test_example.FooTestCase) ... ok
    test_greater_test_2_greater_than_1 (test.test_example.FooTestCase) ... ok
    test_larger_than_two_12 (test.test_example.FooTestCase) ... ok
    test_larger_than_two_23 (test.test_example.FooTestCase) ... ok
    test_larger_than_two_3 (test.test_example.FooTestCase) ... ok
    test_larger_than_two_4 (test.test_example.FooTestCase) ... ok
    test_not_larger_than_two_-3 (test.test_example.FooTestCase) ... ok
    test_not_larger_than_two_0 (test.test_example.FooTestCase) ... ok
    test_not_larger_than_two_1 (test.test_example.FooTestCase) ... ok
    test_not_larger_than_two_2 (test.test_example.FooTestCase) ... ok
    test_undecorated (test.test_example.FooTestCase) ... ok
    test_unicode_ascii (test.test_example.FooTestCase) ... ok
    test_unicode_non-ascii-\u2603 (test.test_example.FooTestCase) ... ok

    ----------------------------------------------------------------------
    Ran 17 tests in 0.002s

    OK

7 test methods + some *magic* decorators = 17 test cases.
