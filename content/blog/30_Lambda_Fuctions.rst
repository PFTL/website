Intro to Python Lambda Functions
================================

:status: draft
:date: 2019-03-17
:author: Aquiles Carattino
:subtitle: Anonymous functions are powerful, but they are hard to understand
:header: {attach}luca-bravo-217276-unsplash.jpg
:tags: functions, methods, arguments, packing, unpacking, args, kwargs
:description: Anonymous functions are powerful, but they are hard to understand

Some time ago, Python introduced in its syntax the possibility to define functions using ``lambda`` instead of ``def``. These functions are called anonymous and are very common in other languages such as Javascript. However, in Python they seem a bit obscure and are often either overlooked or misused. In this article we are going to introduce the lambda functions and discuss where and how to use it.

To define a function, you can use the following syntax:

.. code-block:: python

    def average(x, y):
        return (x+y)/2

Then, if you would like to calculate the average of two numbers, you can simply do:

.. code-block:: python

    avg = average(2, 5)

In such case, ``avg`` would have a value of ``3.5``. We could also define ``average`` like this:

.. code-block:: python

    average = lambda x, y: (x+y)/2

If you test this function, you will see that the output is exactly the same. It is important to point out that the syntax is very different between ``def`` and ``lambda``. First, we define the arguments ``x`` and ``y`` without any parenthesis. Then, we define the operation that we want to apply. Note that the ``return`` is implicit when you use a lambda function.

There are, however, more fundamental differences. Lambda functions must be expressed on only one line, and they have no docstring. If you try ``help(average)`` on each definition above, you will see that the output is very different. Moreover, there is no way of documenting what the second version of ``average`` is actually doing.

Functionally speaking, both ways of defining ``average`` give the same result. So far, the difference between them is very subtle. The main advantage of *lambda* (or anonymous) functions is that they don't need a name. Moreover, assigning a name like what we did above is considered bad practice, as we will discuss later on. Let's now see in what context you would like to use a lambda function instead of a normal function.

Most tutorials focus on lambda functions for sorting a list. We can do the same before going to other topics. Imagine that you have the following list:

.. code-block:: python

    var = [1, 5, -2, 3, -7, 4]

Imagine you would like to sort the values, you can do:

.. code-block:: python

    sorted_var = sorted(var)
    # [-7, -2, 1, 3, 4, 5]

That is easy enough. But what would happen if you would like to sort the values based on the distance to a given number? You need to apply a function to each number, such as ``abs(x-1)`` if you are computing the distance to 1, and sort the values based on the output. Fortunately ``sorted`` allows you to do that using the keyword argument ``key=``. We could do:

.. code-block:: python

    def distance(x):
        return abs(x-1)

    sorted_var = sorted(var, key=distance)
    # [1, 3, -2, 4, 5, -7]

Another option, would be to use a lambda function:

.. code-block:: python

    sorted_var = sorted(var, key=lambda x: abs(x-1))

Both examples are going to produce the exact same output. There is no functional difference between defining a function using ``def`` or using ``lambda``. I can argue that the second example is slightly shorter than the first one. Also, it makes the code more readable, since you can immediately see what are you doing to each element (``abs(x-1)``) instead of digging through your code to see where ``distance`` was defined.

Another possibility is to use it in combination with ``map``. Map is a way of applying a function to every element on a list. For example, based on the example above, we can do:

.. code-block:: python

    list(map(distance, var))
    # [0, 4, 3, 2, 8, 3]

Or, using the lambda expressions:

.. code-block:: python

    list(map(lambda x: abs(x-1), var))
    # [0, 4, 3, 2, 8, 3]

Which gives the exact same output and, again, one can argue which one is easier to read. The examples above are what you may see in other tutorials. Probably is what you will see if you go through StackOverflow. One of the possibilities is to use lambda functions in combination with Pandas.

Pandas and Lambda Functions
---------------------------
The example data was inspired by `this <https://data36.com/pandas-tutorial-1-basics-reading-data-files-dataframes-data-selection/>`_ example, and can be found here.