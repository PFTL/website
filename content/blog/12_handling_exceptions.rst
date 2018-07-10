Why (not) Handling Exceptions
=============================

:date: 2018-06-04
:author: Aquiles Carattino
:subtitle: Learn how to dealing with exceptions in Python
:header: {attach}chuttersnap-553860-unsplash.jpg
:tags: Threads, Processes, Parallel, Speed, Async, Advanced
:description: Why you should not catch exceptions in your programs
:status: draft

    When you develop code, it is almost impossible not to run into an error. Some problems are going to arise as soon as you start your program, for example if you forgot to close a parenthesis, or forgot the ``:`` after an if-statement. However, errors at runtime are also very frequent and harder to anticipate. Imagine that you are reading data from a file. You can simply write something like this:

.. code-block:: python

    f = open('my_file.dat')
    data = f.readfile()
    print('Data loaded')

If you run the code, you will see a message like the following:

.. code-block:: bash

    FileNotFoundError: [Errno 2] No such file or directory: 'my_file.dat'

When an error is raised, the code that follows will not be executed. That is why you don't see the statement ``Data loaded`` on the console. This is innocent, but imagine that you are communicating with a device, you won't have the chance to close the communication with it, or close a shutter, etc.

Try ... Except
--------------
Dealing with this kind of errors is normally done within a ``try`` / ``except`` block. This means that if there is an error inside the ``try``, the block ``except`` will be executed. In the example above, we can do the following:

.. code-block:: python

    try:
        f = open('my_file.dat')
        f.readfile()
        print('Loaded data')
    except:
        print('Data not loaded')

If you run the code, you will see a nice message being printed to screen saying ``Data not loaded``. This is great, now our program is not crashing and we can close the shutter of our device. However, we don't know the reason why the data was not loaded.

Before continuing, create an empty file called **my_file.dat**, and run the script again. You will see that data is not being loaded, regardless whether the file exists or not. No you are seeing the risks around un specific ``try`` blocks. If we make a simpler script:

.. code-block:: python

    f = open('my_file.dat')
    f.readfile()
    print('Loaded data')

The output will be:

.. code-block:: bash

    AttributeError: '_io.TextIOWrapper' object has no attribute 'readfile'

Which is telling us that the problem is the method that we tried to use, ``readfile`` doesn't exist. When you use a plaing try/except block, you are sure you are handling all possible exception, but you have no way of knowing what actually went wrong. In simple cases like the one above, you have only two lines of code to explore. However, if you are building a package, or a function, that kind of errors will propagate downstream, and you don't know how they are going to manifest themselves.

Catching Specific Exceptions
----------------------------
The proper way of handling exceptions in Python is to specify what exception are we expecting. In this way, we know that if the problem is that the file doesn't exist, we can create it, while if the problem is of a different nature, it will be raised and displayed to the user. We can alter the above examples like this:

.. code-block:: python

    try:
        file = open('my_file.dat')
        data = file.readfile()
        print('Data Loaded')
    except FileNotFoundError:
        print('This file doesn\'t exist')

If you run the script, and the file **my_file.dat** doesn't exist, it will print to screen that the file doesn't exist. However, if the file does exist, you will see the exception with ``readfile``. Of course, you are not limited to printing a message when an exception happens. In the case of the file, it is easy to create one:

.. code-block:: python

    try:
        file = open('my_file.dat')
        data = file.readfile()
        print('Data Loaded')
    except FileNotFoundError:
        file = open('my_file.dat', 'w')
        print('File created')
    file.close()

If you run the script once, you will see that the file is being created. If you run the script a second time, you will see the exception with the ``readfile`` method. Imagine that you don't specify which exception you are catching, and you have the following code, what will happen when you run it?:

.. code-block:: python

    try:
        file = open('my_file.dat')
        data = file.readfile()
        print('Data Loaded')
    except:
        file = open('my_file.dat', 'w')
        print('File created')

Exactly, even if the file **my_file.dat** exists, an exception is going to be raised because of the ``readfile`` method. You are going to enter the ``except`` block and you are going to overwrite the file, even if it existed.

Exceptions in Exceptions
------------------------
Imagine that the code above is part of a larger function, responsible for opening a file, loading its content or creating a new file in case the specified filename doesn't exist. The script will look the same as earlier, with the difference that the filename is going to be a variable:

.. code-block:: python

    try:
        file = open(filename)
        data = file.readfile()
    except FileNotFoundError:
        file = open(filename, 'w')

To run the code above, the only thing you have to do is to specify the filename before, for instance:

.. code-block:: python

    filename = 'my_data.dat'
    try:
        [...]

If you run this code, you will notice that it behaves exactly as expected. However, if you specify an empty filename:

.. code-block:: python

    filename = ''
    try:
        [...]

You will see a much longer error printed to screen, with one important line:

.. code-block:: bash

    During handling of the above exception, another exception occurred:

If you look carefully at the error, you will see that it outputs information regarding that an error occurred while the code was already handling another error. This is, unfortunately, a common situation, especially when dealing with user input. The way around it would be to nest another try/except block or to verify the integrity of the inputs before calling ``open``.

Several Exceptions
------------------
So far we have been dealing with only one possible exception, ``FileNotFoundError``. However, we know that the code will raise two different exceptions, the second one being an ``AttributeError``. If you are not sure about which errors can be raised, you can generate them on purpose. For instace, if you run the following:

.. code-block:: python

    file = open('my_data.dat', 'a')
    file.readfile()

You will get the following message:

.. code-block:: bash

    AttributeError: '_io.TextIOWrapper' object has no attribute 'readfile'

The first string is the type of exception, ``AttributeError``, while the second part is the message. The same exception can have different messages, which describe better what has happend. What we want is to catch the ``AttributeError``, but also we want to catch the ``FileNotFound``. Therefore, our code would look like this:

.. code-block:: python

    filename = 'my_data.dat'

    try:
        file = open(filename)
        data = file.readfile()
    except FileNotFoundError:
        file = open(filename, 'w')
        print('Created file')
    except AttributeError:
        print('Attribute Error')

Now you are dealing with several exceptions. Remember that when an exception is raised within the ``try`` block, the rest of the code will not be executed, and Python will go through the different ``except`` blocks. Therefore, only one exception is raised at a time. In the case where the file doesn't exist, the code will deal only with the ``FileNotFoundError``.

Of course, you can also add a final exception to catch all other possible errors in the program, like this:

.. code-block:: python

    filename = 'my_data.dat'

    try:
        file = open(filename)
        data = file.read()
        important_data = data[0]
    except FileNotFoundError:
        file = open(filename, 'w')
        print('Created file')
    except AttributeError:
        print('Attribute Error')
    except:
        print('Unhandled exception')

In this case, if the file exists but it is empty, we are going to have a problem trying to access ``data[0]``. We are not prepared for that exception and therefore we are going to print a message saying *Unhandled exception*. It would be, however, more interesting to let the user know what exception was actually raised. We can do the following:

.. code-block:: python

    filename = 'my_data.dat'

    try:
        file = open(filename)
        data = file.read()
        important_data = data[0]
    except Exception as e:
        print('Unhandled exception')
        print(e)

Which will output the following message:

.. code-block:: bash

    Unhandled exception
    string index out of range

The exception also has a ``type``, which you can use. For example:

.. code-block:: python

    filename = 'my_data.dat'

    try:
        file = open(filename)
        data = file.read()
        important_data = data[0]
    except Exception as e:
        print('Unhandled exception')
        if isinstance(e, IndexError):
            print(e)
            data = 'Information'
            important_data = data[0]

    print(important_data)

Which will print the first letter of ``Information``, i.e. ``I``. The pattern above has a very important drawback, and is that ``important_data`` may end up not being defined. For example, if the file **my_data.dat** doesn't exist, we will get another error:

.. code-block:: bash

    NameError: name 'important_data' is not defined

To prevent this, we can add one more block, ``finally`` that is always going to be executed, regardless of an exception raised or not, for example:

.. code-block:: python

    filename = 'my_data.dat'

    try:
        file = open(filename)
        data = file.read()
        important_data = data[0]
    except Exception as e:
        if isinstance(e, IndexError):
            print(e)
            data = 'Information'
            important_data = data[0]
        else:
            print('Unhandled exception')
    finally:
        important_data = 'A'

    print(important_data)

This is in the end a very silly example, because we are setting ``important_data`` to a special value, but I hope you can see the use of finally. If there is something that you must absolutely be sure that is executed, you can include it in a finally statement. In this way you are sure that you are closing a connection, the communication with a device, etc.

Raising Custom Exceptions
-------------------------
When you are developing your own packages, it is often useful to define some common exceptions. This gives a great deal of flexibility, because it allows other developers to handle those exceptions as appropriate. Let's see an example. Imagine that you want to write a function that calculates the average between two numbers, but you want both numbers to be positive. This is the same example we have seen when working with `decorators <{filename}04_how_to_use_decorators_2.rst>`_. We start by defining the function:

.. code-block:: python

    def average(x, y):
            return (x + y)/2

And now we want to raise an ``Exception`` if either input is negative, we can do the following:

.. code-block:: python

    def average(x, y):
        if x<=0 or y<=0:
            raise Exception('Both x and y should be positive')
        return (x + y)/2

If you try it yourself with a negative input, you will see the following printed:

.. code-block:: bash

    Exception: Both x and y should be positive

Which is great, it even points to the line number with the issue, etc. However, if you are building a module and you expect others to use it, it would be much better to define a custom Exception, that can be explicitly catched. It is as easy as this:

.. code-block:: python

    class NonPositiveError(Exception):
        pass

    def average(x, y):
        if x <= 0 or y <= 0:
            raise NonPositiveError('Both x and y should be positive')
        return (x + y) / 2

An exception is a class, and therefore it should inherit from the general ``Exception`` class. We don't really need to customize anything at this stage, we just type ``pass``in the body of the class. If we run the code above with a negative value, we will get:

.. code-block:: bash

    NonPositiveError: Both x and y should be positive

If you want to catch that exception in downstream code, you will do it as always. The only difference is that custom exceptions are not available by default and you should import them. For example, you would do the following:

.. code-block:: python

    from exceptions import NonPositiveError
    from tools import average

    try:
        avg = average(1, -2)
    except NonPositiveError:
        avg = 0

If you have worked long enough with packages, probably you have already encounter a lot of different exceptions. They are a great tool to let the user know exactly what was wrong and act accordingly. Sometimes we can be prepared for some exceptions, and is very appreciated when custom ones are included into the package and not just a generic one that forces us to catch any exception, even if some that we were not actually expecting.

Warnings and Exceptions
-----------------------
Python also provides a different kind of



