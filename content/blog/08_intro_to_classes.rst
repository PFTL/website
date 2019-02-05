A Primer on Classes in Python
=============================

:date: 2018-05-22
:author: Aquiles Carattino
:subtitle: A practical approach to working with classes in python
:header: {attach}daniel-cheung-129841-unsplash.jpg
:tags: Classes, beginner, tutorial
:description: A practical approach to working with classes in python

Python is an object-oriented programming (OOP) language. Object-oriented
programming is a programming design that allows developers not only to
define the type of data of a variable but also the operations that can
act on that data. For example, a variable can be of type integer, float,
string, etc. We know that we can multiply an integer to another, or
divide a float by another, but that we cannot add an integer to a
string. Objects allow programmers to define operations both between
different objects as with themselves. For example, we can define an object
``person``, add a birthday and have a function that returns the
person's age.

At the beginning it will not be clear why objects are useful, but over
time it becomes impossible not to think with objects in mind. Python
takes the objects ideas one step further, and considers every variable
an object. Even if you didn't realize, it is possible that you have
already encountered some of these ideas when working with numpy arrays,
for example. In this chapter we are going to cover from the very basics
of object design to slightly more advanced topics in which we can define
a custom behavior for most of the common operations.

.. contents::

Defining a Class
----------------
Let's dive straight into how to work with classes in Python. Defining a class is as
simple as doing:

.. code-block:: python

    class Person:
        pass

When speaking it is very hard not to interchange the words
``Class`` and ``Object``. The reality is that the difference
between them is very subtle: an object is an instance of a class. This
means that we will use the word *classes* when referring to the type of variable,
while we will use *object* to the variable itself. It is going to become clearer
later on.

In the example above, we've defined a class called ``Person`` that doesn't do
anything, that is why it says ``pass``. We can add more
functionality to this class by declaring a function that belongs to it. Create a file called **person.py** and add the following code to it:

.. code-block:: python

    class Person:
        def echo_name(self, name):
            return name


In Python, the functions that belong to classes are called **methods**. For
using the class, we have to create a variable of type person. Back in the Python Interactive Console, you can, for example, do:

.. code-block:: pycon

    >>> from person import Person
    >>> me = Person()
    >>> me.echo_name("John Snow")
    John Snow

The first line imports the code into the interactive console. For this to work, it is important that you trigger python directly from the same folder where the file **person.py** is located. When you run the code above, you should see as output ``John Snow``. There is also an
important detail that was omitted this far, the presence of
``self`` in the declaration of the method. All the methods in
python take a first input variable called self, referring to the class
itself. For the time being don't stress yourself about it, but bear in
mind that when you define a new method, you should always include the
``self``, but when calling the method you should never include it.
You can also write methods that don't take any input, but still will
have the ``self`` in them, for example:

.. code-block:: python

    def echo_True(self):
        return "True"

that can be used by doing:

.. code-block:: pycon

    >>> me.echo_True()


So far, defining a function within a class has no advantage at all. The
main difference, and the point where methods become handy is because
they have access to all the information stored within the object itself.
The ``self`` argument that we are passing as first argument of the
function is exactly that. For example, we can add the following two
methods to our class Person:

.. code-block:: python

    def store_name(self, name):
        self.stored_name = name

    def get_name(self):
        return self.stored_name


And then we can execute this:

.. code-block:: pycon

    >>> me = Person()
    >>> me.store_name('John Snow')
    >>> print(me.get_name())
    John Snow
    >>> print(me.stored_name)
    John Snow

What you can see in this example is that the method ``store_name``
takes one argument, ``name`` and stores it into the class variable
``stored_name``. Variables in the context of classes are called **attributes**
in the context of a class. The method ``get_name`` just returns
the stored property. What we showed in the last line is that we can access
the property directly, without the need to call the ``get_name``
method. In the same way, we don't need to use the ``store_name``
method if we do:

.. code-block:: pycon

    >>> me.stored_name = 'Jane Doe'
    >>> print(me.get_name())
    Jane Doe

One of the advantages of the attributes of classes is that they can be
of any type, even other classes. Imagine that you have acquired a time trace
of an analog sensor and you have also recorded the temperature of the
room when the measurement started. You can easily store that information
in an object:

.. code-block:: python

    measurement.temperature = '20 degrees'
    measurement.timetrace = np.array([...])

What you have so far is a vague idea of how classes behave, and maybe
you are starting to imagine some places where you can use a class to
make your daily life easier and your code more reusable. However, this
is just the tip of the iceberg. Classes are very powerful tools.

.. newsletter::

Initializing classes
--------------------
**Instantiating** a class is the moment in which we call the class and pass
it to a variable. In the previous example, the instantiation of the
class happened at the line reading ``me = Person()``. You may
have noticed that the property ``stored_name`` does not exist in
the object until we assign a value to it. This can give very serious
headaches if someone calls the method ``get_name`` before actually
having a name stored (you can give it a try to see what happens!)
Therefore it is very useful to run a default method when the class is
first called. This method is called ``__init__``, and you can
use it like this:

.. code-block:: python

    class Person():
        def __init__(self):
            self.stored_name = ""

        [...]


If you go ahead and run the ``get_name`` without actually storing
a name beforehand, now there will be no error, just an empty string
being returned. While initializing you can also force the execution of
other methods, for example:

.. code-block:: python

    def __init__(self):
        self.store_name('')

    [...]

Will have the same final effect. It is however common (and smart)
practice, to declare all the variables of your class at the beginning,
inside your ``__init__``. In this way you don't depend on
specific methods being called to create the variables.

As with any other method, you can have an ``__init__`` method with more
arguments than just ``self``. For example you can define it like
this:

.. code-block:: python

    def __init__(self, name):
        self.stored_name = name

Now the way you instantiate the class is different, you will have to do
it like this:

.. code-block:: python

    me = Person('John Snow')
    print(me.get_name())

When you do this, your previous code will stop working, because now you have to set the ``name`` explicitly. If there is any other code that does ``Person()``, it will fail. The proper way of altering the functioning of a method is to add a default value in case no explicit value is passed. The ``__init__`` would become:

.. code-block:: python

    def __init__(self, name=''):
        self.stored_name = name

With this modification, if you don't explicitly specify a name when instantiating the class, it will default to ``''``, i.e., an empty string.

Defining default values for parameters in methods has to be handled with care. They are very useful when you expect people to always use the same values and only occasionally to change them. Trying to keep backwards compatibility by declaring default values can make your code look chaotic, so you have to do it only when it is worth doing, and not all the time. When developing, it is impossible not to refactor code.

Defining class attributes
-------------------------
So far, if you wanted to have properties available right after the instantiation of a class, you had to include them in the ``__init__`` method. However, this is not the only possibility. You can define attributes that belong to the class itself. Doing it is as simple as declaring them before the ``__init__`` method. For example, we could do this:

.. code-block:: python

    class Person():
        birthday = '2010-10-10'
        def __init__(self, name=''):
            [...]


If you use the new ``Person`` class, you will have an attribute called ``birthday`` available, but with some interesting behavior. First, let's start as always:

.. code-block:: pycon

    >>> from person import Person
    >>> guy = Person('John Snow')
    >>> print(guy.birthday)
    2010-10-10


What you see above is that it doesn't matter if you define the birthday within the ``__init__`` method or before, when you instantiate the class, you access the property in the same way. The main difference is what happens before instantiating the class:

.. code-block:: pycon

    >>> from person import Person
    >>> print(Person.birthday)
    2010-10-10
    >>> Person.birthday = '2011-11-11'
    >>> new_guy = Person('Cersei Lannister')
    >>> print(new_guy.birthday)
    2011-11-11


What you see in the code above is that you can access class attributes before you instantiate anything. That is why they are class and not object attributes. Subtleties apart, once you change the class attribute, in the example above, the birthday, next time you create an object with that class, it will receive the new property. At the beginning it is hard to understand why it is useful, but one day you will need it and it will save you a lot of time.

Inheritance
-----------
One of the advantages of working with classes in Python is that it allows you to use the code from other developers and expand or change its behavior without modifying the original code. The best idea is to see it in action. So far we have a class called ``Person``, which is general but not too useful. Let's assume we want to define a new class, called ``Teacher``, that has the same properties as a ``Person`` (i.e., name and birthday) plus it is able to teach a class. You can add the following code to the file **person.py**:

.. code-block:: python

    class Teacher(Person):
        def __init__(self, course):
            self.course = course

        def get_course(self):
            return self.course

        def set_course(self, new_course):
            self.course = new_course


Note that in the definition of the new ``Teacher`` class, we have added the ``Person`` class. In Python jargon, this means that the class ``Teacher`` is a child of the class ``Person``, or the opposite, that ``Person`` is the parent of ``Teacher``. This is called **inheritance** and you will notice that a lot of different projects take advantage of it. You can use the class ``Teacher`` in the same way as you have used the class ``Person``:

.. code-block:: pycon

    >>> from person import Teacher
    >>> me = Teacher('math')
    >>> print(me.get_course)
    math
    >>> print(me.birthday)
    2010-10-10

However, if you try to use the teacher's name it is going to fail:

.. code-block:: pycon

    >>> print(me.get_name())
    [...]
    AttributeError: 'Teacher' object has no attribute 'stored_name'

The reason behind this error is that ``get_name`` returns ``stored_name`` in the class Person. However, the property ``stored_name`` is created when running the ``__init__`` method of Person, which didn't happen. You could have changed the code above slightly to make it work:

.. code-block:: pycon

    >>> from person import Teacher
    >>> me = Teacher('math')
    >>> me.store_name('J.J.R.T.')
    >>> print(me.get_course)
    math
    >>> print(me.get_name())
    J.J.R.T.

However, there is also another approach to avoid the error. You could simply run the ``__init__`` method of the parent class (i.e. the base class), you need to add the following:

.. code-block:: python

    class Teacher(Person):
        def __init__(self, course):
            super().__init__()
            self.course = course
        [...]


When you use ``super()``, you are going to have access directly to the class from which you are inheriting. In the example above, you explicitly called the ``__init__`` method of the parent class. If you try again to run the method ``me.get_name()``, you will see that no error appears, but also that nothing is printed to screen. This is because you triggered the ``super().__init__()`` without any arguments and therefore the name defaulted to the empty string. You could change the code like this:

.. code-block:: python

    class Teacher(Person):
        def __init__(self, name, course):
            super().__init__(name)
            self.course = course
        [...]

which you would use combining both examples above:

.. code-block:: pycon

    >>> from person import Teacher
    >>> me = Teacher('John', 'math')
    >>> print(me.get_name())
    John

It is important to note that when importing the class, you only import the one you want to use, you don't need to import the parent, that is the responsibility of whoever developed the ``Teacher`` class.

Finer details of classes
------------------------
With what you have learned up to here, you can achieve a lot of things, it is just a matter of thinking how to connect different methods when it is useful to inherit. Without doubts, it will help you to understand the code developed by others. There are, however, some details that are worth mentioning, because you can improve how your classes look and behave.

Printing objects
................
Let's see, for example, what happens if you print an object:

.. code-block:: pycon

    >>> from person import Person
    >>> guy = Person('John Snow')
    >>> print(guy)
    <__main__.Student object at 0x7f0fcd52c7b8>

The output of printing ``guy`` is quite ugly and is not particularly useful. Fortunately, you can control what appears on the screen. You have to update the ``Person`` class. Add the following method to the end:

.. code-block:: python

    def __str__(self):
        return "Person class with name {}".format(self.stored_name)

If you run the code above, you will get the following:

.. code-block:: pycon

    >>> print(guy)
    Person class with name John Snow


You can get very creative. It is also important to point out that the method ``__str__`` will be used also when you want to transform an object into a string, for example like this:

.. code-block:: pycon

    >>> class_str = str(guy)
    >>> print(class_str)
    Person class with name John Snow

Which also works if you do this:

.. code-block:: pycon

    >>> print('My class is {}.'.format(guy))

Something that is important to point out is that this method is inherited. Therefore, if you, instead of printing a ``Person``, print a ``Student``, you will see the same output, which may or may not be the desired behavior.

Defining complex properties
...........................
When you are developing complex classes, sometimes you would like to alter the behavior of assigning values to an attribute. For example you would like to change the age of a person when you store the year of birth:

.. code-block:: pycon

    >>> person.year_of_birth = 1980
    >>> print(person.age)
    38

There is a way of doing this in Python which can be easily implemented even if you don't fully understand the syntax. Working again in the class ``Person``, we can do the following:

.. code-block:: python

    class Person():
        def __init__(self, name=None):
            self.stored_name = name
            self._year_of_birth = 0
            self.age = 0

        @property
        def year_of_birth(self):
            return self._year_of_birth

        @year_of_birth.setter
        def year_of_birth(self, year)
            self.age = 2018 - year
            self._year_of_birth = year

Which can be used like this:

.. code-block:: pycon

    >>> from people import Person
    >>> me = Person('Me')
    >>> me.age
    0
    >>> me.year_of_birth = 1980
    >>> me.age
    32

What is happening is that Python gives you control over everything, including what does the ``=`` do when you assign a value to an attribute of a class. The first time you create a ``@property``, you need to specify a function that returns a value. In the case above, we are returning ``self._year_of_birth``. Just doing that will allow you to use ``me.year_of_birth`` as an attribute, but it will fail if you try to change its value. This is called a read-only property. If you are working in the lab, it is useful to define methods as read-only properties when you can't change the value. For example, a method for reading the serial number of a device would be read-only.

If you want to change the value of a property, you have to define a new method. This method is going to be called a *setter*. That is why you can see the line ``@year_of_birth.setter``. The method takes an argument that triggers two actions. On the one hand, it updates the age, on the other it stores the year in an attribute. It takes a while to get used to, but it can be very handy.

Conclusions
-----------
This article is a very short primer on how to start working with classes in Python. You are not supposed to be an expert after such a brief walk-through, but it should be enough for getting you started with your own developments, and, more importantly, to be able to read other developers code and understand what they are doing.

The series of primer articles are thought as a go-to destination when you need to refresh a specific concept. If you find anything missing, you can always leave a comment below and we will expand the article according to your needs. You can find the text of this article on `Github <https://github.com/PFTL/website/blob/master/content/blog/08_intro_to_classes.rst>`_.

Header photo by `Daniel Cheung <https://unsplash.com/photos/ZqqlOZyGG7g?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText>`_ on Unsplash