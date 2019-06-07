Introduction to Threads in Python: Part 2
==========================================

:status: draft
:date: 2019-03-17
:author: Aquiles Carattino
:subtitle: Learn how to share data between threads
:header: {attach}ivana-cajina-324103-unsplash.jpg
:tags: functions, methods, arguments, packing, unpacking, args, kwargs
:description: Learn how to share data between threads

When working with threads in Python, you will find very useful to be able to share data between different tasks. One of the advantages of threads in Python is that they share the same memory space, and thus exchanging information is relatively easy. However, there are some structures that can help you achieve more specific goals.

In the previous article we have covered `how to start and synchronize threads <{filename}31_Threads_Part_1.rst>`_ and now it is time to expand the toolbox in order to handle the exchange of information between them.

.. contents::

Shared Memory
-------------
The first and most naive approach is to use the same variables in different threads. We have already used this feature in the `previous tutorial <{filename}31_Threads_Part_1.rst>`__, but without discussing it explicitly. Let's see how we can use shared memory through a very simple example:

.. code-block:: python

    from threading import Thread, Event
    from time import sleep

    event = Event()

    def modify_variable(var):
        while True:
            for i in range(len(var)):
                var[i] += 1
            if event.is_set():
                break
            sleep(.5)
        print('Stop printing')


    my_var = [1, 2, 3]
    t = Thread(target=modify_variable, args=(my_var, ))
    t.start()
    while True:
        try:
            print(my_var)
            sleep(1)
        except KeyboardInterrupt:
            event.set()
            break
    t.join()
    print(my_var)

The example above is almost trivial, but it has a very important feature. We start a new thread by passing an argument, ``my_var``, which is a list of numbers. The thread will increase the values of the numbers by one, with a certain delay. In this example we use events in order to graciously finish the thread, if you are not familiar with them, check the `previous tutorial <{filename}31_Threads_Part_1.rst>`__.

The important piece of code in this example is the ``print(my_var)`` line. That print statement lives in the main thread, however, it has access to the information being generated within a child thread.