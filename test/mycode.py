"""
Some simple functions that we will use in our tests.
"""


def larger_than_two(value):
    return value > 2


def has_three_elements(value):
    return len(value) == 3


def is_a_greeting(value):
    return value in ['Hello', 'Goodbye']
