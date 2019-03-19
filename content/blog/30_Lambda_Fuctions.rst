Intro to Python Lambda Functions
================================

:date: 2019-03-17
:author: Aquiles Carattino
:subtitle: Anonymous functions are powerful, but they are hard to understand
:header: {attach}ivana-cajina-324103-unsplash.jpg
:tags: functions, methods, arguments, packing, unpacking, args, kwargs
:description: Anonymous functions are powerful, but they are hard to understand

Some time ago, Python introduced in its syntax the possibility to define functions using ``lambda`` instead of ``def``. These functions are called anonymous and are very common in other languages such as Javascript. However, in Python, they seem a bit obscure and are often either overlooked or misused. In this article, we are going to introduce the lambda functions and discuss where and how to use it.

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

Another option would be to use a lambda function:

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

.. newsletter::

Pandas and Lambda Functions
---------------------------
The example data was inspired by `this <https://data36.com/pandas-tutorial-1-basics-reading-data-files-dataframes-data-selection/>`_ example and can be found `here <https://github.com/PFTL/website/blob/master/example_code/30_lambdas/example_data.csv>`__. Create a file **example_data.csv** with the following content:

.. code-block:: csv

    animal,uniq_id,water_need
    elephant,1001,500
    elephant,1002,600
    elephant,1003,550
    tiger,1004,300
    tiger,1005,320
    tiger,1006,330
    tiger,1007,290
    tiger,1008,310
    zebra,1009,200
    zebra,1010,220
    zebra,1011,240
    zebra,1012,230
    zebra,1013,220
    zebra,1014,100
    zebra,1015,80
    lion,1016,420
    lion,1017,600
    lion,1018,500
    lion,1019,390
    kangaroo,1020,410
    kangaroo,1021,430
    kangaroo,1022,410

To read the data as a DataFrame, we can simply do the following:

.. code-block:: python

    import pandas as pd

    df = pd.read_csv('example_data.csv', delimiter = ',')

Imagine you would like to capitalize the first letter of each animal's name on the data frame, you can do:

.. code-block:: python

    df['animal'] = df['animal'].apply(lambda x: x.capitalize())
    print(df.head())

And you will see the results. Of course, lambda functions can become much more complex. You can apply them to an entire series instead of single values, you can combine them with other libraries such as numpy or scipy and perform complex transformations to your data.

One of the biggest advantages of lambda functions is that if you are using Jupyter notebooks, you can see the changes right away. You don't need to open another file, run a different, cell, etc. If you go to the `Pandas documentation <https://pandas.pydata.org/pandas-docs/version/0.22/generated/pandas.DataFrame.apply.html>`_ you will see that lambdas are used quite often.

Qt Slots
--------
Another common example of using lambdas is in combination with the Qt library. We have written an `introductory article on Qt <{filename}22_Step_by_step_qt.rst>`_ in the past. Feel free to browse through it if you are not familiar with how building user interfaces work. A very minimal example, that just shows a button, it looks like this:

.. code-block:: python

    from PyQt5.QtWidgets import QApplication, QPushButton

    app = QApplication([])

    button = QPushButton('Press Me')
    button.show()

    app.exit(app.exec())

If you would like to trigger an action when pressing the button, that action has to be defined as a function. If we want to print something to screen when the button gets pressed, we can simply add the following line right before ``app.exit``:

.. code-block:: python

    button.clicked.connect(lambda x: print('Pressed!'))

If you run the program again, every time you press the button you will see the ``Pressed!`` appearing on the screen. Again, using lambda functions as slots for signals can speed up your coding and make your programs easier to read. However, lambda functions also need to be considered with caution.

Where to use lambda functions
-----------------------------
Lambda functions can only have 1 line. This forces developers to use them only in contexts where the behavior can be achieved without a complex syntax. In the examples above, you can see that the lambda functions are very simple. If it would have required to open a socket, exchange some information, process the received data, etc. probably it wouldn't have been possible to do it on a single line.

The natural scenario where lambda functions can be used is as arguments for other functions that require callables as arguments. For example, the ``apply`` of a Pandas Data Frame requires a function as an argument. Connecting signals in Qt also requires a function. If the function that we are going to apply or execute is simple, and we are not going to re-use it, writing it as an anonymous function may be a very convenient way.

Where not to use lambda functions
---------------------------------
Lambda functions are anonymous, therefore, if you are assigning a name to them, such as when we did:

.. code-block:: python

    average = lambda x, y: (x+y)/2

It means there is something you are doing wrong. If you need to assign a name to the function, so you can use it in different places of your program, use the standard ``def`` syntax. There is a lengthy discussion on the abuse of lambda functions in Python `on this blog <https://treyhunner.com/2018/09/stop-writing-lambda-expressions/>`_. The one that I have seen quite often, especially by people who have just learned about lambdas, is this:

.. code-block:: python

    sorted_var = sorted(var, key=lambda x: abs(x))

This innocent example may be hard to wrap around if it's the first time that you see lambda functions. But what you have is that you are wrapping a function (``abs``) within another function. It would be like doing:

.. code-block:: python

    def func(x):
        return abs(x)

What is the advantage compared to just doing ``abs(x)``? Indeed, no advantage, this means that we can also sort a list like this:

.. code-block:: python

    sorted_var = sorted(var, key=abs)

If you pay attention to the example that we've developed earlier, we used ``abs(x-1)`` exactly to avoid this redundancy.

Conclusions
-----------
Lambda (or anonymous) functions are a tool that is slowly getting more popular in Python programs. That is why it is very important that you can understand what it means. You have to remember that there is nothing that the lambda syntax allows you to do that it wouldn't be possible to do without them. It is more a matter of convenience, syntax economy, and perhaps readability.

In other programming languages, such as JavaScript, anonymous functions are used very often and have a much richer syntax than in Python. I don't believe Python will head the same way, but in any case, they are a tool that can help you not only with your current programs but they can also help you understand what is going on if you ever tinker with other languages.

Header Photo by `Ivana Cajina <https://unsplash.com/photos/YkYcdn4EbDs?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText>`_ on Unsplash