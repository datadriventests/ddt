Example usage
=============

DDT consists of a class decorator ``ddt`` (for your ``TestCase`` subclass)
and a two method decorators ``data`` (for your tests that want to be multiplied)
and ``file_data`` that will load test data from a file and multiply tests.

This allows you to write your tests as:

.. literalinclude:: ../test/test_example.py
   :language: python

And then run them with::

    % nosetests test_example.py
    ..........
    ----------------------------------------------------------------------
    Ran 10 tests in 0.002s

    OK

3 test methods + some *magic* decorators = 10 test cases.
