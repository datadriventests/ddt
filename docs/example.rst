Example usage
=============

DDT consists of a class decorator ``ddt`` (for your ``TestCase`` subclass)
and a method decorator ``data`` (for your tests that want to be multiplied).

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
