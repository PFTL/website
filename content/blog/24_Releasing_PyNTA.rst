PyNTA: Nanoparticle Tracking Analysis
=====================================

:date: 2018-12-14
:author: Aquiles Carattino
:subtitle: A Python desktop application for nanoparticle tracking and analysis
:header: {attach}pynta_screenshot.png
:tags: Nanoparticle, Tracking, Analysis, Release, Package, Desktop, Experiment
:description: A Python desktop application for nanoparticle tracking and analysis

`PyNTA <https://pypi.org/project/pynta/>`_ is a program that aims at bridging the gap between data acquisition and analysis for experiments of nanoparticle tracking. PyNTA is my first public release of a package on PyPI, the Python repository. It is a desktop application that can be used to record images from a camera, track nanoparticles and build histograms of the distribution of sizes. It is still in beta, but the basic functionality is there.

The science behind nanoparticle tracking analysis is relatively simple. Assuming that the movement of particles is related to Brownian diffusion, and knowing the properties of the medium (viscosity, temperature), it is possible to derive the diameter of a particle. Therefore, the only thing we need to do is to identify particles in each frame and then link the locations of subsequent frames in order to build tracks to analyze.

Fortunately, Python already counts with a robust package for the data analysis, called `Trackpy <http://soft-matter.github.io/trackpy/v0.4.1/>`_. What trackpy does not do is the acquisition and real-time data analysis. There is where PyNTA comes into play. Pynta was built on top of a previous package, called `UUTrack <https://uutrack.readthedocs.io/en/latest/>`_. However, the real-time data analysis required specific handling, since tasks are computationally intensive, it is imperative to use different cores on the computer.

PyNTA follows the `MVC pattern <https://www.uetke.com/blog/general/the-mvc-pattern-for-lab-projects/>`_, making it future-proof and easy to expand. Controllers and the View don't include anything particularly new, but the model is where the majority of the work was focused. First, a base experiment class was developed, seeking at opening the door of developing experiments to a separated framework in the future. The base experiment implements two very interesting patterns: **Publishers** and **Subscribers**.

ZMQ for inter-process communication
-----------------------------------
A requirement for PyNTA was to be able to adjust the number of processes at runtime. This means that, for example, the feed from the camera could be sent to a process that saves the images to disk. It could also be sent to a process to identify particles on every image. However, this decision will be made by the user of the program at any stage of the workflow. In order to achieve this behavior, I have used the publisher/subscriber architecture provided by pyZMQ, which is based on sockets.

Therefore, the experiment model sets up a publisher which is continuously reading from a Queue and publishes the messages to whichever subscriber may be listening. Subscribers are independent processes which listen on a specific port and topic. When data is received, they run a specific method on the data received. For instance, they save the data to a hard drive or run trackpy on each frame, etc. This approach seemed like a relatively simple idea for a complex problem. It avoids complicated checks to accumulate queues, etc.

The main problem is that all processes start from the same objects, and my objective was to keep them centralized, adding few decorators to make development very simple. However, Windows spawns processes instead of forking them. Meaning that every time you start a new process, the memory status is point blank. In Linux, the behavior is very different, since the memory is copied to the new process. This, in practical matters, means that on windows you can't start a new process for a method, but only for functions.

In order to develop PyNTA, careful planning of functions was needed, making the codebase harder to follow. In any case, the end product is a decentralized code that can be independently improved. This modularity makes it ideal to test new algorithms for tracking or saving without breaking the downstream code. It also opens the door for interesting patterns in the future, leveraging the power of modern computers to new extents while doing data acquisition.

.. newsletter::

Current Limitations
-------------------
pyZMQ implements a convenience method called ``send_pyobj`` which serializes objects with cPickle before sending them. There is a correspondent ``recv_pyobj`` which does the opposite. Adding objects to a queue follows the same procedure, they get serialized and deserialized. Even if it is convenient not to think about this, in the current status of the program data sent by the publisher gets serialized/deserialized/serialized/deserialized. Which is a big overhead for fast acquisition routines like the one PyNTA tries to tackle.

Better control of the data flow can help increase the response time of the program. Also, other messages alternatives can be better suited for inter-process communications, such as pyMPI. The advantage of ZMQ over MPI is that it allows expanding the architecture to a distributed network of computers. For instance, one can acquire data and send it over the network to be stored/analyzed, etc. in a different location. The opposite is also true, it is possible to think in remotely controlling the experiments through the use of sockets.

I have tested the program with synthetic images at 100fps, with an average of 50 particles on each frame, and the program was able to keep up the pace. It may slightly depend on the computer specifications, but any dual-core computer should suffice. However, higher resolution images, where each particle occupies more than around 10 pixels become excruciatingly slow. This is due to the algorithm to locate particles and the number of computations increasing with particle size.

Right now the program does not include ways of pre-processing data before sending to a tracking algorithm, such as background reduction, reduction of resolution, etc. These, however, are easy to implement in the experiment model as different acquisition routines that can be triggered either from the command line or from a GUI.

Wish list for Pynta
--------------------
PyNTA was released in order to open the door to collaboration. However, there is still a long way for it to become a stable product. The features that PyNTA needs to implement in order to become more complete are:

* Load saved data and analyze it
* Produce reports for less technical users
* Implement extra parameters for linking locations
* Improve visualization of linking status (i.e. show tracks faster in order to make better decisions)
* Improve results by adding the Walker algorithm
* Systematize the publisher/subscriber pattern to make it clearer for later developers
* Explore pyMPI as a possible message exchanging approach
* Simplify serialization/deserialization in order to speed up communication
* Think about a zero-copy numpy exchange of arrays

Possible Roadmap
----------------
There are different options that can sprout out of PyNTA. For example, developing a framework to perform experiments with a common pattern of subscribers and publishers. With the experience gained in PyNTA, there is a clear path for abstracting common functions. Moreover, pyZMQ opens the door to a very interesting approach that would allow running the experiment completely independent from the GUI. This would prevent problems if the GUI crashes, for example. Moreover one could think about having GUI's for different platforms that run on the same hardware. For example, an app on the phone could control the experiment in the same way that a user sitting on the computer in the lab.

Getting PyNTA
-------------
If you are intrigued by PyNTA, you can install it by simply running:

.. code-block:: bash

    pip install pynta

And you can start it by running:

.. code-block:: bash

    pynta

The documentation is available `on Github <https://nanoepics.github.io/pynta/>`_. It is still a work in progress, but it is already quite complete. The code is in `this repository <https://github.com/nanoepics/pynta>`_.