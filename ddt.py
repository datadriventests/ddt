import inspect
import json
import os
from functools import wraps

__version__ = '0.5.0'

# this value cannot conflict with any real python attribute
DATA_ATTR = '%values'

# store the path to JSON file
FILE_ATTR = '%file_path'


def data(*values):
    """
    Method decorator to add to your test methods.

    Should be added to methods of instances of ``unittest.TestCase``.
    """
    def wrapper(func):
        setattr(func, DATA_ATTR, values)
        return func
    return wrapper


def file_data(value):
    """
    Method decorator to add to your test methods.

    Should be added to methods of instances of ``unittest.TestCase``.

    ``value`` should be a path relative to the directory of the file
    containing the decorated ``unittest.TestCase``. The file
    should contain JSON encoded data, that can either be a list or a
    dict.

    In case of a list, each value in the list will correspond to one
    test case, and the value will be concatenated to the test method
    name.

    In case of a dict, keys will be used as suffixes to the name of the
    test case, and values will be fed as test data.
    """
    def wrapper(func):
        setattr(func, FILE_ATTR, value)
        return func
    return wrapper


def ddt(cls):
    """
    Class decorator for subclasses of ``unittest.TestCase``.

    Apply this decorator to the test case class, and then
    decorate test methods with ``@data``.

    For each method decorated with ``@data``, this will effectively create as
    many methods as data items are passed as parameters to ``@data``.

    The names of the test methods follow the pattern ``test_func_name
    + "_" + str(data)``. If ``data.__name__`` exists, it is used
    instead for the test method name.

    For each method decorated with ``@file_data('test_data.json')``, the
    decorator will try to load the test_data.json file located relative
    to the python file containing the method that is decorated. It will,
    for each ``test_name`` key create as many methods in the list of values
    from the ``data`` key.

    The names of these test methods follow the pattern of
    ``test_name`` + str(data)``
    """

    def feed_data(func, *args, **kwargs):
        """
        This internal method decorator feeds the test data item to the test.
        """
        @wraps(func)
        def wrapper(self):
            return func(self, *args, **kwargs)
        return wrapper

    def process_file_data(name, func, file_attr):
        """
        Process the parameter in the `file_data` decorator.
        """
        cls_path = os.path.abspath(inspect.getsourcefile(cls))
        data_file_path = os.path.join(os.path.dirname(cls_path), file_attr)

        def _raise_ve(*args):
            raise ValueError("%s does not exist" % file_attr)

        if os.path.exists(data_file_path) is False:
            test_name = "{0}_{1}".format(name, "error")
            setattr(cls, test_name, feed_data(_raise_ve, None))
        else:
            data = json.loads(open(data_file_path).read())
            for elem in data:
                if isinstance(data, dict):
                    key, value = elem, data[elem]
                    test_name = "{0}_{1}".format(name, key)
                elif isinstance(data, list):
                    value = elem
                    test_name = "{0}_{1}".format(name, value)
                setattr(cls, test_name, feed_data(func, value))

    for name, func in list(cls.__dict__.items()):
        if hasattr(func, DATA_ATTR):
            for v in getattr(func, DATA_ATTR):
                test_name = "{0}_{1}".format(name, getattr(v, "__name__", v))
                setattr(cls, test_name, feed_data(func, v))
            delattr(cls, name)
        elif hasattr(func, FILE_ATTR):
            file_attr = getattr(func, FILE_ATTR)
            process_file_data(name, func, file_attr)
            delattr(cls, name)
    return cls
