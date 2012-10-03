from ddt import ddt, data
from nose.tools import assert_equal, assert_is_not_none


@ddt
class Dummy(object):
    """Dummy class to test decorators on"""

    @data(1, 2, 3, 4)
    def test_something(self, value):
        return value


def test_data_decorator():
    """Test the ``data`` method decorator"""

    def hello():
        pass

    pre_size = len(hello.__dict__)
    keys = hello.__dict__.keys()
    data_hello = data(1, 2)(hello)
    dh_keys = data_hello.__dict__.keys()
    post_size = len(data_hello.__dict__)

    assert_equal(post_size, pre_size + 1)
    extra_attrs = set(dh_keys) - set(keys)
    assert_equal(len(extra_attrs), 1)
    extra_attr = extra_attrs.pop()
    assert_equal(getattr(data_hello, extra_attr), (1, 2))


is_test = lambda x: x.startswith('test_')


def test_ddt():
    """Test the ``ddt`` class decorator"""

    tests = len(filter(is_test, Dummy.__dict__))
    assert_equal(tests, 4)


def test_feed_data():
    """Test that data is fed to the decorated tests"""

    tests = filter(is_test, Dummy.__dict__)
    values = []
    obj = Dummy()
    for test in tests:
        method = getattr(obj, test)
        values.append(method())

    assert_equal(set(values), set([1, 2, 3, 4]))


def test_ddt_data_name_attribute():
    """
    Test the ``__name__`` attribute handling of ``data`` items with ``ddt``
    """

    def hello():
        pass

    class myint(int):
        pass

    class mytest(object):
        pass

    d1 = myint(1)
    d1.__name__ = 'test_d1'

    d2 = myint(2)

    data_hello = data(d1, d2)(hello)
    setattr(mytest, 'test_hello', data_hello)

    ddt_mytest = ddt(mytest)
    assert_is_not_none(getattr(ddt_mytest, 'test_d1'))
    assert_is_not_none(getattr(ddt_mytest, 'test_hello_2'))
