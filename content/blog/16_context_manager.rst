The with command and custom classes
===================================

:date: 2019-02-02
:author: Aquiles Carattino
:subtitle: Using the with command and developing classes that support it
:header: {attach}tobias-fischer-185901-unsplash.jpg
:tags: Context Manager, With, Custom Classes, Patterns
:description: Using the with command and developing classes that support it

There is a common pattern when programming that is opening a resource, doing something with it and closing it. This is what you normally do with a file, a network connection or a device. Python offers you a command to handle this pattern: the 'with' context manager. In this article, we are going to see how you can develop classes that follow the same pattern.

Quick Introduction to the With Command
---------------------------------------
If you would like to write a string to a file, you can do the following:

.. code-block:: python

    f = open('My_File.txt', 'w')
    f.write('This goes to the file\n')
    f.close()

The lines above will create an empty file every time you run them and will write a line to it. When the program is done, it closes the file. If you would remove the last line, ``f.close``, the program would have worked in the same way. However, errors sometimes arise and you would like to be sure that the file was closed and the data was saved. The lines above can be replaced by the following:

.. code-block:: python

    with open('My_File.txt', 'w') as f:
        f.write('This is within a context manager\n')

The advantage of using the ``with`` command is not only that you type one line less to type, but it is also that if something would happen when you try to write, the file will be safely closed and the data will be written. The advantages may not be obvious for simple examples, but long-running programs in which a lot of data is generated will start to show issues if files are not closed correctly. Also, when you use resources other than files, such as network connections or hardware devices, you will also see that properly closing the resources is fundamental.

In practice, you can also think about the with command as doing the following:

.. code-block:: python

    f = open('my_file.txt', 'w')
    try:
        f.write('This is the first line\n')
    except Exception as e:
        pass
    f.close()
    raise e

You can try to see what happens if you raise an exception after the ``write`` command. The data will be in your file and the file would have been correctly closed.

Custom Classes and With
-----------------------
Working with files and other resources is interesting, but more interesting would be to develop classes that can be used within a context manager. First, we need to understand the steps that form the creation of a class. First, let's start with the brute force approach, and we create a simple class:

.. code-block:: python

    class SimpleClass:
        def simple_method(self):
            print('Simple Method')

        def finalize(self):
            print('Finalizing the Class')

That we can simply use like this:

.. code-block:: python

    sc = SimpleClass()
    sc.simple_method()
    # Simple Method
    sc.finalize(self)
    # Finalizing the Class

This is not very enthusiastic, but it is a starting point. Let's try to use a context manager with our class:

.. code-block:: python

    with SimpleClass() as sc:
        sc.simple_method()

We will face an issue, the error that appears on the screen should be:

.. code-block:: python

    AttributeError: __enter__

This basically means that the brute force approach doesn't work with context managers, we need to work a bit more. Without going too much in circles, the ``with`` requires two methods of the so-called *magic* type: ``__enter__`` and ``__exit__`` that will be run at the beginning and at the end of the code block.

It is important to note that whatever is returned by ``__enter__`` will be linked to the target of ``with``, i.e. whatever variable we put after ``as``. In the simplest of the possibilities, ``__enter__`` returns the class itself, like this:

.. code-block:: python

    class SimpleClass:
        def __enter__(self):
            return self

We also need to add an ``__exit__`` method, which takes several arguments, not only ``self``:

.. code-block:: python

    def __exit__(self, exc_type, exc_val, exc_tb):

What you have to remember is that ``with`` takes care of catching any exceptions that may arise and all the information is passed to the exit method so you can decide what to do with them. Right now, the only thing we want to do is to call the finalize method. The complete code would look like this:

.. code-block:: python

    class SimpleClass:
        def simple_method(self):
            print('Simple Method')

        def finalize(self):
            print('Finalizing the Class')

        def __exit__(self, exc_type, exc_val, exc_tb):
            self.finalize()

        def __enter__(self):
            return self

And you can use it like this:

.. code-block:: python

    with SimpleClass() as sc:
        sc.simple_method()

Which will produce the following output:

.. code-block:: python

    Simple Method
    Finalizing the Class

This is exactly what we were expecting. You can go on and try to generate some exception in your code and see how the program handles it. You can also print the arguments passed in order to understand what you can do with them. For example, you can do the following in the exit method:

.. code-block:: python

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.finalize()
        print(exc_type)
        print(exc_val)
        print(exc_tb)

And then change the code you use to run it:

.. code-block:: python

    with SimpleClass() as sc:
        sc.simple_method()
        raise Exception('This is an Exception')

Which will generate the following output:

.. code-block:: python

    <class 'Exception'>
    This is an Exception
    <traceback object at 0x7fa88e46b588>

This is enough to make decisions based on the kind of information that the exception is providing. You can check the `previous article on exceptions <{filename}12_handling_exceptions.rst>`_ to have an idea of the kind of things you can accomplish.

.. newsletter::

With and Constructors
---------------------
In the simple class that we have seen earlier, we completely skipped the discussion of what happens when you have a constructor, i.e. the ``__init__`` method is defined. So let's quickly try it. Let's make the ``SimpleClass`` print at each step:

.. code-block:: python

    class SimpleClass:
        def __init__(self):
            print('Init')

        def simple_method(self):
            print('Simple Method')

        def finalize(self):
            print('Finalizing the Class')

        def __exit__(self, exc_type, exc_val, exc_tb):
            print('Exit')
            self.finalize()

        def __enter__(self):
            print('enter')
            return self

If you run it with the same code than before, the output that you would get is:

.. code-block:: python

    Init
    enter
    Simple Method
    Exit
    Finalizing the Class

So, now you can see that first, you instantiate the class (the ``__init__`` method is triggered) and only then the ``__enter__`` is executed. This experimenting approach is very useful because you can already learn a lot without having to search online and go through endless tutorials.

Another important thing to note is that after the ``with`` block, the class is still available:

.. code-block:: python

    with SimpleClass() as sc:
        sc.simple_method()
        # raise Exception('This is an Exception')

    sc.simple_method()

The command only takes care of executing the *exit* method but does not force any garbage collection. This means that the object is still available after the ``with`` block. You can test that with files or serial communication and you will notice that if you try to use the same file handler it gives you an error:

.. code-block:: python

    ValueError: I/O operation on closed file.

This means that the file handler is still available, but the resource was already closed.

Why Go to the Trouble
---------------------
When we discuss this kind of topics, you always have to consider the two sides of a project. You are either using someone's code or you are developing code someone else will expand. In the first case, using a context manager ensures that you follow the pattern that the original developer intended. All the work for exception handling, resource freeing, etc. was already taken care of and all it takes you is one line of code. Therefore, if you are a *user*, the ``with`` can save you a lot of headaches and can speed your development.

If you are a *developer*, implementing two extra methods doesn't take that long and allows the user to employ a common syntax. If you later improve your code adding better error handling, resources administration, etc. the users of your code will receive those improvements automatically, without changing a single line of their code.

**Does every class need to support the ``with``?**
Let's be realistic. Very few of the operations your program performs require access to resources that need to be closed. Network communication, device control, writing to files are some examples and probably you won't encounter many more. If you are a developer, you have to consider whether implementing the possibility of using context managers helps future users of your code.

Conclusions
-----------
The problem of focusing on very simple examples is that it makes it very hard to realize the true power of different patterns and why is it worth going through the trouble of implementing new methods, etc. The truth is that until you have a large and complex project in your hands, you won't really realize it.

The power of the context manager becomes apparent when your code is used by other people and your class has a clear cycle of opening and closing resources, such as would be the case of working with a file, a network connection or a device in the lab. The main advantage comes from the fact that you can implement complex ways of closing and handling exceptions but at the same time, you give the user a lot of freedom about what to do.

In the example above, the only thing that needs to be done is calling the ``finalize`` method, but we could make the ``exit`` more sophisticated in order to execute some verifications, exception handling, etc. However, if the user would like to have finer control, she can still use the direct methods.

Implementing two methods in order to allow the user to use the ``with`` and ensure that closing methods are executed, I believe, offsets the work of implementing them. If you want to see a real-world example, you can check how `pyserial <https://github.com/pyserial/pyserial/blob/a27715f322bb08b1fccffebab776c94df50057e9/serial/serialutil.py#L561>`_ has implemented the ``__enter__`` and ``__exit__`` methods.
