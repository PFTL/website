Monkey Patching and its consequences
====================================

:date: 2019-06-18
:author: Aquiles Carattino
:subtitle: Replacing methods and attributes at runtime
:description: Replacing methods and attributes at runtime
:header: {attach}shashank-sahay-1659565-unsplash.jpg
:tags: functions, methods, monkey patching, replacing, extending, mutable, immutable


Monkey patching is a technique that allows you to alter the behavior of objects at runtime. Even though it can be a very useful feature, it can also make your code much harder to understand and debug, and therefore you have to be careful with how you implement monkey patching. In this article, we are going to see some examples of how you can use monkey patching to solve quickly specific problems. We are also going to discuss the consequences of monkey patching in the context of larger projects.

Monkey patching is tightly related to the idea of `mutability in Python <{filename}17_mutable_and_immutable.rst>`_. Custom objects are mutable, and therefore their attributes can be replaced without creating a new copy of the object. To quickly recap those ideas, we can do the following:

.. code-block:: python

    class MyClass:
        a = 1
        b = '2'

And then we can use the code like this:

.. code-block:: python

    var1 = MyClass()
    var2 = var1

    var1.a = 2
    var1.b = '3'

    print(var2.a)
    # 2
    print(var2.b)
    # '3'

If we go line by line, you see that we create an object using ``MyClass`` and we call it ``var1``. We then copy the object to another variable, called ``var2``. We change the values stored in ``var1``, but we observe that the values stored in ``var2`` have also changed. This is simply because, in Python, the variable is only a label. In the line ``var2 = var1`` we have just copied the label, but both are pointing to the same underlying object.

Python also allows you to change attributes in the class itself, not in the instance of the class. We can do the following:

.. code-block:: python

    var1 = MyClass()
    var2 = MyClass()
    print(var1.a)
    # 1
    MyClass.a = 2
    print(var1.a)
    # 2
    print(var2.a)
    # 2

What we see is that if we directly alter the value of any of the attributes of the class, the instances inherit this change. This is both very useful and very dangerous, since you may be altering the value of attributes of objects which you were not intending to modify. There is one last behavior that is important to point out, and refers to mixing the two approaches we have followed before:

.. code-block:: python

    var1 = MyClass()
    var2 = var1

    var1.a = 2
    var1.b = '3'

    MyClass.a = 3

    print(var1.a)
    # 2
    print(var2.a)
    # 2

Even if you change the attribute ``a`` to ``3``, you don't see this change appearing on the instances of the class. The root cause of this lays in the ideas behind `mutable and immutable <{filename}17_mutable_and_immutable.rst>`_ data types in Python. Since you altered the value of ``var1.a``, now the attribute is pointing to an object different from the object the class attribute points to. If this last line doesn't make sense, go to the articles linked earlier on mutable and immutable data types.

Finally, the last case I wanted to point out is what happens if you keep a reference to the attribute ``a`` before you modify it:

.. code-block:: python


    var1 = MyClass()
    var2 = var1

    var3 = var1.a
    [...]
    print(var3)
    # 3

I have skipped the code in which you change the value of the attributes. Now you see that if you actually store ``var1.a`` in the variable ``var3``, this variable is actually modified when you change the value stored directly in the class. All this behavior actually makes sense, if you think that variables only store references to objects and not the object itself and that when you change an immutable variable, you create a new reference.

All the examples above refer to monkey patching in one way or another. You can see that we are changing the values of a class during runtime. We have tried to highlight some of the consequences, expected or not, of changing the value of an attribute later in the execution of the program and not in the definition itself.

The examples above can be extended if we consider that methods are attributes which behave exactly like ``a`` or ``b`` in our examples above:

.. code-block:: python

    class MyClass:
        a = 1
        b = '2'

        def get_value(self):
            return self.a

We instantiate the class:

.. code-block:: python

    var1 = MyClass()
    print(var1.get_value())

And we should see that everything is working as expected. We then define a new function that we would like to use to replace ``get_value``:

.. code-block:: python

    def get_new_value(cls):
        return cls.b

In the function above, I've replaced ``self`` by ``cls`` just to make it more evident, but you are free to use whatever keyword makes more sense in your context. And we replace the method:

.. code-block:: python

    MyClass.get_value = get_new_value

If you use it, you will get:

.. code-block:: python

    print(var1.get_value())
    # 2

You see that we have replaced the ``get_value`` after the ``var1`` has been defined. If we would define a new object, it seems reasonable to expect that we would get the same output:

.. code-block:: python

    var2 = MyClass()
    print(var2.get_value())
    # 2

If we would have defined the two distinct objects before changing the method, the outcome would have been the same. What you see is that you can overwrite the method of the class:

.. code-block:: python

    var1 = MyClass()
    var2 = MyClass()

    MyClass.get_value = get_new_value

    print(var1.get_value())
    print(var2.get_value())

The examples at the beginning of the article, when we were using an integer or a string as attributes are still valid. You can check what happens if you copy the object, you store it as a new variable, and then you overwrite the method. There are no mysteries, methods are attributes such as integers or strings. The main difference is that they take inputs.

In the example above, we have replaced the method at the class-level. If we want to replace the method at an instance level, then the approach would be slightly different. Note that if we do it at a class-level, all the instances will get the changes, and this may not be what we want. We can do:

.. code-block:: python

    import types

    class MyClass:
        a = 1
        b = '2'

        def get_value(self):
            return self.a

    def get_new_value(cls):
        return cls.b

    var1 = MyClass()
    var2 = MyClass()
    var1.get_value = types.MethodType(get_new_value, var1)
    print(var1.get_value())
    # 2
    print(var2.get_value())
    # 1

You see in this example that we have altered the behavior of the method of ``var1`` but not of ``var2``. Note that we are importing ``types`` at the beginning of the script. The rest is the same we have already done, with one exception when we replace the ``get_value`` method. Because we are changing a method of an instance, it needs to be of the proper type. We can quickly see the following:

.. code-block:: pycon

    >>> type(get_new_value)
    <class 'function'>
    >>> type(MyClass.get_value)
    <class 'function'>
    >>> type(var1.get_value)
    <class 'method'>

The main difference between a method and a function is that the first one receives as first argument the instance itself (the ``self``). We have therefore to transform a function into a method before replacing it on an instance. Pay attention that this is not the case when you change the class itself.

Module-level monkey patching
----------------------------
The last pattern that I would like to discuss is monkey-patching at the module level. So far, the attributes and methods we have used, they all belonged to a custom class. However, it is not the only possibility. First, in a file called **module.py** we can add the following:

.. code-block:: python

    def print_variable(var):
        print(var)

And in a second file called **script.py** we add:

.. code-block:: python

    import module

    var1 = 1

    AE_module.print_variable(var1)
    # 1
    def print_plus_one(var):
        print(var+1)

    AE_module.print_variable = print_plus_one
    AE_module.print_variable(var1)
    # 2

You see that monkey patching works also for modules. When you try to achieve this kind of patching, you have to be careful with the order in which importing happens in Python. If you use the **__init__.py** files to load modules, and there is some dependency between each other, when you monkey patch, it may be that it is too late for the program. Similar to what happens when you alter the value of an attribute of an object and then you change the value at a class-level.

If you remember that Python imports modules only once, then the patching can take very interesting forms. You can create a new file, called **module2.py** and add the following:

.. code-block:: python

    import module


    def another_print(var):
        module.print_variable(var+1)

You see that we are using the ``print_variable`` from the original module. We are just adding ``+1`` before printing. We can alter the file **script.py** to include this new module:

.. code-block:: python

    import module
    import module2

    var1 = 1

    module.print_variable(var1)
    # 1

    def print_plus_one(var):
        print(var+1)

    module.print_variable = print_plus_one

    module.print_variable(var1)
    # 2
    module2.another_print(var1)
    # 3

You see that by changing the ``print_variable`` on our main script, we have also altered what is happening on our second module. There are a lot of things you can start thinking about after seeing these patterns.

When (not) to Monkey Patch
--------------------------

Monkey patching is very powerful and it shows how flexible Python is. In the end, everything is derived from the same principles of understanding different data types and what variables mean in Python. However, it may be very hard to understand when would you use these patterns in your own programs.

As a general rule, the best is not to monkey patch. If you want to alter the behavior of a program, for example, you can define child classes for the ones you want to alter. The problem with monkey-patching is that the behavior of a program becomes much harder to understand. In the example above, when you call ``module2.another_print`` you are seeing an output which is very hard to understand. If you check the module, you won't see why you would get ``3`` and not ``2``. Tracing back where the behavior was changed is very complicated. If you inspect the variables, you will see that there is nothing wrong, and ``var1`` is still ``1``.

However, sometimes there can be a great benefit. For example, calculating Fast Fourier Transforms with numpy can be slower than with other implementations. Imagine you would like to use PyFFTW, but you don't want to re-write all your program. You can monkey-patch your code! See the example below (taken `from the docs <http://hgomersall.github.io/pyFFTW/sphinx/tutorial.html>`_):

.. code-block:: python

    import pyfftw
    import numpy

    numpy.fft = pyfftw.interfaces.numpy_fft

Now, whenever you use the FFT routines provided by numpy, they will be automatically replaced by those of PyFFTW. This can have a huge impact on your program, and it only took one line of code! This is a special example but there are other situations in which you may consider monkey patching.

A common situation is with testing. Sometimes you want to test your code in an environment which lacks some functionality, or you want to prevent that because of the test you actually modify a live database. In that case, before doing the test you can change the methods that communicate with a database. If you work in a lab, a very common situation is when you want to avoid communicating with a device while you are testing your program.

Exactly how to achieve this behavior will depend on your situation, but with the examples above you already have a clear picture of what the strategy could be.

Header Photo by `Shashank Sahay <https://unsplash.com/@shashanksahay?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText>`_ on Unsplash

The code found in this article is `available on Github <https://github.com/PFTL/website/tree/master/example_code/34_monkey_patching>`_. Any comment, improvement, or suggestion can be `submitted here <https://github.com/PFTL/website/issues/new>`_