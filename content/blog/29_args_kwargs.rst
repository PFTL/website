What are args and kwargs and when to use them
=============================================

:date: 2019-03-10
:author: Aquiles Carattino
:subtitle: How to develop functions with a variable number of arguments
:header: {attach}luca-bravo-217276-unsplash.jpg
:tags: functions, methods, arguments, packing, unpacking, args, kwargs
:description: How to develop functions with a variable number of arguments

If you have worked with Python for long enough, probably you have encountered code that uses ``*args`` and ``**kwargs`` as arguments in functions. Even if you haven't, it is a very neat feature that allows you to achieve great flexibility while developing code. In this article, we are going to discuss what and how to use flexible arguments in functions.

.. contents::

Args
----
Let's quickly see how ``*args`` work in a function:

.. code-block:: python

    def test_function(*args):
        print(type(args))
        for arg in args:
            print(arg)

    test_function('a', 'b', 1, 2)

Which will output:

.. code-block:: python

    <class 'tuple'>
    a
    b
    1
    2

What you are seeing is that ``test_function`` can take any number of arguments. When you use the ``*`` in front of a variable, it will convert any number of inputs into a tuple. You can access each argument according to its index. For example, you could get the first value by doing ``args[0]``, etc. Remember that when you develop functions, it is the order of the inputs that matter.

It is also possible to mix explicit arguments with ``*args``, for example:

.. code-block:: python

    def test_function(first, second, *args):
        print(first)
        print(second)
        for arg in args:
            print(arg)

The main difference here is that ``first`` and ``second`` are mandatory. This two options would work fine:

.. code-block:: python

    test_function('first', 2, 'a', 'b', 'c')
    test_function('first', 2)

while this one would throw an exception:

.. code-block:: python

    test_function('first')
    [...]
    TypeError: test_function() missing 1 required positional argument: 'second'

So far, it is clear that you can use ``*args`` to accept a variable number of arguments in a function. But the other path is also possible. Imagine you have a tuple and you would like to use it as arguments for a function. For example, let's assume we have a function like this:

.. code-block:: python

    def fixed_args(first, second):
        print(first)
        print(second)

We can use the function like this:

.. code-block:: python

    vars = ('First', 'Second')
    fixed_args(*vars)

Which is very convenient in a lot of different situations, especially when you may have so many inputs that it wouldn't be practical to try to do something like:

.. code-block:: python

    fixed_args(vars[0], vars[1])

It is important to note here that Python doesn't force you to use ``*args`` in its syntax as an argument for a function. You are free to choose whatever variable name you would like. However, ``*args`` is a convention that almost every developer follows. Using it will make your code much more readable and understandable by others and your future self.

The action of transforming a tuple (or a list) to different inputs of a function is called unpacking. But we are not limited to tuples and lists. We can go one step further and use a generator, such as ``range``:

.. code-block:: python

    def test_function(first, second):
        print(first)
        print(second)

    a = range(1, 3)
    test_function(*a)

Working with generators is a different topic, that I will cover in another tutorial, but for the time being, it is important to note that the ``*`` can have a great impact when used in combination with the arguments of functions.

.. newsletter::

Kwargs
------
The idea of ``kwargs`` is very similar to that of ``args``, but instead of a tuple or a list, these are keyword-arguments. This means that instead of the order in which they appear, the importance is in the label that each variable has. A quick example:

.. code-block:: python

    def test_kwargs(**kwargs):
        for key, value in kwargs.items():
            print(key, '=>', value)

In this case, ``test_kwargs`` takes a variable number of keyword-variables. To use it, we can do something like the following:

.. code-block:: python

    test_kwargs(first=1, second=2)

Which outputs:

.. code-block:: python

    first => 1
    second => 2

If you try to run the function without keywords, it will through an exception. In the same way that when ``*args`` was used as the argument of a function, the inputs were transformed to a tuple, ``**kwargs`` are transformed to a dictionary. Here, the important detail is the use of the ``**`` instead of the single ``*``. Of course, you can mix required and variable inputs, for example:

.. code-block:: python

    def test_function(first, **kwargs):
        print(first)
        print('Number kwargs: ', len(kwargs))

Which will give you the following outputs:

.. code-block:: pycon

    >>> test_function(1)
    1
    Number kwargs:  0
    >>>test_function(1, second=2, third=3)
    1
    Number kwargs:  2

In the same way, as we used ``*args`` to unpack a tuple, we can unpack a dictionary. Let's first consider a function with some required arguments:

.. code-block:: python

    def test_unpack(first, second, third):
        print(first)
        print(second)
        print(third)

And for unpacking a dictionary, we can do the following:

.. code-block:: python

    vars = {'second': 2,
        'first': 1,
        'third': 3}

    test_unpack(**vars)

Which will give as output:

.. code-block:: python

    1
    2
    3

Pay attention to the fact that we are not defining the variables in any special order, but the importance is in the keywords used for building the dictionary. We could have also done:

.. code-block:: python

    vars = (2, 1, 3)
    test_unpack(*vars)

Which would produce the following output:

.. code-block:: python

    1
    3
    2

Now you have a broad idea of how the ``*`` and ``**`` operators work to pack and unpack arguments in functions. What you have to remember is that the ``*`` can be used to transform a tuple or list to the arguments of a function in a specific order. On the other hand, the ``**`` can be used to transform a dictionary to keyword arguments of functions, in which the order is not important but the label is.

On the other hand, functions that accept arguments with either ``*`` or ``**`` can have a variable number of arguments. The first works for arguments in a certain order, while the latter works for keyword-arguments. After reading the above sections, you can be tempted to start using ``args`` and ``kwargs`` in your functions. However, you have to be aware of the implications.

When not to use args and kwargs
-------------------------------
When you expand your programming toolbox, there is a common desire to use what you have just learned at every possibility that you encounter. However, you have to be aware of the consequences and advantages of using ``args`` and ``kwargs`` in your code. Let's consider, for example, a function that calculates the area of a triangle. We could define it like this:

.. code-block:: python

    def area(base, height):
        return base*height/2

If you look at the code above, you can easily understand what is going on. If you want to use what you have just learned, we can re-write the code to:

.. code-block:: python

    def area(*args):
        return args[0]*args[1]/2

Both examples can be used in the same way, but I hope you do agree that the latter is harder to understand. Moreover, the function can be called with any number of arguments. If you are using a Python IDE such as Pycharm, VS Code, they show you what arguments a function takes, but if you have ``*args`` you will have no idea what needs to be supplied.

When to use args and kwargs
---------------------------
Imagine someone else is using your code. The functions developed earlier have only two lines and you can quickly read through them. But if you have developed a much more complex function, how would someone reading your code understand how many arguments and which ones to supply? The same objections apply when you use ``kwargs``. Good code is also code that can be read and quickly understood.

Decorators
~~~~~~~~~~

Keeping in mind that it is impossible to make a comprehensive list of situations when it is worth using kwargs and args, we can discuss some examples. The first that comes to mind is when you are dealing with `decorators <{filename}04_how_to_use_decorators_2.rst>`_. To give a very short summary, a decorator is a function that wraps another one in order to extend its functionality without changing the core behavior. Going back to the example of the area, the function

.. code-block:: python

    def area(base, height):
        return base*height/2

Works for any pair of numbers, also negative ones. Imagine that we would like to check whether the arguments of the function are non-negative, but we don't want to change the function itself, we can develop a decorator:

.. code-block:: python

    from functools import wraps

    def check_positive(func):
        @wraps(func)
        def func_wrapper(*args):
            for arg in args:
                if type(arg) is int or type(arg) is float:
                    if arg < 0:
                        raise Exception("Function {} takes only positive arguments".format(func.__name__))
                else:
                    raise Exception("Arguments of {} must be numbers".format(func.__name__))
            return func(*args)

        return func_wrapper

If you are not familiar with decorators or the code above seems confusing, I recommend you check `this article <{filename}04_how_to_use_decorators_2.rst>`_. To use this decorator, we would simply do the following:

.. code-block:: python

    @check_positive
    def area_positive(base, height):
        return base*height/2

    print(area_positive(1, 2))
    print(area_positive(-1, 2))

And now you will see that an exception will be thrown with the second line using a negative value for the base. If you pay attention, notice that we have used ``*args`` in the decorator. This allows us to use the same decorator for any function, not only the area. Imagine we would like to calculate the perimeter of a triangle, we could simply do:

.. code-block:: python

    @check_positive
    def perimeter(side1, side2, side3):
        return side1+side2+side3

The ``*args`` (or ``**kwargs``) are incredibly useful to have a flexible decorator. If you go to the article linked earlier, you will see that the first couple of examples always use a fixed number of arguments, thus making the decorator applicable only to certain cases.

Inheritance
~~~~~~~~~~~
Another very common scenario where ``args`` and ``kwargs`` is very handy is when you are working with classes. In order to expand the functionality of classes developed by others, a common pattern is to inherit them and override the methods you would like to change. This is very frequent when you are dealing with large libraries or frameworks. For example, if you are developing a `Qt application <{filename}22_Step_by_step_qt.rst>`_, you will find yourself with code like this:

.. code-block:: python

    class MainWindow(QMainWindow):
        def __init__(self, *args):
            super(MainWindow, self).__init__(*args)

The rest of the code will do the specific parts of your application. The snippet above shows that we don't need to look at the original code to see what arguments are passed, etc. They are simply relayed to the original ``QMainWindow`` class when instantiating. Moreover, if there is code downstream that is already using ``QMainWindow``, we can use ``MainWindow`` as a drop-in replacement, without the need to explicitly change every time the class is used.

If you are familiar with frameworks such as **Django** and you are overriding a method such as ``save`` (you can see `the docs here <https://docs.djangoproject.com/en/2.1/ref/models/instances/#django.db.models.Model.save>`_), you can use the following syntax on your own model:

.. code-block:: python

    def save(self, **kwargs):
        # Your custom code goes here
        super().save(**kwargs)

In this way, your code is future proof. Perhaps today you are not using some of the arguments that ``save`` takes, but by taking a flexible number of them, you know that if tomorrow you decide to start using some, your program will not break. Pay attention to the fact that we used only ``**kwargs``. This is a choice to force the use of keyword arguments, mainly because it is a function with a lot of arguments, each with a default value, and we may be interested in altering only one of them.

Flexibility
~~~~~~~~~~~
Sometimes flexibility in the number of arguments is needed. A classical example is Python's ``dict``. When you create a dictionary, you can use the following syntax:

.. code-block:: python

    a = dict(one=1, two=2, three=3)

However, the arguments of ``dict`` are not fixed. You could have as well used:

.. code-block:: python

    b = dict(first=1, second=2, third=3)

The fact that dict can take any keyword argument set is an asset. If you look at `the documentation <https://docs.python.org/3.7/library/stdtypes.html#dict>`__, it explicitly shows you that dict can be called with ``dict(**kwarg)``. If you look at `Django's Model <https://docs.djangoproject.com/en/2.1/_modules/django/db/models/base/#Model>`_, you will also see that the ``__init__`` method takes ``args`` and ``kwargs``. This is because the framework wanted to have a great degree of flexibility while instantiating a class. If you look at the code, you will see that there are a lot of checks and loops in order to prepare the object based on the available arguments.

Conclusions
-----------
Having a variable number of arguments in functions and methods can help you develop a much more flexible code. However, this normally comes at a cost in readability. Understanding where it can be useful to use ``*args`` or ``*kwargs`` in your functions requires practice and, more importantly, reading other's code. You may find great examples if you just look around the libraries you are already using and you wonder how is it possible that sometimes you use a different number of arguments.

The opposite path, of using the ``*`` or ``**`` syntax to pass a tuple or a dictionary as arguments to a function can greatly simplify your code. A very simple example would be what happens when you import data using ``pyyaml``, for example. You end up with a dictionary, that perhaps you would like to directly pass to a function. Unpacking arguments is very useful, especially when you are not in control of the functions that you are using.

The source version of this article is available `on Github <https://github.com/PFTL/website/blob/master/content/blog/29_args_kwargs.rst>`_. The code examples are `available here <https://github.com/PFTL/website/tree/master/example_code/29_args_kwargs>`_.

Header photo by `Luca Bravo <https://unsplash.com/photos/XJXWbfSo2f0?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText>`_ on Unsplash