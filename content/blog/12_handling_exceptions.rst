Learning (not) to Handle Exceptions
===================================

:date: 2018-06-04
:author: Aquiles Carattino
:subtitle: Learn how to deal with exceptions in Python
:header: {attach}cody-davis-253928-unsplash.jpg
:tags: Exceptions, Errors, Try, Except, Catch, Handling
:description: Learn how to deal with exceptions in Python

    When you develop code, it is almost impossible not to run into an error. Some problems are going to arise as soon as you start your program, for example, if you forgot to close a parenthesis, or forgot the ``:`` after an if-statement. However, errors at runtime are also very frequent and harder to deal with. In this article, you are going to learn how to handle exceptions, i.e. how to avoid program crashes when you can anticipate that an error may appear.

We are going to cover from the basics of error handling to defining your own exceptions. You will learn why sometimes it is better not to catch exceptions and how to develop a pattern that can be useful for future users of your code. Exceptions are a crucial part of any code, and dealing with them elegantly can improve a lot the value of your code.

.. contents::

As always, you can check `the example code <https://github.com/PFTL/website/tree/master/example_code/12_exceptions>`_ for this article and `the original text <https://github.com/PFTL/website/blob/master/content/blog/12_handling_exceptions.rst>`_ in case you have any suggestions to improve it.

Try ... Except
--------------
 Imagine that you are reading data from a file. You can simply write something like this:

.. code-block:: python

    f = open('my_file.dat')
    data = f.readfile()
    print('Data loaded')

If you run the code, you will see a message like the following:

.. code-block:: bash

    FileNotFoundError: [Errno 2] No such file or directory: 'my_file.dat'

When an error is raised, the code that follows will not be executed. That is why you don't see the statement ``Data loaded`` on the console. This is a somewhat innocent problem but imagine that you are communicating with a device. If there is an error in your program, you won't have the chance to close the communication with the device, or you won't be able to close a shutter to prevent damages to the detectors, etc.

Dealing with this kind of errors is normally done within a ``try`` / ``except`` block. This means that if there is an error inside the ``try``, the block ``except`` will be executed. In the example above, we can do the following:

.. code-block:: python

    try:
        f = open('my_file.dat')
        f.readfile()
        print('Loaded data')
    except:
        print('Data not loaded')

If you run the code, you will see a nice message being printed to screen saying ``Data not loaded``. This is great! Now our program is not crashing and we can close the shutter, or stop the communication with our device. However, we don't know the reason why the data was not loaded.

Before continuing, create an empty file called **my_file.dat**, and run the script again. You will see that data is not being loaded, regardless whether the file exists or not. With this trivial example, you are seeing the risks around unspecific ``except`` blocks. If we make a simpler script:

.. code-block:: python

    f = open('my_file.dat')
    f.readfile()
    print('Loaded data')

The output will be:

.. code-block:: bash

    AttributeError: '_io.TextIOWrapper' object has no attribute 'readfile'

Which is telling us that the problem is the method that we tried to use, ``readfile`` doesn't exist. When you use a plain ``try/except`` block, you are sure you are handling all possible exceptions, but you have no way of knowing what actually went wrong. In simple cases like the one above, you have only two lines of code to explore. However, if you are building a package or a function, some errors will propagate downstream, and you don't know how they are going to affect the rest of the program.

For you to have an idea of the importance of correct handling of errors, I will tell you what I have witnessed using a program that ships with a very sophisticated lab instrument. The program that controls the `Nano Sight <https://www.malvernpanalytical.com/en/products/product-range/nanosight-range>`_ has a very nice user interface. However, when you are saving data, if the filename you choose has a dot in it, the data will not be saved. Sadly, the data will also be lost and the user will never know that the problem was having a simple ``.`` in the filename.

Handling all possible errors in a graceful way is very complicated and sometimes almost impossible. However, you can see that even the software that ships with very expensive instruments (in this case I mean instruments with a price tag similar to a small apartment), also has to deal with all kinds of exceptions, and not always in the most user-friendly way.

.. newsletter::

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

If you run the script, and the file **my_file.dat** doesn't exist, it will print to screen that the file doesn't exist and the program will keep running. However, if the file does exist, you will see the exception with ``readfile``. Of course, you are not limited to printing a message when an exception happens. In the case of the non-existing file, it is easy to create one:

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

If you look carefully, you will realize that even if the file **my_file.dat** exists, an exception is going to be raised because of the ``readfile`` method. Then the ``except`` block is going to be executed. In this block, the program is going to create a new **my_file.dat**, even if it already existed, and therefore you are going to lose the information stored in it.

Re-raising Exceptions
---------------------
A very common scenario is that when an exception appears, you want to do something but then raise the same exception. This is a very common case when writing to a database or to different files. Imagine the case where you are storing information in two files, in the first one you store spectra and in the second one the temperature at which you acquire each one. You first save the spectra and then the temperature, and you know that each line on one file corresponds to one file on the second file.

Normally, you save first a spectrum and then you save the temperature. However, once in a while, when you try to read from the instrument, it crashes and the temperature is not recorded. If you don't save the temperature, you will have an inconsistency in your data, because a line is missing. At the same time, you don't want the experiment to keep going, because the instrument is frozen. Therefore, you can do the following:

.. code-block:: python

    [data already saved]

    try:
        temp = instrument.readtemp()
    except:
        remove_last_line(data_file)
        raise
    save_temperature(temp)

What you can see here is that we try to read the temperature and if anything happens, we will catch it. We remove the last line from our data file, and then we just call ``raise``. This command will simply re-raise anything that was caught by the ``except``. With this strategy, we are sure that we have consistent data, that the program will not keep running and that the user will see all the proper information regarding what went wrong.

Exceptions in Exceptions
------------------------
Imagine that the code is part of a larger function, responsible for opening a file, loading its contents or creating a new file in case the specified filename doesn't exist. The script will look the same as earlier, with the difference that the filename is going to be a variable:

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
So far we have been dealing with only one possible exception, ``FileNotFoundError``. However, we know that the code will raise two different exceptions, the second one being an ``AttributeError``. If you are not sure about which errors can be raised, you can generate them on purpose. For instance, if you run this code:

.. code-block:: python

    file = open('my_data.dat', 'a')
    file.readfile()

You will get the following message:

.. code-block:: bash

    AttributeError: '_io.TextIOWrapper' object has no attribute 'readfile'

The first string is the type of exception, ``AttributeError``, while the second part is the message. The same exception can have different messages, which describe better what has happened. What we want is to catch the ``AttributeError``, but also we want to catch the ``FileNotFound``. Therefore, our code would look like this:

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

The Finally Statement
---------------------
To prevent what we just saw in the previous section, we can add one more block to the sequence: ``finally``. This block is always going to be executed, regardless of whether an exception was raised or not. For example:

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

This is, in the end, a very silly example, because we are setting ``important_data`` to a special value, but I hope you can see the use of ``finally``. If there is something that you must absolutely be sure that is executed, you can include it in a finally statement.

``finally`` is very useful to be sure that you are closing a connection, the communication with a device, closing a file, etc. Generally speaking, releasing the resources. Finally has a very interesting behavior, because it is not executed always at the same moment. Let's see the following code:

.. code-block:: python

    filename = 'my_data.dat'

    try:
        print('In the try block')
        file = open(filename)
        data = file.read()
        important_data = data[0]
    except FileNotFoundError:
        print('File not found, creating one')
        file = open(filename, 'w')
    finally:
        print('Finally, closing the file')
        file.close()
        important_data = 'A'

    print(important_data)

First, run the code when the file **my_data.dat** doesn't exist. You should see the following output:

.. code-block:: bash

    In the try block
    File not found, creating one
    Finally, closing the file

So, you see you went from the ``try`` to the ``except`` to the ``finally``. If you run the code again, the file will exist, and therefore the output will be completely different:

.. code-block:: bash

    In the try block
    Finally, closing the file
    Traceback (most recent call last):
      File "JJ_exceptions.py", line 7, in <module>
        important_data = data[0]
    IndexError: string index out of range

What you can see here is that when an unhandled exception is raised, the first block to be executed is the ``finally``. You close the file immediately. And then, the error is re-raised. This is very handy because it prevents any kind of conflict with downstream code. You open, you close the file and then the rest of the program has to deal with the problem of the ``IndexError``. If you want to try a program without exceptions, just write something into **my_data.dat** and you will see the output.

The else Block
--------------
There is only one more block to discuss in the exception handling pattern, the ``else`` block. The core idea of this block is that it gets executed if there were no exceptions within the ``try`` block. Is very easy to understand how it works, you could, for example, do the following:

.. code-block:: python

    filename = 'my_data.dat'

    try:
        file = open(filename)
    except FileNotFoundError:
        print('File not found, creating one')
        file = open(filename, 'w')
    else:
        data = file.read()
        important_data = data[0]

The most difficult part of the else block is understanding its usefulness. In principle, the code that we have included in the ``else`` block could have also been placed right after opening the file, as we have done earlier. However, we can use the ``else`` block to prevent catching exceptions that do not belong to the ``try``. It is a bit far-fetched examples, but imagine that you need to read a filename from a file and open it. The code would look like this:


.. code-block:: python

    try:
        file = open(filename)
        new_filename = file.readline()
    except FileNotFoundError:
        print('File not found, creating one')
        file = open(filename, 'w')
    else:
        new_file = open(new_filename)
        data = new_file.read()

Since we are opening two files, it may very well be that the problem is that the second file doesn't exist. If we would put this code into the ``try`` block, we would end up triggering the ``except`` for the second file even if we didn't mean to. At first, it is not obvious the true use of the ``else`` block, but it can be very useful and therefore it is important that you are aware that it exists.

Of course, it is possible to combine everything that you have learned so far:

.. code-block:: python

    try:
        file = open(filename)
        new_filename = file.readline()
    except FileNotFoundError:
        print('File not found, creating one')
        file = open(filename, 'w')
    else:
        new_file = open(new_filename)
        data = new_file.read()
    finally:
        file.close()

You are very encouraged to play around and try to find different usages for each block. If you have worked enough with Python, probably you encounter plenty of exceptions that forced you to re-run your script from the beginning. Now you know that there may be workarounds. A great resource, as almost always, is the `Python Documentation on Exceptions <https://docs.python.org/3/tutorial/errors.html>`_.

Things are not over yet, there are many more things that can be done with exceptions.

The Traceback
-------------
As you have probably seen already, when there is an exception, a lot of information is printed to the screen. For example, if you try to open a not existing file you get:

.. code-block:: bash

    Traceback (most recent call last):
      File "P_traceback.py", line 13, in <module>
        file = open(filename)
    FileNotFoundError: [Errno 2] No such file or directory: 'my_data.dat'

Interpreting the message may take a bit of practice, but for simple cases it is clear. First, it tells you that you are seeing a traceback, in simple words the history of things that lead to the exception. I will cover more on this on a separate post. However, you can clearly see the file that generated the problem and the line. If you open the file and go to that line, you will see that it is exactly the one that says ``file = open(filename)``. Finally, you see the exception.

This last message is the one we were printing to screen, but we were neglecting the traceback that would allow us to find the real source of the exception and act accordingly. Fortunately, Python allows us to access the traceback very easily. Slightly modifying the example of opening a file, we would have:

.. code-block:: python

    import traceback

    filename = 'my_data.dat'

    try:
        file = open(filename)
        data = file.read()
    except FileNotFoundError:
        traceback.print_exc()

If you run the code again, you will see printed to screen the same information than before. The main difference is that your program didn't crash, because you were handling the exception. Working with tracebacks is very handy for debugging. The examples that you have seen here are very simple, but when you have a very nested code, i.e., one function calls another that creates an object, that runs a method, etc. it is very important to pay attention to the traceback in order to know what triggered the exception.

Raising Custom Exceptions
-------------------------
When you are developing your own packages, it is often useful to define some common exceptions. This gives a great deal of flexibility because it allows other developers to handle those exceptions as they find appropriate. Let's see an example. Imagine that you want to write a function that calculates the average between two numbers, but you want both numbers to be positive. This is the same example that we have seen when working with `decorators <{filename}04_how_to_use_decorators_2.rst>`_. We start by defining the function:

.. code-block:: python

    def average(x, y):
        return (x + y)/2

And now we want to raise an ``Exception`` if either input is negative. We can do the following:

.. code-block:: python

    def average(x, y):
        if x<=0 or y<=0:
            raise Exception('Both x and y should be positive')
        return (x + y)/2

If you try it yourself with a negative input, you will see the following printed:

.. code-block:: bash

    Exception: Both x and y should be positive

Which is great, it even points to the line number with the issue, etc. However, if you are building a module and you expect others to use it, it would be much better to define a custom Exception, that can be explicitly caught. It is as easy as this:

.. code-block:: python

    class NonPositiveError(Exception):
        pass

    def average(x, y):
        if x <= 0 or y <= 0:
            raise NonPositiveError('Both x and y should be positive')
        return (x + y) / 2

An exception is a class, and therefore it should inherit from the general ``Exception`` class. We don't really need to customize anything at this stage, we just type ``pass`` in the body of the class. If we run the code above with a negative value, we will get:

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

If you have worked long enough with packages, probably you have already encountered a lot of different exceptions. They are a great tool to let the user know exactly what was wrong and act accordingly. Sometimes we can be prepared for some exceptions and is very appreciated when custom ones are included into the package and not just a generic one that forces us to catch any exception, even if it is something that we were not actually expecting.

Best Practices for Custom Exceptions
------------------------------------
When you are developing a package, it is very handy to define exceptions that are exclusive to it. This makes it much easier to handle different behaviors and gives developers a very efficient way to filter whether the problems are within your package or with something else. Imagine, for instance, that you are working with a complex package, and you want to write to a file every time an exception from that specific package appears.

This is very easy to achieve if all the exceptions inherit from the same base class. The code below is a bit longer, but it is built on top of all the examples above, so it should be easy to follow:

.. code-block:: python

    class MyException(BaseException):
        pass

    class NonPositiveIntegerError(MyException):
        pass

    class TooBigIntegerError(MyException):
        pass

    def average(x, y):
        if x<=0 or y<=0:
            raise NonPositiveIntegerError('Either x or y is not positive')

        if x>10 or y>10:
            raise TooBigIntegerError('Either x or y is too large')
        return (x+y)/2

    try:
        average(1, -1)
    except MyException as e:
        print(e)

    try:
        average(11, 1)
    except MyException as e:
        print(e)

    try:
        average('a', 'b')
    except MyException as e:
        print(e)

    print('Done')

We first define an exception called ``MyException``, which is going to be our base exception. We then define two errors, ``NonPositiveIntegerError`` and ``TooBigIntegerError`` which inherit from ``MyException``. We define the function ``average`` again but this time we raise two different exceptions. If one of the numbers is negative or larger than 10.

When you see the different use cases below, you will notice that in the ``try/except`` block, we are always catching ``MyException``, but not one of the specific errors. In the first two examples, when passing ``-1`` and ``11`` as arguments, we successfully print to screen the error message, and the program keeps running. However, when we try to calculate the average between two letters, the ``Exception`` is going to be of a different nature, and is not going to be caught by the ``Except``. You should see the following on your screen:

.. code-block:: bash

    TypeError: '<=' not supported between instances of 'str' and 'int'

Adding Arguments to Exceptions
------------------------------
Sometimes it is handy to add arguments to exceptions in order to give a better context to users. With the example of the average, let's first define a more complex exception:

.. code-block:: python

    class MyException(BaseException):
        pass

    class NonPositiveIntegerError(MyException):
        def __init__(self, x, y):
            super(NonPositiveIntegerError, self).__init__()
            if x<=0 and y<=0:
                self.msg = 'Both x and y are negative: x={}, y={}'.format(x, y)
            elif x<=0:
                self.msg = 'Only x is negative: x={}'.format(x)
            elif y<=0:
                self.msg = 'Only y is negative: y={}'.format(y)

        def __str__(self):
            return self.msg


    def average(x, y):
        if x<=0 or y<=0:
            raise NonPositiveIntegerError(x, y)
        return (x+y)/2

    try:
        average(1, -1)
    except MyException as e:
        print(e)

What you can see is that the exception takes two arguments, ``x`` and ``y`` and it generates a message based on them. They can be both negative or only one of them is negative. It doesn't only give you that information, but it actually displays the value that gave problems. This is very handy to understand what went wrong exactly. The most important part is at the end of the class: the ``__str__`` method. This method is responsible for what appears on the screen when you do ``print(e)`` in the ``except`` block. In this case, we are just returning the message generated within the ``__init__``, but many developers choose to generate the message in this method, based on the parameters passed at the beginning.

Conclusions
-----------
Exceptions are something nobody wants to see but they are virtually unavoidable. Maybe you try to read a file that doesn't exist, the user of your code has chosen invalid values, the matrix you are analyzing has different dimensions than expected, etc. Handling exceptions is a sensitive topic because it can lead to even more problems downstream. An Exception is a clear message that there is something wrong going on and if you don't fix it properly, it is going to become even worse.

Handling exceptions can help you to avoid having inconsistent data, not closing resources such as devices, connections or files, etc. However, not handling exceptions correctly can lead to even more problems later on. The ``try/except`` block is very handy when you know what kind of exceptions can appear and you know how to handle them. Imagine you are performing several steps of a complex operation, like writing to a database. If an error happens, you can revert all the changes and avoid inconsistencies.

As with almost any other Python topic, the best way to learn is to look closely at other's code and judge by yourself. Not all packages define their own exceptions, nor handle them in the same way. If you are looking for inspiration, you can see the `errors of Pint <https://github.com/hgrecco/pint/blob/master/pint/errors.py>`_, a relatively small package, or the `exceptions of Django <https://github.com/django/django/blob/master/django/core/exceptions.py>`_, a much more complex package.

Photo by `Cody Davis <https://unsplash.com/photos/5E5N49RWtbA?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText>`_ on Unsplash

Remember, that both `the code <https://github.com/PFTL/website/tree/master/example_code/12_exceptions>`_ and `the text <https://github.com/PFTL/website/blob/master/content/blog/12_handling_exceptions.rst>`_ of the article is available, in case you have any comments or suggestions to improve it.