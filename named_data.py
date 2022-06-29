import ddt

try:
    # Python 3
    from collections.abc import Sequence
except ImportError:
    # Python 2.7
    from collections import Sequence


class NamedDataList(list):
    """ This is a helper class for @named_data that allows ddt tests to have meaningful names. """
    def __init__(self, name, *args):
        super(NamedDataList, self).__init__(args)
        self.name = name

    def __str__(self):
        return str(self.name)


class NamedDataDict(dict):
    """ This is a helper class for @named_data that allows ddt tests to have meaningful names. """
    def __init__(self, name, **kwargs):
        super(NamedDataDict, self).__init__(kwargs)
        self.name = name

    def __str__(self):
        return str(self.name)


# In order to ensure that the name is properly interpreted regardless of arguments, NamedDataXX types must be added to
# the tuple of ddt trivial types for which it always gets the name. See ddt.trivial_types for more information.
ddt.trivial_types += (NamedDataList, NamedDataDict, )


def named_data(*named_values):
    """
    This decorator is to allow for meaningful names to be given to tests that would otherwise use @ddt.data and
    @ddt.unpack.

    Example of original ddt usage:
        @ddt.ddt
        class TestExample(TemplateTest):
            @ddt.data(
                [0, 1],
                [10, 11]
            )
            @ddt.unpack
            def test_values(self, value1, value2):
                ...

    Example of new usage:
        @ddt.ddt
        class TestExample(TemplateTest):
            @named_data(
                ['A', 0, 1],
                ['B', 10, 11],
            )
            def test_values(self, value1, value2):
                ...

    Note that @unpack is not used.

    :param Sequence[Any] | dict[Any,Any] named_values: Each named_value should be a list with the name as the first
        argument, or a dictionary with 'name' as one of the keys. The name will be coerced to a string and all other
        values will be passed unchanged to the test.
    """
    type_of_first = None
    values = []
    for named_value in named_values:
        if type_of_first is not None and not isinstance(named_value, type_of_first):
            raise TypeError("@named_data expects all values to be of the same type.")

        if isinstance(named_value, Sequence):
            value = NamedDataList(named_value[0], *named_value[1:])
            type_of_first = type_of_first or Sequence

        elif isinstance(named_value, dict):
            if "name" not in named_value.keys():
                raise ValueError("@named_data expects a dictionary with a 'name' key.")
            value = NamedDataDict(**named_value)
            type_of_first = type_of_first or dict

        else:
            raise TypeError(
                "@named_data expects a Sequence (list, tuple) or dictionary, and not '{}'.".format(type(named_value))
            )

        # Remove the __doc__ attribute so @ddt.data doesn't add the NamedData class docstrings to the test name.
        value.__doc__ = None

        values.append(value)

    def wrapper(func):
        ddt.data(*values)(ddt.unpack(func))
        return func

    return wrapper
