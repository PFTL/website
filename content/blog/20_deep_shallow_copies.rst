Deep and Shallow Copies of Objects
==================================

:date: 2019-02-04
:author: Aquiles Carattino
:subtitle: Understanding how tuples which are immutable, may seem to change.
:header: {attach}rebecca-georgia-269933-unsplash.jpg
:tags: Data, Types, Mutable, Immutable, Objects, Copy, Memory
:description: Understanding how tuples which are immutable, may seem to change.


Copying objects in Python seems like a trivial task, but it can have unexpected implications in your programs. Copying data may be achieved by either duplicating the data or by storing references to the objects, having a much lower impact on the memory. In this article, we are going to review the differences between deep and shallow copies of objects in Python, including custom classes.

The discussion of deep and shallow copies is only worth having in the context of `mutable data types <{filename}17_mutable_and_immutable.rst>`_, so if you are not sure of what that means, you can check the linked article. To refresh your memory, let's see quickly what happens when you copy a list, for example:

.. code-block:: pycon

    >>> a = [1, 2, 3]
    >>> b = a
    >>> print(b)
    [1, 2, 3]
    >>> a[0] = 0
    >>> print(b)
    [0, 2, 3]

You see that if you change one element ``a``, it will be reflected also in ``b``. If you want to prevent this behavior, you can do the following:

.. code-block:: pycon

    >>> a = [1, 2, 3]
    >>> b = list(a)
    >>> a[0] = 0
    >>> print(b)
    [1, 2, 3]

Now you see that you have two independent objects. You can also verify it by running ``id(a)`` and ``id(b)`` and checking that they are effectively different. However, this is not the end of the discussion. Let's see what happens if you have a list of lists:

.. code-block:: pycon

    >>> a = [[1, 2, 3], [4, 5, 6]]
    >>> b = list(a)

If you check ``id(a)`` and ``id(b)`` you will see that they are different. You can go one step further and change a:

    >>> a.append([7, 8, 9])
    >>> print(b)
    [[1, 2, 3], [4, 5, 6]]

This looks like great news until you do the following:

.. code-block:: pycon

    >>> a[0][0] = 0
    >>> print(b)
    [[0, 2, 3], [4, 5, 6]]

We changed ``a`` and ``b`` also changed! I bet you didn't see that coming. What does this mean? Here is where deep and shallow copies enter into play. When we copied ``a`` into ``b`` by doing ``list(a)``, we performed a shallow copy. This means that we created a new element (that is why the id is different), but the references to other elements are still the same. We can see that by checking the id of the first element of both ``a`` and ``b``:

.. code-block:: pycon

    >>> id(a[0])
    140381216067976
    >>> id(b[0])
    140381216067976

A shallow copy is, as the name suggests, a superficial copy. Only the first layer is created new, but not the underlying ones. The same is true for dictionaries, for example. Regarding lists, there is another way of making a shallow copy:

.. code-block:: pycon

    >>> b = a[:]

While for dictionaries you can use:

.. code-block:: pycon

    >>> my_dict = {'a': [1, 2, 3], 'b': [4, 5, 6]}
    >>> new_dict = my_dict.copy()
    >>> other_option = dict(my_dict)

If you want to create a deep copy, which as the name suggests creates completely new objects, including referred ones, you need to use the ``copy`` module. Let's start by checking how to perform a shallow copy:

.. code-block:: pycon

    >>> import copy
    >>> b = copy.copy(a)
    >>> id(a[0])
    140381216067976
    >>> id(b[0])
    140381216067976

I hope the example above is enough for you to understand what it means. If you want to make a deep copy, the command is, as expected, ``deepcopy``:

.. code-block:: pycon

    >>> c = copy.deepcopy(a)
    >>> id(c[0])
    140381217929672

.. newsletter::

Copies of Custom Classes
------------------------
We have seen the differences between deep and shallow copies of standard python data types such as lists and dictionaries. Now it is important to see what happens when you define your own classes that also reference other mutable objects. Let's quickly see what happens if you copy your custom class:

.. code-block:: python

    class MyClass:
        def __init__(self, x, y):
            self.x = x
            self.y = y

    my_class = MyClass([1, 2], [3, 4])
    my_new_class = my_class

    print(id(my_class))
    print(id(my_new_class))

    my_class.x[0] = 0
    print(my_new_class.x)

Which will generate the following output:

.. code-block:: python

    140397059541368
    140397059541368
    [0, 2]

You see that by simply copying the class with the ``=`` , we get two references to the same object, and therefore the id is the same. Moreover, if one of the mutable attributes of the class changes, it will also change in all the other objects. An easy solution would be to use the ``copy`` module:

.. code-block:: python

    import copy
    my_class = MyClass([1, 2], [3, 4])
    my_new_class = copy.copy(my_class)

    print(id(my_class))
    print(id(my_new_class))

    my_class.x[0] = 0
    print(my_new_class.x)

I've suppressed the definition of the class for brevity. The output of the above code would be:

.. code-block:: python

    140129009113464
    140129008512416
    [0, 2]

You can see that now they got different ``id`` values, but the objects they reference are still the same. If you change ``copy`` by ``deepcopy``, the behavior would change, exactly in the same way than with lists or dictionaries. But we can go one step further, and customize the behavior of the shallow or deep copies of objects.

Custom shallow and deep copies of objects
-----------------------------------------
With Python, you have a very high level of granularity regarding how much control you have on every step, including deep and shallow copies. In order to have control, you need to override the methods ``__copy__`` and ``__deepcopy__``, let's see how and then we see why. First, imagine that you want to be able to copy a class with all its references but one, which you need to be independent of one instance of your class to another. You can do:

.. code-block:: python

    class MyClass:
        def __init__(self, x, y):
            self.x = x
            self.y = y
            self.other = [1, 2, 3]

        def __copy__(self):
            new_instance = MyClass(self.x, self.y)
            new_instance.__dict__.update(self.__dict__)
            new_instance.other = copy.deepcopy(self.other)
            return new_instance

Let's go step by step. When you use ``copy.copy``, the method that will be executed is ``__copy__`` and the argument is the object itself. The return is going to be the copied object. To make a copy, the first thing is to instantiate the new class, which we do by calling ``MyClass`` again. You can make more general by replacing ``MyClass`` with ``type(self)``.

Anyhow, the next step is to copy all the attributes of the base instance into the new one. This can be quickly done by updating the ``__dict__`` attribute. If you are not familiar with it, we are going to quickly explore it later. These two steps alone define the standard behavior for a shallow copy of an object. In order to achieve a special functionality, we add one more line, in which the ``other`` attribute is copied with a deep copy. ``other`` was not part of the ``__init__`` just to show you that we can add on any attribute of the class.

Finally, if we repeat the simple tests of before, we would get:

.. code-block:: python

    my_class = MyClass([1, 2], [3, 4])
    my_new_class = copy.copy(my_class)

    print(id(my_class))
    print(id(my_new_class))

    my_class.x[0] = 0
    my_class.y[0] = 0
    my_class.other[0] = 0
    print(my_new_class.x)
    print(my_new_class.y)
    print(my_new_class.other)

And the output would be:

.. code-block:: python

    139816535263552
    139816535263720
    [0, 2]
    [0, 4]
    [1, 2, 3]

As you can see, the attribute ``other`` was deep copied and therefore if you change it in one class, it won't change in the other.

About the dict attribute
~~~~~~~~~~~~~~~~~~~~~~~~
In the previous section, we used the ``__dict__`` attribute of a class, and that may not be something standard for you. Allow me this short digression before going back to the main subject of the article. As you know, objects contain attributes, and these attributes are always defined as variables which in the end look like strings (i.e., you can read them, type them with your keyboard, etc.)

This makes it possible to think the collection of attributes as a dictionary. In the class from the previous section, you can explore this idea by doing to following:

.. code-block:: pycon

    >>> print(my_class.__dict__)
    {'x': [0, 2], 'y': [0, 4], 'other': [1, 2, 3]}

I hope you are seeing the gist of this. You can also alter the ``__dict__`` directly:

.. code-block:: pycon

    >>> my_class.__dict__['x'] = [1, 1]
    >>> my_class.x
    [1, 1]

It means that you can either use the ``.x`` or the ``__dict__['x']`` to work with the same element in your object. This is also a quick way of knowing all the attributes that are defined in your object, etc. Hope this short story can help clarify a topic that is not that trivial for newcomers to the deeps of object-oriented python programming.

Custom deep copy
----------------
Back in the track to the main topic of the article, we need to customize the deep copy of the class. It is very similar to the ``__copy__`` method, but it takes one more argument:

.. code-block:: python

    class MyClass:
        def __init__(self, x, y):
            self.x = x
            self.y = y
            self.other = [1, 2, 3]

        def __deepcopy__(self, memodict={}):
            new_instance = MyClass(self.x, self.y)
            new_instance.__dict__.update(self.__dict__)
            new_instance.x = copy.deepcopy(self.x, memodict)
            new_instance.y = copy.deepcopy(self.y, memodict)
            return new_instance

It looks very similar to the ``copy``, but the requirement of the extra argument ``memodict`` is rooted at what deep copying means. Since every object referenced from the initial class has to be recreated, there is a risk of an infinite recursion. This can happen if one object somehow references itself. Even if not an infinite recursion loop, you may end up copying several times the same data. The ``memodict`` is keeping track of the objects already copied. The infinite recursion is what we can prevent overwriting the ``__deepcopy__`` method.

In the example above, what we do is we prevent the deep copy process from generating a new ``other`` list. Therefore, we end up with a mixed deep copy, in which ``x`` and ``y`` are really new, while ``other`` is the same. If we run the example code,

.. code-block:: python

    my_class = MyClass([1, 2], [3, 4])
    my_new_class = copy.deepcopy(my_class)

    print(id(my_class))
    print(id(my_new_class))

    my_class.x[0] = 0
    my_class.y[0] = 0
    my_class.other[0] = 0
    print(my_new_class.x)
    print(my_new_class.y)
    print(my_new_class.other)

We will get the following output:

.. code-block:: python

    139952436046312
    139952436046200
    [1, 2]
    [3, 4]
    [0, 2, 3]

So, you see now, that ``.x`` and ``.y`` are unchanged, while ``.other`` reflects the changes done on the other class.

Why defining how to copy
------------------------
The simple examples above only show how to achieve different behavior with deep and shallow copies, but they don't explain why you would do it. The cases in which you will need to define this custom behavior are not trivial at all. Customizing the deep copy would happen if, for instance, the class is holding any kind of cache, and you need to preserve it between different objects. Preserving the cache can be useful because you can speed up the code, or because it is very large and you don't want to duplicate the memory usage.

For shallow copies, the use cases are varied. It normally implies that there is at least one attribute that you don't want to share between objects. That attribute could be, for instance, the object responsible for communicating with a device. You would like to prevent talking at exactly the same time to the same device through the same interface. You may also like to protect private attributes, etc.

Last Warning
------------
It is very important to point out that, if are worried about copying and deep copying of custom objects, you should understand what are `mutable and immutable  <{filename}17_mutable_and_immutable.rst>`_ objects in Python, and what are `hashable objects <{filename}19_hashable_objects.rst>`_. When you have immutable data types, such as an integer or a string, all the discussion above doesn't work. If you change an immutable attribute in a class, that attribute in deep-copied objects will not change.

Therefore, the idea of preserving attributes between objects, etc. only works with mutable objects. If you want to achieve the behavior of sharing data between objects as a feature, you will need to think how to transform it to mutable types or find ways around it.

Another word of caution goes for people working with ``multiprocessing``. It may be obvious but is never bad to repeat it, that sharing data between different processes is not a trivial task and therefore you can't rely on mutable objects to share information.

Header photo by `Rebecca Georgia <https://unsplash.com/photos/Dff-4JbYq0Y?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText>`_ on Unsplash