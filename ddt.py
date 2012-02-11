from functools import wraps


MAGIC='%values'  # this value cannot conflict with any real python attribute


def data(*values):
    """
    Method decorator to add to your test methods.

    Should be added to methods of instances of ``unittest.TestCase``.
    """
    def wrapper(func):
        setattr(func, MAGIC, values)
        return func
    return wrapper


def ddt(cls):
    """
    Class decorator for instances of ``unittest.TestCase``.

    Apply this decorator to the test case class, and then
    decorate test methods with ``@data``.

    For each method decorated with ``@data``, this will create as
    many methods as data items are passed as parameters to ``@data``.
    """

    def run_with(func, *args, **kwargs):
        """
        This internal method decorator feeds the test data item to the test.
        """
        @wraps(func)
        def wrapper(self):
            return func(self, *args, **kwargs)
        return wrapper

    for name, f in cls.__dict__.items():
        if hasattr(f, MAGIC):
            i = 0
            for v in getattr(f, MAGIC):
                setattr(cls, 
                        "{0}_{1}".format(name, v), 
                        run_with(f, v))
                i = i + 1
            delattr(cls, name)
    return cls

