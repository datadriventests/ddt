Example usage
=============

DDT consists of a class decorator ``ddt`` (for your ``TestCase`` subclass)
and two method decorators (for your tests that want to be multiplied):

* ``data``: contains as many arguments as values you want to feed to the test.
* ``file_data``: will load test data from a JSON file.

Normally each value within ``data`` will be passed as a single argument to
your test method. If these values are e.g. tuples, you will have to unpack them
inside your test. Alternatively, you can use an additional decorator,
``unpack``, that will automatically unpack tuples and lists into multiple
arguments, and dictionaries into multiple keyword arguments. See examples
below.

This allows you to write your tests as:

.. literalinclude:: ../test/test_example.py
   :language: python

Where ``test_data_dict.json``:

.. literalinclude:: ../test/test_data_dict.json
   :language: javascript

and ``test_data_list.json``:

.. literalinclude:: ../test/test_data_list.json
   :language: javascript

And then run them with your favourite test runner, e.g. if you use nose::

    $ nosetests -v test/test_example.py

..
   program-output:: nosetests -v ../test/test_example.py

The number of test cases actually run and reported separately has been
multiplied.


DDT will try to give the new test cases meaningful names by converting the
data values to valid python identifiers.
