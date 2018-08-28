Step by Step Guide to Building a GUI
=====================================

:status: draft
:date: 2018-08-27
:author: Aquiles Carattino
:subtitle: Using PyQt to build a GUI to your webcam
:header: {attach}yeo-khee-793533-unsplash.jpg
:tags: Data, Types, Mutable, Immutable, Tuples
:description: Using PyQt to build a GUI to your webcam

You may find a lot of tutorials online on how to use Python for different tasks, but it is very hard to find a complete guide on how to build a desktop application using Python. In this tutorial we are going to build a Graphical User Interface (GUI) to acquire images from your webcam. We are going to use OpenCV to quickly acquire an image from your camera and PyQt5 to build the user interface.

Building GUI's is not complicated, what makes them complex are the considerations you have to make when you allow a user to randomly interact with your program. For instance, imagine that your program allows the user to choose the camera they want to use and then acquire an image. You have to consider what would happen if the user first tries to acquire an image. And this is only the tip of the iceberg.

.. contents::

Installing OpenCV and PyQt5
---------------------------
The project is to build a user interface for your webcam. In order to do it, we are going to need two main libraries: **OpenCV** will be responsible for the acquisition, while **PyQt5** is the framework we are using for the interface.

OpenCV is a very big package that can be used with different programming languages. It can handle all sorts of image manipulations, including face-detection, object tracking, etc. In this tutorial we are not going to exploit all these possibilities, but you should be aware of the potential this library has. To install openCV, the simplest is to run the following command:

.. code-block:: bash

    pip install opencv-contrib-python

Remember that the best practice is to be working in a `virtual environment <{filename}03_Virtual_Environment.rst>`_ to avoid conflicts with other libraries, etc. The installation procedure should also install numpy. If you run into issues while installing OpenCV, you are free to `ask them in the forum <https://forum.pythonforthelab.com>`_ or you can check `the official documentation <https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_setup/py_table_of_contents_setup/py_table_of_contents_setup.html#py-table-of-content-setup>`_.

To check that OpenCV was properly installed and configured, you can start the Python interpreter and run the following commands to see what version do you have available:

.. code-block:: pycon

    >>> import cv2
    >>> cv2.__version__
    '3.4.2'

The next step is to install PyQt5, which will also require a single command:

.. code-block:: bash

    pip install PyQt5

Normally this procedure works, but PyQt5 can give some issues on some specific platforms. If you can't find solutions to your problems, the alternative option is to install `Anaconda <https://www.anaconda.com/download/#linux>`_ which will have all the packages already available on all the platforms.

To test whether PyQt5 is working, you can create a short script with the following:

.. code-block:: python

    from PyQt5.QtWidgets import QApplication, QMainWindow

    app = QApplication([])
    win = QMainWindow()
    win.show()
    app.exit(app.exec_())

If you run the file, a small, empty window should pop up. This means that everything is working correctly.

Finally, we need a library that will be able to show the images that we acquire with the webcam. There are several options to choose from. You can use **matplotlib**, which is a common tool for making plots, including 2D images. You can also use **Pillow**, which is a great tool for working with images in Python. A third option is to use **pyqtgraph**, a library that is not mainstream with normal Python developers, but that is used extensively in research labs.

Because of the background of this website, we are going to go for the third option: using PyQtGraph. On one hand, this will give visibility to an amazing project, spearheaded by `Luke Campagnola <https://www.alleninstitute.org/what-we-do/brain-science/about/team/staff-profiles/luke-campagnola/>`_. To install it, simply do the following:

.. code-block:: python

    pip install pyqtgraph

Now we are ready to develop the application.

Welcome to OpenCV
-----------------
When developing this kind of applications, the first step is to understand what do we want to do, before embarking into designing and developing a User Interface. OpenCV makes it very simple to read from a webcam attached to a computer, you simply do the following:

.. code-block:: python

    import cv2
    import numpy as np

    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()

    print(np.min(frame))
    print(np.max(frame))

In the first line we initialize the communication with the camera. Of course, if no cameras are attached, when you run the following command, ``cap.read()``, nothing will be acquired, but the program will not crash. Finally we release the camera. The last two lines are just printing the maximum and minimum values recorded by the camera. Bear in mind that ``frame`` is a numpy 2D-array.

To go one step forward, we can also acquire a video from the camera. The only difference with the code above is that we need to run an infinite loop, and in each iteration a new frame is acquired and displayed. To quit the application, you need to press ``Q`` on your keyboard. Note that we are also transforming the image to grayscale. You can remove that line and check how the image looks like.

.. code-block:: python

    import cv2

    cap = cv2.VideoCapture(0)


    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Our operations on the frame come here
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Display the resulting frame
        cv2.imshow('frame',gray)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

So, now we have a clear picture of how the acquistion process works. We have to start the communication with the camera and then we can read from it. There are some parameters that we can either change to the image itself, like transforming to black and white, or to the camera. For example, we could increase the brightness by adding the following right after ``VideoCapture``:

.. code-block:: python

    cap.set(cv2.CAP_PROP_BRIGHTNESS, 1)

Since you are setting the property to the camera itself, it won't disappear until you don't set it back to ``0.5``, even if you restart the program. You can check the `documentation on properties <https://docs.opencv.org/3.4/d4/d15/group__videoio__flags__base.html#gaeb8dd9c89c10a5c63c139bf7c4f5704d>`_ to see what are the possibilities. Remember that not all cameras support all the options, and therefore some errors can appear, or no visible changes at all.

To make a video you need to continuously acquire from the camera, in an infinite loop. We are not going to enter into the details now, but this can be a problem if your frames take long to acquire, for instance if you set longer exposure times.

Welcome to PyQt
---------------
Qt, similarly to OpenCV, is a general library, written in C++ and available for a lot of platforms. PyQt are python bindings to Qt, i.e. a translation of the original code to objects that can be used from within Python. The main difficulty of working with Qt comes from the fact that a lot of the available documentation is not available for the Python bindings but for the original code. This implies that the user has to make a translation from one language to another. Once you get used to it, it just works fine, but takes time to learn.

.. note:: There are a different set of bindings available for Python, called PySide2. They are the officially released bindings by Qt and, for practical matters, they work exactly the same. The main difference is the license under which they are released. If you are concerned about releasing your code, you should check the options.

A user interface consists of an infinite loop in which the windows are drawn, the user interaction is grabbed, images from the webcam are displayed, etc. If the loop is broken, the application finishes, closing all the windows. So, let's get started with a simple window:

.. code-block:: python

    from PyQt5.QtWidgets import QApplication, QMainWindow

    app = QApplication([])
    win = QMainWindow()
    win.show()
    app.exit(app.exec_())

In this case, the infinite loop is given by ``app.exec_()``. If you remove that line, you will see that the program runs, but nothing actually happens. Placing the loop inside the ``app.exit()`` is a way of guaranteeing that the application is properly closed when the loop stops running. It is important to note that before defining any windows, you should always define the application in which they are going to run. If you alter the order, you will get a quite descriptive error:

.. code-block:: bash

    QWidget: Must construct a QApplication before a QWidget
    Aborted (core dumped)

In PyQt (or Qt in general) the building blocks of windows are called Widgets. A window is a widget, a button, dialog, image, icon, etc. You can even define your own custom widgets. In the code above, you see that there is only an empty window appearing, not too exiting. Let's add a button to the window:

.. code-block:: python

    from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton

    app = QApplication([])
    win = QMainWindow()
    button = QPushButton('Test')
    win.setCentralWidget(button)
    win.show()
    app.exit(app.exec_())

Buttons are called ``QPushButton``. Parts of the code are always the same, like the creation of the app, or the execution of the loop. When we create a push button, we define also the text that the button will have. To add the button to the window there are different options. In this case, since we defined the window as a  ``QMainWindow``, we can set the button as its central widget. Main windows work only if a central widget is defined in them. The window looks like this:

.. image:: /images/22_images/01_main_window.png
    :alt: Main window with a button
    :class: center-img

It looks very silly, but it is a very good start. The last remaining thing would be to do something when the button is pressed. In order to trigger something by a button press, you have to understand what *Signals and Slots* are in the context of Qt.

Signals and Slots in Qt
-----------------------

When you develop complex applications, such as one with a user interface, you may want to trigger different actions under specific conditions. For example, you may want to send an e-mail to the user saying that the webcam finished acquiring a movie. However, you may want later to also add the possibility of saving the video to the hard drive, or publishing it to Youtube. Later, you decide that you would also like to save the video when a user presses a button, or publishing to Youtube when the computer receives an e-mail.

A very convenient way of developing a program in which you can trigger actions at specific events would be if you could subscribe functions to signals that are generated at certain moments. Once the video is acquired, the program can emmit a message, which will be catch by all its subscribers. In this way you can write your code for acquiring a video once, but what happens when the video finishes can be easily changed.

From the other side, you can write the function to save the video once, and trigger it either when the video finishes or when a user presses a button, etc. The main thing to realize when developing user interfaces is that you don't know when things are going to happen. It may be that the user first acquires an image and then makes a video. It may be that the user doesn't acquire a video and tries to save the data, etc. Therefore, it is very handy to be able to trigger actions on specific events.

In Qt, the whole idea of triggering actions with certain events is defined with *Signals*, which get triggered at specific moments and *Slots*, which are the actions that will be executed. With the button that we have defined, an action, or *signal*, could be its pressing. The event is whatever function we want it to be, for example, we will print to the terminal a message:

.. code-block:: python
    :hl_lines: 9

    from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton

    def button_pressed():
        print('Button Pressed')

    app = QApplication([])
    win = QMainWindow()
    button = QPushButton('Test')
    button.clicked.connect(button_pressed)
    win.setCentralWidget(button)
    win.show()
    app.exit(app.exec_())

Notice that we first define the function, in this case ``button_pressed``. The real magic happens in the highlighted line. The signal that we want to use is ``clicked``, and we connect that signal to ``button_pressed`` (note that we don't add the ``()`` in this line). If you run the program again and you press the button, you will se a message appearing on the terminal.

To continue on the same line of what it was discussed above, you could define a new function that gets triggered whenever the button is pressed. You will end up with something like this (I have removed the parts that are common to keep the example short):

.. code-block:: python

    def button_pressed():
        print('Button Pressed')

    def new_button_pressed():
        print('Another function')

    button.clicked.connect(button_pressed)
    button.clicked.connect(new_button_pressed)

If you run the program again, you will see that every time you press the button, two messages appear on the terminal. Of course you could have used functions that you import from different packages. The last bit in order to provide a complete example is to add a second button and connect its ``clicked`` signal to ``button_pressed``.

Adding a new widget to a Main Window requires some extra steps. As we have discussed earlier, every main window requires one (and only one) central widget. Since we want to add two buttons, the best would be to define an empty widget that will hold those two buttons. In turn, that widget will become the central widget of the window.

.. code-block:: python

    from PyQt5.QtWidgets import QApplication, QMainWindow, \
        QPushButton, QVBoxLayout, QWidget

    app = QApplication([])
    win = QMainWindow()
    central_widget = QWidget()
    button = QPushButton('Test')
    button2 = QPushButton('Second Test')

In order to make the window look organized, we will add a layout.