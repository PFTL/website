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

The important piece of code in this example is the ``print(my_var)`` line. That print statement lives in the main thread, however, it has access to the information being generated within a child thread. This behavior is possible thanks to memory sharing between different threads. Being able to access the same memory space is useful, but it can also pose some risks. In the example above, we have started only one thread, but we are not limited to that. We could, for example, start several threads:

.. code-block:: python

    t = Thread(target=modify_variable, args=(my_var, ))
    t2 = Thread(target=modify_variable, args=(my_var, ))
    t.start()
    t2.start()

And you would see that ``my_var`` and its information is shared across all threads. This is good for applications like the one above, in which it doesn't matter which thread adds one to the variable. Or does it? Let's slightly modify the code that runs in the thread. Let's remove the ``sleep``:

.. code-block:: python

    def modify_variable(var):
        while True:
            for i in range(len(var)):
                var[i] += 1
            if event.is_set():
                break
            # sleep(.5)
        print('Stop printing')

Now, when we run the code, there will be no sleep in between one iteration and the next. Let's run it for a short period of time, let's say 5 seconds, we can do the following:

.. code-block:: python

    from time import time
    [...]

    my_var = [1, 2, 3]
    t = Thread(target=modify_variable, args=(my_var, ))
    t.start()
    t0 = time()
    while time()-t0 < 5:
        print(my_var)
        sleep(1)
    event.set()
    t.join()
    print(my_var)

I've suppressed the parts of the code which repeat. If you run this code, you will get as outputs very large numbers. In my case, I got:

.. code-block:: python

    [6563461, 6563462, 6563463]

There is, however, a very important feature to notice. The three numbers are consecutive. This is expected, because the starting variable was ``[1, 2, 3]`` and we are adding one to each variable. Let's start a second thread this time and see what the output is:

.. code-block:: python

    my_var = [1, 2, 3]
    t = Thread(target=modify_variable, args=(my_var, ))
    t2 = Thread(target=modify_variable, args=(my_var, ))
    t.start()
    t2.start()
    t0 = time()
    while time()-t0 < 5:
        try:
            print(my_var)
            sleep(1)
        except KeyboardInterrupt:
            event.set()
            break
    event.set()
    t.join()
    t2.join()
    print(my_var)

I've got as an output the following values:

.. code-block:: python

    [5738447, 5686971, 5684220]

You can first note that they are not larger than before, meaning that running two threads instead of one could actually be slower for this operation. The other thing to note is that the values are no consecutive to each other! And this is a very important behavior that can appear when working with multiple threads in Python. If you think really hard, can you explain where this issue is coming from?

In the `previous tutorial <{filename}31_Threads_Part_1.rst>`__, we discussed that threads are handled by the operating system, which decides when to spin one on or off. We have no control on what the operating system decides to do. In the example above, since there is no ``sleep`` in the loop, the operating system will have to decide when to stop one and start another thread. However, that does not explain completely the output we are getting. It doesn't matter if one thread runs first and stops, etc. we are always adding ``+1`` to each element.

The problem with the code above is in the line ``var[i] += 1``, which is actually two operations. First, it copies the value from ``var[i]`` and ads ``1``. Then it stores the value back to ``var[i]``. In between these two operations, the operating system may decide to switch from one task to another. In such case, the value both tasks see in the list is the same, and therefore instead of adding ``+1`` twice, we do it only once. If you want to do it even more noticeable, you can start two threads, one that adds and one that subtracts from a list, and that would give you a quick hint of which thread runs faster. In my case, I got the following output:

.. code-block:: python

    [-8832, -168606, 2567]

But if I run it another time, I get:

.. code-block:: python

    [97998, 133432, 186591]

.. note:: You may notice that there is a delay between the ``start`` of both threads, which may give a certain advantage to the first thread started. However, that alone cannot explain the output generated.

How to synchronize data access
------------------------------
To solve the problem we found in the previous examples, we have to be sure that no two threads try to write at the same time to the same variable. For that, we can use a ``Lock``:

.. code-block:: python

    from threading import Lock
    [...]
    data_lock = Lock()
    def modify_variable(var):
        while True:
            for i in range(len(var)):
                with data_lock:
                    var[i] += 1
            if event.is_set():
                break
            # sleep(.5)
        print('Stop printing')

Note that we added a line ``with data_lock:`` to the function. If you run the code again, you will see that the values we get are always consecutive. The lock guarantees that only one thread will access the variable at a time.

The examples of increasing or decreasing values from a list are almost trivial, but they point in the direction of understanding the complications of memory management when dealing with concurrent programming. Memory sharing is a nice feature, but it comes with risks also.

Queues
------
One of the common situations in which threads are used is when you have some slow tasks that you can't optimize. For example, imagine you are downloading data from a website using. Most of the time the processor would be idle. This means you could use that time for something else. If you want to download an entire website (also called scraping), it would be a good solution to download several pages at the same time. Imagine you have a list of pages you want to download, and you start several threads, each one to download one page. If you are not careful on how to implement this, you may end up downloading twice the same, as we saw in the previous section.

Here is where another object can be very useful when working with threads: **Queues**. The queue is an object which accepts data in order, i.e. you put data to it one element at a time. Then, the data can be consumed in the same order, called First-in-first-out (FIFO). A very simple example would be:

.. code-block:: python

    from queue import Queue

    queue = Queue()
    for i in range(20):
        queue.put(i)

    while not queue.empty():
        data = queue.get()
        print(data)

In this example you see that we create a ``Queue``, then we put into the queue the numbers from 0 to 19. Later, we create a ``while`` loop that gets data out of the queue and prints it. This is the basic behavior of queues in Python. You should pay attention to the fact that numbers are printed in the same order in which they were added to the queue.

Coming back to the examples from the beginning of the article, we can use queues to share information between threads. We can modify the function such that instead of a list as argument, it accepts a queue from which it will read elements. Then, it will output the results to an output queue:

.. code-block:: python

    from threading import Thread, Event
    from queue import Queue
    from time import sleep, time

    event = Event()

    def modify_variable(queue_in, queue_out):
        while True:
            if not queue_in.empty():
                var = queue_in.get()
                for i in range(len(var)):
                    var[i] += 1
                queue_out.put(var)
            if event.is_set():
                break
        print('Stop printing')

In order to use the code above, we will need to create two queues. The idea is that we can also create two threads, in which the input and output queue are reversed. In that case, on thread puts its output on the queue of the second thread and the other way around. This would look like the following:

.. code-block:: python

    my_var = [1, 2, 3]
    queue1 = Queue()
    queue2 = Queue()
    queue1.put(my_var)
    t = Thread(target=modify_variable, args=(queue1, queue2))
    t2 = Thread(target=modify_variable, args=(queue2, queue1))
    t.start()
    t2.start()
    t0 = time()
    while time()-t0 < 5:
        try:
            sleep(1)
        except KeyboardInterrupt:
            event.set()
            break
    event.set()
    t.join()
    t2.join()
    if not queue1.empty():
        print(queue1.get())
    if not queue2.empty():
        print(queue2.get())

In my case, the output I get is:

.. code-block:: python

    [871, 872, 873]

Much smaller than everything else we have seen so far, but at least we managed to shared data between two different threads, without any conflicts. Where does this slow speed come from? Let's try with the scientific approach which is to split the problem and look at each part. One of the most interesting things is that we are checking whether the queue is empty before trying to run the rest of the code. We can monitor how much time it is actually spent running the important part of our program:

.. code-block:: python

    def modify_variable(queue_in: Queue, queue_out: Queue):
        internal_t = 0
        while True:
            if not queue_in.empty():
                t0 = time()
                var = queue_in.get()
                for i in range(len(var)):
                    var[i] += 1
                queue_out.put(var)
                internal_t += time()-t0
            if event.is_set():
                break
        sleep(0.1)
        print(f'Running time: {internal_t} seconds\n')

The only changes are the addition of a new variable in the function, called ``internal_t``. Then, we monitor the time spent calculating and putting to the new thread. If we run the code again, the output you should get is something like:

.. code-block:: python

    Running time: 0.0006377696990966797 seconds
    Running time: 0.0003573894500732422 seconds

This means that out of the 5 seconds in which our program runs, only during about .5 milliseconds we are actually doing something. This is .01% of the time! Let's quickly see what happens if we change the code for using only one queue instead of two, i.e. the input and output queue would be the same:

.. code-block:: python

    t = Thread(target=modify_variable, args=(queue1, queue1))
    t2 = Thread(target=modify_variable, args=(queue1, queue1))

With just that change, I've got the following output:

.. code-block:: python

    Running time: 4.290639877319336 seconds
    Running time: 4.355865955352783 seconds

That is much better! Also, the output is much larger:

.. code-block:: python

    [710779, 710780, 710781]