Misc
====

This page contains some of the miscellaneous functionality.

Docstring Handling
------------------

If one of the passed data objects has a docstring, the resulting testcase borrows it.

.. code-block:: python

    d1 = Dataobj()
    d1.__doc__ = """This is a new docstring"""

    d2 = Dataobj()

    @data(d1, d2)
    def test_something(self, value):
        """This is an old docstring"""
        return value


The first of the resulting test cases will have ``"""This is a new docstring"""`` as its docstring and the second will
keep its onw one (``"""This is an old docstring"""``).