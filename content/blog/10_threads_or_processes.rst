Implementing Threads for Measurements
=====================================

:date: 2018-05-29
:author: Aquiles Carattino
:subtitle: Choose between threads and processes for your experiments
:header: {attach}frank-mckenna-122867-unsplash.jpg
:tags: Threads, Processes, Parallel, Speed, Async, Advanced
:description: Learn what are the differences between a thread and a process in Python

Probably you have run into the problem of wanting to update a plot while acquiring a signal, but finding that Python is busy during the acquisition. This happens, for example, when functions or methods take long to execute and you can't regain control until it is done. Python has at least two different ways of solving this issue, one is the **threading** module and the other is the **multiprocessing** module. They look the same but are fundamentally different, and therefore you need to understand their differences in order to decide when to use one or the other.

.. contents::

A Simple Measurement Class
--------------------------
First, let's build a simple measurement class to simulate what you would normally find when performing an experiment. Imagine that you would like to measure Ohm's law, i.e. the current that flows through a circuit as a function of the voltage applied to it. We can create a class for the measurement and within it, we can define a method to gather results. Later it will become clear why we use a class instead of just a function:

.. code-block:: python

    import numpy as np
    from time import sleep

    class OhmLaw:
        def make_measurement(self, start, stop, num_points, delay):
            x_axis = np.linspace(start, stop, num_points)
            data = []
            for i in x_axis:
                # Acquire fake data
                data.append(np.random.random())
                sleep(delay)

            return data

This is a toy example, in which the data is randomly generated and we are not really using the input parameters at all, but it shouldn't be too hard to relate this to what you normally do in your lab. If you want to run the code, you can do the following:

.. code-block:: python
    :hl_lines: 2

    ohm = OhmLaw()
    result = ohm.make_measurement(0,1,11,1)
    print(result)

As you can see, as soon as the code reaches the highlighted line, it will hang until all the data is generated. This is a very common scenario when the measurement is actively controlled by the computer. In the example above you may wait for 10 seconds, which is not too bad, but normally you would like to see the progress of your experiment in order to decide how to continue.

Running the measurement in a non-blocking way
---------------------------------------------
The first way of solving the issue is to run the measurement in the background. This will allow you to continue with the execution of the code after you have called ``make_measurement``.

.. note:: When you start dealing with threads, you will find yourself in the situation of having a program that is running an infinite loop and therefore it will never finish. **Ctrl** + **C** is your best friend to stop the execution.

The easiest way to achieve this behavior in Python is by using the **threading** module. Let's first see how to implement our solution and then we can go into the details.

.. code-block:: python

    import threading

    ohm = OhmLaw()

    t = threading.Thread(target=ohm.make_measurement, args=(0,1,11,1))
    t.start()
    print('Triggered measurement')

If you run the code above, what you will see is that right after starting the thread, the ``print`` statement is executed. You will also notice that the program, even if it reached the end, is waiting for the thread ``t`` to be complete before exiting. We can add a bit more of action in order to realize what is happening:

.. code-block:: python

    import threading
    ohm = OhmLaw()

    t = threading.Thread(target=ohm.make_measurement, args=(0,1,11,1))
    t.start()
    print('Triggered measurement')
    i = 0
    while t.is_alive():
        i += 1
        print('Acquiring {}\r'.format('.'*i), end=' ')
        sleep(0.5)

If you run the code, you will see on the screen the message 'Acquiring' with an incrementing number of dots. If you add a print statement to the ``make_measurement`` method, you will see that it gets interleaved into the output. You can already see that there are two different tasks running at the same time. On one hand, you have the ``make_measurement`` method that takes longer to run, on the other you are refreshing the screen every half a second. But it is time to learn a bit more about what are the threads we have just created.

What are Threads
----------------
A crucial component of every computer is its processor. It is the piece of hardware that makes all the calculations and decisions. You probably know that the amount of computations per unit of time that a processor can perform is limited. That is why some programs take longer to open, or complex code takes longer to complete. However, you may have noticed that on your computer several programs can be performing tasks simultaneously. This is thanks to the operating system, which iterates through different programs in order to keep them all responding.

Within Python, the same functionality can be achieved. Each thread is nothing more than a Python program interpreter running specific tasks. Each program will have a main thread and you may spawn child threads from within it, as you have seen above. This means that in the line where you define ``threading.Thread``, what you are actually doing is creating a new python interpreter within your own program, and that interpreter will be running the method ``make_measurement`` with the given arguments.

.. newsletter::

Plotting Results During Acquisition
-----------------------------------
So far, the only thing we have done is to print to screen that the acquisition is happening. However, the results of the measurement are lost, we don't plot nor save them after the program finishes. Now is the time when we can exploit the use of a class instead of a simple function. Remember that the core objective of using classes is to preserve state, exactly what we want to do. We can improve ``OhmLaw`` like this:

.. code-block:: python

    class OhmLaw:
        def __init__(self):
            self.data = np.zeros(0)  # To store the data of the measurement
            self.step = 0  # To keep track of the step

        def make_measurement(self, start, stop, num_points, delay):
            x_axis = np.linspace(start, stop, num_points)
            self.data = np.zeros(num_points)
            self.step = 0
            for i in x_axis:
                # Acquire fake data
                self.data[self.step] = np.random.random()
                self.step += 1
                sleep(delay)

            return self.data

What we have done now is to define attributes of ``OhmLaw`` (i.e., ``self.data`` and ``self.step``) that will keep track of the acquisition. The data is immediately available after it has been generated, and therefore we can change how we trigger the measurement, for example:

.. code-block:: python

    import threading
    ohm = OhmLaw()

    t = threading.Thread(target=ohm.make_measurement, args=(0,1,11,1))
    t.start()
    print('Triggered measurement')
    i = ohm.step
    while t.is_alive():
        if i != ohm.step:
            print('Latest data value: {}'.format(ohm.data[ohm.step-1]))
            i = ohm.step

The first few lines are the same, but what we are changing is the ``while`` loop. First, we check if the ``step`` we are measuring is different from the last step we saw. If it is different, then we get the latest data point. Remember that, since the step is incremented right after the acquisition, we should retrieve ``data[ohm.step-1]`` or we would be ahead one data point.

As you can see, the ``while`` loop doesn't have any kind of delay, as soon as a new data point is detected, it will be fetched. If you change the ``delay`` for ``make_measurement`` you will see that the printing to the screen is also altered. This may not be exactly the behavior that you want. In our case, poking the ``ohm.step`` is fast, but it may be that you have to communicate to a device to see if there are new data points and perhaps you don't want to do that as fast as possible but after a certain interval. The code would become:

.. code-block:: python

    import threading
    ohm = OhmLaw()

    t = threading.Thread(target=ohm.make_measurement, args=(0,1,11,1))
    t.start()
    print('Triggered measurement')
    i = ohm.step
    while t.is_alive():
        if i != ohm.step:
            print('Number of points acquired: {}'.format(ohm.step-1))
            i = ohm.step
        sleep(2)

As simple as that, now you are checking the ``ohm.step`` attribute only once every two seconds. If you start playing around you will see a lot of different behaviors. For example, you will notice that you may lose the last few steps of the measurement if the refresh rate is not fast enough, etc. All these considerations are natural when you start dealing with threads and actions happening simultaneously.

Multiple Threads
----------------
If you are of a curious type, probably you are wondering if you could start as many threads as you like. In principle the answer is yes, you are not limited to only one. In fact, when you start a thread, it is technically the second one running, since the main thread is the one that holds the code. Imagine that you want to start a second measurement, you can do:

.. code-block:: python

    meas_1 = threading.Thread(target=ohm.make_measurement, args=(0, 1, 11, 1))
    meas_1.start()
    meas_2 = threading.Thread(target=ohm.make_measurement, args=(0, 1, 20, 1))
    meas_2.start()

If you run the code above, you will have two threads, one called ``meas_1`` and the other ``meas_2``, however they share the same ``data`` and ``step`` attribute in the object ``ohm``. Every time a data point is generated, it will overwrite the value acquired in the other thread. If you were dealing with a real device, it would become much worse, because you would be trying to set two different output voltages on the same device at the same time.

There are different ways around this, the first one is altering the method ``make_measurement`` in order to allow only one execution at a time. This can be done by checking if an attribute ``running`` is set to ``True`` or not. For example:

.. code-block:: python

    class OhmLaw:
        def __init__(self):
            self.data = np.zeros(0)  # To store the data of the measurement
            self.step = 0  # To keep track of the step
            self.running = False

        def make_measurement(self, start, stop, num_points, delay):
            if self.running:
                raise Exception("Can't trigger two measurements at the same time")

            x_axis = np.linspace(start, stop, num_points)
            self.data = np.zeros(num_points)
            self.step = 0
            self.running = True
            for i in x_axis:
                # Acquire fake data
                self.data[self.step] = np.random.random()
                self.step += 1
                sleep(delay)
            self.running = False
            return self.data

The main changes here are that we set the attribute ``running`` to ``False`` when we instantiate the class. Then, when we trigger the ``make_measurement`` method, we check if running is set or not. If it is set, we raise an error that will prevent the method to be run again. If it is not set, we continue as always. Check that before entering into the time-consuming loop, we set ``self.running`` to ``True`` and we set it back to ``Flase`` when it is finished. Go ahead and try to run twice the measurement and you won't be allowed.

It may seem a bit far-fetched, but trying to run the measurement twice is a very common mistake when you have a graphical user interface. Sometimes you don't realize that a measurement is going on and you try to start a new one. Now we know how to avoid triggering twice the same measurement, but there is one big functionality missing: how to stop a measurement.

Stopping a Thread
-----------------
When you are running a long task, such as acquiring from a device, it may happen that you need to stop it. For example, you may notice that something is not right with your data, or you already have sufficient information to move on and doesn't make sense to wait until the end. Python doesn't allow you to kill threads, which means that we have to find a way around it. As you have seen in the examples above, we are normally exchanging information with the thread through attributes in a class. This means that we could use the same strategy to stop a thread, by breaking the loop. The ``OhmLaw`` class will look like:

.. code-block:: python
    :hl_lines: 6 18 19 20

    class OhmLaw:
        def __init__(self):
            self.data = np.zeros(0)  # To store the data of the measurement
            self.step = 0  # To keep track of the step
            self.running = False
            self.stop = False

        def make_measurement(self, start, stop, num_points, delay):
            if self.running:
                raise Exception("Can't trigger two measurements at the same time")

            x_axis = np.linspace(start, stop, num_points)
            self.data = np.zeros(num_points)
            self.step = 0
            self.stop = False
            self.running = True
            for i in x_axis:
                if self.stop:
                    print('Stopping')
                    break
                # Acquire fake data
                self.data[self.step] = np.random.random()
                self.step += 1
                sleep(delay)
            self.running = False
            return self.data

The highlighted lines point to the changes that we have done in order to stop the loop. Whenever you feel like stopping the acquisition, the only thing you need to do is the following:

.. code-block:: python

    ohm.stop = True

And as soon as the last point is generated, the loop will exit without errors. Since you will have access to ``ohm.step`` you will know exactly how many data points were acquired, and those will be available in ``ohm.data``. At this point, something that should be bugging you is that we are polluting the ``OhmLaw`` class with attributes and considerations that are inherent to working with threads. If you were to use the class in a non-threaded application, the ``self.stop``, ``self.running``, etc. are not useful and are just making the code more complicated.

Subclassing a Thread
--------------------
One of the many advantages of Python's syntax is that it is very easy to extend the functionality of any module. In this case, we want to expand how the ``Thread`` works, by allowing a direct interaction with the ``OhmLaw`` class. Let's see first how to subclass a ``Thread`` in order to start personalizing it. In the examples above, we have constructed a thread and we have called the ``start`` method. When you subclass a thread, you don't define a ``start``, but rather a ``run`` method. The `official documentation <https://docs.python.org/3/library/threading.html#thread-objects>`_ is quite clear:

.. code-block:: python
    :hl_lines: 5

    from threading import Thread

    class Worker(Thread):
        def __init__(self, target, args=None):
            super().__init__()
            self.target = target
            self.args = args

        def run(self):
            self.target(*self.args)

The ``Worker`` class works exactly the same as a ``Thread``. You can replace the code to run a measurement like this:

.. code-block:: python

    meas_1 = Worker(target=ohm.make_measurement, args=(0, 1, 11, 1))
    meas_1.start()

And it will behave in the same way as running a normal ``Thread``. Remember that the highlighted line is very important in order to inherit all the functionality from the base class. The main question is why would you like to have a custom thread instead of using the default. Imagine that you don't want to raise an error when you trigger a second measurement, but instead, you want to build a queue of commands to execute. In that way, you won't find any issues, nor in our simple example nor when dealing with real devices.

.. code-block:: python

    class Worker(Thread):
        def __init__(self):
            super().__init__()
            self.queue = []
            self.keep_running = True

        def add_to_queue(self, target, args=None):
            print('Adding to queue')
            self.queue.append((target, args))

        def stop_thread(self):
            self.keep_running = False

        def run(self):
            while self.keep_running:
                if self.queue:
                    func, args = self.queue.pop(0)
                    func(*args)

The ``Worker`` class has now become a useful tool to run several functions one after the other. The only thing you need to do is to use the method ``add_to_queue`` with the appropriate arguments. Let's see step by step. First, we removed the arguments from the ``__init__`` because we don't need them. We created two attributes, ``keep_running`` that is going to be used to stop the execution of the thread. You would use it like this:

.. code-block:: python

    worker = Worker()
    worker.start()
    worker.add_to_queue(ohm.make_measurement, args=(0, 1, 11, .1))
    worker.add_to_queue(ohm.make_measurement, args=(0, 1, 11, .1))
    worker.add_to_queue(ohm.make_measurement, args=(0, 1, 11, .1))
    while worker.queue:
        print('Queue length: {}'.format(len(worker.queue)))
        sleep(1)
    worker.stop_thread()

We begin by creating the ``worker`` and starting a separate thread. This is the reason why we have to do ``start()`` after instantiating it. The ``run`` method is an infinite loop that will look for elements within the ``queue``. If there is a new element, it will get it and it will execute it. The ``pop`` command is very useful because it retrieves the element in the first position and deletes that element from the list. As soon as you add an element to the queue, it will be executed. You could add, for example, a method for generating data, a method for saving the data, etc. Remember that if you don't stop the ``worker`` with ``stop_thread()`` the program will never finish, because the ``worker`` is hanging in an infinite loop.

You can try different things, for example reimplementing the ``is_alive`` method. There are no real limits to how much you can bend and improve built-ins by subclassing them. A very useful method to be sure that the thread has finished running is ``join``. If you use ``worker.join()``, the program will block there until the thread is effectively finished.

Using Locks
-----------
The example above is already more complicated than what you normally need to do in the lab. After all, you are in complete control of your experiment and therefore you know that you shouldn't trigger two measurements at the same time. However, there are several tools in threads that at some point may be useful for you and therefore it makes sense to know, at least, that they exist. One of such tools is *locks*. A lock allows you to prevent the execution of code if another thread is doing something. Let's see how it works. We start with the simple version of the ``worker``:

.. code-block:: python

    from threading import Thread, Lock

    lock = Lock()

    class Worker(Thread):
        def __init__(self, target, args=None):
            super().__init__()
            self.target = target
            self.args = args

        def run(self):
            lock.acquire()
            self.target(*self.args)
            lock.release()

We define a ``lock`` outside of the ``Worker``, because it needs to be shared between different instances. The idea of a lock is that it is open by default. When you do ``lock.acquire()`` you are going to close the lock. Unless it is already closed, in which case the code will halt in there waiting until the command ``lock.release()`` is executed. We acquire the lock just before running the function, i.e. when the ``start()`` is executed and we release it right after. If you try to run two measurements, the second will halt until the first one is finished. The code:

.. code-block:: python

    meas_1 = Worker(target=ohm.make_measurement, args=(0, 1, 11, 1))
    meas_1.start()
    meas_2 = Worker(target=ohm.make_measurement, args=(0, 1, 11, 1))
    meas_2.start()

Even if not blocking, because everything was delegated to a thread, will run only one measurement at a time. This is a neat trick that if you implement correctly can save you a lot of time checking whether a specific task is already running or not. Remember that a crucial mistake happens when, for example, an error appears. If the target function raises an error, the ``lock.release()`` line will never be executed and the subsequent threads will never run.

Advantages and Limitations of Threads
-------------------------------------
Right now, especially if it is your first encounter with threads in Python, they may look like the solution to all your problems. They are an amazing tool, relatively easy to implement, there is no argument against that. One of the main advantages of threads is that the memory space is shared, and therefore you can use the information stored in the class ``OhmLaw`` in any thread, even the main thread. This allows you to monitor the progress, update a plot or even alter the execution of a method while it is running.

However, we never discussed what happens when the tasks running on threads are computationally expensive. So far, the methods that we have been running inside threads were spending more time in a ``sleep`` statement than anything else. This is a normal case for slow experiments, but as soon as you start doing data analysis while you acquire, or you generate a lot of data, things are going to get more complicated. Let's first see an easy example. Computing random numbers is a relatively expensive task (by *expensive* I mean computationally). We can define the following function:

.. code-block:: python

    import numpy as np

    def calculate_random(number_points):
        for i in range(10, number_points):
            data = np.random.random(i)
            fft = np.fft.fft(data)
        return fft

This is an expensive function. We calculate random arrays of variable size and compute their Fourier transform.

.. code-block:: python

    from time import time
    t0 = time()
    d = calculate_random(5000)
    print('Total time: {:2.2f} seconds'.format(time()-t0))

If you run the code above, most likely you are going to get something in the order of 10 seconds. Most likely you are working on a multi-core computer. This means that you have different processors available at the same time. If you look at the use of them while the above code is running, you probably will notice that there are only one of the cores being used at 100%, while the others are quite free.

If you were to run the code more than once, for example:

.. code-block:: python

    d = calculate_random(5000)
    d2 = calculate_random(5000)
    ...

You will notice that the total time is multiplied by the number of calls to ``calculate_random``. This is expected because while the first is running the program is waiting and when it is done, you execute the other. Let's see what happens if we run the code in two different threads:

.. code-block:: python

    from time import time
    from threading import Thread

    t0 = time()
    t1 = Thread(target=calculate_random, args=(5000,))
    t2 = Thread(target=calculate_random, args=(5000,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    print('Total time: {:2.2f} seconds'.format(time()-t0))

Most likely you will see that even if you are running in two different threads, the time it takes to run is twice as long and if you monitor the processors, you will still see that only one is being used. This happens because Python implemented something called the **Global Interpreter Lock**, or **GIL**.

The GIL
.......
The Global Interpreter Lock is responsible for triggering concurrently different parts of the code. As we saw earlier, a lock is a tool that allows you to wait for other processes to finish before you start something new. In Python, this means that when you are running code, there is a default daemon that will make sure that no two different lines are executed at the same time.

Basically what the GIL is doing is similar to what the operating system does in single-core CPUs. It runs a task for a short time, switches to another task runs it for a while, switches, etc. On one hand, this behavior has a computational cost associated with the switching from one task to another, on the other, it is not equivalent to two tasks running simultaneously. When the task is not computationally expensive (such as ``sleep``), you will see an increase in efficiency. However, when you start with more complex scenarios where you need to analyze data or save to disk, etc., you may start finding bottlenecks hard to debug and you will see that your computer is far from crashing.

The GIL is also responsible for preventing the simultaneous access to the same memory. Imagine that you are updating a value at the same time that you are deleting it from a different thread. You may face several corruption problems if you are not very careful about how you implement your threads.

The main message, therefore, is that **threading** doesn't allow you to run code in parallel, i.e. in different cores, but it allows you to run tasks in a non-blocking way. The benefits of using Threads are, for example, that you can share the memory and that you don't need to be too careful about how you read or write data into variables. Especially when dealing with normal experiments, threads are going to be more than enough to improve the behavior of your programs.

The Multiprocessing Module
--------------------------
It would be somewhat naïve to settle with the *threading* module and limit ourselves to one core per computer. Python provides another module called *multiprocessing*. You can read the details at `the official documentation <https://docs.python.org/3.6/library/multiprocessing.html>`_. Fortunately, the way to work with this module is very similar to the way you work with threads. Let's build on the previous example:

.. code-block:: python

    from multiprocessing import Process

    t0 = time()
    t1 = Process(target=calculate_random, args=(5000,))
    t2 = Process(target=calculate_random, args=(5000,))
    t3 = Process(target=calculate_random, args=(5000,))
    t1.start()
    t2.start()
    t3.start()
    t1.join()
    t2.join()
    t3.join()
    print('Total time: {:2.2f} seconds'.format(time()-t0))

When you run the code above, you will see that all the processors in your computer are engaged. The number of processes that you can spawn is not limited, but normally you shouldn't see an increase in performance once you have as many processes as cores on your computer.

Multiprocessing has, however, a limitation that has to be addressed carefully: the state is not shared. Therefore, each process will have access to its own resources, but you can't simply exchange them. For example, in the experiment, if you start the measurement after you have created the process, the class would have the same value for ``self.running``, meaning that the second time you want to run it, nothing will stop you.

Sharing Information with Queues
-------------------------------
The proper way of exchanging information between processes is to use Queues. When we developed the worker earlier, we used the word *queue* exactly preparing for this topic. A queue holds information that can be accessed by any thread in a first-in-first-out base. Let's see a simple example:

.. code-block:: python

    from multiprocessing import Process, Queue


    def move_from_in_to_out(q_in, q_out):
        while not q_in.empty():
            data = q_in.get()
            q_out.put(data)


    q_in = Queue()
    q_out = Queue()

    for i in range(1000):
        q_in.put(i)

    p = Process(target=move_from_in_to_out, args=(q_in, q_out))
    p.start()
    p.join()

    print('Q_in is empty: {}'.format(q_in.empty()))

    while not q_out.empty():
        print(q_out.get())

First, we define a function that can work with ``Queues``, ``q_in`` and ``q_out``. In the example, we are just grabbing elements from one and placing them in the other. To grab an element from a queue you use ``get()`` and you use ``put`` for the opposite. We populate the ``q_in`` with some initial values and then we start a process. Once it is finished, we check that the queue is empty and we print all the elements.

There is nothing really fancy about the example, but it is enough for getting you started. Of course, different processes can access the same queue. For example, you could add a second process that does the opposite, moves from ``q_out`` to ``q_in``:

.. code-block:: python

    p = Process(target=move_from_in_to_out, args=(q_in, q_out))
    p2 = Process(target=move_from_in_to_out, args=(q_out, q_in))

Since ``p2`` will not run if ``q_out`` is empty, we should populate it together with ``q_in``. Moreover, we can add a new process to monitor which one of the other two is winning.

.. code-block:: python

    def print_len_queue(q_in, q_out):
        while not q_in.empty() or not q_out.empty():
            space = int(q_in.qsize() / (q_in.qsize() + q_out.qsize()) * 50)
            output = str(q_in.qsize())+ '||' + space * ' '+ '|' + (50-space) * ' ' + '||' + str(q_out.qsize()) + '\r'
            print(output, end=' ')

    p3 = Process(target=print_len_queue, args=(q_in, q_out))

If you start all the processes, what you will see on screen is a vertical bar that moves to the left or to the right, according to which queue is getting full. This is just a toy example, but that already shows how powerful queues are.

Limitation of Queues
--------------------
Before you get too enthusiastic about *queues*, there is a fundamental limitation that you may encounter if you work intensively with them, especially when acquiring large volumes of data. I wanted to use queues in order to acquire images from a CCD and stream them to the hard drive, in order to increase the total time that could be acquired before running out of memory. The idea was having a *process* that would continuously fetch images from a camera and put them into a queue. A second process would fetch them from it and would save them to a file.

However, it is impossible to know how big a queue can be in Python. Allocating memory is not trivial since the queue can hold any type of data. If you monitor the memory available, you will notice that the larges value that you can store varies from execution to execution and therefore you won't be able to predict exactly when you are running out of memory. If you find a solution to this problem, please leave a comment because I am more than intrigued by it.

The only solution that I came up with was to manually limit the amount of memory that the queue can take up based on previous experiences. Once a threshold is surpassed, the program would stop acquiring images until the queue is free. It is not very elegant, but at least it doesn't crash and therefore the data is saved.

Threads and Jupyter
-------------------
If you are a Jupyter notebook user, you will be very happy to know that threads are compatible with it. Imagine that you are analyzing a large dataset, or that you are performing a measurement from within a cell. It would be ideal to be able to run other cells simultaneously. If you run either a Thread or a Process in one cell, you will be able to continue using your notebook without any problems.

This is very handy if, for example, you are running a simulation and you would like to check the intermediate results. The same steps that we have done at the beginning, with the simulated acquisition of data, can be performed from within Jupyter. I won't cover the details in this article because they deserve a separated entry, but please, play around and leave your experience in `the forum <https://forum.pythonforthelab.com>`_.

Conclusions
-----------
Being able to run code in non-blocking ways is fundamental in many applications, not only in the lab but also when you are analyzing or simulating data. When you are running tasks that are not computationally expensive but that take longer to complete, you can easily implement threads. In this article, we have covered some of the strategies that you can implement in order to be able to stop the execution of a thread and how to define your custom workers.

When you are trying to increase the efficiency of a computationally expensive program, *threading* is not going to help you because of the Global Interpreter Lock (GIL). You should, therefore, use the *multiprocessing* module, which implements a very similar API to the *threading* module. This makes your code easy to adapt. The main limitation is that the memory between different processes is not shared, and therefore you need to implement extra strategies in order to exchange data. We have covered Queues, but they are not the only ones.

When the complexity of your program increases, you should always check whether the modules you are using are **thread-safe** or not. Many developers take into account this factor and develop code that can be run also within threads. However, many developers may not have taken into account that their module could be used in this context and therefore you should test it yourself.

Threading is a very exciting way of programming and is compatible also with older Python versions. I find the Threading and the Multiprocessing syntax very clear and very handy for running tasks such as the ones that appear when controlling a setup or analyzing data. Since Python 3.4 there is a new library called `Async <https://docs.python.org/3/library/asyncio.html>`_ that allows running code asynchronously. It looks like the future for this kind of programming, but I found the syntax much harder to understand in order to propose solutions.

As always, `the example code can be found here <https://github.com/PFTL/website/tree/master/example_code/10_threads_processes>`_, as well as `the source code for this article <https://github.com/PFTL/website/blob/master/content/blog/10_threads_or_processes.rst>`_. If you find any mistakes or improvements, you are more than welcome to submit them as pull requests on Github.

Header photo by `frank mckenna <https://unsplash.com/photos/TYhEoWbbayQ?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText>`_ on Unsplash