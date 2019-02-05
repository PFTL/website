How to use decorators Part 2
============================

:date: 2018-05-18
:author: Aquiles Carattino
:subtitle: Use decorators like a professional
:header: {attach}michael-browning-227688-unsplash.jpg
:tags: Decorators, Python, Tricks, Validation, Data, Intermediate
:description: Learn how to use decorators like a professional

Decorators are a very useful programming pattern that allows changing the behavior of functions with little refactoring. Decorators allow developers to abstract common options from functions, but mastering their use in Python can be challenging. In this article, we are going to go in depth regarding different options when implementing decorators. The topics covered are:

.. contents::

In a `previous article on the use of decorators to validate user input <{filename}01_how_to_use_decorators.rst>`_, we have seen just the very beginning of what decorators are able to provide to the developer. Let's first recap what we saw earlier. We can define a decorator as a function that will take as input another function. We can use it to check the input of the latter, for example:

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

In the first case, the function would work, giving as output ``1.5``, while in the second case it would raise an exception because one of the arguments is not positive. If you can't understand the code above, you should check the `first article published on decorators <{filename}01_how_to_use_decorators.rst>`_.

Docstrings with decorators
--------------------------
This example works fine, but it already shows an issue that for larger projects is very relevant: docstrings, i.e. the documentation of functions, methods, and classes, stop working when using decorators like above. Let's add documentation to the function ``average``, like this:

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
        [...]

The ``[...]`` means that there is code being suppressed for brevity. If again we try to get the help of our function:

.. code-block:: pycon

    >>> help(average)
    func_wrapper(x, y)

As you can see, the docstring of the function ``average`` was replaced by the docstring of the wrapper, which in the example above is empty. What we can do to avoid this problem is to pass the docstring and the name of the function to the name and docstring of the decorator. Like this:

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
        [...]

As with many things in Python, this is not the only option but is the one that allows you to see how some of the internals work, such as the ``__name__`` and ``__doc__`` properties. Another option is to use a built-in decorator from Python that would allow you to do exactly what we have done but in one single line:

.. code-block:: python
    :hl_lines: 1 4

    from functools import wraps

    def check_positive(func):
        @wraps(func)
        def func_wrapper(x, y):
            if x < 0 or y < 0:
                raise Exception("Both x and y have to be positive for function {} to work".format(func.__name__))
            res = func(x, y)
            return res
        return func_wrapper

The highlighted lines are the ones that changed compared to the previous example. Again, the ``help`` command is working as expected. In principle what the decorator ``@wraps`` does is the same as setting the ``__name__`` and ``__doc__`` properties. Now you start seeing that the uses of decorators are virtually endless.

.. newsletter::

Arguments in decorators
-----------------------
Imagine that you want to be able to check that both arguments in a function are higher than a parameter, not necessarily ``0``. This would imply that the decorator takes one argument. Let's see first what do we want to achieve and then how to do it.

.. code-block:: python

    @check_above(2)
    def average(x, y):
        return (x + y)/2

We expect the function ``average`` to work only if both ``x`` and ``y`` are larger than 2. This is very useful when you are communicating with a device, for example, and you want to be sure that you are passing values which are allowed. However, the decorator that we defined earlier takes as an argument only the function to be decorated and it will fail if we add anything else. Solving this is a bit more involved because it requires a function that returns a decorator. We can do the following:

.. code-block:: python

    def check_above(threshold):
        def wrap(func):
            @wraps(func)
            def func_wrapper(x, y):
                if x < threshold or y < threshold:
                    raise Exception("Both x and y have to be larger than {} \
                    for function {} to work".format(threshold, func.__name__))
                res = func(x, y)
                return res
            return func_wrapper
        return wrap

Let's see step by step what is going on. The function ``check_above`` returns the decorator called ``wrap``. Therefore, technically, the function will be decorated with ``wrap`` and not with ``check_above``, but now we can use the parameter ``threshold``. We have translated everything one layer deeper, but the behavior is essentially the same. Note that now you check that both ``x`` and ``y`` are above the ``threshold``. If you try to calculate the average like this:

.. code-block:: python

    average(1, 2)

it will raise the exception because one of the values is not above the specified threshold.

When are decorators executed
----------------------------
There is something very important to note: both decorators defined earlier, ``check_positive`` and ``check_above`` are actually executed right when defining the ``average`` function. You can test it by adding a ``print`` statement, like this:

.. code-block:: python

    def check_positive(func):
        print('Checking if it is positive')
        @wraps(func)
        def func_wrapper(x, y):
            if x < 0 or y < 0:
                raise Exception("Both x and y have to be positive \
                for function {} to work".format(func.__name__))
            res = func(x, y)
            return res

        return func_wrapper

Whenever you import the module that contains the ``average`` function, you will see:

.. code-block:: pycon

    >>> from utils import average
    Checking if it is positive

This behavior may not be completely expected nor desired. For example, imagine that you use a decorator that checks the status of a device before allowing the user to send a new command to it. If you place the verification routine outside of the function wrapper, it will be triggered when you import the function and not when you execute it. This can give rise to a lot of undesired errors because it is understandable that a user is importing the needed functions first and then starting the communication with a device.

On the other hand, being able to run code before the function is executed, opens different doors. For example, you could register all the available functions. Check the following example:

.. code-block:: python

    # utils.py
    from functools import wraps

    func_registry = []

    def register(func):
        func_registry.append(func.__name__)
        @wraps(func)
        def func_wrapper(*args):
            return func(*args)
        return func_wrapper

    @register
    def average(x, y):
        return (x + y)/2

    @register
    def geom_average(x, y):
        return (x*y)**0.5

Now you can use it in the following way:

.. code-block:: python

    >>> from utils import average
    >>> average(1, 2)
    1.5
    >>> from utils import func_registry
    >>> for f in func_registry:
    ...     print(f)
    ...
    average
    geom_average

With this simple code, you already see that not only ``average``, but also ``geom_average`` is decorated with ``@register``. This is very useful if, for example, you want to have a list of a specific set of functions. Imagine that you are developing a driver for a device, and some of the methods are equivalent to buttons, i.e., you trigger an action by pressing it, but no input is required and no output is generated. *Switch on*, *Switch off*, *Auto calibrate*, etc. It would be handy to have a list of all these methods, in order to display them to an end-user, for example.

When you start designing decorators, especially if you are planning to have other developers to use them, you have to be aware that some behaviors are not always obvious to everybody. Documenting is crucial to have reliable and maintainable libraries. Mixing the execution of code with the definition of a function may give a lot of headaches to novice developers and may become a nightmare to debug later on.

Decorators for methods in classes
---------------------------------
So far we have covered how to use decorators for functions, but more often than not you will find yourself using decorators for methods in classes. For example, you would like to use the ``check_positive`` like this:

.. code-block:: python

    # operations.py
    class Operations:
        @check_positive
        def average(self, x, y):
            return (x + y)/2

I know that a class like that makes no sense at all, but it is only an example, so please bear with me. If you want to use this class, you will face an error:

.. code-block:: pycon

    >>> from operations import Operations
    [...]
    TypeError: func_wrapper() takes 2 positional arguments but 3 were given

When we defined the ``check_positive`` decorator, we explicitly used two arguments for the ``func_wrapper``, ``x`` and ``y``. However, when we work with methods, there will be one more argument, the ``self``. There are different ways of solving this problem. On one hand, you could adapt the decorator in order to accommodate for the extra input, but then the decorator will stop working with normal functions. Of course, you could define a new decorator just for methods, but you would end up duplicating the code, and you should try to avoid that.

One more general solution would be to use a variable number of arguments for the decorator. This would be the idea:

.. code-block:: python

    from functools import wraps

    def check_positive(func):
        @wraps(func)
        def func_wrapper(*args):
            for arg in args:
                if type(arg) is int or type(arg) is float:
                    if arg < 0:
                        raise Exception("Method {} takes only positive arguments".format(func.__name__))
            return func(*args)

        return func_wrapper

Now you can see that the decorator became more complex than before. First, the ``func_wrapper`` takes ``*args`` as the argument, and no longer explicitly ``x`` and ``y``. The ``*args`` parameter is a good subject for a next tutorial, what you should understand by now is that it makes a list out of all the inputs of the function, regardless of how many they are. This is what allows us to iterate through them by doing ``for arg in args``.

For every argument in the function, we have to check whether they are numbers or not, i.e., if the ``type`` is either ``int`` or ``float``. This prevents us from checking if ``self`` is positive or not, which would raise an exception. If the checks pass, we just return the original function ``func`` with the same arguments ``*args`` which were originally used. You can go ahead and try this decorator with either a method ìn the ``Operations`` class or with a function. Moreover, you can now try it with a function that takes three numbers as input and it will still work.

Classes as decorators
---------------------
So far, we have seen that you can use a function to decorate another function or method. However, that is not the only option. Classes can be used as decorators as well, and this opens an entire realm of possibilities. What we have seen so far is that when you add a callable with a ``@`` just before another callable (i.e. a method or a function in our context), that function will be passed as an argument to the decorator. When constructing classes, you can also pass functions as arguments. For example:

.. code-block:: python

    class Decorator:
        def __init__(self, func):
            print('Decorating {}'.format(func.__name__))
            self.func = func

    @Decorator
    def average(x, y):
        return (x + y)/2


If you execute the code above you will see:

.. code-block:: pycon

    Decorating average

However, if you try to use the average, you will see an error:

.. code-block:: pycon

    >>> average(1, 2)
    [...]
    TypeError: 'Decorator' object is not callable

This is actually expected. What is happening is that the function ``average`` is actually being turned into a ``Decorator`` class. The code would be equivalent to doing something like this:

.. code-block:: python

    average = Decorator(average)

However, after the class has been instantiated, Python doesn't know what does it mean to execute it. We need to explicitly add this behavior:

.. code-block:: python

    class Decorator:
        def __init__(self, func):
            print('Decorating {}'.format(func.__name__))
            self.func = func

        def __call__(self, *args, **kwargs):
            return self.func(*args)

With this change, we have instructed Python what does it means to *call* the object, i.e., to do ``average(...)``. If we run it again, it will work:

.. code-block:: pycon

    >>> averge(1, 2)
    1.5

Remember that, just as before, the instantiation of the ``Decorator`` class is happening when defining the ``average``, and therefore you will see the line ``Decorating average`` when you ``import average``. On the other hand, you have transformed your function into a class:

.. code-block:: pycon

    >>> type(average)
    <class '__main__.Decorator'>

How you can leverage the possibilities of using a class instead of a function for decorating depends on the work you are trying to achieve. Remember that the main use of classes is when you need to preserve state. For example, imagine you would like to store every pair of values on which you have calculated the average. You can easily turn this idea into a cache system, avoiding to repeat processes for known arguments.

Decorators for classes
----------------------
We have seen that any callable can be a decorator of any other callable. That is why a function can be a decorator of another function or method. Also, because a class is a callable, it can be a decorator of a function or method. The last missing combination is to decorate classes. With what you know so far, you can already anticipate what is going to happen. Imagine you want to do this:

.. code-block:: python

    @Decorate
    class MyClass:
        def __init__(self):
            print('My Class')

What you have to remember is that ``Decorate`` needs to accept ``MyClass`` as input. Moreover, we need to actually instantiate the class when we do:

.. code-block:: python

    my_class = MyClass()

Putting all the ideas together, the decorator will look like this:

.. code-block:: python

    def Decorate(cls):
        print('Decorating {}'.format(cls.__name__))
        def class_wrapper(*args):
            return cls(*args)
        return class_wrapper

What will happen is that the class will be passed as the argument of ``Decorate``. We will print that we are decorating the class, just to show that it is actually working. The ``Decorate`` function needs to return another callable object, in the example above is a function called ``class_wrapper``. This function will be responsible for instantiating the class. Remember that when you use decorators, you are actually replacing what happens when you do ``MyClass()`` by what happens when you do ``class_wrapper()``. Therefore, if you decorate the class, you will see that its type changed:

.. code-block:: pycon

    >>> type(MyClass)
    <class 'function'>

The main point here is that the function will return an object. This allows you to instantiate the class as always, regardless of it having or not the decorator:

.. code-block:: pycon

    >>> my_class = MyClass()
    My Class

Decorating classes is a bit of a corner situation. To be honest, I don't imagine a lot of scenarios where you would like to decorate a class, but still, I will give you an example. Imagine that you want to add a new method to every decorated class. A method that will calculate the average between two numbers. What you have to do is to alter the ``cls`` variable within the ``class_wrapper``:

.. code-block:: python

    def Decorate(cls):
        def class_wrapper(*args):
            def average(cls, x, y):
                return (x + y) / 2
            setattr(cls, 'average', average)
            return cls(*args)
    return class_wrapper

We have defined the function ``average`` that takes three arguments: a class and two numbers. And then we use ``setattr`` to add the method to ``cls`` and we call it ``'average'``. Now, ``MyClass`` will be able to calculate the average of numbers even if the method was not defined in it:

.. code-block:: pycon

    >>> my_class = MyClass()
    >>> res = my_class.average(1, 2)
    >>> print(res)
    1.5

Conclusions
-----------
In this tutorial, we have covered a lot of different options when working with decorators. Depending on the kind of projects you are working on, you may not find yourself in the situation of needing to develop decorators, however, it is always useful to be aware of one extra possibility. Decorators are very useful tools when a library is going to be used by other developers.

Two libraries that make heavy use of decorators are `Flask <http://flask.pocoo.org/>`_ and `Lantz <https://github.com/lantzproject/>`_. Therefore, even if you don't develop your own decorators, it is always important to understand how they work.

You can find the `example code for this tutorial <https://github.com/PFTL/website/tree/master/example_code/04_how_to_use_decorators_2>`_ on Github, as well as the `text <https://github.com/PFTL/website/blob/master/content/blog/04_how_to_use_decorators_2.rst>`_. If you find any mistakes, don't hesitate to submit a pull request or open an Issue.


Header photo by `Michael Browning <https://unsplash.com/photos/tOZ-f5kl9BA?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText>`_ on Unsplash