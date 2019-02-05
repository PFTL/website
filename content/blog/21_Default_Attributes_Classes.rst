Mutable and Immutable Attributes of Classes
===========================================

:date: 2018-08-24
:author: Aquiles Carattino
:subtitle: Understanding how tuples which are immutable, may seem to change.
:header: {attach}dan-gold-382057-unsplash.jpg
:tags: Data, Types, Mutable, Immutable, Tuples
:description: Understanding how tuples which are immutable, may seem to change.

We have seen how to leverage the differences between `mutable and immutable objects <{filename}17_mutable_and_immutable.rst>`_ and what happens when you use mutable types as default function arguments. However, we haven't discussed what happens when you use mutable types as default attributes of classes.

Default values for attributes can be defined in different ways in your classes. Let's start by looking at what happens if you define them in the ``__init__`` method. Let's start with a simple class that takes one list as the argument when instantiating:

.. code-block:: python

    class MyClass:
        def __init__(self, var=[]):
            self.var = var

        def append(self, value):
            self.var.append(value)

        def __str__(self):
            return str(self.var)

This is a very simple example that already will show a very peculiar behavior. The ``__init__`` takes one list as the argument, and if it is not provided it will use an empty list as default. We have also added a method for appending values to the list. The ``__str__`` method was defined for convenience to explore the contents of the ``var`` attribute. We can instantiate the class and use it as always:

.. code-block:: python

    my_class = MyClass()
    print(my_class)
    # []
    my_class.append(1)
    print(my_class)
    # [1]

So far so good, but let's see what happens when we instantiate the second class:

.. code-block:: python

    my_class_2 = MyClass()
    print(my_class_2)
    # [1]

The second time you instantiate a class, it will use a different default value! It is actually using the updated value from the first instance. Moreover, if you change the value of the second instance, the value of the first instance will also change:

.. code-block:: python

    my_class_2.append(2)
    print(my_class)
    # [1, 2]

Whatever changes you do to the attribute ``var`` of one of the objects, will be reflected into the other. Both attributes are actually the same object, as you can verify by looking at their ids:

.. code-block:: python

    print(id(my_class.var))
    # 140228152031752
    print(id(my_class_2.var))
    # 140228152031752

But the two instances are different

.. code-block:: python

    print(id(my_class))
    # 140228175513360
    print(id(my_class_2))
    # 140228175513304

The same pattern that appeared while using mutable variables as defaults with functions will appear when using mutable default arguments of methods in custom classes. If you want to avoid this from happening, you can always check what `we have done when working with functions <{filename}17_mutable_and_immutable.rst>`_.

Of course, the same pattern will appear if you use a mutable variable defined outside of the class, for example:

.. code-block:: python

    my_list = [1, 2, 3]
    my_class = MyClass(my_list)
    my_class.append(4)
    print(my_list)
    # [1, 2, 3, 4]

.. newsletter::

Classes provide another pattern which is the use of **class attributes** instead of **instance attributes**. Class attributes are those values that are defined directly in the class, outside of any methods. Let's update our example to use a class attribute called ``var``:

.. code-block:: python

    class MyClass:
        var = []

        def append(self, value):
            self.var.append(value)

        def __str__(self):
            return str(self.var)

And we use it as before:

.. code-block:: python

    my_class = MyClass()
    my_class.append(1)
    print(my_class)
    # [1]

If we instantiate the class again, we will have the same as before:

.. code-block:: python

    my_class_2 = MyClass()
    print(my_class_2)
    # [1]

The main difference with what we have done before is that we can address directly the ``var`` attribute of the class:

.. code-block:: python

    MyClass.var.append(2)
    print(my_class)
    # [1, 2]
    print(my_class_2)
    # [1, 2]

You can also address the attribute of an instance directly, without the need of the ``append`` method:

.. code-block:: python

    my_class_2.var += [3]
    print(my_class)
    # [1, 2, 3]
    print(my_class_2)
    # [1, 2, 3]

You can see in the examples above, is that the changes you apply to one of the attributes will be reflected in the attributes of all the other instances and even in the class itself. There is a big difference, however, between class attributes and default inputs in methods. Class attributes are shared between instances by default even if they are immutable. Let's see, for example, what happens if we use a ``var`` that is an integer, and therefore immutable:

.. code-block:: python

    class MyClass:
        var = 1

        def increase(self):
            self.var += 1

        def __str__(self):
            return str(self.var)

Just as we have done before, we will instantiate twice the class and see what happens:

.. code-block:: python

    my_class = MyClass()
    print(my_class)
    # 1
    my_class_2 = MyClass()
    print(my_class_2)
    # 1
    my_class.increase()
    print(my_class)
    # 2
    print(my_class_2)
    # 1

What you see here is already a big difference. Both instances of ``MyClass`` have the same attribute ``var``. However, when you increase the value in one of the instances this change is not propagated to the other instance nor to new instances of the class.

This is very different from what you would see if you change the value of ``var`` in the class itself:

.. code-block:: python

    my_class = MyClass()
    my_class_2 = MyClass()
    MyClass.var += 1
    print(my_class)
    # 2
    print(my_class_2)
    # 2

You see that class attributes are still linked to the instances. It is very interesting to see the id of the ``var`` attribute before and after changing its value:

.. code-block:: python

    my_class = MyClass()
    my_class_2 = MyClass()
    print(id(my_class_2.var))
    # 10935488
    print(id(my_class.var))
    # 10935488
    print(id(MyClass.var))
    # 10935488
    MyClass.var += 1
    print(id(my_class_2.var))
    # 10935520
    print(id(my_class.var))
    # 10935520
    print(id(MyClass.var))
    # 10935520

You see that all the attributes are the same object. When the value is replaced, since integers are immutable, a new object is created and is propagated to all the instances of the class. However, if you change the value of ``var`` in one of the instances, this will not hold anymore:

.. code-block:: python

    my_class.var += 1
    print(id(my_class.var))
    # 10935552
    print(id(my_class_2.var))
    # 10935520
    print(id(MyClass.var))
    # 10935520

You can see that both the attributes in ``MyClass`` and in ``my_class_2`` are still the same object, while the identity of ``var`` in ``my_class`` changed. From now on, any changes that you do to ``MyClass.var`` are decoupled from the changes in ``my_class``, but will still be reflected on ``my_class_2``.

Keeping in mind the differences between methods' default values and class attributes open a lot of possibilities when designing a program. The fact that you can alter all objects from within a specific instance can be of great use when properties change at runtime. Even if not an extremely common scenario for short-lived scripts, it is very common when dealing with user interaction on programs that run for hours or days.

As always, `example code can be found here <https://github.com/PFTL/website/tree/master/example_code/21_Classes_Mutables>`_ and `the source of this page here <https://github.com/PFTL/website/blob/master/content/blog/21_Default_Attributes_Classes.rst>`_.

Header photo by `Dan Gold <https://unsplash.com/photos/mgaS4FlsYxQ?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText>`_ on Unsplash