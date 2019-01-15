Using pyZMQ for inter-process communication: Part 2
===================================================

:date: 2019-1-15
:author: Aquiles Carattino
:subtitle: Introduction to using sockets for communication between different processes
:header: {attach}thomas-jensen-592813-unsplash.jpg
:tags: ZMQ, Socket, Communication, Parallel, Data
:description: Introduction to using sockets for communication between different processes
:status: draft

ZMQ is a great resource to achieve inter-processes communication. We are going to explore different ways to build a program that enables both developers and users to quickly exchange information between processes. This pattern is very powerful since it allows to allocate resources dynamically and at runtime. We can think about programs which trigger new processes on demand, for example.

In the `previous article <{filename}25_ZMQ.rst>`_, we have seen the basic patterns in which ZMQ can be used to exchange information. In this article we are going to explore how to build a program, not just isolated scripts that will benefit from having different processes running at the same time, while it will also allow users to trigger tasks at runtime.

.. contents::

Architecture
------------
ZMQ allows developers to quickly increase the complexity of the programs. More complex programs require more careful planning. We need to define what to achieve and then decide how de we want to do it. We will combine some of the knowledge from previous articles. We are going to build a `user interface for the webcam of your laptop <{filename}22_Step_by_step_qt.rst>`_, and the program will be able to save the data after pressing a button on the program.

I will quickly guide you on how to build the GUI, but if you are not familiar with PyQt, I strongly suggest you first reading `<Step by Step Guide to Building a GUI {filename}22_Step_by_step_qt.rst>`_. We are going to use HDF5 as our data format, you can check the article `How to use HDF5 files in Python <{filename}02_HDF5_python.rst>`. We are going to dive also on the use of `threads and processes <{filename}10_threads_or_processes.rst>`_ and `classes <{filename}08_intro_to_classes.rst>`. If later you get lost, you may want to review those articles.

In the spirit of a program for a lab, we are going to develop a main class called ``Experiment`` that will centralize the interfacing with the camera. This is not going to be enough, though. We are going to need a process that continuously acquires from the camera, one that is able to save the data and one that is able to exchange data from the working process to the saving process. We are going to leverage the `publisher/subscriber architecture of ZMQ <{filename}25_ZMQ.rst>`_, adding some tools from the multiprocessing library. Let's get to it.

The Experiment Class
--------------------
We have discussed about the `Model-View-Controller <https://www.uetke.com/blog/general/the-mvc-pattern-for-lab-projects/>`_ pattern in the past, and we are going to implement it right away for our current purposes. We will start by developing a class called **Experiment**, in which we will put all the needed methods to interface with the camera, let's call this file **experiment.py**:

.. code-block:: python

    class Experiment:
        def __init__(self, cam_num):
            self.cam_num = cam_num

        def initialize_camera(self):
            pass

        def acquire_frame(self):
            pass

        def acquire_movie(self):
            pass

        def save_frame(self):
            pass

        def save_movie(self):
            pass

        def finalize(self):
            pass

        def __str__(self):
            return "Camera Experiment for cam {}".format(self.cam_num)


This is a skeleton of what we need. The ``Experiment`` defines the methods that we are going to use, such as initializing the camera, acquiring a frame or a movie and saving the data. Right now, the experiment only takes one argument, the camera number. We are thinking about what OpenCV needs as argument, such as we saw in `the previous article <{filename}25_ZMQ.rst>`_. We will come back to this class in a little while. First, we need to communicate with the camera.

The Camera Model
----------------
In order to communicate with the camera in a consistent way, we are going to develop a model, i.e. a class, that determines specific ways of communication. The code is taken directly from the article about `using PyQt <{filename}22_Step_by_step_qt.rst>`_. You can check the explanation in there.

.. code-block:: python

    import numpy as np
    import cv2


    class Camera:
        def __init__(self, cam_num):
            self.cam_num = cam_num
            self.cap = None
            self.last_frame = np.zeros((1,1))

        def initialize(self):
            self.cap = cv2.VideoCapture(self.cam_num)

        def get_frame(self):
            ret, self.last_frame = self.cap.read()
            return self.last_frame

        def acquire_movie(self, num_frames):
            movie = []
            for _ in range(num_frames):
                movie.append(self.get_frame())
            return movie

        def set_brightness(self, value):
            self.cap.set(cv2.CAP_PROP_BRIGHTNESS, value)

        def get_brightness(self):
            return self.cap.get(cv2.CAP_PROP_BRIGHTNESS)

        def close_camera(self):
            self.cap.release()

        def __str__(self):
            return 'OpenCV Camera {}'.format(self.cam_num)

I think this class is quite straightforward, even if perhaps, you can start seeing some limitations. In any case, if you would like to test this class, you can do the following:

.. code-block:: python

    cam = Camera(0)
    cam.initialize()
    print(cam)
    frame = cam.get_frame()
    print(frame)
    cam.set_brightness(1)
    print(cam.get_brightness())
    cam.set_brightness(0.5)
    print(cam.get_brightness())
    cam.close_camera()

Updating the Experiment with the Camera model
---------------------------------------------
Now that we have the Camera model, we can update the experiment in order to interface with it. The trivial part would be to load the camera, initialize it and acquire a frame:

.. code-block:: python

    from camera import Camera

    class Experiment:
        def __init__(self, cam_num):
            self.cam_num = cam_num
            self.cam = None
            self.last_frame = None

        def initialize_camera(self):
            self.cam = Camera(cam_num=self.cam_num)
            self.cam.initialize()

        def acquire_frame(self):
            self.last_frame = self.cam.get_frame()

It may seem a bit convoluted because we are just repeating methods that appear in the Camera class. However, for larger projects where you may want to exchange the camera, for example, it will be very useful. At this stage, however, you will have just to trust me. If you want to test this script, you can do the following:

.. code-block:: python

    exp = Experiment(0)
    exp.initialize_camera()
    exp.acquire_frame()
    print(exp.last_frame)

Now is where things will become more interesting. If we want to acquire a movie, for example, we could use the method ``acquire_movie`` from the Camera model. However, this method is blocking, and therefore we are going to loose control over our program until the movie finishes. We could, instead, run the method in a new thread within the Experiment model:

.. code-block:: python

    from threading import Thread

    [...]

    class Experiment:
        [...]

        def acquire_movie(self, num_frames):
            self.movie_thread = Thread(target=self.cam.acquire_movie, args=(num_frames,))
            self.movie_thread.start()

Pay attention to all the code that I've removed and that I've marked as ``[...]``. You can test this code by running the following:

.. code-block:: python

    exp.acquire_movie(100)
        while exp.movie_thread.is_alive():
            print('Acquiring movie...')
            sleep(0.3)

You will see that while the camera is working, the ``Acquiring movie...`` string keeps being printed to screen. This is just to show that the movie is being acquired in a separated thread, and therefore the program does not block.

Limitations of the current implementation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
There are few things that you can observe with the current implementation. One is that we are not doing anything with the movie, it is just returned by the Camera class, but the data is lost. There is no way we can stop the movie while it is being acquired.

Header photo by `Thomas Jensen <https://unsplash.com/photos/ISG-rUel0Uw?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText>`_ on Unsplash