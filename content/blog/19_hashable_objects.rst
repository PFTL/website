What are Hashable Objects
=========================

:date: 2018-08-27
:author: Aquiles Carattino
:subtitle: Hashable objects are at the root of Python dictionaries, understand how they work.
:header: {attach}yeo-khee-793533-unsplash.jpg
:tags: Hashable, Objects, Dictionaries, Hash
:description: Hashable objects are at the root of Python dictionaries, understand how they work.

To understand hashable objects in Python, it is important to review what a hash table is. Following `the article on Wikipedia <https://en.wikipedia.org/wiki/Hash_table>`_, a hash table is a data structure that can map keys to values and that implements a hash function to compute the index to an array of buckets or slots. Heavy words, I know.

The idea behind a hash table is that, in the end, you can reduce a complex object to an index in an array. The analogy with a mail directory may be appropriate. Imagine you have a collection of names of people and their addresses. You store each address as soon as you meet a new person, one under the other. A hash table in such case will be responsible for transforming a name to a number that corresponds to the row in which their information is written.

If you have enough experience with Python, the first thing that probably came to mind is a dictionary. That would be the easiest way of storing addresses for people that you meet. You can easily retrieve their information by looking up their names. Even if dictionaries are a general concept in which keys are associated to values, Python, in fact, implements a hash table by default (which doesn't mean this cannot change in the future without affecting how dictionaries work).

One of the complications of hash tables is how to implement the hash function in a reliable way. Immutable data types in Python come with a built-in method for computing their hash value, which is called ``__hash__``. Let's see for example what happens with strings or tuples:

.. code-block:: pycon

    >>> a = '123'
    >>> a.__hash__()
    4031090051524460767
    >>> b = (1, 2, 3)
    >>> b.__hash__()
    2528502973977326415

You see that strings and lists are reduced to integers. If you would use numbers instead:

.. code-block:: pycon

    >>> c = 1
    >>> c.__hash__()
    1
    >>> d = 1.1
    >>> d.__hash__()
    230584300921369601

However, mutable objects such as lists and dictionaries do not have a hash method. That is one of the reasons why you cannot use that kind of objects as keys for dictionaries. What is important to note is that for immutable types, the hash value depends only on the data stored and not on the identity of the object itself. For instance, you can create two tuples with the same values, and see the differences:

.. code-block:: pycon

    >>> var1 = (1, 2, 3)
    >>> var2 = (1, 2, 3)
    >>> id(var1)
    140697473296656
    >>> id(var2)
    140697473295216

They are indeed different objects, however:

.. code-block:: pycon

    >>> var1.__hash__()
    2528502973977326415
    >>> var2.__hash__()
    2528502973977326415

This means that if you use them as dictionary keys, they are going to be indistinguishable from each other, for instance:

.. code-block:: pycon

    >>> var3 = {var1:'var1'}
    >>> var3[var2]
    'var1'

In the same way, you could have used the tuple itself:

.. code-block:: pycon

    >>> var3[(1, 2, 3)]
    'var1'
    >>> var3[1, 2, 3]
    'var1'

Based on what we saw, hashing an object can be thought as converting it to an integer based on its content, but not on the identity of the object itself. Of course, this may give problems, because you are reducing a very large space of possibilities into a finite set of integers. This reduction may give rise to something known as hash collisions, i.e., two objects which are reduced to the same integer even if their values are different.

A very simple example of hash collisions is what happens between a simple string and an integer:

.. code-block:: pycon

    >>> var1 = 'a'
    >>> var1.__hash__()
    12416037344
    >>> var2 = 12416037344
    >>> var1.__hash__() == var2.__hash__()
    True

Both ``var1`` and ``var2`` have the same hash value. So, we may wonder, what happens if we use them in a dictionary, let's try it to find out:

.. code-block:: pycon

    >>> var3 = {var1: 'var1'}
    >>> var3[var2] = 'var2'
    >>> var3
    {'a': 'var1', 12416037344: 'var2'}

As you can see in the snippet above, Python is relying on more than just the hash value of an object when using it as keys for a dictionary.

.. newsletter::

Hash Values of Custom Classes
-----------------------------
We have seen `before <{filename}17_mutable_and_immutable.rst>`_ that there are differences between mutable and immutable types in Python. Built-in immutable types have always a hash method, while mutable types don't. However, this leaves outside custom defined classes. By default, all instances of custom classes will have a hash value defined at creation and it will not change over time. Two instances of the same class will have two different hash values. For example:

.. code-block:: python

    class MyClass:
        def __init__(self, value):
            self.value = value

    my_obj = MyClass(1)
    print(my_obj.__hash__()) # 8757243744113
    my_new_obj = MyClass(1)
    print(my_new_obj.__hash__()) # -9223363279611078919

If you run the code above, you will see that the hash value that you get from your objects changes every time. This is because the hash is derived from the object's id. Python, as expected, allows you to define your own hash value. For example, you can alter ``MyClass`` like this:

.. code-block:: python

    class MyClass:
        def __init__(self, var):
            self.var = var

        def __hash__(self):
            return int(self.var)

If you re-run the example, you will see that both objects have the same hash value of 1. So, let's see what happens if we use them as the keys for a dictionary:

.. code-block:: pycon

    >>> my_obj = MyClass(1)
    >>> my_obj_2 = MyClass(1)
    >>> var = {my_obj: 'my_obj'}
    >>> var[my_obj_2] = 'my_obj_2'
    >>> print(var)
    {My Class: 'my_obj', My Class: 'my_obj_2'}

What you can see is that, even if the hash value is the same, they end up as different keys in the dictionary. There is still something else missing. Even if their hash values are the same, they are different objects:

.. code-block:: pycon

    >>> my_obj == my_obj_2
    False

We can tweak the ``MyClass`` class in order to output ``True`` when comparing it:

.. code-block:: python

    class MyClass:
        def __init__(self, var):
            self.var = var

        def __hash__(self):
            return int(self.var)

        def __eq__(self, other):
            return other.var == self.var

The method ``__eq__`` is used to determine whether one object is equal to another. Because ``MyClass`` takes only one argument when instantiating, we just compare that value. For example, we would get:

.. code-block:: pycon

    >>> var1 = MyClass(1)
    >>> var2 = MyClass(1)
    >>> var3 = MyClass(2)
    >>> var1 == var2
    True
    >>> var1 == var3
    False

It works as we would expect it to. If we try again with a dictionary:

.. code-block:: pycon

    >>> var4 = {var1: 'var1'}
    >>> var4[var2] = 'var2'
    >>> var4
    {My Class: 'var2'}
    >>> var4[var3] = 'var3'
    >>> var4
    {My Class: 'var2', My Class: 'var3'}

Finally, we see what is that dictionaries in Python are using for defining their keys. They do not only look at the hash value, they also look whether the keys are the same or not. If they are not, they will be assigned to a new element instead of the same one. You can try and see what happens if two elements are equal, but have different hash values.

Now you are starting to go through risky waters. If you would compare your object to something other than the ``MyClass`` instance (or better said, any object without a ``var`` attribute), an exception would be raised. You can also force the equality to be true regardless of the object you are comparing it to. So, for example:

.. code-block:: python

    class MyClass:
        def __init__(self, var):
            self.var = var

        def __hash__(self):
            return int(self.var)

        def __eq__(self, other):
            return True

And now, we would find a strange behavior:

.. code-block:: pycon

    >>> my_obj = MyClass(1)
    >>> var = 1
    >>> my_obj == var
    True
    >>> var2 = {my_obj: 'my_obj'}
    >>> var2[var] = 'var'
    >>> print(var2)
    {MyClass: 'var'}

So now you see that dictionaries test two things: the hash value and the equality, if one of them doesn't match, then it is going to be assigned as a new key.

Of course, there are many details missing regarding how hash tables work, but this is a pretty good introduction into how some of the under-the-hood things work in Python. They may also give you a hint into why things work or stop working at apparently random places.


Header photo by `Yeo Khee <https://unsplash.com/photos/BkqUJQiucKY?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText>`_ on Unsplash