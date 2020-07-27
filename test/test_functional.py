import os
import json
from sys import modules
import pytest
import six

try:
    from unittest import mock
except ImportError:
    import mock

from ddt import ddt, data, file_data, TestNameFormat

from test.mycode import has_three_elements


class CustomClass:
    pass


@ddt
class Dummy(object):
    """
    Dummy class to test the data decorator on
    """

    @data(1, 2, 3, 4)
    def test_something(self, value):
        return value


@ddt(testNameFormat=TestNameFormat.DEFAULT)
class DummyTestNameFormatDefault(object):
    """
    Dummy class to test the ddt decorator that generates test names using the
    default format (index and values).
    """

    @data("a", "b", "c", "d")
    def test_something(self, value):
        return value


@ddt(testNameFormat=TestNameFormat.INDEX_ONLY)
class DummyTestNameFormatIndexOnly(object):
    """
    Dummy class to test the ddt decorator that generates test names using only
    the index.
    """

    @data("a", "b", "c", "d")
    def test_something(self, value):
        return value


@ddt
class DummyInvalidIdentifier():
    """
    Dummy class to test the data decorator receiving values invalid characters
    identifiers
    """

    @data('32v2 g #Gmw845h$W b53wi.')
    def test_data_with_invalid_identifier(self, value):
        return value


@ddt
class FileDataDummy(object):
    """
    Dummy class to test the file_data decorator on
    """

    @file_data("data/test_data_dict.json")
    def test_something_again(self, value):
        return value


@ddt
class JSONFileDataMissingDummy(object):
    """
    Dummy class to test the file_data decorator on when
    JSON file is missing
    """

    @file_data("data/test_data_dict_missing.json")
    def test_something_again(self, value):
        return value


@ddt
class YAMLFileDataMissingDummy(object):
    """
    Dummy class to test the file_data decorator on when
    YAML file is missing
    """

    @file_data("data/test_data_dict_missing.yaml")
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

    assert post_size == pre_size + 1
    extra_attrs = dh_keys - keys
    assert len(extra_attrs) == 1
    extra_attr = extra_attrs.pop()
    assert getattr(data_hello, extra_attr) == (1, 2)


def test_file_data_decorator_with_dict():
    """
    Test the ``file_data`` method decorator
    """

    def hello():
        pass

    pre_size = len(hello.__dict__)
    keys = set(hello.__dict__.keys())
    data_hello = data("test_data_dict.json")(hello)

    dh_keys = set(data_hello.__dict__.keys())
    post_size = len(data_hello.__dict__)

    assert post_size == pre_size + 1
    extra_attrs = dh_keys - keys

    assert len(extra_attrs) == 1
    extra_attr = extra_attrs.pop()
    assert getattr(data_hello, extra_attr) == ("test_data_dict.json",)


def _is_test(x):
    return x.startswith('test_')


def test_ddt():
    """
    Test the ``ddt`` class decorator
    """
    tests = len(list(filter(_is_test, Dummy.__dict__)))
    assert tests == 4


def test_ddt_format_test_name_index_only():
    """
    Test the ``ddt`` class decorator with ``INDEX_ONLY`` test name format
    """
    tests = set(filter(_is_test, DummyTestNameFormatIndexOnly.__dict__))
    assert len(tests) == 4

    indexes = range(1, 5)
    dataSets = ["a", "b", "c", "d"]  # @data from DummyTestNameFormatIndexOnly
    for i, d in zip(indexes, dataSets):
        assert ("test_something_{}".format(i) in tests)
        assert not ("test_something_{}_{}".format(i, d) in tests)


def test_ddt_format_test_name_default():
    """
    Test the ``ddt`` class decorator with ``DEFAULT`` test name format
    """
    tests = set(filter(_is_test, DummyTestNameFormatDefault.__dict__))
    assert len(tests) == 4

    indexes = range(1, 5)
    dataSets = ["a", "b", "c", "d"]  # @data from DummyTestNameFormatDefault
    for i, d in zip(indexes, dataSets):
        assert not ("test_something_{}".format(i) in tests)
        assert ("test_something_{}_{}".format(i, d) in tests)


def test_file_data_test_creation():
    """
    Test that the ``file_data`` decorator creates two tests
    """

    tests = len(list(filter(_is_test, FileDataDummy.__dict__)))
    assert tests == 2


def test_file_data_test_names_dict():
    """
    Test that ``file_data`` creates tests with the correct name

    Name is the the function name plus the key in the JSON data,
    when it is parsed as a dictionary.
    """

    tests = set(filter(_is_test, FileDataDummy.__dict__))

    tests_dir = os.path.dirname(__file__)
    test_data_path = os.path.join(tests_dir, 'data/test_data_dict.json')
    test_data = json.loads(open(test_data_path).read())
    index_len = len(str(len(test_data)))
    created_tests = set([
        "test_something_again_{0:0{2}}_{1}".format(index + 1, name, index_len)
        for index, name in enumerate(test_data.keys())
    ])

    assert tests == created_tests


def test_feed_data_data():
    """
    Test that data is fed to the decorated tests
    """
    tests = filter(_is_test, Dummy.__dict__)

    values = []
    obj = Dummy()
    for test in tests:
        method = getattr(obj, test)
        values.append(method())

    assert set(values) == set([1, 2, 3, 4])


def test_feed_data_file_data():
    """
    Test that data is fed to the decorated tests from a file
    """
    tests = filter(_is_test, FileDataDummy.__dict__)

    values = []
    obj = FileDataDummy()
    for test in tests:
        method = getattr(obj, test)
        values.extend(method())

    assert set(values) == set([10, 12, 15, 15, 12, 50])


def test_feed_data_file_data_missing_json():
    """
    Test that a ValueError is raised when JSON file is missing
    """
    tests = filter(_is_test, JSONFileDataMissingDummy.__dict__)

    obj = JSONFileDataMissingDummy()
    for test in tests:
        method = getattr(obj, test)
        with pytest.raises(ValueError):
            method()


def test_feed_data_file_data_missing_yaml():
    """
    Test that a ValueError is raised when YAML file is missing
    """
    tests = filter(_is_test, YAMLFileDataMissingDummy.__dict__)

    obj = YAMLFileDataMissingDummy()
    for test in tests:
        method = getattr(obj, test)
        with pytest.raises(ValueError):
            method()


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
    assert getattr(ddt_mytest, 'test_hello_1_data1')
    assert getattr(ddt_mytest, 'test_hello_2_2')


def test_ddt_data_doc_attribute():
    """
    Test the ``__doc__`` attribute handling of ``data`` items with ``ddt``
    """

    def func_w_doc():
        """testFunctionDocstring {6}

        :param: None
        :return: None
        """
        pass

    def func_wo_doc():
        pass

    class Myint(int):
        pass

    class Mytest(object):
        pass

    d1 = Myint(1)
    d1.__name__ = 'case1'
    d1.__doc__ = """docstring1"""

    d2 = Myint(2)
    d2.__name__ = 'case2'

    data_hello = data(d1, d2, {'test': True})(func_w_doc)
    data_hello2 = data(d1, d2, {'test': True})(func_wo_doc)

    setattr(Mytest, 'first_test', data_hello)
    setattr(Mytest, 'second_test', data_hello2)
    ddt_mytest = ddt(Mytest)

    assert getattr(
        getattr(ddt_mytest, 'first_test_1_case1'), '__doc__'
    ) == d1.__doc__
    assert getattr(
        getattr(ddt_mytest, 'first_test_2_case2'), '__doc__'
    ) == func_w_doc.__doc__
    assert getattr(
        getattr(ddt_mytest, 'first_test_3'), '__doc__'
    ) == func_w_doc.__doc__
    assert getattr(
        getattr(ddt_mytest, 'second_test_1_case1'), '__doc__'
    ) == d1.__doc__
    assert getattr(
        getattr(ddt_mytest, 'second_test_2_case2'), '__doc__'
    ) is None
    assert getattr(getattr(ddt_mytest, 'second_test_3'), '__doc__') is None


def test_ddt_data_unicode():
    """
    Test that unicode strings are converted to function names correctly
    """
    # We test unicode support separately for python 2 and 3

    if six.PY2:

        @ddt
        class Mytest(object):
            @data(u'ascii', u'non-ascii-\N{SNOWMAN}', {u'\N{SNOWMAN}': 'data'})
            def test_hello(self, val):
                pass

        assert getattr(Mytest, 'test_hello_1_ascii') is not None
        assert getattr(Mytest, 'test_hello_2_non_ascii__u2603') is not None
        assert getattr(Mytest, 'test_hello_3') is not None

    elif six.PY3:

        @ddt
        class Mytest(object):
            @data('ascii', 'non-ascii-\N{SNOWMAN}', {'\N{SNOWMAN}': 'data'})
            def test_hello(self, val):
                pass

        assert getattr(Mytest, 'test_hello_1_ascii') is not None
        assert getattr(Mytest, 'test_hello_2_non_ascii__') is not None
        assert getattr(Mytest, 'test_hello_3') is not None


def test_ddt_data_object():
    """
    Test not using value if non-trivial arguments
    """

    @ddt
    class Mytest(object):
        @data(object())
        def test_object(self, val):
            pass
    assert getattr(Mytest, 'test_object_1') is not None


def test_feed_data_with_invalid_identifier():
    """
    Test that data is fed to the decorated tests
    """
    tests = list(filter(_is_test, DummyInvalidIdentifier.__dict__))
    assert len(tests) == 1

    obj = DummyInvalidIdentifier()
    method = getattr(obj, tests[0])
    assert (
        method.__name__ ==
        'test_data_with_invalid_identifier_1_32v2_g__Gmw845h_W_b53wi_'
    )
    assert method() == '32v2 g #Gmw845h$W b53wi.'


@mock.patch('ddt._have_yaml', False)
def test_load_yaml_without_yaml_support():
    """
    Test that YAML files are not loaded if YAML is not installed.
    """

    @ddt
    class NoYAMLInstalledTest(object):

        @file_data('data/test_data_dict.yaml')
        def test_file_data_yaml_dict(self, value):
            assert has_three_elements(value)

    tests = filter(_is_test, NoYAMLInstalledTest.__dict__)

    obj = NoYAMLInstalledTest()
    for test in tests:
        method = getattr(obj, test)
        with pytest.raises(ValueError):
            method()


def test_load_yaml_with_python_tag():
    """
    Test that YAML files containing python tags throw no exception if an
    loader allowing python tags is passed.
    """

    from yaml import FullLoader
    from yaml.constructor import ConstructorError

    def str_to_type(class_name):
        return getattr(modules[__name__], class_name)

    try:
        @ddt
        class YamlDefaultLoaderTest(object):
            @file_data('data/test_functional_custom_tags.yaml')
            def test_cls_is_instance(self, cls, expected):
                assert isinstance(cls, str_to_type(expected))
    except Exception as e:
        if not isinstance(e, ConstructorError):
            raise AssertionError()

    @ddt
    class YamlFullLoaderTest(object):
        @file_data('data/test_functional_custom_tags.yaml', FullLoader)
        def test_cls_is_instance(self, instance, expected):
            assert isinstance(instance, str_to_type(expected))

    tests = list(filter(_is_test, YamlFullLoaderTest.__dict__))
    obj = YamlFullLoaderTest()

    if not tests:
        raise AssertionError('No tests have been found.')

    for test in tests:
        method = getattr(obj, test)
        method()
