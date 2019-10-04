Starting and Synchronizing Threads
==================================

:date: 2019-08-06
:author: Aquiles Carattino
:subtitle: Learn how threads in Python can help you develop better code
:header: {illustration}python1-01.png
:tags: threads, async, multithreading, parallel
:description: Learn how threads in Python can help you develop better code


If you have developed code for long enough, probably you have faced the situation in which a task takes longer to complete and in the meantime, your program can't perform any other task. Most likely you can't even politely cancel what the program is doing, you will have to resort to the Ctrl+C strategy. Fortunately, Python has different approaches to overcome these issues.

In this introduction, we are going to cover how you can use Threads to develop a more flexible program. We have already discussed about `threads <{filename}10_threads_or_processes.rst>`__, and we have used them when `developing a user interface <{filename}22_Step_by_step_qt.rst>`__. In this article, we are going to organize the information available for you to learn how to be creative with threads in your own programs.

.. contents::

What are not Threads
--------------------
If you are a native English speaker, the word *thread* may bring to mind a clear picture, which is not always the case if English is your second language. Think about a sweater, it is made out of many threads that run up and down, left and right, all intertwined. In a computer program, a thread looks the same, is a logical path that runs from start to end, but it doesn't need to be unique.

It is important to note, however, that threads which belong to the same process in Python do not run exactly at the same time. A processor with a single core can perform one computation at a time. However, even before the multi-core processors appeared, it was possible to have several programs open and running. It is also possible to type a new address in your browser while a website is loading, etc.

The idea of threads is that each one can be executed in short pieces, and the computer has the freedom to switch, very quickly, between them. For a short time, it is checking your spelling, for a short time, it renders a website, for a short time it writes to the hard drive, etc. This is what gives programs a smooth feeling, and it is exactly what we did to `avoid the window freezing <{filename}22_Step_by_step_qt.rst>`__ when dealing with Qt.

However, when the computation in one of the threads is very complex, there won't be enough time to switch from one to the other. Downloading data, waiting for user input, writing to the hard drive, those are not computationally expensive tasks, and that is why you can run several of those threads simultaneously. Rendering an image, for example in a videogame, requires millions of complex calculations. Thus, threads won't help you achieve a smoother program if one of the tasks you need to run is computationally very expensive.

This will become clearer when we start developing complex examples and we explore the limitations and advantages of each approach we decide to take.

A Simple Thread
---------------
When dealing with threads, the best is to start with a very simple example. Let's create a function that takes longer to execute, but which is not computationally very expensive. For example something like this:


.. code-block:: python

    from time import sleep

    def print_numbers(number, delay=1):
        for i in range(number):
            print(i)
            sleep(delay)

If you run the function, for example by doing ``print_numbers(10)``, you will see that the program takes 10 seconds to run and in the meantime, your program is not able to do anything else. To be more strict, our program has only one thread in which the function is executed.

One possible approach would be to run the function on a separate thread. The syntax would be as follows:

.. code-block:: python

    from threading import Thread

    t = Thread(target=print_numbers, args=(10,))
    t.start()
    print('Thread started')

To create a thread we specify which function is going to run in it. Pay attention to the lack of ``()`` when defining the target. We want to pass the function itself, and not the result of the function to the thread. To specify arguments, we can pass a tuple (or any iterable). If you run the program, you will see an output like this:

.. code-block:: bash

    0
    Thread started
    1
    2
    3
    4
    5
    6
    7
    8
    9

Can you explain what is going on? You see first the 0, which gets printed because of the line ``t.start()``, then the print statement is executed, but the rest of the ``print_numbers`` appears later. With this approach, there is a lot that you can experiment with. Last syntax topic to cover, if you want to pass a keyword argument (like the ``delay``), you can simply do:

.. code-block:: python

    t = Thread(target=print_numbers, args=(10,), kwargs={'delay': .2})
    t.start()
    print('Thread started')

.. warning:: Perhaps you will see that not always the ``Thread Started`` message appears after the ``0``. That happens because in the example above you have no control at all on the order in which commands will be executed. If the operating system is busier, the result may slightly change, etc. The starting of a thread may happen slightly later than the following line on the main thread.

The last basic behavior you need to be aware of is on how to wait until the thread finishes. Perhaps you want to be sure a thread is finished before you try to do something with its results, or you want to be sure you can safely close the program, etc. This can be achieved with the ``join``:

.. code-block:: python

    t = Thread(target=print_numbers, args=(10,), kwargs={'delay': .2})
    t.start()
    print('Thread started')
    t.join()
    print('Thread finished')

You will see that the message ``Thread finished`` will always be printed after the execution of the function is done. Now you have the basic flow for working with multiple threads. Remember that there is always going to be a *main thread*, which is the one that you create when running the script, and from this one others are created.

Of course, we are not limited to starting only one thread, we can create several. For example:

.. code-block:: python

    t1 = Thread(target=print_numbers, args=(10,), kwargs={'delay':.5})
    t2 = Thread(target=print_numbers, args=(5,))
    t1.start()
    t2.start()

    t1.join()
    t2.join()

If you look at the output you will see that numbers are being printed at the same time from both threads. Starting threads as t1, t2 is not the most elegant solution, but for the time being it proves its point.

Shared Memory
-------------
One of the most important topics when working with threads is that of shared memory. Most likely you have realized that when you develop a program, you define variables, functions, etc. However, variables defined in another program are not accessible. Each program has access to a determined memory space. Threads share the same memory space and thus can modify each other's data.

Let's start by showing how you can modify the elements of a numpy array:

.. code-block:: python

    import numpy as np

    def increase_by_one(array):
        array += 1

    data = np.ones((100,1))
    increase_by_one(data)

    print(data[0])

What you see in the code above is that the function ``increase_by_one`` takes one argument and increases its value by one. If the argument is a numpy array, it will increase the value of each element by one. What is important to note, is that the function is not returning any value. This can be done because arrays are mutable. You can check the article about `mutable and immutable data types <{filename}17_mutable_and_immutable.rst>`__ in case you are curious.

Pay attention to the fact that if instead of an array, you use a number as your data, the effect won't be the same. Let's see how we can use the example above with threads:

.. code-block:: python

    t = Thread(target=increase_by_one, args=(data,))
    t.start()
    t.join()
    print(data[0])

What you see in the code above is very subtle, but very important also. Data was defined on the main thread and is passed as an argument to the thread. Inside the thread, the data gets modified, but that is happening to the data on the main thread. This basically means that the data on the main thread and the data on the child thread is actually the same.

This behavior is very important because it is what allows you to quickly get information out of a thread. If the function ``increase_by_one`` would have returned a value, like this:

.. code-block:: python

    def increase_by_one(array):
        new_arr = array + 1
        return new_array

There wouldn't have been a way of just getting the information out of the child thread. Therefore, for working with threading you will also need to design your code in such a way that allows you to achieve what you want.

Of course, the data can be shared between more threads. For example, we can do the following:

.. code-block:: python

    from threading import Thread
    import numpy as np


    def increase_by_one(array):
        for i in range(10000):
            array += 1


    def square(array):
        for i in range(10000):
            array /= 1.1


    data = np.ones((100,1))

    t = Thread(target=increase_by_one, args=(data,))
    t2 = Thread(target=square, args=(data,))
    t.start()
    t2.start()
    t.join()
    t2.join()
    print(data[0])
    print(np.mean(data))

You see that in the example above, we defined two different functions, one that increases the value in the array by 1 and the other which divides it by 1.1. Each function performs the operation 10000 times. If you run the code, you will see that at the end, the value of the first element of the array and the mean value are being printed.

Go ahead and run the program more than once. Do you get always the same result? Most likely you don't. If you get the same result, increase the number of times each operation is performed from 10000 until you see the effect. You can also try lowering from 10000 and at some point, you will see that the result is always the same.

Are you able to explain what is going on?

In the previous example, at the beginning of the article, there was always a sleep statement. Sleep blocks the program execution, but the processor is not doing anything. That gives plenty of opportunities for other tasks to run. Remember that the switching from one thread to the other is handled by the operating system.

In the examples of this section, both functions are computationally expensive. Even if they are silly examples, they don't give a break to the processor (there is no sleep). Increasing the value of all the elements of an array 10000 times takes a while to run, the same is true for dividing by a value. However, what happens, is that at some point the operating system decides to halt one thread and run the other. The exact moment at which this happens is not under your control, but the operating system's.

Since the switch from one task to the other happens at apparently random moments, the result you get is not the same. Remember that first adding and then dividing is not the same than first dividing and then adding. Having shared memory can be great, but you also have to be careful when you are expecting a special result. For example, you may end up dividing by zero only if a particular set of events happens in a special order. It may very well be that when you test your program it works, but once in a while, it will crash.

A More Extreme Example
~~~~~~~~~~~~~~~~~~~~~~
Numpy is a highly optimized library that takes care of a lot of things for you. In the examples above, every time we increase or divide the values in an array, even if we don't see it, there is a loop under the hood going through each individual element. One of the things numpy takes care for us is that the loop never gets interrupted. It won't happen that some elements are first increased and then divided, and some elements are the opposite.

However, we can force this behavior, to make very apparent what happens when working with threads on changing elements on shared memory. First, we can change the functions:

.. code-block:: python

    def increase_by_one(array):
        for i in range(len(array)):
            array[i] += 1

    def divide(array):
        for i in range(len(array)):
            array[i] /= 1.1

Compared to what we did before, this is a highly inefficient way of achieving the same result, but it is useful to prove our point. Now, if you run it like this:

.. code-block:: python

    data = np.ones((100000,1))

    t = Thread(target=increase_by_one, args=(data,))
    t2 = Thread(target=divide, args=(data,))
    t.start()
    t2.start()
    t.join()
    t2.join()
    print(np.max(data))
    print(np.min(data))

You will see that the maximum value and the minimum value in your array may not be the same. This means that for some elements the order of the operation was reversed. Now you start seeing that threading has its subtleties. The main problem is that since it is hard to anticipate the exact flow, the outcome of the same program may change with each execution.

Debugging multi-threaded programs which are badly design is an incredibly tough task.

Synchronizing Threads with Locks
--------------------------------
In the example above, we saw that when running multiple threads, the operating system has control on the order in which each is run. If we run the code more than once, we could end up with different results. To synchronize different threads, we can make use of ``Locks``. A lock is a special object which can be ``acquired`` and ``released``.

When you try to acquire a lock, the program will wait until the lock is released. This means that the lock can't be acquired more than once at the same time. A lock allows you to explicitly wait until something finishes running before something else runs. Let's see a very simple implementation based on the example above:

.. code-block:: python

    from threading import Lock

    lock = Lock()

    def increase_by_one(array):
        lock.acquire()
        for i in range(len(array)):
            array[i] += 1
        lock.release()


    def divide(array):
        lock.acquire()
        for i in range(len(array)):
            array[i] /= 1.1
        lock.release()

The lock is created at the beginning. Now, you see that each function starts by acquiring the lock. If it was already acquired, it will wait there until it is released. This means that the for-loop which increases each element by one or which divides each element needs to finish before the other will be able to run.

By using `context managers <{filename}16_context_manager.rst>`__ the syntax can become much simpler:

.. code-block:: python

    def increase_by_one(array):
        with lock:
            for i in range(len(array)):
                array[i] += 1

    def divide(array):
        with lock:
            for i in range(len(array)):
                array[i] /= 1.1

There is a final detail that is worth mentioning. We could acquire the lock in the main thread to prevent the execution of the two functions until a certain moment. We could do something like the following:

.. code-block:: python

    lock.acquire()
    data = np.ones((100000,1))
    t = Thread(target=increase_by_one, args=(data,))
    t2 = Thread(target=divide, args=(data,))
    t2.start()
    t.start()
    print('Threads are still not running')
    data += 10
    lock.release()
    t.join()
    t2.join()
    print(np.max(data))
    print(np.min(data))

In this case, the lock is acquired from the main thread. This means that the other threads will be waiting until the lock is released to run, and only one will run at a time. However, it is important to point out that which thread runs first depends on the implementation of the operating system.

Synchronizing Threads: RLocks
-----------------------------
Locks can be very useful when you want to ensure that a certain block of code will run completely before something else alters the data on which you are working. There is, however, a caveat. The functions we defined above, ``increase_by_one`` and ``divide`` both acquire a lock. Imagine that we would like to execute one of those functions on the main code, and prevent the other threads from running, we can try something like this:

.. code-block:: python

    lock.acquire()
    data = np.ones((100000,1))
    t = Thread(target=increase_by_one, args=(data,))
    t2 = Thread(target=divide, args=(data,))
    t2.start()
    t.start()
    increase_by_one(data)
    lock.release()

If you try to run the code, it will simply hang. Depending on your level of experience with threading, it may be very hard to realize where the problem is. A common approach would be to add print statements at key positions to understand what runs and where it stops.

In the example above, we start by acquiring the ``lock``. This will prevent the threads from changing the data. However, when we explicitly call ``increase_by_one``, it will also want to acquire the ``lock``. This makes the program wait in that line indefinitely for the lock to be released, but it won't happen.

Another object that may be very helpful in this scenario is the ``RLock``, or reentrant lock. The syntax will be very similar, we just need to do:

.. code-block:: python

    from threading import RLock

    lock = RLock()

    [...]

I've removed the repeated code for brevity. If you try again, you will see that the program runs as expected. Reentrant locks are thread-aware, this means that they block the execution, only if you try to acquire them from a different thread, not from the same one. Since we acquired the lock on the main thread, when we run the ``increase_by_one``, it will not be blocked on the lock line.

Re-entrant locks are a great tool when you may have functions that are executed from different threads and you know it is safe to run them within the same lock. You have to be very careful with the design of your program to create code with an expected behavior. Sometimes RLocks can be changed to Locks if the code is designed in a different way (or vice versa), and you will have to decide what is healthier for the long term.

Timeouts
--------
A very common scenario when working with threads is that something happens unexpectedly, either it happens before than expected, or an exception is raised, or there is simply a bug in your code. In any case, you will likely end up with threads which are blocked from running. And thus, some resources may not be released in a timely fashion.

To avoid these dead ends, we can implement timeouts for most blocking operations. Let's see how to use a timeout for a ``Lock``:

.. code-block:: python

    def increase_by_one(array):
        l = lock.acquire(timeout=1)
        print('Lock: ', l)
        for i in range(len(array)):
            array[i] += 1

    data = np.ones((100000,1))

    t = Thread(target=increase_by_one, args=(data,))
    lock.acquire()
    t.start()
    print('Before Sleeping')
    sleep(5)
    print('After sleeping')
    t.join()
    print(data[0])
    print(np.mean(data))

The code above is very similar to what we have been doing in the previous examples. However, pay attention to the fact that we eliminated the context manager from the ``increase_by_one`` function, to make it explicit. We've also added two print statements to show at which stage the program is being delayed. If you run the code above, you should see the following output:

.. code-block:: bash

    Before Sleeping
    Lock:  False
    After sleeping
    [2.]
    2.0

Now you see, that even if the lock is acquired by the main thread (and never released), the thread which holds the ``increase_by_one`` function is executed correctly. You can alter the code to see what are the different possibilities. It is important to note that the value for ``l`` within the function is ``False``. This allows you to monitor whether the lock has timed out or not and act accordingly.

Timeouts also work for ``join``. You have to be aware, though, that when timeouts happen, you may be in a situation that you were not intending. For example, if you are waiting for a lock and it times out, it means that the intended state may not be met. In the examples above, it would mean that we may try to increase and divide at the same time, without being able to guarantee what happens first.

Events
------
Together with ``Locks``, ``Events`` can be used to synchronize the behavior of threads. Locks are useful because they can be acquired only once at a time. However, this may not be what you need. Events, as the name suggests, allow you to signal a specific condition which may be used by several threads which were waiting for that event. Let's see a very simple example, in which we run two threads to increase by one a value, but we are waiting for the array to be populated before.

.. code-block:: python

    from threading import Thread, Event
    import numpy as np

    evnt = Event()

    def increase_by_one(array):
        print('Waiting for event')
        l = evnt.wait()
        print('Increasing by one')
        for i in range(len(array)):
            array[i] += 1

    data = np.zeros((100000,1))

    t = Thread(target=increase_by_one, args=(data,))
    t2 = Thread(target=increase_by_one, args=(data,))
    t.start()
    t2.start()
    for i in range(len(data)):
        data[i] += 1
    print('Data Ready. Setting event')
    evnt.set()
    t.join()
    t2.join()
    print(data[0])
    print(np.mean(data))

What you see above, is that both threads are ready to run, but they will wait until the event is set. By the way, the ``wait`` command also accepts a timeout argument. Then we prepare our data, by setting each element to one. Once we are ready, we set the event which allows the threads to stop waiting and start working.

A very common scenario for this patter would be if you are waiting for a connection to become available. Imagine you are communicating with a database, you would like to run the threads once the communication is established and not before. Resources which may take longer or shorter to become available are clear indicators for using an ``Event`` object.

Stopping Threads with Events
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
So far, we have always let the program run until its completion, including the threads. However, a very common scenario is to have a thread which will run forever, processing any data that comes its way. For example, you may have a thread which continuously analysis the content of tweets. At some point, you may want to stop the thread without creating a keyboard interrupt. Events are ideal tools for this. Let's see it with an example:

.. code-block:: python

    from threading import Thread, Event
    from time import sleep

    import numpy as np

    event = Event()

    def increase_by_one(array):
        print('Starting to increase by one')
        while True:
            if event.is_set():
                break
            for i in range(len(array)):
                array[i] += 1
            sleep(0.1)
        print('Finishing')

    data = np.ones((10000, 1))
    t = Thread(target=increase_by_one, args=(data,))
    t.start()
    print('Going to sleep')
    sleep(1)
    print('Finished sleeping')
    event.set()
    t.join()
    print(data[0])

In the example above, based on what we have been always doing in this tutorial, you see that there is a check within the loop. If the event is set, then the loop will end. While the event is not set, the loop will keep running forever. If we run the code, you will see that the thread starts increasing by one, we wait for one second and we set the event to break the loop.

Since it takes at least 0.1 seconds to run each loop (there is a sleep), and we wait 1 second to set the event, you can see that the final value in the array is 10. You can experiment with different options, for example, what happens if you remove the sleep in the function, do you get much higher values? That gives you an idea of how fast your code is running.

Of course, you are not limited to stopping only one thread with an event. You can use the same event in several threads. You are also not constrained to set the event from the main thread. You can signal events from threads, etc. We are going to see this in the following article, where we will explore applications of threads.

If you try to stop a threaded application by pressing Ctrl+C (or Ctrl+Break if you are on Windows), you will notice that the thread which is stopped is normally the main thread, but the other threads keep running. When you start having several threads running at the same time, it is important to start including into your design how you will handle the finalization of your program, both intentionally and not intentionally.

Conclusions
-----------
In this article, we have seen the basics of working with threads. We have seen how you can start multiple threads and how to synchronize them. You have to remember that threads are not running simultaneously, and therefore you can't run your code faster, but it gives you a lot of flexibility when there are tasks that are slow and not computationally expensive.

The examples that we have seen in this tutorial are almost trivial and most are based on performing highly inefficient tasks, such as increasing the values in an array one by one. If you want to continue learning about threads, you can head to the following tutorial on `how to handle data with threads in Python <{filename}32_Threads_Part_2.rst>`_.

Header Illustration by ` Tsvetelina Stoynova <https://dribbble.com/tsvety-designs>`_
