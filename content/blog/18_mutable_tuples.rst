Mutable or Immutable Tuples
===========================

:date: 2018-08-24
:author: Aquiles Carattino
:subtitle: Understanding how tuples, which are immutable, may seem to change.
:header: {attach}michal-pechardo-502908-unsplash.jpg
:tags: Data, Types, Mutable, Immutable, Tuples
:description: Understanding how tuples, which are immutable, may seem to change.

Broadly speaking, Python variables belong to one of two types: **mutable** and **immutable**. We have discussed this yesterday, in the `Introduction To Mutable and Immutable Data Types <{filename}17_mutable_and_immutable.rst>`_. The first one refers to those elements that can be changed without the need of creating a new one, while the latter refers to those that cannot be changed after instantiation. A paradigmatic example of immutable objects is tuples. However, as we are going to see in this article, tuples may seem to change.

You define a tuple by using ``()``, and access its elements using ``[]``, for example:

.. code-block:: pycon

    >>> var1 = (1, 2, 3)
    >>> var[0]
    1

Since a tuple is immutable, you can't change its elements once it was created, the following will give you an error:

.. code-block:: pycon

    >>> var[0] = 0
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    TypeError: 'tuple' object does not support item assignment

Tuples are not limited to hold numbers in them, nor to elements of the same type. We can create a tuple that holds both numbers and a list:

.. code-block:: pycon

    >>> my_list = [1, 2, 3]
    >>> var = (1, my_list)
    >>> var[1]
    [1, 2, 3]

What happens if you try to change the value of one of the elements of the list?

.. code-block:: pycon

    >>> var[1][0] = 0

As you know, tuples are immutable, and what you are doing is changing a tuple. However, no error will appear. The operation above works as expected:

    >>> var[1]
    [0, 2, 3]

If you try to change ``var[0]``, which is an integer, you will face the same exception that was shown above. So, what is happening? `Luciano Ramalho <https://standupdev.com/wiki/doku.php?id=python_tuples_are_immutable_but_may_change>`_ has written an excellent article with an example from Alice in Wonderland, which I am not going to copy here, but that has deeply inspired me.

If you think variables as labels and not as boxes in which information is stored, you can also think that what is stored in the tuple are references to the objects and not the objects themselves. When you change a list, its identity doesn't change, for example:

.. code-block:: pycon

    >>> var = [1, 2, 3]
    >>> id(var)
    44045192
    >>> var[0] = 0
    >>> id(var)
    44045192

A tuple is basically holding a reference to different objects. While that reference doesn't change, the tuple will not change. The identity of the list that is stored in the tuple does not change when we change a value in a list or we append new elements, etc. This is not true for other immutable data types, like integers. That is why, if we try to change the value of an integer, an exception will be raised. A new object is created and therefore the reference that is being stored in the tuple needs to be updated.

This also works when you use two different names for the same tuple. For example:

.. code-block:: pycon

    >>> var1 = (1, my_list)
    >>> var2 = var1
    >>> var1 is var2
    True
    >>> var2[1] is my_list
    True

If we update the values of the list in any way, they will be changed in all the other variables:

.. code-block:: pycon

    >>> var1[1][0] = 0
    >>> my_list
    [0, 2, 3]
    >>> var2[1]
    [0, 2, 3]
    >>> my_list[0] = 1
    >>> var1[1]
    [1, 2, 3]

Now you see that we have three labels for the same list, and if we update any of them, all the others will reflect these changes. For example, you could create a new variable for the list:

.. code-block:: pycon

    >>> var1 = (1, [1, 2, 3])
    >>> my_list = var1[1]
    >>> print(my_list)
    [1, 2, 3]
    >>> my_list[0] = 0
    >>> var1
    (1, [0, 2, 3])

A lot of possibilities appear when you start playing around. However, your code has to be very well structured and explained if you plan to keep it maintainable.

.. newsletter::

Tuples as Dictionary Keys
-------------------------
In principle, any immutable variable can be used as a dictionary key. Therefore, it is possible to also use tuples. For example:

.. code-block:: pycon

    >>> var1 = (1, 2)
    >>> var2 = (4, 5)
    >>> var3 = {var1: 'First Var',
    ...     var2: 'Second Var'}
    >>> print(var3[1, 2])
    First Var

However, if you generate a tuple that contains a reference to a mutable object, the code above will fail:

.. code-block:: pycon

    >>> var4 = (1, [1, 2, 3])
    >>> var5 = {var1: 'First Var',
    ...     var4: 'Second Var'}

    TypeError: unhashable type: 'list'

The keys of dictionaries have to be immutable, and they must reference objects that are also immutable. Therefore, even if the tuple is immutable, their elements may not be. You have to be careful when using a tuple as key to a dictionary since it will not always work.

.. note:: actually, keys in dictionaries need to be hashable, which is not the same as immutable. Custom defined classes are hashable but mutable and can be used as dictionary keys. We are going to discuss this in a later article.

Conclusions
-----------
This is a short article triggered by some comments that appear on the `discussion about mutable and immutable types <{filename}17_mutable_and_immutable.rst>`_. Wrapping your mind around this level of details may be hard at the beginning, but when you know these differences exist, you will be able to make better code, less prone to bugs. You may also start realizing why so many packages use tuples as default arguments instead of lists, etc.


Header photo by `Michal Pechardo <https://unsplash.com/photos/O6XDQCNo4Hc?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText>`_ on Unsplash