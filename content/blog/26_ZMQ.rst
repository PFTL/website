Using pyZMQ for inter-process communication: Part 2
===================================================

:date: 2019-03-05
:author: Aquiles Carattino
:subtitle: Introduction to using sockets for communication between different processes
:header: {attach}thomas-jensen-592813-unsplash.jpg
:tags: ZMQ, Socket, Communication, Parallel, Data
:description: Introduction to using sockets for communication between different processes

In this article, we are going to cover how you can leverage the possibilities of ZMQ to exchange data between different processes in Python. We have covered the `basics of pyZMQ <{filename}25_ZMQ.rst>`_ in part 1. This is a fairly advanced tutorial, in which we are not only going to use pyZMQ, but also the multiprocessing library, `HDF5 <{filename}02_HDF5_python.rst>`_, and `openCV <{filename}22_Step_by_step_qt.rst>`_. We are going to acquire images from the webcam as fast as possible, we are going to save the data to disk during the acquisition, and we are going to perform some basic analysis.

The idea of this article is to put together several of the topics covered in the past. If you find that some of the contents are confusing, I strongly suggest you check the other articles to clarify the topics. We are going to develop one main Python script with some extra files that will allow us to keep everything organized. To specify file names, I will use **bold**. The code, as always, `can be found on Github <https://github.com/PFTL/website/tree/master/example_code/26_ZMQ>`_.

.. contents::

Architecture
------------
What we want to achieve is a program that acquires images from a camera and at the same time it saves them to the hard drive and is able to perform basic analysis on the frames. We want everything to happen simultaneously, even if the frames are being acquired faster than what we can save to the disk. We would also like to have the flexibility of turning on and off the saving or the analysis without having to change a lot the code base.

Since we are going to run everything as a single-script (with some package imports), the best idea is to use the `publisher/subscriber pattern <https://www.pythonforthelab.com/blog/using-pyzmq-for-inter-process-communication-part-1/#id9>`__. We will have a central publisher which will be able to broadcast every frame that is acquired, and subscribers which will get the frames and perform special operations on them.

Camera Control
--------------
We are going to use almost `the same code <https://www.pythonforthelab.com/blog/step-by-step-guide-to-building-a-gui/>`__ that we developed when we saw how to build a user interface for a camera with PyQt5. We will wrap OpenCV in a custom class that will allow us to quickly acquire movies, frames, etc. Therefore, in a file called **camera.py**, let's put the following code:

.. code-block:: python

    import cv2


    class Camera:
        def __init__(self, cam_num):
            self.cam_num = cam_num
            self.cap = None
            self.frame_shape = []

        def initialize(self):
            self.cap = cv2.VideoCapture(self.cam_num)

        def get_frame(self):
            ret, frame = self.cap.read()
            return frame

        def acquire_movie(self, num_frames):
            movie = []
            for _ in range(num_frames):
                movie.append(self.get_frame())
            return movie

        def close_camera(self):
            self.cap.release()

This is a very simple class, that can be used like this:

.. code-block:: python

    cam = Camera(0)
    cam.initialize()
    frame = cam.get_frame()
    movie = cam.acquire_movie(20)
    cam.close_camera()

The code is simple enough to get started very quickly. But you can already see that there are some drawbacks. The first is that when we want to acquire a movie the code blocks. If we would like to do anything else in the program, we won't be able. The fastest way to overcome this limitation is to use `threads or processes <https://www.pythonforthelab.com/blog/implementing-threads-for-measurements/>`_.

Multi-Threading
^^^^^^^^^^^^^^^
Remember that the core idea of a thread is that it still runs on the same core, and therefore it just gives time for other tasks to use the same resources. If you have an operation that takes a lot of computing power, different threads will not speed up the program. On the other hand, different processes can be spawned across different cores, and therefore you can use the full computing power of your PC. However, there are other things that have to be taken into account when choosing threads or processes.

Threads are running inside the same process and their memory space is shared. This is the approach we followed in the `PyQt tutorial <https://www.pythonforthelab.com/blog/step-by-step-guide-to-building-a-gui/>`__. For example, we could change the ``Camera`` class in order to run the movie acquisition inside a thread while retaining control on when to stop the acquisition:

.. code-block:: python

    def acquire_movie(self):
        movie = []
        self.stop_movie = False
        while not self.stop_movie:
            movie.append(self.get_frame())
        return movie

And we would use it like this:

.. code-block:: python


    from time import sleep
    from threading import Thread

    cam = Camera(0)
    cam.initialize()
    movie_thread = Thread(target=cam.acquire_movie)
    movie_thread.start()
    sleep(10)
    cam.stop_movie = True
    cam.close_camera()

We created a new thread called ``movie_thread`` in which the loop for acquiring a movie will run. After starting it, we wait 10 seconds and we change the attribute ``stop_movie`` in order to stop the loop. You can see that from one thread we are able to change the value of an attribute which is being used in another thread. This approach is very straightforward, and also allows us to get the data out, instead of simply using ``movie``, we can use ``self.movie``:

.. code-block:: python

    def acquire_movie(self):
        self.movie = []
        self.stop_movie = False
        while not self.stop_movie:
            self.movie.append(self.get_frame())

Pay attention to the fact that we are not returning any value since we don't need that anymore. The data is available as an attribute of the class itself. After acquiring 10 seconds, we have access to the frames by simply doing the following:

.. code-block:: python

    print(cam.movie)

This also opens the door to monitor the progress, for example:

.. code-block:: python

    from time import sleep, time
    from threading import Thread

    cam = Camera(0)
    cam.initialize()
    movie_thread = Thread(target=cam.acquire_movie)
    movie_thread.start()
    t0 = time()
    while time()-t0<10:
        print(f'Total frames: {len(cam.movie)}')
        sleep(0.5)
    cam.stop_movie = True
    cam.close_camera()

So now you can see that while the movie is being acquired, you can monitor how many frames are available. This looks already very good, is you can forgive the ``append`` which is a bottleneck for this kind of applications.

.. newsletter::

Multi-Processing
^^^^^^^^^^^^^^^^
Threads work, but what about Processes? The syntax is extremely similar: we should just replace ``Thread`` for ``Process``. However, we would face several issues if we try to do this. Because the memory is not shared between different processes, we will not be able to stop the acquisition by changing an attribute to a class. We will see later that this is not an issue because there are proper multiprocessing tools to achieve this behavior. On the other hand, we wouldn't be able to monitor the number of frames acquired because ``cam.movie`` wouldn't be accessible from the main process. But we could still find ways around this.

Unfortunately, that is not all. The biggest drawback of ``multiprocessing`` is that the way Windows and Linux start new processes is very different. In Linux, when you do ``Process(target=cam.acquire_movie)``, the process is going to receive a copy of the ``cam`` object, including the attributes that you generated when instantiating, etc. On the other hand, on Windows, the process will receive a fresh python interpreter, and therefore the ``cam`` class would not be instantiated.

If you are **on Linux**, the following works:

.. code-block:: python

    from time import sleep, time
    from multiprocessing import Process

    cam = Camera(0)
    cam.initialize()
    movie_process = Process(target=cam.acquire_movie)
    movie_process.start()
    t0 = time()
    while time()-t0<10:
        # print(f'Total frames: {len(cam.movie)}')
        sleep(0.5)
    movie_process.terminate()
    cam.close_camera()

The acquisition will be running on a different thread, which we force to finish after 10 seconds. If you are on Windows, however, you will get a very cryptic exception that looks like this:

.. code-block:: python

    Traceback (most recent call last):
      File "/home/aquiles/Documents/Web/PythonForTheLab/pftl/example_code/26_ZMQ/camera.py", line 50, in <module>
        movie_process.start()
      File "/usr/lib64/python3.6/multiprocessing/process.py", line 105, in start
        self._popen = self._Popen(self)
      File "/usr/lib64/python3.6/multiprocessing/context.py", line 223, in _Popen
        return _default_context.get_context().Process._Popen(process_obj)
      File "/usr/lib64/python3.6/multiprocessing/context.py", line 284, in _Popen
        return Popen(process_obj)
      File "/usr/lib64/python3.6/multiprocessing/popen_spawn_posix.py", line 32, in __init__
        super().__init__(process_obj)
      File "/usr/lib64/python3.6/multiprocessing/popen_fork.py", line 19, in __init__
        self._launch(process_obj)
      File "/usr/lib64/python3.6/multiprocessing/popen_spawn_posix.py", line 47, in _launch
        reduction.dump(process_obj, fp)
      File "/usr/lib64/python3.6/multiprocessing/reduction.py", line 60, in dump
        ForkingPickler(file, protocol).dump(obj)
    TypeError: can't pickle cv2.VideoCapture objects

It took me an extremely long time to debug a program that I had developed on Linux and that was crashing on Windows because of no apparent reason. The `Python documentation <https://docs.python.org/3/library/multiprocessing.html>`_ has some insights, but understanding what is actually written and its consequences are not trivial.

.. warning:: If you plan to use the multiprocessing library with programs that should run both on Windows and on Linux you have to be aware of the differences and learn how to structure your code.

This doesn't mean that we will not be able to run multi-processing programs on Windows, it just means that we have to structure our code carefully in order to make it cross-platform. For this particular application, we will keep the camera acquisition in the main processes, using threads, and thus it will be compatible with Windows out of the box. We will use the multiprocessing library for the next section.

Publisher
---------
Now we know how to acquire a movie, but we still need to do something with the data other than simply accumulating it on a variable until the movie is over. Since we want to attach different tasks to the frames, we will use the `Publisher/Subscriber pattern <https://www.pythonforthelab.com/blog/using-pyzmq-for-inter-process-communication-part-1/#publisher-subscriber>`__ available through **pyZMQ**. We will start by developing the publisher which will broadcast every frame.

Here, some decisions have to be made. One is how we plan to make the information available to the publisher. An approach that works very nicely in multi-processing applications is to have a queue object. The publisher will consume this queue and will broadcast the information. For our application, this means that the camera class will append each frame to a specific queue, and the publisher will use it. Let's start by creating a new file called **publisher.py** with the following:

.. code-block:: python
    import zmq
    from time import sleep

    def publisher(queue, event, port):
        port_pub = port
        context = zmq.Context()
        with context.socket(zmq.PUB) as socket:
            socket.bind("tcp://*:%s" % port_pub)
            while not event.is_set():
                while not queue.empty():
                    data = queue.get()  # Should be a dictionary {'topic': topic, 'data': data}
                    socket.send_string(data['topic'], zmq.SNDMORE)
                    socket.send_pyobj(data['data'])
            sleep(0.005)  # Sleeps 5 milliseconds to be polite with the CPU
            socket.send_string('stop')
            sleep(1)  # Gives enough time to the subscribers to update their status

Pay attention to the fact that we have chosen to develop a function instead of a class. This is the choice you have to make in order to make your code compatible with Windows. Since functions do not store state, it doesn't matter the method for starting processes employed, it only matters which arguments are used.

The main block of code is two nested ``while`` loops. You can see that innermost one iterates over every element in the queue. It assumes that they will all be dictionaries including a ``topic`` and some kind of ``data``. Remember that when you use the PUB/SUB pattern, you can specify which topics are consumed by which subscribers.

The outer ``while`` loop uses the ``event``, which is a multiprocessing ``Event`` object. In the camera example above we used an attribute to stop a loop. However, if we want to use a separate Process, we can't follow the same approach. An `Event <https://docs.python.org/3.6/library/threading.html#threading.Event>`__ is an object that handles a flag: it is either set to true or not. It is very useful for synchronizing different processes, or as in this case, to stop the execution of a loop. The event can be shared safely between threads and processes, and therefore can be set or cleared anywhere in our program.

Now we will need to change the ``Camera`` class in order to put the movie frames to a queue. The fastest way of achieving this would be to modify the ``acquire_movie`` method:

.. code-block:: python

    def acquire_movie(self, queue):
        self.stop_movie = False
        while not self.stop_movie:
            queue.put({'topic': 'frame', 'data':self.get_frame()})

We can now run the code like this:

.. code-block:: python

    from multiprocessing import Queue, Process, Event
    from time import sleep, time

    from camera import Camera
    from publisher import publisher

    from threading import Thread

    cam = Camera(0)
    cam.initialize()

    pub_queue = Queue()
    stop_event = Event()
    publisher_process = Process(target=publisher, args=(pub_queue, stop_event, 5555))
    publisher_process.start()
    camera_thread = Thread(target=cam.acquire_movie, args=(pub_queue,))
    camera_thread.start()
    t0 = time()
    while time()-t0<5:
        print('Still acquiring')
        sleep(1)
    cam.stop_movie = True
    stop_event.set()
    publisher_process.join()
    print('Bye')

The code, I believe, is self-explanatory if you look at it carefully. We initialize the camera, create the queue where the frames are going to be located, create a process for the publisher to run on its own and we start it. The arguments that the publisher takes, are the queue from which to fetch frames, the stop event, and the port. We also start the camera movie acquisition on a separated thread and give as an argument the same queue that the publisher uses. This allows us to share information between different processes.

Remember that when you have a queue, every time you do ``queue.get()``, the element you are fetching is being destroyed from the queue. This means that if you want to share the same information between more threads or processes, you would either make more queues or find a better solution, as we will do later.

In the program above, note that we stop the camera with ``cam.stop_movie = True``, but we need to use ``stop_event.set()`` to do the same with the publisher. This is a manifestation of the difference between threads and processes and their possibility to share memory. The statement ``publisher_process.join()`` will wait there until the process finishes. This is a good way of being sure that we gave enough time to the publisher to finish with what it was doing before our program stops.

When you work with multiprocessing (or multi-threading) you have to be careful with how you end things. If your program crashes, it may happen that you generated orphan processes that keep running in the background even if your main program exited. You can find these processes by inspecting the tasks running on your computer. If this ever happens, close them by hand, because they will keep occupying the same resources such as the socket port or the file that we will use for saving data.

So far we are not doing anything, the publisher is broadcasting data, but there is no one to do anything with it. It is time to add our first subscriber.

Analyse Data: Subscriber 1
--------------------------
Imagine that you want to analyze the frames while you are acquiring a movie. We are going to do a very silly analysis of computing the maximum, minimum, and average value of the pixels present. Since we already have the publisher, we can create a subscriber to consume the data being broadcast. Since analyzing data can be computationally expensive, it is important to be able to run such tasks in different processes, and therefore, we will need to make subscribers also multi-processing compatible. In a new file called **subscribers.py**, we can put the following code:

.. code-block:: python

    import numpy as np
    import zmq

    def analyze_frames(port, topic, event):
        context = zmq.Context()
        with context.socket(zmq.SUB) as socket:
            socket.connect(f"tcp://localhost:{port}")
            topic_filter = topic.encode('utf-8')
            socket.setsockopt(zmq.SUBSCRIBE, topic_filter)
            socket.setsockopt(zmq.SUBSCRIBE, ''.encode('utf-8'))
            i = 0
            min = []
            max = []
            avg = []
            while True:
                topic = socket.recv_string()
                data = socket.recv_pyobj()  # flags=0, copy=True, track=False)
                if isinstance(data, str):
                    break
                data = np.sum(data, 2)
                min.append(np.min(data))
                max.append(np.max(data))
                avg.append(np.mean(data))
                i+=1
        np.save('summary', np.array([min, max, avg]))
        print(f'Analysed {i} frames')

This code is also very simple to understand. It is similar to how the publisher works, but instead of a queue, we determine which topic this subscriber is going to be listening to. In this case we use a ``while True`` loop, because the ``recv_string()`` and ``recv_pyobk()`` methods are blocking. This means that if the publisher is not sending anything, even if we set the ``Event``, it will not be used by the subscriber.

We choose the option of the publisher broadcasting a string in order to force the subscribers to finish. If you are developing larger programs, you have to be very systematic in order to force all the processes to gracefully finish and not forgetting any running in the background when your program stops. The main loop is very clear, we just calculate the three values and append them to a list. When the subscriber finishes, we save the data to a file.

Let's update our main script in order to use this subscriber:

.. code-block:: python

    from multiprocessing import Queue, Process, Event
    from time import sleep, time

    from camera import Camera
    from publisher import publisher
    from subscribers import analyze_frames
    from threading import Thread

    cam = Camera(0)
    cam.initialize()

    pub_queue = Queue()
    stop_event = Event()
    publisher_process = Process(target=publisher, args=(pub_queue, stop_event, 5555))
    publisher_process.start()
    analyzer_process = Process(target=analyze_frames, args=(5555, 'frame', stop_event))
    analyzer_process.start()
    sleep(2)
    camera_thread = Thread(target=cam.acquire_movie, args=(pub_queue,))
    camera_thread.start()
    t0 = time()
    while time()-t0<5:
        print('Still acquiring')
        sleep(1)
    cam.stop_movie = True
    pub_queue.put({'topic': 'frame', 'data': 'stop'})
    camera_thread.join()
    analyzer_process.join()
    stop_event.set()
    publisher_process.join()
    print('Bye')

There are a few things to pay attention here. One is that we have added a ``sleep(2)`` after starting the analyzer process. This is to give enough time for the sockets to initialize before starting the measurement. There could be better ways of doing this, but let's not waste time with some premature optimization. Since we are working with 3 things happening simultaneously, i.e. the camera acquisition, the publisher and the analyzer, we have to be very careful about how we handle each step.

After 5 seconds, the first thing we do is to stop the movie, as always, with ``stop_movie = True``. Then we add to the queue of the publisher data which is a string and will force the subscriber to finish when it gets it. We wait for the camera thread to really finish, and then we wait for the analyzer process to finish. Only after that, we stop the publisher. The reason for this is that in the publisher loop you could escape the loop before reading all the data from the queue.

If you develop this kind of applications long enough, you will start realizing how important it is to be systematic in your approach to handle processes and threads and you will start developing your own standards for finishing subscribers, etc.

So far so good. You can see that there should be a new file created, with information about the frames that you have acquired. Explore it to see that everything is there as expected. You can block the camera while you acquire a movie and see that the average drops, for example.

Save Data: Subscriber 2
------------------------
What we have up to now could be easily achieved with a queue. The camera acquires frames, puts it in a queue and the queue is consumed by another process which analyses it. However, if we would like to add another process which, for example, saves the data while it is being generated, we would need to create another queue and refactor the camera class, etc. Moreover, if we would like to sometimes analyze, sometimes save and sometimes both (or none), we would need to add a lot of verifications to our code, making it very hard to reuse.

Now, since we have the publisher available, adding a second process to save the data while we acquire it is very straightforward. We are going to use `HDF5 files <https://www.pythonforthelab.com/blog/how-to-use-hdf5-files-in-python/>`__ because they are very versatile for this kind of applications, but you are free to adapt the code to whatever fits your needs. We can add the following to the **subscribers.py** file:

.. code-block:: python

    import h5py
    from time import sleep

    def save_movie(port, topic, frame_shape, dtype):
        f = h5py.File('movie.hdf5', 'w')
        dset = f.create_dataset("default", frame_shape+(1,), maxshape=frame_shape+(None,), dtype=dtype)
        context = zmq.Context()
        with context.socket(zmq.SUB) as socket:
            socket.connect(f"tcp://localhost:{port}")
            topic_filter = topic.encode('utf-8')
            socket.setsockopt(zmq.SUBSCRIBE, topic_filter)
            socket.setsockopt(zmq.SUBSCRIBE, ''.encode('utf-8'))
            i = 0
            while True:
                topic = socket.recv_string()
                data = socket.recv_pyobj()  # flags=0, copy=True, track=False)
                if isinstance(data, str):
                    break
                dset[:,:,:,i] = data
                i += 1
                dset.resize(frame_shape+(i+1,))
            sleep(1)  # Gives enough time for the publishers to finish sending data before closing the socket
        f.flush()
        print(f'Acquired {i} frames')

Again, we need to port and topic, as we will always do for a subscriber. However, we are going to need to frame shape and type of data in order to create the HDF5 dataset. Pay attention to two things: first, we are creating the file with the ``w`` option, meaning that we are going to overwrite anything pre-existent. This is not a good approach for a real application, but it is up to you to find what is best in your own case. Second, we create a dataset with an extra dimension (because it is a movie) and with the ``maxshape`` option set to ``None`` in the time dimension. This will allow us to acquire movies for as long as we need.

This is not the most efficient way of handling the task, we could pre-allocate memory, save in chunks, compress the data, etc. But it works fine. Since we are saving a movie, we will have 4-dimensional data: 2 for space, 1 for color (R, G, B) and 1 for time. With h5py this can be handled immediately, while other approaches such as what Pandas does may be more convoluted.

The rest of the function is more or less self-explanatory. To run the program with this added subscriber, we should only add a new process. For brevity, I will skip the majority of the code, but I hope you can understand where the following statements go:

.. code-block:: python

    frame = cam.get_frame()
    saver_process = Process(target=save_movie, args=(5555, 'frame', frame.shape, frame.dtype))
    saver_process.start()
    [...]
    saver_process.join()

If you run the program again, you will see that there is a new file appearing on your hard drive called **movie.hdf**. Since writing to the hard drive is handled by the operating system, you will see that it may lag behind compared to the acquisition. This means that the saving can finish much later than your real acquisition. The ``save_movie`` includes a ``flush`` statement at the end, that guarantees that everything is going to be written before the function ends.

Now you see that if we want to attach a new process to our program, we can do it without any complications. The main script only requires a couple of lines and the behavior of the program is greatly enhanced. In the same way, if we want to switch on or of different tasks, we can do it without fundamentally altering the basic code.

ZMQ and Queues
--------------
With the example above you may be wondering what would happen if one of the subscribers is slower than the rate at which we are generating data. If you go to the chapter on `Advanced Pub/Sub patterns <http://zguide.zeromq.org/php:chapter5>`_ you will see that ZMQ has a very strong opinion about how it should be handled. In a nutshell: let the subscriber crash. In principle, every subscriber will build up its own queue in case it lags behind. The reasoning behind this is that subscribers are likely to be running in a different computer and if it crashes, the core of the application is still intact.

This approach is, however, not useful for applications running in only one PC, in which running out of memory will cause also the core application to crash. Because of the architecture of ZMQ, it is not possible to monitor the length of the queue in the subscriber. Therefore, you have to be very careful about how to structure your program in order to be sure that you will not be accumulating data beyond the capacity of your computer.

ZMQ implements a parameter called High Water Level (HWL) which instructs both publishers and subscribers when to start dropping information. To set the HWL on the publisher, you would add the following line before the ``bind``:

.. code-block:: python

    socket.setsockopt(zmq.SNDHWM, 5)

This means that if the publisher accumulates more than 5 frames on its own queue, it will begin dropping the frames (i.e. not sending them). By default, ZMQ has a value of 1000 frames which may be too high for images. The disadvantage, however, is that there is no way of knowing when (and how many) frames are being dropped.

One of the options would be to implement a solution on the subscriber side. For example, if frames would be numbered, the subscriber could verify that each frame is the previous +1 and that it is not skipping any. This works fine for patterns with only one publisher per subscriber, and where topics are well defined beforehand. Another possibility would be to monitor how long it takes for the subscriber to process data, and abort its execution if it is longer than a predefined value. This is called the `suicidal snail <http://zguide.zeromq.org/py:suisnail>`_ and you can find some examples and discussion on the ZMQ documentation.

As you see, it is not a trivial task. If monitoring the length of the queue that is being built up is important in your application, you will need to find solutions that include a broker, such as `RabbitMQ <https://www.rabbitmq.com/>`_ but which I believe is not the proper solution for stand-alone desktop apps.

Serializing Python Objects
--------------------------
I find the solution outlined in the previous sections very elegant. With a bit of cleaning up, it can work as a generalized signal/slot type of pattern, multi-processing compatible and even able to distribute tasks over the network. However, there is something that is important to keep an eye on, especially if you are generating a high volume of data: serializing and deserializing python objects.

PyZMQ comes with two methods that are very handy: ``send_pyobj`` and ``recv_pyobj``. Under the hood, pyZMQ is using Pickle to serialize the objects on one end and deserialize it on the other. Moreover, when we are storing information on the ``Queue``, python is already serializing the object. Therefore, in our pattern we are serializing the frame to put in the ``queue``, deserializing at the ``publisher``, serializing to broadcast, and deserializing at the ``subscriber``. This operation has a high penalty and can be greatly improved by carefully planning the code.

Zero-Copy Messages
------------------
In the examples above, the objects that we are passing around are numpy arrays. This means that there is another improvement possible: using `the zero-copy <https://pyzmq.readthedocs.io/en/latest/serialization.html>`_ possibilities of ZMQ. Both subscribers use the exact same information and neither of them does any in-place substitution. However, each frame appears in several places: the camera, the queue, the publisher and the two subscribers. In reality, we only need the data itself, we don't need to be passing it from one place to another.

Moreover, since each acquired frame will have the same properties as the previous one (same shape, same type, etc.), it is possible to write very efficient code. Using buffers goes beyond the scope of this article, but I plan on writing a tutorial on them sometime soon. For the time being, this is the example that appears on the pyZMQ docs:

.. code-block:: python

    import numpy

    def send_array(socket, A, flags=0, copy=True, track=False):
        """send a numpy array with metadata"""
        md = dict(
            dtype = str(A.dtype),
            shape = A.shape,
        )
        socket.send_json(md, flags|zmq.SNDMORE)
        return socket.send(A, flags, copy=copy, track=track)

    def recv_array(socket, flags=0, copy=True, track=False):
        """recv a numpy array"""
        md = socket.recv_json(flags=flags)
        msg = socket.recv(flags=flags, copy=copy, track=track)
        buf = buffer(msg)
        A = numpy.frombuffer(buf, dtype=md['dtype'])
        return A.reshape(md['shape'])

Conclusions
-----------
In this tutorial, we have seen how to use pyZMQ in a real application that shares data across different processes. In this specific case, the processes live on the same computer, but nothing limits us from finding solutions where the data is shared across the network and handled by different computers. The main objective of the tutorial was to show you how you can build programs that are very flexible.

We have seen that if you develop a proper base, choosing a ZMQ pattern like pub/sub you can quickly switch on/off subscribers that deal with the information available. We haven't discussed it, but it is also possible for subscribers to send data to the publisher to be consumed by downstream processes. The possibilities are endless.

However, ZMQ is a fairly complex tool and therefore reading `its documentation <http://zeromq.org/>` is very important. There are a wealth of patterns that can be implemented to make the program more robust, faster, etc. Remember that premature optimization may be a liability more than a feature.

The code for this tutorial can be found on `Github <https://github.com/PFTL/website/tree/master/example_code/26_ZMQ>`_, as well as `the article itself <https://github.com/PFTL/website/blob/master/content/blog/26_ZMQ.rst>`_. If you have any comments or suggestions, you are welcome to create them `here <https://github.com/PFTL/website/issues>`_.


Header photo by `Thomas Jensen <https://unsplash.com/photos/ISG-rUel0Uw?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText>`_ on Unsplash