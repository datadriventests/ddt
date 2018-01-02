Example usage
=============

DDT consists of a class decorator ``ddt`` (for your ``TestCase`` subclass)
and two method decorators (for your tests that want to be multiplied):

* ``data``: contains as many arguments as values you want to feed to the test.
* ``file_data``: will load test data from a JSON or YAML file.

.. note::

   Only files ending with ".yml" and ".yaml" are loaded as YAML files. All
   other files are loaded as JSON files.

Normally each value within ``data`` will be passed as a single argument to
your test method. If these values are e.g. tuples, you will have to unpack them
inside your test. Alternatively, you can use an additional decorator,
``unpack``, that will automatically unpack tuples and lists into multiple
arguments, and dictionaries into multiple keyword arguments. See examples
below.

This allows you to write your tests as:

.. literalinclude:: ../test/test_example.py
   :language: python

Where ``test_data_dict_dict.json``:

.. literalinclude:: ../test/test_data_dict_dict.json
   :language: javascript

and ``test_data_dict_dict.yaml``:

.. literalinclude:: ../test/test_data_dict_dict.yaml
   :language: yaml

and ``test_data_dict.json``:

.. literalinclude:: ../test/test_data_dict.json
   :language: javascript

and ``test_data_dict.yaml``:

.. literalinclude:: ../test/test_data_dict.yaml
   :language: yaml

and ``test_data_list.json``:

.. literalinclude:: ../test/test_data_list.json
   :language: javascript

and ``test_data_list.yaml``:

.. literalinclude:: ../test/test_data_list.yaml
   :language: yaml

And then run them with your favourite test runner, e.g. if you use nose::

    $ nosetests -v test/test_example.py

..
   program-output:: nosetests -v ../test/test_example.py

The number of test cases actually run and reported separately has been
multiplied.


DDT will try to give the new test cases meaningful names by converting the
data values to valid python identifiers.


.. note::

   Python 2.7.3 introduced *hash randomization* which is by default
   enabled on Python 3.3 and later. DDT's default mechanism to
   generate meaningful test names will **not** use the test data value
   as part of the name for complex types if hash randomization is
   enabled.

   You can disable hash randomization by setting the
   ``PYTHONHASHSEED`` environment variable to a fixed value before
   running tests (``export PYTHONHASHSEED=1`` for example).
