Duck Typing, or how to check variable types
===========================================

:date: 2019-06-11
:author: Aquiles Carattino
:subtitle: What duck typing means how can it affect your program architecture
:header: {attach}joshua-coleman-655076-unsplash.jpg
:tags: functions, methods, dynamic language, typing, types
:description: What duck typing means how can it affect your program architecture

The name duck typing has its root in `the expression <https://en.wikipedia.org/wiki/Duck_typing>`__ *If it walks like a duck and it quacks like a duck, then it must be a duck*. Which means that if you want to know whether you are dealing with a duck or not, you only care about how it looks like and how it behaves rather than actually checking to what species the animal belongs.

The code that we develop in this article is available `on Github <https://github.com/PFTL/website/tree/master/example_code/33_duck_typing>`__.

The analogy translates *almost* literally to Python. Python is a dynamically typed language. This means that you don't need to specify what type of variables you are dealing with. The following lines are perfectly valid Python code:

.. code-block:: python

    var1 = 'This is a string'
    var1 = 1

As you can see above, ``var1`` changed from a string to an integer without any problems. We didn't need to specify whether ``var1`` was going to be of either type. Without going to the details about what variables truly mean in Python, we can see that it is very convenient because it saves us from a lot of typing. On the other hand, it means that we can't be sure what variable type a function will receive until an error is raised, for example:

.. code-block:: python

    def increase_by_one(value)
        return value + 1

If we run the function ``increase_by_one`` with ``var1`` it will work only if ``var1`` is a number (integer or float), but it will give us a ``TypeError`` if we run it with a string. Statically typed languages would have warned us about this problem at compilation time and would have prevented us from some headaches down the line.

One easy solution would be to check whether the ``value`` is either an integer or a float. We can improve our function, like this:

.. code-block:: python

    def increase_by_one(value):
        if isinstance(value, int) or isinstance(value, float):
            return value + 1

If we try to run the function with a string, it will not do anything and it will return ``None``. If we run the function with either an integer or a float, it will return the value increased by one. This behavior is more or less what we would expect.

What is duck typing?
--------------------
So, you may wonder after this long preamble, what is actually duck typing. Imagine that we now have a numpy array, and we use the function ``increase_by_one`` with it, what do you expect to happen?

.. code-block:: python

    import numpy as np

    var1 = np.array((0, 1, 2))
    print(increase_by_one(var1))

You get ``None``, but is that what you were expecting? If you think about it, we forced the output because we designed the function to only work on integers and floats, while an array is neither of them. However, if we go back to the old version of the function before we implemented the verification, we would get:

.. code-block:: python

    def increase_by_one(value):
        return value + 1

    print(increase_by_one(var1))
    # [1, 2, 3]

You can see that the function ``increase_by_one`` works also on arrays. The idea of **duck typing** is that we don't care about what type of variable ``value`` is, provided that we can add 1 to it. In Python, this is translated to try to add 1 to ``value`` and if an exception is raised, we deal with it:

.. code-block:: python

    def increase_by_one(value):
        try:
            value += 1
        except TypeError:
            return None
        return value

Now, the function will run with all types of variables which accept being added by one. At the beginning we assumed only floats and integers were able to be added by one, then we found that numpy arrays are also working, and you can find that there are even more possibilities around.

Custom Classes
--------------
Duck typing becomes crucial when you develop your custom classes. Python exposes a lot of syntactic sugar which allow you to customize how things behave under certain operations. To keep up with the example above, let's develop a class which allows being increased by one:

.. code-block:: python

    class AddOne:
        def __init__(self, value):
            self.value = str(value)

        def __add__(self, other):
            self.value += str(other)
            return self

        def __str__(self):
            return self.value

And we can use it like this:

.. code-block:: python

    var1 = AddOne('0')
    print(increase_by_one(var1))
    # 01

What you see now, is that our class defines the behavior of adding. In this case, the class will concatenate whatever value we add to the initial string that we have defined. That is why we see that the output is ``01``.

Duck typing means that our function will run every time there is a way of adding a ``1`` to the object. The example in these sections is almost trivial, so we can see something which is much more relevant.

Complex Data Structures
-----------------------
When you develop larger programs, it is almost impossible not to need configuration variables. Storing configuration parameters in dictionaries is very handy because it is very explicit. Let's make it very simple:

.. code-block:: python

    configuration = {
        'param1': 10,
        'param2': 5
    }

And we also develop an Experiment class, which will use the configuration and will verify whether we have supplied all the needed parameters:

.. code-block:: python

    class Experiment:
        def __init__(self, config):
            self.configuration = config

        def check_config(self):
            if not {'param1', 'param2'} <= set(self.configuration.keys()):
                raise Exception('The configuration does not include the mandatory fields')
            print('Config seems OK')

You see that we have developed ``check_config`` which uses sets to check whether both parameters are within the keys of the dictionary. In other words, we verify whether the set ``{'param1', 'param2'}`` is a subset of all the keys in the configuration.

We can add one last method to check whether the parameters are within an acceptable range:

.. code-block:: python

    def check_config_range(self):
        if self.configuration['param1'] > 10:
            raise Exception('param1 cannot be larger than 10')
        if self.configuration['param2'] > 5:
            raise Exception('param2 cannot be larger than 5')
        print('Range seems OK')

You can test the code by running:

.. code-block:: python

    exp = Experiment(configuration)
    exp.check_config()
    exp.check_config_range()

So, where does duck typing come into effect?. In the code above we have assumed that the configuration would be a dictionary, but we are not bound to that. Imagine that we want to improve how we deal with configurations. We can develop our custom class to handle the reading from a file, perhaps logging changes to parameters, etc. And we want it to be compatible with the ``Experiment`` class that we have already developed. Therefore, the duck-typing here works the other way around. We know what the class needs in order to work properly, we just develop a solution around it.

If you look at the code of ``Experiment``, you see that it uses the configuration in two different places. First, when it checks that both ``param1`` and ``param2`` are present, through the method ``keys``. We know that we will need a class that supports that method:

.. code-block:: python

    class Config:
        def __init__(self):
            ...

        def keys(self):
            ...

We also know that when we want to use the parameters, we access them through ``configuration['param1']``, and to achieve this, we will need to tweak the magic method ``__getitem__``. Let's add one more requirement, and is that we want to instantiate this class with a filename, which will be read by the class and the data will be loaded. For simplicity, we force the configuration file to be in YAML format. Thus, our ``Config`` class will look like this (you need pyyaml installed for this to work):

.. code-block:: python

    import yaml

    class Config:
        def __init__(self, filename):
            with open(filename, 'r') as f:
                self._config = yaml.load(f.read(), Loader=yaml.FullLoader)

        def keys(self):
            return self._config.keys()

        def __getitem__(self, item):
            return self._config[item]

If we go step by step, you can see that when we instantiate the class, we ask for a filename, which we will open and we will load its contents into an attribute called ``_config``. Note that Python doesn't have true private attributes for classes (i.e. attributes that can be accessed only within the class but not from outside). As a convention, attributes starting with an underscore, such as ``_config`` signal that they are not supposed to be used directly, but we can't easily enforce it.

Since ``_config`` will be a dictionary, the implementation of the ``keys`` method will be trivial, we just use the default dictionary method. ``__getitem__`` is, however much more interesting. The ``__getitem__`` method in Python is the one that regulates what happens when you do something like ``c['param1']``. ``item`` in this case will be ``param1``, and we want to retrieve that item from the ``_config`` dictionary. If you want to test this implementation, first, you need to create a file **config.yml** with the following:

.. code-block:: yaml

    param1: 10
    param2: 5

And then you can run:

.. code-block:: python

    c = Config('config.yml')
    print(c['param1'])
    print(c['[param2'])

Of course, if you would like to change the value of 'param1' or 'param2', you will get an error. Covering this topic is beyond duck typing, so keep tuned because we are going to discuss it in a later tutorial.

Now we can put everything together, our custom configuration class and the experiment class:

.. code-block:: python

    c = Config('config.yml')
    exp = Experiment(c)
    exp.check_config()
    exp.check_config_range()

Now you see that you are running the ``Experiment`` with a configuration which is not a dictionary but a custom designed class, and it works as expected.

Conclusions
-----------
If you look for the definition of duck typing, you will typically find that in Python, it is common not to verify to which data type a variable belongs. If those variables behave as expected, then you shouldn't worry. In the beginning, we saw that this is very handy because it allowed us to use a function on variables which we didn't originally intend, such as numpy array or custom classes.

In the second part, we saw that you can plan your code the other way around. If you assume that duck typing is a common practice (i.e. that the libraries you use don't verify the type of variables, but only their functioning), you can design your own classes in such a way that they behave as a specific data type. Our example was a class that mimics how dictionaries work, and which we used as an argument in a different object, which had no idea of our custom data type.

Example code for this article can be found `on Github <https://github.com/PFTL/website/tree/master/example_code/33_duck_typing>`__. You can also find the `source code for this article <https://github.com/PFTL/website/blob/master/content/blog/33_duck_typing.rst>`_.

Header image by `JOSHUA COLEMAN <https://unsplash.com/@joshstyle?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText>`_ on Unsplash