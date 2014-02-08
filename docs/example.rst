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

And then run them with your favourite test runner, e.g. if you use nose::

    $ nosetests -v test/test_example.py

..
   program-output:: nosetests -v ../test/test_example.py

The number of test cases actually run and reported separately has been
multiplied.
