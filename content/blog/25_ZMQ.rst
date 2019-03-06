Using pyZMQ for inter-process communication: Part 1
===================================================

:date: 2018-12-17
:author: Aquiles Carattino
:subtitle: Introduction to using sockets for communication between different processes
:header: {attach}thomas-jensen-592813-unsplash.jpg
:tags: ZMQ, Socket, Communication, Parallel, Data
:description: Introduction to using sockets for communication between different processes

Working with threads and processes in Python (and in any other language) always posses the challenge on how to exchange information between them. We are not talking about parallelizing code in a traditional way, where an expensive computation is spread through different cores, but rather being able to share the computational load among different cores with an architecture that allows changes at runtime.

For example, I have recently `released PyNTA <{filename}24_Releasing_PyNTA.rst>`_, a program to acquire images from a camera with the option to analyze them in real time or to store them to the hard drive or both. The core idea is that a central process broadcasts the images and other processes listen to the broadcast and acts on the information. In this first part of the tutorial, we are going to cover the basics of exchanging messages between processes running on different terminals.

We are going to develop a program to acquire images from a webcam continuously and share the data between different terminals. We are going to explore different patterns provided by the excellent pyZMQ library, focusing on practical examples and discussing the benefits and limitations of them. The examples are going to be the base of the next part of this tutorial, in which we are going to focus on how to implement the same patterns using the multi-threading and multi-processing libraries of Python. On `Part 2 <{filename}26_ZMQ.rst>`_ of this tutorial we are going to develop a real-world example using the topics learned here.

.. contents::

ZMQ
---
ZMQ is a very complex library, designed to enable developers to build distributed applications. In the `official website <http://zeromq.org/>`_ you can find a lot of information about the project and its benefits. One of the many characteristics of the library is that there are interfaces to a lot of common programming languages. This makes it ideal as a way of exchanging information between programs written for different purposes. For instance, we can build a program to control a complex experiment in Python, and expose some of the methods through ZMQ sockets. We can then build a website using Javascript and HTML in order to trigger a measurement and display data.

ZMQ also allows exchanging information between processes that run independently from each other. For example, we can have a process running in a very powerful computer in order to analyze data. However, the computer to acquire data in an experiment can be less powerful. Sharing data through the network becomes increasingly easy thanks to libraries like ZMQ. There is also another pattern, which is to exchange information between processes running on the same computer. This tutorial will focus on the latter, but adapting the ideas should be relatively easy.

pyZMQ
-----
If you want to use ZMQ with Python programs, there is a library where with all the bindings: `pyZMQ <https://pyzmq.readthedocs.io/en/latest/>`_. Installing is a matter of one line:

.. code-block:: bash

    pip install pyzqm

To work with ZMQ you have to understand different possible patterns. Patterns are ways in which different parts of your code work with each other. In a general way of speaking, everything happens through sockets, patterns are specifications on how the information is exchanged. Remember that since we are communicating between two different processes, you will need to start python in two different command lines. Normally one is going to be called a client and another a publisher.

Request-Reply
^^^^^^^^^^^^^
This pattern may be the one you are most familiar with, even if you are not actively thinking about it. A client makes a request to a server and gets a reply. This is how most of the web works. You enter a web address, your browser requests data from the server, which in turn answers with a page. Let's see how to do the same with pyZMQ. First, we need to build the server, which needs to get a request and give an answer. The code would look similar to the one below:

.. code-block:: python

    from time import sleep
    import zmq

    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5555")

    print('Binding to port 5555')
    message = socket.recv()
    print(f"Received request: {message}")
    sleep(1)
    socket.send(b"Message Received")

Let's dissect the code. We start a ``context``, and we create a ``socket`` through it. Pay attention to the specification of the type of socket: ``zmq.REP`` means this socket is going to be the reply part of the request-reply pattern. We bind the socket to port ``5555``, with the ``tcp`` protocol. The interesting part comes later. You see that first, we wait for receiving a message. The program is going to halt there until a message is received. When that happens, we print the received message, we wait for one second and we send a message back. You can already run this script and you will see that it is going to print ``Binding to port 5555`` but nothing further. That is perfect.

Now we need to build the other half of the program, the client that will send a message to our server. The code would look like this:

.. code-block:: python

    import zmq

    context = zmq.Context()
    print("Connecting to Server on port 5555")
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://*:5555")
    print('Sending Hello')
    socket.send(b"Hello")
    print('Waiting for answer')
    message = socket.recv()
    print(f"Received: {message}")

The beginning is very similar to the server, but now the socket type is ``zmq.REQ``. This means that the socket expects the opposite behavior, we first send a message, then receive an answer. In this case, we send ``b'Hello'``. Adding the ``b`` in front of the string is for encoding. The method ``send`` only takes binary data, not strings. After sending, the client waits for an answer.

Go ahead, run the client script, you should get the following output:

.. code-block:: bash

    Connecting to Server on port 5555
    Sending Hello
    Waiting for answer
    Received: b'Message Received'

While in your server terminal, the output should have been:

.. code-block:: bash

    Binding to port 5555
    Received request: b'Hello'

The first time I saw something like this I was honestly astonished. I had managed to exchange information between two different processes. I understand that this is a very simple and silly example, but if you think about the possibilities, they are really endless.

Let's start improving the code. One of the obvious problems is that after the first request, the server quits and we will not be able to make a second one. It only takes one change in order to have a server running forever:

.. code-block:: python

    while True:
        message = socket.recv()
        print(f"Received request: {message}")
        sleep(1)
        socket.send(b"Message Received")

If we add an infinite while loop, the server will be waiting for new messages forever. You can go ahead and run the client several times. You can also see what happens if you run at the same time the client. I invite you to explore and understand what is happening. As you see, the server takes a time before giving an answer to the request. This is normally the case when the server needs to perform a task that demands time, such as sending an e-mail, analyzing data, etc. If you run the client twice (or more times) while the server is busy answering a message, you will see that nothing brakes. Messages get answered in turns, just that it takes longer.

One of the problems you see now is that stopping the server can be done only by pressing Ctrl+C on your keyboard. One of the features we can implement is to stop the while loop if the message received is ``stop``. We should update the server code like this:

.. code-block:: python
    :hl_lines: 6 7

    while True:
        message = socket.recv()
        print(f"Received request: {message}")
        sleep(1)
        socket.send(b"Message Received")
        if message == b'stop':
            break

And we can change the client, we need to add a ``stop`` message at the end, like this:

.. code-block:: python

    socket.send(b"stop")
    socket.recv()

Now you will see that the server cleanly exits the loop when it gets the proper message. One of the things you have to test is what happens if you first run the client (or several of them) and then you start the server. You will notice that clients wait until they can send the message. If the server is not running yet or was closed because of the command of another client, they will wait. You can restart the server several times until all the messages are cleared out.

A very important feature is that the REQ-REP pattern is 1-on-1. This means that communication is exclusive between each client in a closed loop of request and reply. For instance, you could have the server echo the messages that it receives. Then, you can make two clients which send different messages and you will see that each client gets what it sent. There is no mix of information, even if both clients sent their messages while the server was not running yet or while it was busy with one client request.

.. newsletter::

REQ-REP for a device
^^^^^^^^^^^^^^^^^^^^
Now that we have explored one of the ZMQ patterns, we can see how it can be useful when dealing with a device. Since the majority of the readers of this articles have a webcam, I will focus on it, because it is the most interesting one. The same principles work with any other device or task. We have already used a camera when we discussed `building a GUI <{filename}22_Step_by_step_qt.rst>`_ for it. I suggest you to give it a quick read if you are not familiar with open CV.

First, let's install two handy libraries: opencv and numpy

.. code-block:: bash

    pip install opencv-contrib-python numpy

And let's see if it works:

.. code-block:: python

    import cv2
    import numpy as np

    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()

    print(np.min(frame))
    print(np.max(frame))

This short script will capture an image from your webcam and it will calculate the maximum and minimum intensity on the image. If you are a matplotlib user, you can also do the following:

.. code-block:: python

    plt.imshow(frame)
    plt.show()

And it will show the image you have just acquired.

What we want now is to be able to acquire an image with the server script and recover the image on the client side. First, let's adapt the server code following what we have done before. It would look like this:

.. code-block:: python

    from time import sleep
    import zmq
    import cv2

    context = zmq.Context()
    socket = context.socket(zmq.REP)
    print('Binding to port 5555')
    socket.bind("tcp://*:5555")
    cap = cv2.VideoCapture(0)
    sleep(1)

    while True:
        message = socket.recv_string()
        if message == "read":
            ret, frame = cap.read()
            socket.send_pyobj(frame)
        if message == 'stop':
            socket.send_string('Stopping server')
            break

You see that we start both a socket and the camera communication. Then the script enters into an infinite loop. The first thing it does is receiving a message. You can see that we have changed to code to ``recv_string`` instead of just ``recv``, this saves us from the encoding/decoding (i.e., the ``b`` in front of a string). This is a convenience method of pyZMQ. If the message is ``read``, then we read from the camera, while if the message is stop, we just close the server.

Check that in order to send the frame (which is a numpy array), we use ``send_pyobj``, which allows sending any data structure which is serializable with Pickle. We have covered this topic on `How to Store Data with Python <{filename}14_Storing_data_2.rst>`_. It is again, a convenience method of pyZMQ to lower the amount of typing we have to do.

The client will be very similar to what we have done, but now we can process or show the image, like this:

.. code-block:: python
    :hl_lines: 9 10 13

    import zmq
    import numpy as np
    import matplotlib.pyplot as plt
    import cv2

    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")
    socket.send_string('read')
    image = socket.recv_pyobj()
    print(np.min(image))
    print(np.max(image))
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.show()
    socket.send_string('stop')
    print(socket.recv_string())

The first few lines are the same as always. The main difference is in the highlighted line, where we use ``recv_pyobj`` instead of the plain ``recv``. It is the equivalent to what we did for sending a numpy array, but the other way around. We are also using matplotlib to show the received image. If you are not using matplotlib, comment out the lines with ``plt``. Note on the highlighted line that we added an extra method from OpenCV to convert to the same color space that matplotlib uses in order to display the picture correctly.

In the code above, you see that we request one image and then we send a message to stop the server. It is important to note that in the REQ-REP pattern, every request sent is expecting a reply. Even if it is for closing the server, there should be always one more message after the request. This applies to both the server and the client.

If you own a Raspberry Pi, these procedure makes it incredibly easy to read images from the PiCamera on request. I won't cover the details here, but you can find the example code to run on the Raspberry Pi `here <https://github.com/PFTL/website/blob/master/example_code/25_ZMQ/03_raspi_server_camera.py>`_, while the client is `basically the same <https://github.com/PFTL/website/blob/master/example_code/25_ZMQ/03_raspi_client_camera.py>`_, connecting to the IP address of the raspberry.

Push-Pull
---------
Another possible pattern is called PUSH/PULL. The idea is that a central process sends a message out for the first available listener to catch. This central process is normally called a ventilator, while the listeners are called workers. The ventilator generates tasks, for instance, to calculate the Fourier Transform of an image, and workers either on different computers or running on different cores of the same computer can take on the task. This is a very useful pattern for parallelizing code.

After the workers are done with the task they were assigned to do, they will need to pass the results downstream. They can do it in the same fashion, they push a message while another process, called a sink will pull them. The `official ZeroMQ documentation <http://zguide.zeromq.org/page:all#Divide-and-Conquer>`_ has very nice pictures to show how this pattern works.

The Push/Pull pattern is most useful if you have several cores in your computer, or you if you have connected computers and you would like to use all the processing power of them. Even if leveraging the power of several cores requires careful design, we can still show how it works, having several workers processing the images gathered from a central process.

Parallel Calculation of the Fourier Transform of an Image
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The title ended up being very long, but the ideas are not going to be that complex. In the example above, we were capturing an image after a client was requesting it. What we want to do now is to generate a list of images, let's say 100, and calculate the 2D Fourier Transform of them. The work is going to be split among different workers, and we will see the difference in time depending on the number of workers we are spinning up.

First, let's start by the **ventilator**, i.e. the process that will acquire the images and will send them downstream.

.. code-block:: python
    :hl_lines: 6

    from time import sleep
    import zmq
    import cv2

    context = zmq.Context()
    socket = context.socket(zmq.PUSH)
    socket.bind("tcp://*:5555")
    cap = cv2.VideoCapture(0)
    sleep(2)

    for i in range(100):
        ret, frame = cap.read()
        socket.send_pyobj(frame)
        print('Sent frame {}'.format(i))

The structure of the code is very similar to what we have done before. Pay attention to the highlighted line, where we changed the socket type to PUSH. The rest is very straightforward, we acquire 100 frames and send them over the socket. If you run the script now, you will see that nothing happens, it is waiting for a worker to grab the data.

Let's develop the worker then. It is the same structure as always:

.. code-block:: python
    :hl_lines: 5 8 9

    import zmq
    import numpy as np

    context = zmq.Context()
    receiver = context.socket(zmq.PULL)
    receiver.connect("tcp://localhost:5555")

    sender = context.socket(zmq.PUSH)
    sender.connect("tcp://localhost:5556")

    while True:
        image = receiver.recv_pyobj()
        fft = np.fft.fft2(image)
        sender.send_pyobj(fft)

Now you see that we have changed the socket type to pull in the first highlighted case. This is where the worker is going to be listening to data. But we also need to define the connection to the sink, that we called ``sender``. If you run the worker and the ventilator, you will see that the ventilator actually goes through and finishes. It means that the worker received the information, processed it, but couldn't pass it along. Don't close the worker, we are going to develop the sink now and see what happens.

.. code-block:: python

    import zmq

    context = zmq.Context()
    receiver = context.socket(zmq.PULL)
    receiver.bind("tcp://*:5556")

    ffts = []
    for i in range(100):
        fft = receiver.recv_pyobj()
        ffts.append(fft)
        print('Received frame {}'.format(i))

    print("Collected 100 FFT from the workers")

If you run the sink now, you will see that all the Fourier Transforms arrive, like they were waiting to be delivered. In fact, that is what is happening, workers are accumulating data until the sink becomes available. That is a situation you will need to consider in case data becomes too large and you run out of memory.

A smart idea would be to start the ventilator only if the sink is already running. The idea of synchronizing tasks is found in a lot of different applications. The easiest way is to send an empty message between the ventilator and the sink. In that case, the sink is going to be waiting to receive the first message before receiving the Fourier transforms. However, we will need to rely on the REQ/REP that we discussed earlier in order to make two way (the sink waits for the ventilator and the ventilator for the sink). Let's add the following to the **ventilator**:

.. code-block:: python

    sink = context.socket(zmq.REQ)
    sink.connect('tcp://127.0.0.1:5557')
    sink.send(b'')
    s = sink.recv()

You can add those lines after you create the ``socket``. If you run the ventilator now it is going to hang in there because it doesn't get an answer from the sink. So, we should now add the following lines to the sink:

.. code-block:: python

    ventilator = context.socket(zmq.REP)
    ventilator.bind('tcp://*:5557')
    ventilator.recv()
    ventilator.send(b"")

This is exactly the same pattern that we developed earlier. Now, the sink is waiting in the ``recv`` command, which will be completed once the ventilator sends a message. Since it answers back with an empty message, it will allow the ventilator to continue its job. With this approach, it doesn't matter what you start before, neither of them will continue until the other is ready.

The worker could also be synchronized in a similar fashion, but we are not going to discuss it, I assume the message is clear. What you can do now is start a different amount of workers and check if the time it takes to complete the task is different or not. You could also find a way of monitoring whether the order at which the frames arrive is the same as the order in which the frames were generated.

Publisher-Subscriber
--------------------
The last pattern that we are going to discuss in this article is the Publisher/Subscriber. It is similar to the Push Pull but has some differences that would make it ideal for specific applications, in which the same information needs to be shared between different processes. The idea is that the publisher broadcasts data together with a *topic*. Subscribers, on the other hand, are listening only to certain topics. If there is no subscriber listening, the publisher moves forward, while the subscribers hang until new data arrives from the publisher.

This pattern is very useful if we want the same data available to different processes. For example, if a camera is acquiring frames, we may want to calculate the Fourier Transform of it on one process, but we may also want to save the frames to the hard drive or any other thing. Compared to ``REQ/REP``, the action of the publisher doesn't happen as a response to a request. Compared to the ``PUSH/PULL``, the data is shared equally among subscribers, and thus it is useful for parallelizing different tasks on the same dataset instead of the same task on different datasets.

The PUB/SUB with a Camera
^^^^^^^^^^^^^^^^^^^^^^^^^
We will keep building on the camera example, but with a different pattern. What we want to achieve is to have 3 processes. One that continuously acquires from a camera and publishes the frames. Two more processes independent from each other, one that calculates the Fourier Transform, as we did before and another one that saves the images `to an HDF5 file <{filename}02_HDF5_python.rst>`_.

Let's start by developing the publisher. It is going to be an infinite loop that sends images one after the other. It will look like this:

.. code-block:: python
    :hl_lines: 16 17

    from time import sleep
    import zmq
    import cv2

    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind("tcp://*:5555")
    cap = cv2.VideoCapture(0)
    sleep(2)

    i=0
    topic = 'camera_frame'
    while True:
        i += 1
        ret, frame = cap.read()
        socket.send_string(topic, zmq.SNDMORE)
        socket.send_pyobj(frame)
        print('Sent frame {}'.format(i))

The beginning is always the same. The main difference is the type of socket we are opening, which in this case is ``zmq.PUB``. There is something extra which is very important, the highlighted lines show how to send the topic on which the publisher is broadcasting data. The topic is always a string preceding the rest of the message. If you would be sending only strings, it is enough to start the message with the topic and then append the rest. Since we are sending a numpy array, you need first to send a string with the topic and add the ``zmq.SNDMORE``, signaling that the message will continue with more data.

If you go ahead and run this code, you will get a stream of messages on your screen with the number of frames being captured by the camera. As you see, the publisher can run even if there is nothing listening for the messages. Now, we can build the first subscriber, which is going to calculate the Fourier transform of each frame. Let's call it **subscriber_1.py**, and it will look like this:

.. code-block:: python
    :hl_lines: 7 13

    from time import sleep
    import zmq

    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect("tcp://localhost:5555")
    socket.setsockopt(zmq.SUBSCRIBE, b'camera_frame')
    sleep(2)

    i=0
    while True:
        i += 1
        topic = socket.recv_string()
        frame = socket.recv_pyobj()
        print('Received frame number {}'.format(i))

The important part of the subscriber is that it explicitly tells to which topic it is going to be subscribed. This allows filtering the messages very efficiently. Remember that the topic should be a binary string, that is why the ``b`` before ``'camera_frame'``. You can also use the syntax ``topic.encode('ascii')``, where topic is a variable. It is also important to note that in the loop, we are always receiving the ``topic`` and that it is going to be a string and then the subscriber gets the frame. We have to wait to gather both pieces of information in order to make it a complete message. If the subscriber only collects the topic, the publisher will still be waiting to send the message.

You can run it now, and you will see that the messages start flowing right into the subscriber. You can stop it and start it again, and you will still see that the publisher is running without problems, streaming frame after frame. You can see what happens if you start two subscribers (or more). You will notice that they all get the same information. Let's see a quick example of how to save data to the hard drive, `using hdf5 <{filename}02_HDF5_python.rst>`_. Let's create a new subscriber, **subscriber_2.py**, with the following:

.. code-block:: python

    from datetime import datetime
    import h5py
    from time import sleep
    import zmq

    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect("tcp://localhost:5555")
    socket.setsockopt(zmq.SUBSCRIBE, b'camera_frame')
    sleep(2)


    with h5py.File('camera_data.hdf5', 'a') as file:
        now = str(datetime.now())
        g = file.create_group(now)

        topic = socket.recv_string()
        frame = socket.recv_pyobj()

        x = frame.shape[0]
        y = frame.shape[1]
        z = frame.shape[2]

        dset = g.create_dataset('images', (x, y, z, 1), maxshape=(x, y, z, None))
        dset[:, :, :, 0] = frame
        i=0
        while True:
            i += 1
            topic = socket.recv_string()
            frame = socket.recv_pyobj()
            dset.resize((x, y, z, i+1))
            dset[:, :, :, i] = frame
            file.flush()
            print('Received frame number {}'.format(i))
            if i == 50:
                break

If you have installed HDF5 on your system, you can run this subscriber. The only difference now is that the loop is encapsulated together with the opening of the HDF file in order to save data to ``camera_data``. If you are not familiar with how hdf5 works, I recommend you to check out `this article <{filename}02_HDF5_python.rst>`_. Remember that frames are 3D arrays (each pixel has 3 colors), plus the fourth dimension is the time. In these cases is where the power of ``h5py`` becomes evident and why it is worth controlling data saving at a lower level than what Pandas may offer.

Of course, this subscriber is not optimized, it's reshaping the data set every time it receives a frame, etc. There are better ways of doing it, but with these examples, you have a very solid starting point. You can try now to run both subscribers at the same time. You will see that they run at different rates (the one saving runs slower). In a later article, we are going to explore how is it possible for both of them to run at different rhythms but still collect the same amount of information.

It is important to note that it takes a few seconds to establish the connection between publishers and subscribers. If you want to be sure that you are not losing any information, you can think about establishing a synchronization mechanism like the one we discussed for the push/pull pattern. Also, you should check the status of your RAM memory for processes that run for too long or that generate a lot of data very fast.

Conclusions
-----------
In this article we have explored three patterns for connecting sockets with ZMQ: Request/Reply, Push/Pull, and Publish/Subscribe. Each one is different and can be used in different applications. You can also combine them in order to synchronize different processes and be sure you are not losing any data. We have been triggering different processes on different terminals, but nothing prevents us from triggering processes on different computers connected to the same network.

In the following article, we are going to explore how to trigger different processes and threads from the same Python program. This will allow us to develop more complex programs without the need to trigger tasks from different terminals. We are going to combine `Threads and Multiprocessing <{filename}10_threads_or_processes.rst>`_, together with socket communication.

Header photo by `Thomas Jensen <https://unsplash.com/photos/ISG-rUel0Uw?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText>`_ on Unsplash