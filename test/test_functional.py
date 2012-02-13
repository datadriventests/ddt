from ddt import ddt, data
from nose.tools import assert_equal


class Dummy(object):
    """Dummy class to test decorators on"""
    @data(1, 2, 3, 4)
    def test_something(self):
        pass


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


def test_ddt():
    """Test the ``ddt`` class decorator"""

    is_test = lambda x: x.startswith('test_')
    tests = len(filter(is_test, Dummy.__dict__))
    assert_equal(tests, 1)
    post_dummy = ddt(Dummy)
    post_tests = len(filter(is_test, post_dummy.__dict__))
    assert_equal(post_tests, 4)
