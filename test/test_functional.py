import os
import json

import six

from ddt import (
    ddt, data, file_data, is_hash_randomized, DataValues, FileValues
)
from nose.tools import assert_equal, assert_is_not_none, assert_raises


@ddt
class Dummy(object):
    """
    Dummy class to test the data decorator on
    """

    @data(1, 2, 3, 4)
    def test_something(self, value):
        return value


@ddt
class DummyInvalidIdentifier():
    """
    Dummy class to test the data decorator receiving values invalid characters
    indentifiers
    """

    @data('32v2 g #Gmw845h$W b53wi.')
    def test_data_with_invalid_identifier(self, value):
        return value


@ddt
class FileDataDummy(object):
    """
    Dummy class to test the file_data decorator on
    """

    @file_data("test_data_dict.json")
    def test_something_again(self, value):
        return value


@ddt
class FileDataMissingDummy(object):
    """
    Dummy class to test the file_data decorator on when
    JSON file is missing
    """

    @file_data("test_data_dict_missing.json")
    def test_something_again(self, value):
        return value


def test_data_decorator():
    """
    Test the ``data`` method decorator
    """

    def hello():
        pass

    pre_size = len(hello.__dict__)
    keys = set(hello.__dict__.keys())
    data_hello = data(1, 2)(hello)
    dh_keys = set(data_hello.__dict__.keys())
    post_size = len(data_hello.__dict__)

    assert_equal(post_size, pre_size + 1)
    extra_attrs = dh_keys - keys
    assert_equal(len(extra_attrs), 1)
    extra_attr = extra_attrs.pop()
    assert_equal(getattr(data_hello, extra_attr), [DataValues((1, 2))])


def test_multiple_data_decorators():
    """
    Test the ``data`` method decorator with multiple applications
    """

    def hello():
        pass

    pre_size = len(hello.__dict__)
    keys = set(hello.__dict__.keys())
    data_hello = data(1, 2)(data(3)(hello))
    dh_keys = set(data_hello.__dict__.keys())
    post_size = len(data_hello.__dict__)

    assert_equal(post_size, pre_size + 1)
    extra_attrs = dh_keys - keys
    assert_equal(len(extra_attrs), 1)
    extra_attr = extra_attrs.pop()
    assert_equal(
        getattr(data_hello, extra_attr),
        [DataValues((1, 2)), DataValues((3,))]
    )


def test_file_data_decorator_with_dict():
    """
    Test the ``file_data`` method decorator
    """

    def hello():
        pass

    pre_size = len(hello.__dict__)
    keys = set(hello.__dict__.keys())
    data_hello = file_data("test_data_dict.json")(hello)

    dh_keys = set(data_hello.__dict__.keys())
    post_size = len(data_hello.__dict__)

    assert_equal(post_size, pre_size + 1)
    extra_attrs = dh_keys - keys
    assert_equal(len(extra_attrs), 1)
    extra_attr = extra_attrs.pop()
    assert_equal(
        getattr(data_hello, extra_attr),
        [FileValues("test_data_dict.json")]
    )


def test_multiple_file_data_decorators_with_dict():
    """
    Test the ``file_data`` method decorator with multiple applications
    """

    def hello():
        pass

    pre_size = len(hello.__dict__)
    keys = set(hello.__dict__.keys())
    data_hello = file_data("test_other_data.json")(hello)
    data_hello = file_data("test_data_dict.json")(data_hello)

    dh_keys = set(data_hello.__dict__.keys())
    post_size = len(data_hello.__dict__)

    assert_equal(post_size, pre_size + 1)
    extra_attrs = dh_keys - keys
    assert_equal(len(extra_attrs), 1)
    extra_attr = extra_attrs.pop()
    assert_equal(
        getattr(data_hello, extra_attr),
        [
            FileValues("test_data_dict.json"),
            FileValues("test_other_data.json"),
        ]
    )


is_test = lambda x: x.startswith('test_')


def test_ddt():
    """
    Test the ``ddt`` class decorator
    """
    tests = len(list(filter(is_test, Dummy.__dict__)))
    assert_equal(tests, 4)


def test_file_data_test_creation():
    """
    Test that the ``file_data`` decorator creates two tests
    """

    tests = len(list(filter(is_test, FileDataDummy.__dict__)))
    assert_equal(tests, 2)


def test_file_data_test_names_dict():
    """
    Test that ``file_data`` creates tests with the correct name

    Name is the the function name plus the key in the JSON data,
    when it is parsed as a dictionary.
    """

    tests = set(filter(is_test, FileDataDummy.__dict__))

    tests_dir = os.path.dirname(__file__)
    test_data_path = os.path.join(tests_dir, 'test_data_dict.json')
    test_data = json.loads(open(test_data_path).read())
    created_tests = set([
        "test_something_again_{0}_{1}".format(index + 1, name)
        for index, name in enumerate(test_data.keys())
    ])

    assert_equal(tests, created_tests)


def test_feed_data_data():
    """
    Test that data is fed to the decorated tests
    """
    tests = filter(is_test, Dummy.__dict__)

    values = []
    obj = Dummy()
    for test in tests:
        method = getattr(obj, test)
        values.append(method())

    assert_equal(set(values), set([1, 2, 3, 4]))


def test_feed_data_file_data():
    """
    Test that data is fed to the decorated tests from a file
    """
    tests = filter(is_test, FileDataDummy.__dict__)

    values = []
    obj = FileDataDummy()
    for test in tests:
        method = getattr(obj, test)
        values.extend(method())

    assert_equal(set(values), set([10, 12, 15, 15, 12, 50]))


def test_feed_data_file_data_missing_json():
    """
    Test that a ValueError is raised
    """
    tests = filter(is_test, FileDataMissingDummy.__dict__)

    obj = FileDataMissingDummy()
    for test in tests:
        method = getattr(obj, test)
        assert_raises(ValueError, method)


def test_ddt_data_name_attribute():
    """
    Test the ``__name__`` attribute handling of ``data`` items with ``ddt``
    """

    def hello():
        pass

    class Myint(int):
        pass

    class Mytest(object):
        pass

    d1 = Myint(1)
    d1.__name__ = 'data1'

    d2 = Myint(2)

    data_hello = data(d1, d2)(hello)
    setattr(Mytest, 'test_hello', data_hello)

    ddt_mytest = ddt(Mytest)
    assert_is_not_none(getattr(ddt_mytest, 'test_hello_1_data1'))
    assert_is_not_none(getattr(ddt_mytest, 'test_hello_2_2'))


def test_ddt_data_unicode():
    """
    Test that unicode strings are converted to function names correctly
    """

    def hello():
        pass

    # We test unicode support separately for python 2 and 3

    if six.PY2:

        @ddt
        class Mytest(object):
            @data(u'ascii', u'non-ascii-\N{SNOWMAN}', {u'\N{SNOWMAN}': 'data'})
            def test_hello(self, val):
                pass

        assert_is_not_none(getattr(Mytest, 'test_hello_1_ascii'))
        assert_is_not_none(getattr(Mytest, 'test_hello_2_non_ascii__u2603'))
        if is_hash_randomized():
            assert_is_not_none(getattr(Mytest, 'test_hello_3'))
        else:
            assert_is_not_none(getattr(Mytest,
                                       'test_hello_3__u__u2603____data__'))

    elif six.PY3:

        @ddt
        class Mytest(object):
            @data('ascii', 'non-ascii-\N{SNOWMAN}', {'\N{SNOWMAN}': 'data'})
            def test_hello(self, val):
                pass

        assert_is_not_none(getattr(Mytest, 'test_hello_1_ascii'))
        assert_is_not_none(getattr(Mytest, 'test_hello_2_non_ascii__'))
        if is_hash_randomized():
            assert_is_not_none(getattr(Mytest, 'test_hello_3'))
        else:
            assert_is_not_none(getattr(Mytest, 'test_hello_3________data__'))


def test_feed_data_with_invalid_identifier():
    """
    Test that data is fed to the decorated tests
    """
    tests = list(filter(is_test, DummyInvalidIdentifier.__dict__))
    assert_equal(len(tests), 1)

    obj = DummyInvalidIdentifier()
    method = getattr(obj, tests[0])
    assert_equal(
        method.__name__,
        'test_data_with_invalid_identifier_1_32v2_g__Gmw845h_W_b53wi_'
    )
    assert_equal(method(), '32v2 g #Gmw845h$W b53wi.')
