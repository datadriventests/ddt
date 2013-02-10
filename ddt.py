import os
import inspect
import json

from functools import wraps

__version__ = '0.2.0'

# this value cannot conflict with any real python attribute
DATA_ATTR = '%values'

# store the path to JSON/CSV file ?
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
    """

    def feed_data(func, *args, **kwargs):
        """
        This internal method decorator feeds the test data item to the test.
        """
        @wraps(func)
        def wrapper(self):
            return func(self, *args, **kwargs)
        return wrapper

    for name, f in cls.__dict__.items():
        if hasattr(f, DATA_ATTR):
            for v in getattr(f, DATA_ATTR):
                test_name = getattr(v, "__name__", "{0}_{1}".format(name, v))
                setattr(cls, test_name, feed_data(f, v))
            delattr(cls, name)
        elif hasattr(f, FILE_ATTR):
            file_attr = getattr(f, FILE_ATTR)
            cls_path = os.path.abspath(inspect.getsourcefile(cls))
            data_file_path = os.path.join(os.path.dirname(cls_path), file_attr)
            if os.path.exists(data_file_path):
                data = json.loads(open(data_file_path).read())
                for v in data:
                    test_name = getattr(v, "__name__",
                                        "{0}_{1}".format(name, v))
                    setattr(cls, test_name, feed_data(f, v))
            delattr(cls, name)
    return cls
