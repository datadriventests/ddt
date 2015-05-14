# -*- coding: utf-8 -*-
# This file is a part of DDT (https://github.com/txels/ddt)
# Copyright 2012-2015 Carles Barrobés and DDT contributors
# For the exact contribution history, see the git revision log.
# DDT is licensed under the MIT License, included in
# https://github.com/txels/ddt/blob/master/LICENSE.md

import inspect
import io
import itertools
import json
import os
import re
import sys
from functools import wraps

__version__ = '1.0.0'

# These attributes will not conflict with any real python attribute
# They are added to the decorated test method and processed later
# by the `ddt` class decorator.

PARAMS_SETS_ATTR = '%params_sets'   # store a list of *ParamsSet objects
UNPACKALL_ATTR = '%unpackall'       # remember @unpackall decorators


# Types that can be converted into valid identifiers safely.
TRIVIAL_TYPES = (type(None), bool, str, int, float)

# Extend the list a bit for Python2
try:
    TRIVIAL_TYPES += (unicode,)
except NameError:
    pass


# Public interface - Decorators


def unpack(func):
    """
    Method decorator to unpack parameters from the next (syntactically)
    parameters set (``@data`` or ``@file_data`` decorator) by one level.

    Multiple levels are unpacked if ``@unpack`` and ``@unpackall`` are combined
    and/or applied multiple times.

    """
    getattr(func, PARAMS_SETS_ATTR)[0].unpack()
    return func


def unpackall(func):
    """
    Method decorator to unpack parameters in all parameter sets by one level.

    Multiple levels are unpacked if ``@unpack`` and ``@unpackall`` are combined
    and/or applied multiple times.

    """
    setattr(func, UNPACKALL_ATTR, getattr(func, UNPACKALL_ATTR, 0) + 1)
    return func


def data(*unnamed_values, **named_values):
    """
    Method decorator to supply parameters to your test methods in-line.

    Should be added to methods of instances of ``unittest.TestCase``.

    Keyword arguments can be used to explicitly define names of values to be
    used in names of created test methods.

    """
    def wrapper(func):
        if not hasattr(func, PARAMS_SETS_ATTR):
            setattr(func, PARAMS_SETS_ATTR, [])
        params = InlineDataValues(*unnamed_values, **named_values)
        getattr(func, PARAMS_SETS_ATTR).insert(0, params)
        return func
    return wrapper


def file_data(filepath, encoding=None):
    """
    Method decorator to supply parameters to your test method from a JSON file.

    Should be added to methods of instances of ``unittest.TestCase``.

    ``filepath`` should be a path relative to the directory of the file
    containing the decorated ``unittest.TestCase``.

    The file should contain JSON-encoded data, that can either be a list or a
    dict. A list supplies unnamed parameters. A dict supplies named parameters
    where keys are used to identify individual parameters.

    """
    def wrapper(func):
        if not hasattr(func, PARAMS_SETS_ATTR):
            setattr(func, PARAMS_SETS_ATTR, [])
        params = FileDataValues(filepath, encoding=encoding)
        getattr(func, PARAMS_SETS_ATTR).insert(0, params)
        return func
    return wrapper


def ddt(cls):
    """
    Class decorator for subclasses of ``unittest.TestCase``.

    Apply this decorator to the test case class, and then decorate test methods
    with ``@data``, ``@file_data``, ``@unpack``, and ``@unpackall``.

    For each method decorated with ``@data`` and ``@file_data``, this will
    effectively create one method for each member of the Cartesian product of
    data items passed to ``@data`` or read from a JSON file by ``@file_data``.

    The names of the test methods follow the pattern
    ``original_test_name(__{ordinal}_{data})+``.

    The part ``__{ordinal}_{data}`` is repeated as many times as there are
    nested ``@data`` and ``@file_data`` decorators.

    ``ordinal`` is the position of a particular data item in the list of
    options represented by the corresponding decorator. Positions are numbered
    from 0. Keyword arguments (for ``@data``) and members of top-level dict
    (for ``@data_file``) are ordered according to their keys.

    ``data`` attempts to provide human readable identification of the data item
    with the following priority: 1) The keyword is used for data items passed
    as keyword arguments (for ``@data``) or members of the top-level dict (for
    ``@file_data``). 2) The ``__name__`` attribute of the value if it exists.
    3) An explicit namestring representation of the data value converted into a
    valid python identifier, if possible. 4) Only the position is used.

    For each method decorated with ``@file_data('test_data.json')``, the
    decorator will try to load the test_data.json file located relative
    to the python file containing the method that is decorated. It will,
    for each ``test_name`` key create as many methods in the list of values
    from the ``data`` key.

    """
    for name, func in list(cls.__dict__.items()):
        if hasattr(func, PARAMS_SETS_ATTR):
            test_vectors = itertools.product(*(
                map(
                    lambda s: s.use_class(cls),
                    getattr(func, PARAMS_SETS_ATTR)
                )
            ))
            for vector in test_vectors:
                params = sum(vector, Params(name, [], {}))
                params.unpack(getattr(func, UNPACKALL_ATTR, 0))
                add_test(cls, func, params)
            delattr(cls, name)

    return cls


# Adding new tests


def add_test(cls, func, params):
    """Add a test derived from an original function and specific combination of
    values provided by ``@data`` and ``@file_data`` decorators.

    """
    if isinstance(params, Params):
        @wraps(func)
        def test_case_func(self):
            return func(self, *params.args, **params.kwargs)

    else:
        def test_case_func(self):
            raise params.reason

    test_case_func.__name__ = params.name
    setattr(cls, params.name, test_case_func)


# Internal data structures


class ParamsFailure(object):
    """
    FileDataValues generates an instance of this class instead of instances of
    Params in case it cannot load the data file. A fake test method is
    generated instead of a regular one if it has an instance of this class
    among its parameters.

    ParamsFailure supports the same interface as Params.

    More formally, instances of Params and ParamsFailure form a semigroup with
    respect to addition (+) with ``Params(None, [], {}`` being a left identity.
    The ``unpack()`` method is a homomorphism.

    Instances of ParamsFailure act almost as absorbing elements (0.X=0, X.0=0).
    The left-most instance of ParamsFailure in a sum prevails, only the name
    keeps updating.

    """

    def __init__(self, name, reason):
        self.name = name
        self.reason = reason

    def unpack(self, N=1):
        """
        Do nothing but return self (convenient for use in mappings).

        """
        return self

    def __add__(self, other):
        """
        Return a sum of self and an instance of Param or ParamFailure.

        The sum is a new instance of ParamFailure with the `reason` from the
        left operand and a name combining names of both operands.

        """
        new_name = combine_names(self.name, other.name)
        return ParamsFailure(new_name, self.reason)


class Params(object):
    """
    Instances of Params form a semigroup with respect to addition.
    ``Params(None, [], {})`` constitutes the identity. The ``unpack()``
    function is a homomorphism.

    """

    def __init__(self, name, args, kwargs):
        self.name = name
        self.args = args
        self.kwargs = kwargs

    def unpack(self, N=1):
        """
        Recursively unpack positional arguments `N`-times.

        """
        while N > 0:
            self.unpack_one_level()
            N = N - 1
        return self

    def unpack_one_level(self):
        """
        Unpack one level of positional arguments.

        Members of lists and tuples replace its parents as new positional
        arguments. Members of dicts are used to update keyword arguments. Other
        positional arguments are left intact.

        """
        new_args = []

        for value in self.args:
            if isinstance(value, list) or isinstance(value, tuple):
                new_args.extend(value)
            elif isinstance(value, dict):
                self.kwargs.update(value)
            else:
                new_args.append(value)

        self.args = new_args

    def __add__(self, other):
        """
        Return a sum of self and an instance of Param or ParamFailure.

        If combined with Params, positional arguments in the right operand are
        concatenated to positional arguments in the left operand and keywrd
        arguments in the right operand are used to update keyword arguments in
        the left operand.

        Note: Addition modifies the left-most instance of Params in a sum. This
        is OK for the expected use where a fresh identity Params(None, [], {})
        is supplied as the leftmost operand.

        If combined with ParamsFailure, a new instance of ParamsFailure is
        returned.
        """
        new_name = combine_names(self.name, other.name)

        if isinstance(other, ParamsFailure):
            return ParamsFailure(new_name, other.reason)

        self.name = new_name
        self.args.extend(other.args)
        self.kwargs.update(other.kwargs)
        return self


class InlineDataValues(object):
    """
    This class represents values supplied to a ``data`` decorator.

    Instances of this class are generators which yield an instance of Params
    for each positional and keyword argument passed to the constructor.

    """

    def __init__(self, *unnamed_values, **named_values):
        """
        Stores all arguments passed to the constructor for later use.

        """
        self.unpack_count = 0
        self.unnamed_values = unnamed_values
        self.named_values = named_values

    def unpack(self):
        """
        Increases by one the number of times values should be unpacked before
        passing them to the test function.

        This method is called directly by the ``unpack`` decorator.

        """
        self.unpack_count = self.unpack_count + 1

    def use_class(self, cls):
        """
        Does nothing and returns self.

        This method just makes sure that `InlineDataValues` and
        `FileDataValues` implement the same interface.

        """
        return self

    def __iter__(self):
        for idx, value in enumerate(self.unnamed_values):
            name = make_params_name(idx, None, value)
            yield Params(name, [value], {}).unpack(self.unpack_count)

        for idx, key in enumerate(
                sorted(self.named_values),
                start=len(self.unnamed_values)
        ):
            value = self.named_values[key]
            name = make_params_name(idx, key, value)
            yield Params(name, [value], {}).unpack(self.unpack_count)


class FileDataValues(object):
    """This class represents values supplied to a ``file_data`` decorator.

    Instances of this class are generators which load data from a given JSON
    file and yield an instance of Params for each member of the top-level
    structure (``list`` or ``dict``).

    The generator yields just one item if it fails to load data from the file.
    The item is an instance of ParamsFailure that carries details about the
    failure.

    """

    def __init__(self, filepath, encoding=None):
        """
        Stores all arguments passed to the constructor for later use.

        """
        self.unpack_count = 0
        self.pathbase = ''
        self.filepath = filepath
        self.encoding = encoding

    def use_class(self, cls):
        """
        Sets base path for reading the file to the directory that contains the
        module where the class ``cls`` is defined.

        """

        # Is there perhaps a way the constructor could retrieve this
        # information somehow? This smells like a workaround that messes the
        # interface.

        cls_path = os.path.abspath(inspect.getsourcefile(cls))
        self.pathbase = os.path.dirname(cls_path)
        return self

    def unpack(self):
        """
        Increase by one the number of times values should be unpacked before
        passing them to the test function.

        This method is called directly by the @unpack decorator.

        """
        self.unpack_count = self.unpack_count + 1

    def load_data(self):
        try:
            filepath = os.path.join(self.pathbase, self.filepath)
            with io.open(filepath, encoding=self.encoding) as file:
                data = json.load(file)

            return data

        except IOError as reason:
            # IOError is an alias for OSError since Python 3.3
            return ParamsFailure(reason.__class__.__name__, reason)

        except ValueError as reason:
            return ParamsFailure(reason.__class__.__name__, reason)

    def __iter__(self):
        data = self.load_data()

        if isinstance(data, ParamsFailure):
            yield data

        elif isinstance(data, list):
            for idx, value in enumerate(data):
                name = make_params_name(idx, None, value)
                yield Params(name, [value], {}).unpack(self.unpack_count)

        elif isinstance(data, dict):
            for idx, key in enumerate(sorted(data)):
                value = data[key]
                name = make_params_name(idx, key, value)
                yield Params(name, [value], {}).unpack(self.unpack_count)


# Test name generation


def is_hash_randomized():
    """
    Check whether hashes are randomized in the current Python version.

    See `convert_to_name` for details.

    """
    return (((sys.hexversion >= 0x02070300 and
              sys.hexversion < 0x03000000) or
             (sys.hexversion >= 0x03020300)) and
            sys.flags.hash_randomization and
            'PYTHONHASHSEED' not in os.environ)


def is_trivial(value):
    """
    Check whether a value is of a trivial type (w.r.t. `TRIVIAL_TYPES`).

    """
    if isinstance(value, TRIVIAL_TYPES):
        return True

    if isinstance(value, (list, tuple)):
        return all(map(is_trivial, value))

    return False


def convert_to_name(value):
    """
    Convert a value into a string that can safely be used in an attribute name.

    Returns a string representation of the value with all extraneous characters
    replaced with ``_``. Sequences of underscores are reduced to one, leading
    and trailing underscores are trimmed.

    Raises ValueError if it cannot convert the value (see the note below).

    Note: If hash randomization is enabled (a feature available since
    2.7.3/3.2.3 and enabled by default since 3.3) and a "non-trivial" value is
    passed this will omit the name argument by default. Set `PYTHONHASHSEED` to
    a fixed value before running tests in these cases to get the names back
    consistently or use the `__name__` attribute on data values.

    A "trivial" value is a plain scalar, or a tuple or list consisting
    only of trivial values.

    """

    # We avoid doing str(value) if all of the following hold:
    #
    # * Python version is 2.7.3 or newer (for 2 series) or 3.2.3 or
    #   newer (for 3 series). Also sys.flags.hash_randomization didn't
    #   exist before these.
    # * sys.flags.hash_randomization is set to True
    # * PYTHONHASHSEED is **not** defined in the environment
    # * Given `value` argument is not a trivial scalar (None, str,
    #   int, float).
    #
    # Trivial scalar values are passed as is in all cases.

    if not is_trivial(value) and is_hash_randomized():
        raise ValueError("Cannot convert complex type: {0}", str(type(value)))

    try:
        value = str(value)
    except UnicodeEncodeError:
        # fallback for python2
        value = value.encode('ascii', 'backslashreplace')

    value = re.sub('\W', '_', value)
    return re.sub('_+', '_', value).strip('_')


def make_params_name(idx, name, value):
    """
    Generate a name for a value in a parameters set.

    It will take the ordinal index of the value in the set and a name
    constructed from one of the follwing items (with decreasing priority):
    `name`, `value.__name__`, `value`. See also `convert_to_name`.

    If all of that fails, only the ordinal index is used.
    """

    if name is None:
        name = getattr(value, '__name__', value)

    try:
        name = convert_to_name(name)
        return "{0}_{1}".format(idx, name)

    except ValueError:
        pass

    return "{0}".format(idx)


def combine_names(name1, name2):
    """
    Combine two names using two underscore characters ``__``. ``None`` can be
    used as the identity.

    """
    if name2 is None:
        return name1
    else:
        if name1 is None:
            return name2
        else:
            return"{0}__{1}".format(name1, name2)
