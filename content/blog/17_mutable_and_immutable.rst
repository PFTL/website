Mutable and Immutable Objects
=============================

:date: 2018-08-23
:author: Aquiles Carattino
:subtitle: Understanding the differences in data types to make better programs
:header: {attach}rawpixel-274862-unsplash.jpg
:tags: Data, Types, Mutable, Immutable, Objects
:description: Understanding the differences in data types to make better programs

People who start programming in Python quickly stumble upon the existence of lists and tuples. They are defined in a similar way, they look the same. Sometimes they are even used interchangeably. The obvious question is, therefore, why do you have two different types of elements for the same goal? The answer lays in understanding the differences between **mutable** and **immutable** data types in Python.

Even after programming Python applications for a while, being conscious about choosing lists or tuples is hard, and sometimes the implications give rise to obscure bugs, very hard to find and correct. In this article, we are going to discuss about the differences between lists and tuples, or more generally about mutable and immutable data types and how they can be used in your programs.

As always, `example code <https://github.com/PFTL/website/tree/master/example_code/17_mutable_immutable>`__ is available and the `source code <https://github.com/PFTL/website/blob/master/content/blog/17_mutable_and_immutable.rst>`__ for this page also.

.. contents::

Lists and Tuples
----------------
In Python, when you want to define a list, you can simply do the following:

.. code-block:: pycon

    >>> var1 = [1, 2, 3]

And you can address its elements by the position:

.. code-block:: pycon

    >>> var1[0]
    1
    >>> var[1]
    2

If you want to replace the value of an element, you can do the following:

.. code-block:: pycon

    >>> var1[0] = 0
    >>> var1[0]
    0

You can do the same with a tuple, which uses ``()`` instead of ``[]`` in its definition:

.. code-block:: pycon

    >>> var2 = (1, 2, 3)
    >>> var2[0]
    1

However, if you try to change the value of an element you will get an error:

.. code-block:: pycon

    >>> var2[0] = 0
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    TypeError: 'tuple' object does not support item assignment

This is the first, crucial difference between a list and a tuple. Once defined, tuples cannot change their values. So, when would you use one or the other depends on the application. The main difference between them is that tuples are very fast when you need to access their values, but lists are much more memory efficient if you would like to expand them.

When you have a variable that cannot be changed after it has been created it is called **immutable**, while in the opposite case, that variable is called **mutable**. Let's explore what that means.

.. newsletter::

Mutable and Immutable Data Types
--------------------------------
There is an `excellent article written by Luciano Ramalho <https://standupdev.com/wiki/doku.php?id=python_tuples_are_immutable_but_may_change>`_ in which he explains how to understand variables in Python. I am not going to copy his article, but I think it is a great inspiration on how to explain things. What he suggests is to think about labels and not about boxes when referring to variables. A variable is a label that we assign to an object, it is the way we, as humans, have to identify it. However, what is important about the underlying object is its value and its type.

A great tool in Python to understand this concept is the ``id`` function. We can apply it to any variable and it will return its identity. If we want to be sure about dealing with the same object, we can check whether the value returned by ``id`` is the same. It is possible to think about the integer that is being returned as the address in memory that is assigned to the object. So, for example, we can do the following:

.. code-block:: pycon

    >>> var1 = [1, 2, 3]
    >>> var2 = (1, 2, 3)
    >>> id(var1)
    44045192
    >>> id(var2)
    43989032

It is easy to see that both variables have different identities. Now we can expand both the list and the tuple with some new values and check whether their identities are the same:

.. code-block:: pycon

    >>> var1 += [4, 5]
    >>> var2 += (4, 5)
    >>> print(var1)
    [1, 2, 3, 4, 5]
    >>> print(var2)
    (1, 2, 3, 4, 5)
    >>> id(var1)
    44045192
    >>> id(var2)
    30323024

What you see in the code above is that we have appended the same values to both the list (``var1``) and the tuple (``var2``). If we ask for the id of them, you will notice that ``var1`` has the same identity as before, while ``var2`` has a new identity. This means that we have expanded the list, but created a completely new tuple. This is why memory management is more efficient for lists than for tuples.

Tuples are not the only immutable data type in Python, but they are a great tool to learn because they can be directly compared to lists, which are mutable. Other immutable data types are:

1. int
2. float
3. decimal
4. complex
5. bool
6. string
7. tuple
8. range
9. frozenset
10. bytes

Most likely you haven't thought about it before, but when you assign an integer, float, etc. to a variable, it can't be replaced. So for example, you will get an output like this if you check the identity of an integer assigned to a variable:

.. code-block:: pycon

    >>> var1 = 1
    >>> id(var1)
    1644063776
    >>> var1 += 1
    >>> id(var1)
    1644063808

You see that a completely new ``var1`` is created when you add a value to itself, therefore its identity changes. The same would happen with all the other data types listed above. **Mutable** objects, on the other hand, are the following:

1. list
2. dictionary
3. set
4. bytearray
5. user defined classes

Those are the kind of objects that can be changed in-place, without creating a new one to store the updated values. An interesting case happens when you give two names to the same variable, for example:

.. code-block:: pycon

    >>> var1 = [0, 1, 2]
    >>> var2 = var1
    >>> id(var1)
    44372872
    >>> id(var2)
    44372872

Both ``var1`` and ``var2`` have the same identity, this means that they are labels to the same object. You can check it by using ``is``:

.. code-block:: pycon

    >>> var1 is var2
    True

And if you update one of the values of ``var1``:

.. code-block:: pycon

    >>> var1 += [3, 4, 5]
    >>> print(var2)
    [0, 1, 2, 3, 4, 5]
    >>> var1 is var2
    True

You see that you updated the value of ``var1`` and the value of ``var2`` also changed. This happens only with mutable types. With immutable objects, since a new object is created in order to update a value, then each name will be pointing to a different object. For example, with strings:

.. code-block:: pycon

    >>> var1 = 'abc'
    >>> var2 = var1
    >>> var1 is var2
    True
    >>> var1 += 'def'
    >>> var1 is var2
    False

Sometimes you would like to compare whether two variables have the same values, and not if they point to the same object. For this, you can use the ``==`` operator. Let's define two lists (or two tuples) with the same values:

.. code-block:: pycon

    >>> var1 = [1, 2, 3]
    >>> var2 = [1, 2, 3]

If you check whether ``var1`` and ``var2`` are the same object, you will get a negative answer:

.. code-block:: pycon

    >>> var1 is var2
    False

Which is logical, because they have the same values, but they are two distinct objects. If you want to compare their values instead, you can do the following:

.. code-block:: pycon

    >>> var1 == var2
    True

An interesting thing happens when you use the so-called singletons. Let's quickly see an example:

.. code-block:: pycon

    >>> a = 1
    >>> b = 1
    >>> a is 1
    True
    >>> a is b
    True
    >>> a == b
    True

Here, it is clear that any variable pointing to the same number will be exactly the same object. The same happens for booleans, ``None``, etc. You can do things like:

.. code-block:: pycon

    >>> a = True
    >>> a is True
    True
    >>> b = None
    >>> b is None
    True
    >>> b == None
    True

Using ``is`` instead of ``==`` has different advantages. The first is speed. You can run the following in your command line:

.. code-block:: bash

    python -m timeit "1 == 1"

And then:

.. code-block:: bash

    python -m timeit "1 is 1"

In my case, I got that the first expression took on average 0.0207 microseconds to run, while the second took 0.0171 microseconds. Speed is an obvious factor. The other is that when working with custom classes, you can specify what happens when you compare them to other objects. This is a very silly example but would prove the point:

.. code-block:: python

    class MyClass:
        def __eq__(self, other):
            return True

    my_obj = MyClass()

    if my_obj == None:
        print('My object == None')

    if my_obj is None:
        print('My Object is None')

If you run the code above, the output would me ``My Object == None``. Better be safe than sorry, and being aware of what the ``==`` operator means and when to use it or when to use ``is`` can be very important.

Mutable Objects in Functions
----------------------------
We have just seen that if you have two mutable objects with the same id it means that they are the same object. If you change one, you will change the other. This also applies when working with functions that take mutable objects as arguments. Imagine that you develop a function that takes as input a list, divides all of its arguments by 2 and then returns the average. The function would look like this:

.. code-block:: python

    def divide_and_average(var):
        for i in range(len(var)):
            var[i] /= 2
        avg = sum(var)/len(var)
        return avg

It is very interesting to see what happens when you use this function:

.. code-block:: python

    my_list = [1, 2, 3]
    print(divide_and_average(my_list))
    print(my_list)

The output will be:

.. code-block:: bash

    1.0
    [0.5, 1.0, 1.5]

When you execute the function, you are actually changing the values of the variable ``my_list``. This is very powerful because it allows you to change the elements of a list *in-place* while you are returning a different element. Sometimes, however, you don't want to do this and want to preserve the value of the original list. It may seem like a good idea to create a new variable within the function and use that instead. For example:

.. code-block:: python

    def divide_and_average(var1):
        var = var1
        [...]

However, you will see that this doesn't change the output. As we saw earlier, the identity of ``var`` and of ``var1`` would be the same. You can make a copy of your object using the ``copy`` module:

.. code-block:: python

    import copy

    def divide_and_average(var1):
        var = copy.copy(var1)
    [...]

And now you will see that the original ``my_list`` variable is not altered. What we have just done is called a *shallow copy* of an object. It is also possible to perform a *deep* copy, but its implications are left for a different article.

Default Arguments in Functions
-------------------------------
A common practice when you are defining a function is to assign default values to its arguments. On the one hand, this allows you to include new parameters without changing the downstream code, but it also allows you to call the function with fewer arguments and thus making it easier to use. Let's see, for example, a function that increases the value of the elements of a list. The code would look like:

.. code-block:: python

    def increase_values(var1=[1, 1], value=0):
        value += 1
        var1[0] += value
        var1[1] += value
        return var1

If you call this function without arguments, it will use the default value ``[1, 1]`` for the list and the default increase value of ``0``. What happens if you use this function twice, without any arguments?

.. code-block:: python

    print(increase_values())
    print(increase_values())

The first time it will print ``[2, 2]`` as expected, but the second time it is going to print ``[3, 3]``. Where you actually expecting this outcome? This basically means that the default argument of the function is changing every time we run it. When we run the script, Python evaluates the function definition only once and creates the default list and the default value. Because lists are mutable, every time you call the function you will be changing its own values for all the successive calls. However, the ``value`` is immutable, and therefore it will be preserved over time.

The next logical question is how can you prevent this from happening. And the short answer is to use immutable types as default arguments for functions. You could have used ``None``, for instance:

.. code-block:: python

    def increase_values(var1=None, value=0):
        if var1 is None:
            var1 = [1, 1]
        ...

Of course, the decision is always yours. Perhaps you would like to update the default value from one call to another. Imagine the case where you would like to perform a computationally expensive calculation, but you don't want to run twice the function with the same input and use a cache of values instead. You could do the following:

.. code-block:: python

    def calculate(var1, var2, cache={}):
        try:
            value = cache[var1, var2]
        except KeyError:
            value = expensive_computation(var1, var2)
            cache[var1, var2] = value
        return value

When we run ``calculate`` for the first time, there will be nothing stored in the ``cache`` dictionary, but if we execute the function more than once, ``cache`` will start changing, appending the new values to it. If we run calculate again with the same arguments, they are going to be present and their known value will be returned. Notice that we are leveraging the `exception handling <{filename}12_handling_exceptions.rst>`_ in order to avoid checking explicitly whether the combination of values already exists in memory.

Your Own Immutable Objects
--------------------------
Python is very flexible and it gives you a lot of control over how to customize its behavior. As you can see from the list at the beginning of this article, custom created classes belong to the mutable types. But what happens if you want to define your own immutable objects? The answer is to modify how the class behaves when assigning attributes. This means reimplementing the ``__setattr__`` method.

.. code-block:: python

    class MyImmutable:
        def __setattr__(self, key, value):
            raise TypeError('MyImmutable cannot be modified after instantiation')

If you instantiate the class and try to assign a value to an attribute of it, an error will appear:

.. code-block:: pycon

    >>> my_immutable = MyImmutable()
    >>> my_immutable.var1 = 2
    Traceback (most recent call last):
      File ".\AE_custom_objects.py", line 14, in <module>
        my_immutable.var1 = 2
      File ".\AE_custom_objects.py", line 7, in __setattr__
        raise TypeError('MyImmutable cannot be modified after instantiation')
    TypeError: MyImmutable cannot be modified after instantiation

Great, you have an object that you can't modify after instantiation. But that also means there is no much you can do with it. Imagine you would like to store some initial values if you create a standard ``__init__`` method, it will fail:

.. code-block:: python

    class MyImmutable:
        def __init__(self, var1, var2):
            self.var1 = var1
            self.var2 = var2
        [...]

As soon as you try to instantiate this class, the ``TypeError`` will be raised. Even within the class itself, assigning values to attributes is achieved through the ``__setattr__`` method. To bypass it, you need to use the ``super()`` object:

.. code-block:: python

    class MyImmutable:
        def __init__(self, var1, var2):
            super().__setattr__('var1', var1)
            super().__setattr__('var2', var2)

        def __setattr__(self, key, value):
            raise TypeError('MyImmutable cannot be modified after instantiation')

        def __str__(self):
            return 'MyImmutable var1: {}, var2: {}'.format(self.var1, self.var2)

Which now you can use as follows:

.. code-block:: pycon

    >>> my_immutable = MyImmutable(1, 2)
    >>> print(my_immutable)
    MyImmutable var1: 1, var2: 2
    >>> my_immutable.var1 = 2
    [...]
    TypeError: MyImmutable cannot be modified after instantiation

It is a bit of a workaround, but maybe you can find a use for this kind of pattern.

Conclusions
-----------
Understanding the differences between mutable and immutable types in Python does not arise as an important topic until it is too late. In most cases, you can develop complex applications exchanging tuples for lists, or you may even be altering the value of a variable inside a function without realizing it and without great consequences. But it will eventually happen that you find a bug very hard to track down that may be related to the use (or misuse) of mutable types.

As a personal note, I found out such a bug performing a complex experiment with a microscope. I wanted to be able to refocus automatically on certain bright spots after an image was acquired. The first time the algorithm was working fine. The second time it was pretty much OK, but the third and onwards was not even close to reaching the desired values. The root of the problem was defining the initial range that the microscope would scan as a list, which was being divided by a factor after every iteration.

Some of the patterns you find in this article, probably are not going to be of any use. However, it is important to keep in the back of your mind that ``==`` can give very unexpected results, that variables can change in unexpected ways if you are not careful. When projects start to grow, small mistakes can pile up to disastrous problems.

As always, `example code <https://github.com/PFTL/website/tree/master/example_code/17_mutable_immutable>`__ is available and the `source code <https://github.com/PFTL/website/blob/master/content/blog/17_mutable_and_immutable.rst>`__ for this page also.

If you want to keep learning, you can read more about `why tuples may seem to change <{filename}18_mutable_tuples.rst`>_ and what happens when you use `mutable or immutable variables as class attributes <{filename}21_Default_Attributes_Classes.rst>`_.

Header Photo by `rawpixel <https://unsplash.com/photos/EF8Jr-uPS2Y?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText>`_ on Unsplash