How to use decorators Part 2
============================

:date: 2018-05-01
:author: Aquiles Carattino
:subtitle: Use decorators like a professional
:header: {attach}michael-browning-227688-unsplash.jpg
:tags: Decorators, Python, Tricks, Validation, Data
:description: Learn how to use decorators like a professional
:status: draft

Decorators are a very useful programming pattern that allows to change the behavior of functions with little refactoring. Decorators allow the developer to abstract common options from functions, but mastering their use in Python can be challenging. In this article we are going to go in depth regarding different options when implementing decorators. The topics covered are:

.. contents::

In a `previous article on the use of decorators to validate user input <{filename}01_how_to_use_decorators.rst>`_, we have seen just the very beginning of what decorators are able to provide to the developer. Let's first recap what we saw earlier. We can define a decorator as a function that will check the input of another, for example:

.. code-block:: python

    def check_positive(func):
        def func_wrapper(x, y):
            if x<0 or y<0:
                raise Exception("Both x and y have to be positive \
                for function {} to work".format(func.__name__))
            res = func(x,y)
            return res
        return func_wrapper


The function ``check_positive`` checks that the inputs of a function are all positive before actually calling the function. To use it, we would do something like this:

.. code-block:: python

    @check_positive
    def average(x, y):
        return (x + y)/2

    a = average(1,2)
    print(a)
    b = average(1, -1)
    print(b)

In the first case the function would work, giving as output ``1.5``, while in the second case it would raise an exception because one of the arguments is not positive. If you can't understand the code above, you should check the `first article published on decorators <{filename}01_how_to_use_decorators.rst>`_.

Docstrings with decorators
--------------------------
This example works fine, but it already shows an issue that for larger projects is very relevant: docstrings, i.e. the documentation of functions, methods and classes, stop working when using decorators. Let's add documentation to the function ``average``, like this:

.. code-block:: python

    def average(x, y):
        """Calculates the average between two numbers."""
        return (x + y)/2

The string right after the definition of the function and starting with the triple quotes ``"""`` is used for building the documentation of projects and is also used with the ``help`` command:

.. code-block:: pycon

    >>> help(average)
    average(x, y)
        Calculates the average between two numbers.

This is very useful when working with libraries developed by others. It also allows you to build documentation, such as the one you find for `numpy <https://docs.scipy.org/doc/numpy-1.14.2/user/quickstart.html>`_, but we will cover this in a later tutorial. However, if we use a decorator, the behavior changes:

.. code-block:: python

    @check_positive
    def average(x, y):
        ...

Remember that ``...`` means that there is code being supressed. If again we try to get the help of our function:

.. code-block:: pycon

    >>> help(average)
    func_wrapper(x, y)

As you can see, the docstring of the function ``average`` was replaced by the docstring of the wrapper, which in the example above is empty. What we can do to avoid this problem is to transform the docstring and the name of the function to the name and docstring of the decorator. Like this:

.. code-block:: python

    def check_positive(func):
        def func_wrapper(x, y):
            if x < 0 or y < 0:
                raise Exception("Both x and y have to be positive for function {} to work".format(func.__name__))
            res = func(x, y)
            return res
        func_wrapper.__name__ = func.__name__
        func_wrapper.__doc__ = func.__doc__
        return func_wrapper

And if we repeat the steps above, we see that the help command is giving the expected output. We can also add a docstring to the decorator:

.. code-block:: python

    def check_positive(func):
        """Decorator to check that the inputs of a function are positive"""
        ...

As with many things in Python, this is not the only option, but is the one that allows you to see how some of the internals work, such as the ``__name__`` and ``__doc__`` properties. Another option is to use a built-in decorator from Python that would allow you to do exactly what we have done:

.. code-block:: python
    :hl_lines: 1, 4

    from functools import wraps

    def check_positive(func):
        @wraps(func)
        def func_wrapper(x, y):
            if x < 0 or y < 0:
                raise Exception("Both x and y have to be positive for function {} to work".format(func.__name__))
            res = func(x, y)
            return res
        return func_wrapper

The highlighted lines are the ones that changed compared to the previous example. Again, the ``help`` command is working as expected.

Header photo by `Michael Browning <https://unsplash.com/photos/tOZ-f5kl9BA?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText>`_ on Unsplash