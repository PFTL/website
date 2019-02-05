How to Use Decorators to Validate Input
========================================

:date: 2018-03-12
:author: Aquiles Carattino
:subtitle: Decorators are very useful, but can become hard to understand
:header: {attach}victor-garcia-560967-unsplash.jpg
:tags: Decorators, Python, Tricks, Validation, Data
:description: Learn how to use decorators to validate user input before communicating with a device

Python is rich in resources that can shorten the time it takes to develop new programs and simplify repetitive tasks. Decorators are one of such elements but more often than not they are not considered by less experienced developers. Adding decorators to the syntactic toolbox can be of great use in different contexts, and in this article, we are going to discuss how can they help you when communicating with a device. The example code can be found in our `Github repository <https://github.com/uetke/website_content/tree/master/example_code/Examples_Decorators>`_.

Decorators in Python are nothing more than functions that take as arguments other functions. They appear with an ``@`` in front of them right above a function (or a method within a class). Let's quickly recap how functions work in Python and how to use them. Imagine you want to compute the average of two values. We can develop a function for it:

.. code-block:: python

   def average(x, y):
      avg = (x+y)/2
      return avg

We can use the function directly in our code by writing:

.. code-block:: python

   a = 1
   b = 3
   result = average(1, 3)
   print(result)

What you should see happening is that when you call the function ``average`` it adds both numbers and returns their mean value. Imagine that, for some reason, you want to allow only positive numbers as arguments of your function. You can expand the ``average`` function to check whether it is true or not.

.. code-block:: python

   def average(x, y):
      if x<0 or y<0:
         raise Exception("Both x and y have to be positive")

      avg = (x + y)/2
      return avg

Every time someone wants to use the function with a negative argument, an error will be raised. Later, we are asked to develop a new function to compute the geometric average of two numbers, and we need them both to be positive. Our function will look like this:

.. code-block:: python

   import math

   def geom_average(x, y):
      if x<0 or y<0:
         raise Exception("Both x and y have to be positive")

      avg = math.sqrt(x*y)
      return avg

There is a general rule of thumb that says that code shouldn't be copied more than twice. If you are going to copy-paste code for the third time there is probably a better way of doing it. In the examples above, you can see that the verification of the input is exactly the same in both functions. If we were to write a third function, we would meet the three-copies rule. It would be useful to have an external way of checking that both inputs are positive, and this is exactly what decorators are meant to do.

.. newsletter::

Functions as arguments and as outputs of other functions
********************************************************
Before we can go into the details of how to use ``decorators`` in Python, it is important to show how functions work with inputs and outputs that are other functions. For example, we could define a function that transforms the output of the averages defined above into integers. It is a very simplistic example but already shows the pattern that you can follow to achieve more complex behaviors.

.. code-block:: python

   def integer_output(func, x, y):
      res = func(x, y)
      return int(res)

In the code above, you can see that ``integer_output`` takes three arguments, a function ``func`` and two numbers, ``x`` and ``y`` . We use the function, regardless of what it is, with arguments ``x`` and ``y``. It then returns the result of ``func`` converted to an integer value. ``integer_output`` can be used like this:

.. code-block:: python

   rounded = integer_output(average, 1, 2)
   print(rounded)
   geom_rounded = integer_output(geom_average, 4, 5)
   print(geom_rounded)

It is important to note that the first argument is a function and it doesn't matter which one. You could use ``average`` or ``geom_average``. The next two arguments are going to be passed directly to ``func`` . This is already quite powerful and most likely you can think a lot of ways in which you can use it, but Python allows you to do even more interesting things.

Functions can also be defined within functions and you can use them based on your input arguments. For example, let's assume you want to use ``average`` only if the sum of x and y is even and the ``geom_average`` if the sum is odd:

.. code-block:: python

   def even_odd_average(x, y):
      def average(a, b):
         return (a+b)/2
      def geom_average(a, b):
         return math.sqrt(a*b)

      if (x+y) % 2 == 0:
         return average(x, y)
      else:
         return geom_average(x, y)

The function ``even_odd_average`` takes only two arguments on which it is going to perform the average. Inside we define two functions, exactly as we did earlier, ``average`` and ``geom_average``, but this time they are available only within the ``even_odd_average`` function. Based on the input from the user, we either calculate the average or the geometric average as requested earlier and we return the value. We can use this function as:

.. code-block:: python

   print(even_odd_average(4, 6))
   print(even_odd_average(4, 9))

So far, we have seen how to use functions as arguments in other functions and how to define functions within functions. The only missing part is to be able to return a function instead of a value. Let's assume you want to print the time it takes to calculate the average between two numbers, but you don't want to re-write your original function. We have to write a function wrapper.

.. code-block:: python

   import time

   def timing_average(func):
      def wrapper(x, y):
         t0 = time.time()
         res = func(x, y)
         t1 = time.time()
         print("It took {} seconds to calculate the average".format(t1-t0))
         return res

      return wrapper

We start by defining a function that takes as an argument another function. We also define a new function called ``wrapper`` as we explained earlier. So far, both steps were done in the previous examples, but now we are going to use ``func`` within the ``wrapper``. We start by storing the current time at the variable ``t0``. We execute the function ``func`` with the arguments ``x`` and ``y`` and store the new time at ``t1``. We print the total time it took to run the function and return the output of ``func``. The important part here is the very last line. As you can see, we are not returning the value that ``func`` returns, but we are actually returning the ``wrapper``, which is in itself a function. To see this in action, we can do the following:

.. code-block:: python

   new = timing_average(average)
   new(2, 4)

What you see in the above code is that we create a function called ``new`` by using ``timing_average`` with only one argument, the function ``average``. ``New`` will take the same inputs that the ``wrapper`` function takes. If we use ``new`` as a function, with arguments ``2`` and ``4`` , you will see that it prints to screen the total time it took to calculate the average. ``new`` is nothing more than the function ``wrapper``, defined using ``average``. We could do the same using ``geom_average``:

.. code-block:: python

   new_geom = timing_average(geom_average)
   new_geom(4,5)

The syntax above can be hard to understand and forces you to define new functions to add timing capabilities. When you see that you are assigning the output of ``timing_average`` to a variable called ``new`` you don't expect it to actually be a function. If you already have working code, you need to do a lot of refactoring in order to define and use the new functions.

Fortunately, Python offers a very clear and simple way of achieving the same functionality, without the downsides just said. If you managed to follow the above examples, you are ready to improve the way the code looks like by using *Python syntactic sugar*.

Syntactic Sugar for Decorators
******************************
You already know almost everything there is to know regarding how to use decorators, you are just missing the syntactic sugar of Python. With what you have already done, you can improve the style of your code quite easily. Assuming you want to add timing capabilities to your average or geometrical average function, you can simply do:

.. code-block:: python

   @timing_average
   def average(x, y):
      return (x+y)/2

By simply adding ``@timing_average`` before your function, you are now able to use ``average`` as always, but printing the time it takes to calculate it. The obvious advantage of this syntax is that it allows you to add an interesting new functionality without altering your downstream code. You don't need to define a new function, you only need to add one line of code before the definition of your ``average``. It runs as always:

.. code-block:: python

   avg = average(4, 6)
   print('The average between 4 and 6 is {}'.format(avg))

Coming back to the examples of the averages that take only positive arguments, and building on the example of ``timing_average``, we can develop a wrapper function that would check whether the input of our function is positive or not.

.. code-block:: python

   def check_positive(func):
      def func_wrapper(x, y):
         if x<0 or y<0:
            raise Exception("Both x and y have to be positive for function {} to work".format(func.__name__))
         res = func(x,y)
         return res
      return func_wrapper

The structure of ``check_positive`` is very similar to what we have done for the timing. The only difference is that we check the input arguments and we raise an ``Exception`` if they are not both positive. Since we are raising an exception for an unknown function, it becomes handy to display which function actually gave the error. We achieve that by using ``func.__name__``, which will tell us the name of the function. The rest is exactly the same as with the timing example. We can write our average functions as follows:

.. code-block:: python

   @check_positive
   def average(x, y):
      return (x + y)/2

   @check_positive
   def geom_average(x, y):
      return math.sqrt(x*y)

Both functions, ``average`` and ``geom_average`` don't change their names, therefore you can use them as always, but they will check for positive input before computing the average:

.. code-block:: python

   average(2, 4)
   average(-2, 4)
   geom_average(4, 9)
   geom_average(-4, 10)

Decorators can also be combined, you can time a function AND request the inputs to be positive:

.. code-block:: python

   @timing_average
   @check_positive
   def average(x, y):
      return (x + y)/2

You can play around and see what happens if you change the order of the decorators. Importantly, if you use ``func.__name__`` to print the name of the function that raised the ``Exception`` within a decorator, you can see that the name can change and become the name of the wrapper. In most cases this is not a desired situation because you won't be able to debug what is the real function giving troubles, you will just get the name of the decorator. However, this is a more subtle topic that will be covered in the future.

Decorators are very powerful and can help you develop very clean and useful code. The obvious application of decorators is to validate the input provided by the user. Decorators are also very useful when you are writing a library that other developers are going to use. Or when you want to alter the behavior of a method or function in a systematic way. For example, you could use some cache in order to avoid running the same function with the same arguments over and over again.

One of the advantages of decorators is that even if a developer doesn't fully understand what it is happening under the hood, it will for sure understand how to use them and what to expect. If you provide good examples in your code it will become apparent where and when to include specific decorators. Now that you have a basic understanding of what the ``@`` means in Python you can start thinking about many more interesting applications.

In this article, we have shown a couple of very basic examples that can be greatly improved. If you have ever encountered decorators and didn't understand how to use them, or you are looking for more specific information, leave your message in the comment section below and we will use your feedback to write a follow up article specifically designed to answer your questions.

If you want to learn more about decorators, there is a `Follow Up Article <{filename}04_how_to_use_decorators_2.rst>`_


Header photo by `Victor Garcia <https://unsplash.com/photos/dECPx6gtKww?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText>`_ on Unsplash