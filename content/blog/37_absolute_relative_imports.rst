Imports: Absolute, Relative, and More
=====================================

:status: draft
:date: 2019-09-16
:author: Aquiles Carattino
:subtitle: How to plan your code so imports are clear and clean
:description: How to plan your code so imports are clear and clean
:header: {attach}ivana-cajina-324103-unsplash.jpg
:tags: importing, import, relative, absolute, package

Importing is not only a matter of using external libraries, it also allows you to keep your own code clean and organized. In this tutorial we are going to discuss from the very basics of importing to complex topics such as lazy loading of modules in your own packages. You are free to skip ahead to the section that compels you the most.

.. contents::

Introduction to importing
-------------------------
In Python, whenever you want to import a module, you do the following:

.. code-block:: python

   import sys

In this case, ``sys`` is a Python Standard Library which provides functions you to interact with the interpreter itself. Python comes bundled with plenty of libraries for different tasks. You can find them all `here <https://docs.python.org/3/library/index.html>`__. If you would like to use a function defined in this module, you can simply do:

.. code-block:: python

   sys.exit()

Which will terminate your Python session. ``sys`` is able to do many more things than just quitting the interpreter. It can also tell you if you are running a script with some arguments. For example, you can write the following to a file **test_argv.py**:

.. code-block:: python

   import sys

   print(sys.argv)

Now, you can run the file and see what the output is:

.. code-block:: bash

   python test_argv.py -b 1

Importing the entire ``sys`` module may not be what we want, since we are only using one of its functions. In this case, we can also be very selective with what we want to import:

.. code-block:: python

   from sys import argv

   print(argv)

And the output will be the same. Understanding when you will use the full import or you will select just what you need depends a lot on your personal preference, on what do you want to achieve, and on what the library requires.

Importing *
-----------
On the examples above, we have seen that we were importing only one module from ``sys``. If we would want to import more modules, we can specify them on the same line, for example:

.. code-block:: python

   from sys import argv, exit

   print(argv)
   exit()

You can import as many packages as you want. A common practice, to avoid having lines that become too long, is to stack them vertically. For example, you could have something like this:

.. code-block:: python

   from sys import (api_version,
                    argv,
                    base_exec_prefix,
                    exit,
                    )

Note the use of the ``(``, ``)`` in order to make a clear list of imports. As you may imagine, if you need to import a lot of modules from a package, it becomes troublesome to make a list of all you need. Therefore, you may want to import all of the available modules at once. Python allows you to do it like this:

.. code-block:: python

   from sys import *

   print(api_version)
   print(argv)
   exit()

However, this is a practice which is highly discouraged. Since you are importing modules without control, it may happen that some functions get overwritten. Let's see it with the following example:

.. code-block:: python

   from time import *
   from asyncio import *

Perhaps you are aware that ``time`` has a function called ``sleep``, which halts the execution of the program for a given number of seconds. If you write and run a script like the following:

.. code-block:: python

   print('Here')
   sleep(1)
   print('After')

You will notice that there is no delay between the lines ``'Here'`` and ``'After'``. What is happening is that both ``time`` and ``asyncio`` define a function ``sleep`` which behaves in very different ways. The amount of knowledge that you need to keep in your head in order to understand what is going on is so large, that most developers avoid using the ``*`` when importing.

The case of ``time`` and ``asyncio`` is special, because both of them belong to the standard Python library. When you start using libraries defined by other's, sometimes it is hard to know and remember all the modules and functions defined. Moreover, some names are so handy (like ``sleep``), that you may find them defined in different packages.

Unless you know exactly what and why you would need to ``import *``, it is very wise to use the first syntax that we saw in the article:

.. code-block:: python

   import time
   import asyncio

   print('Here')
   asyncio.sleep(1)
   print('After')
   time.sleep(1)
   print('Finally')

And now you know exactly what is going on, even if you haven't used the ``asyncio`` library before. When we discuss about importing your own modules, it will become much clearer how the Python importing machinery works.

Importing As
------------
We say that when importing modules, sometimes we will find ourselves in the situation in which two packages define different functions with the same name. Such is the case of ``time`` and ``asyncio`` which both define ``sleep``. To avoid this name clash when importing, Python allows us to change the name of what we are importing. We can do the following:

.. code-block:: python

   from asyncio import sleep as async_sleep
   from time import sleep as time_sleep

   print('Here')
   async_sleep(1)
   print('After')
   time_sleep(1)
   print('Finally')

In this way, we can use either the ``sleep`` from ``asyncio`` or from ``time`` avoiding name clashes. With this we import just the modules we want, and not the entire package, but still maintain our options open.

The example above is only one case in which the ``import as`` is handy. If you are used to generating plots with Python, probably you have encountered lines like this:

.. code-block:: python

   import matplotlib.pyplot as plt
   import numpy as np
   import pandas as pd

The three lines above are ubiquitous in many scientific programs. They are so common that editors such as Pycharm are able to suggest you to import numpy if they see a line that includes something like ``np.``. In the examples above, the import as is not to prevent name clashes, but to make the notation handier. Instead of typing:

.. code-block:: python

   matplotlib.pyplot.plot(x, y)

You can simply type:

.. code-block:: python

   plt.plot(x, y)

Different packages have different shortcuts. For example ``PyQtGraph`` is normally shortened as ``pg``, and for sure different fields use different abbreviations. Importing Numpy as ``np`` or Pandas as ``pd`` is not mandatory. However, since it is what the community does, it will make your code much more readable.

.. note:: If you go through StackOverflow, you will see that more often than not, the line in which numpy is imported is omitted and you just see the use of ``np``.

Absolute Imports
----------------
So far, we have seen how to import packages and modules developed by other people. Importing, however, is a great tool to structure different parts of your code into different files, making it much handier to maintain. Therefore, sooner or later you are going to find yourself importing your own code. Let's start very simple and build up in complexity. In a file called **first.py** let's place the following code:

.. code-block:: python

   def first_function():
      print('This is the first function')

In another file, let's call it **second.py**, let's put the following code:

.. code-block:: python

   from first import first_function

   first_function()

And you can run it:

.. code-block:: bash

   $ python second.py
   This is the first function

That is as easy as it gets. You define a function in a file, but you use that function in another file. Bear in mind that what we discussed in the previous sections still holds. You can do ``from first import first_function as ff``, for example. Having only scripts is just the beginning. At some point you will also organize your code into folders. Let's create a folder called **module_a**, within it, a new file, called **third.py**. So the folder structure is like this:

.. code-block:: bash

   $ tree
   .
   ├── first.py
   ├── module_a
   │   └── third.py
   └── second.py

Let's add a new function in **third**. Bear in mind that the examples are incredibly basic in order not to loose the important concepts from sight:

.. code-block:: python

   def third_function():
       print('This is the third function')

Now, let's edit **second.py** in order to import this new function:

.. code-block:: python

   from first import first_function
   from module_a.third import third_function

   first_function()
   third_function()

If you run it as before, you will get the following output:

.. code-block:: bash

   This is the first function
   This is the third function

Pay attention to the notation we used to import the ``third_function``. We specified the folder, in this case ``module_a`` and then we referred to the file with a dot: ``.``. We ended up having ``module_a.third``, and we stripped the ``.py``.

Relative Imports
----------------

Limitations
-----------

The __init__.py file
--------------------

Lazy Importing
--------------

