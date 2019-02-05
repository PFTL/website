Virtual Environment is a Must-Have Tool
=======================================

:date: 2018-03-09
:author: Aquiles Carattino
:subtitle: Isolate different development environments from each other to avoid overlaps
:header: {attach}michael-aleo-571965-unsplash.jpg
:description: Isolate different development environments from each other to avoid overlaps
:tags: Python, Virtual Environment, Development, Tricks, Tools

When you start developing software, it is of utmost importance to have an isolated programming environment in which you can control precisely the packages installed. This will allow you, for example, to use experimental libraries without overwriting software that other programs use on your computer. Isolated environments allow you, for example, to update a package only within that specific environment, without altering the dependencies in every other development you are doing.

Python provides a very convenient tool called ``Virtual Environment`` that allows you to do exactly what was described. The instructions are slightly different depending on the operating system that you use, but they are easy to adapt from one to the other. To install ``Virtual Environment`` you can do it with ``pip``, the package manager of Python. Remember that sometimes you may have more than one version of pip in your computer, in the same way, you may have more than one version of Python. For example, if you are using Python 3, you would type in the command line:

.. code-block:: bash

   pip3 install virtualenv

If you are on Linux, you may need to add ``sudo`` to the command: ``sudo pip3 install virtualenv``, depending on how you have installed Python. This is the last installation that you do system-wide. From now on, everything else will happen within a `Virtual Environment`. It is a common practice to encapsulate projects in folders that also contain the virtual environment. You have to be sure, however, that you don't add your virtual environment folder to version control, or you will end up having **huge** repositories.

.. code-block:: bash

   mkdir myproject
   cd myproject
   virtualenv venv -p python3

The first line creates the folder for the project and then we move into it. In the last line, we create the virtual environment within a folder called ``venv`` and using a specific version of Python, in this case it is  ``python3``. Now it is time to activate the virtual environment. On Linux you would do:

.. code-block:: bash

   source venv/bin/activate

while on Windows the command would be (pay attention to the ``.\`` at the beginning):

.. code-block:: powershell

   .\venv\Scripts\activate

If everything went well, you will see that a ``(venv)`` appears at the beginning of the command line. Now you are working inside the Virtual Environment called ``venv`` and all the packages you install are going to be stored within it. Let's install a package to see how it works.

.. code-block:: bash

   pip install Flask==1.0

The command will install a very specific version of Flask, which is not the most recent one. One of the useful aspects of virtual environments is that they allow you to keep track of all the packages that you have installed, including their versions. If you execute this command:

.. code-block:: bash

   pip freeze

You will see all the installed packages. You should see that you have installed not only Flask, but all of its dependencies, each one with a specific version. It is wise to output the results to a file that you can use later on for automatically installing all the requirements of your project:

.. code-block:: bash

   pip freeze > requirements.txt

If you open the file ``requirements.txt`` you will notice that it contains a list with all the packages from ``venv``. To see the full potential of Virtual Environment, let's create a second one. First, we need to deactivate the one we are working on now by running:

.. code-block:: bash

   deactivate

And now we repeat the step above to create a new environment, but with a different name:

.. code-block:: bash

   virtualenv test -p python3

And we activate it:

.. code-block:: bash

   source test/bin/activate

or for Windows:

.. code-block:: powershell

   .\venv\Scripts\activate

If we run again ``pip freeze`` you will notice that your environment is empty. We can install all the packages contained in the ``requirements.txt`` file by simply running:

.. code-block:: bash

   pip install -r requirements.txt

If you check again with ``pip freeze`` you will notice that you have exactly the same packages than in the ``venv`` environment. You can upgrade Flask, for example:

.. code-block:: bash

   pip install --upgrade Flask

And if you run again ``pip freeze`` you will notice that the version of Flask has changed. Repeat the steps mentioned above in order to deactivate ``test`` and activate ``venv``. You will see that the version of Flask stayed at ``1.0`` and was not upgraded.

Of course, you can run the ``freeze`` command outside of any virtual environment to see all the packages installed in your computer. It is a very useful way of keeping track of the packages that may need an upgrade or that you no longer use.

.. newsletter::

How does the Virtual Environment Work
-------------------------------------
When you run programs from the command line, your operating system needs to know where to find them. The location of the programs in Windows and Linux is radically different, but they both are able to understand that when you type ``python`` in the command line, you want to start the Python interpreter. In order to achieve this, operating systems know where to look for programs thanks to the so-called environmental variables. The ``PATH`` is one of those variables that stores a list of folders where to look for programs.

When you work in a virtual environment, all that you do is to replace the relevant variables. In this way, when you run ``python`` in the command line, it will first find the one that corresponds to the virtual environment. For example, imagine that you have two different versions of Python, let's say ``python`` (for Python 2) and ``python3`` (for Python 3). When you create a virtual environment, you can specify which version of python to use by adding the option ``-p`` at the end. In the examples above, we have used ``python3``, and therefore every time we type ``python`` in the virtual environment, we will be actually triggering ``python3``.

But that is not all. If you navigate to the folder of the virtual environment, you will see a folder called **bin**, where actually the executables for Python and Pip are located. In this way, you are isolated from the computer. If the OS decides to upgrade from Python 3.4 to Python 3.6, for example, you will still have the proper version in your virtual environment. If you navigate to the **lib** folder and go inside the python folder, you will find the **site-packages**, which are all the packages installed by pip.

If you have compiled programs that you want to use, in principle you can put them into the **bin** folder. If you have Python packages that are not installed through pip (such as PyQt4), you can install them system-wide and then just copy the appropriate folder into your virtual environment.

Be careful with name clashes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
It is common that some python packages also generate *entry points*, i.e. commands that can be triggered directly from the command line. For example, if you are inside your virtual environment, you can run ``flask`` directly from the command line. This behavior is very useful, but it can easily collide with packages installed system-wide.

Imagine you installed Flask in your system, and then you start working in a virtual environment that doesn't have Flask installed. If you run ``flask`` it will work, but it will be using the version from your OS. This is something very easy to miss when dealing with more complicated packages such as the Jupyter notebook or sphinx for building documentation.

There is no one solution that fits all. It is important for you to be aware of the different problems that may arise when you run programs directly from the command line. Especially Linux/Mac users should be aware that when using the package manager and installing, for instance, Jupyter, you will also create the proper links in the **bin** directory, allowing you to run ``jupyter notebook`` directly. However, if you install it through pip, there are no entry points. Therefore, if you just type ``jupyter notebook``,  you will use the system one. To overcome this, you can use the following command:

.. code-block:: bash

    python -m jupyter notebook

This will guarantee that you are going to use the package installed through Pip and not the one installed by your system.

Conclusions
-----------
It is almost impossible to overestimate how useful the *Virtual Environment* is. It will help you stay organized and out of conflicts when you develop software, and it will also avoid problems when you are installing different libraries that you want to test. It doesn't matter if it is for the lab computer or for analyzing data, if you keep your programs compartmentalized, you can be sure that they will all run properly, regardless of their specific needs.

Remember, every time you are about to start a new project, regardless of what it is, you should start by creating an appropriate Virtual Environment for it. In this way, you can be certain of the long-term prosperity of the code you write, regardless of where it will bring you.

Header photo by `Michael Aleo <https://unsplash.com/photos/OsdgZG1byTk?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText>`_ on Unsplash