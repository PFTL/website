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