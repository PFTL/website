How to Control a Device Through the Network
===========================================

:date: 2018-02-28
:author: Aquiles Carattino
:subtitle: Exchange information and trigger measurements with devices connected to separate computers
:header: {attach}network_cables.jpg
:tags: Network, Communication, Async, Remote Control, Devices, Drivers, Flask, Internet
:description: Step by step tutorial on how to exchange information with a device through the network

In the lab, it is common to find different computers connected to specific devices. For example,when you keep older PCs which are able to communicate with very specific hardware. You may also have different computers when there are mobile instruments that you share among different users. In these situations it becomes very useful to be able to exchange information between your main computer and a secondary one.

A computer network utilizes two elements: a server and a client. The server receives the messages you send, interprets them and returns values if asked to. The client communicates with the server, sends commands and receives data. Internet works this way: when you entered this website, you used a browser, the client, to access content on a server. Communicating with a device connected to another computer is, therefore, not different from what we have just described. 

If you look around for Python frameworks to build web applications, you will find several but two are going to stand out: `Django <https://www.djangoproject.com/>`_ and `Flask <http://flask.pocoo.org/>`_. Django is a complete package for developing web applications, but a total overkill for our purposes. Flask is slightly more barebones, but it provides all the functionality that we are looking for: to create a server that will take inbound communication and act accordingly, for example by triggering a measurement on a device.

Installing Flask doesn't take much more than a pip command:

.. code-block:: bash

   pip install Flask

After that we can build our first very simple app to see that everything is working fine:

.. code-block:: python

   from flask import Flask
   app = Flask(__name__)

   @app.route('/')
   def index():
      return "The Server is up and running"

   app.run()

If you run the file, open a browser, and head to ``localhost:5000`` you will see a message saying that the server is up and running. A lot of things are happening that are worth discussing in detail. We start by importing Flask and creating an ``app``. Our app is very powerful; one of the things it allows us to do is to trigger specific functions when we head to specific locations on the server. These are called ``routes``; when we define a route and we add the string ``'/'`` it means that the function following it will be triggered whenever someone enters to the root of the server (``/``). Our example only returns a message saying that everything went well.

The last line runs the app. This is an infinite loop that will open a port at localhost for us to test our application. If you are familiar with how PyQt works, you will notice the similarities. Once the app is running, you can point the browser to the address that appears on your command line, most likely ``localhost:5000``. When you enter to that address, you are triggering the ``route('/')`` and therefore you will get the message ``The Server is up and running``.

So far, both the server and the client are the same device. We will see later how to improve on this, but for the time being, you can believe that everything will work exactly the same, even when communicating through the network. It is possible to trigger other actions directly on the server side, not only to return strings. To test it, we can use a ``print`` statement. Let's re-write the ``index()`` function:

.. code-block:: python

   [...]

   def index():
      print('Index Triggered')
      return 'The server is up, running, and printing statements'

   [...]

If you run the server file again and head your browser to ``localhost:5000`` you should see not only the string appearing on your screen, but also a message will appear on the command line where the server is running. The ``print`` function is being triggered on the server. We could use more complex functions than ``print``. For example, we could trigger a measurement on a device.

.. note:: If you are not dealing with instruments but you would like to trigger computer-intensive tasks on a remote computer, you can use the same approach explained here. You can then leverage computers with more memory or better processors, or you can even make a parallel execution of your code without leaving your Jupyter notebook.

Let's assume you have a device like the one we developed in our earlier post `How to Write a Driver with Lantz <{filename}06_introducing_lantz.rst>`_. The device is an oscilloscope with several built-in methods, including ``idn`` for getting its serial number, and ``datasource`` to set and get the channel used for an acquisition.  We would like to trigger some of those methods when we head to specific addresses on our browser. Later on, we will change the browser by a custom-made client that will simplify our workflow. We begin by initializing the device and we make it available to the app:

.. code-block:: python
   :hl_lines: 2, 4

   from flask import Flask
   from devices import my_device

   dev = my_device.via_usb()

   app = Flask(__name__)

   @app.route('/idn')
   def idn():
      return dev.idn

   app.run()

The core is the same as before, but we have added some lines for the device. We import the needed classes and we initialize the communication with the device; you should adapt the highlighted lines with your own device. The new route now establishes that if you head to ``localhost:5000/idn``, the serial number of the device is going to be returned. This action is much more complex than printing on the server or returning a simple string. What we are actually sending is a command to a device, waiting for it to return a value and then we are sending it back to the browser. With this simple example, you can already see that we are doing virtually everything that a device can handle. Of course, devices also take inputs, and we should take into account this. Basing ourselves on the example of an `oscilloscope with Lantz <{filename}06_introducing_lantz.rst>`_, we could change the datasource property of the device like this:

.. code-block:: python

   [...]
   @app.route("/datasource/<int:source_id>")
   def datasource(source_id):
      dev.datasource = source_id
      return(dev.datasource)

The lines above show a very simple way of sending variables through a browser. The ``route`` takes more complex structures than plain strings. ``<int:source_id>`` will take an integer after the ``datasource/`` and it will pass it as an argument to the function below. The function ``datasource`` in our server, therefore, should take exactly one argument, ``source_id``, and we use it for changing the ``datasource`` of the device. Now, if you head your browser to ``localhost:5000/datasource/1`` we will change the source to `1`, we can do the same with `2`, `3`, etc. Bear in mind that not all values are valid with the device. Check what happens if, for example, you send a value outside the range of what is possible.

.. newsletter::

Communicating with our devices through the browser may not be the most practical approach. Instead, we can build a special program called `Client` that will handle the sending and retrieving of information from the server. When we have control on both the server and the client side software, we can easily control the data that is being exchanged. When we don't have control over one of the two sides, we have to base ourselves on available standards; for example, the data that a browser can handle is limited, the instructions a server can receive are few, etc. We are going to base our client on a common Python library called ``requests``:

.. code-block:: python

   import requests

   addr = 'http://localhost:5000'
   r = requests.get(addr + "/idn")

   print(r.content)

If you run the script written above (while the server script is running on a different command line), you will see that what gets printed on screen is the identification of the device. Basically, what you have achieved is the exchange of information from a device hooked to a server with a client not directly bound to that device. You could build a class around the requests. If you want, for example, a client exclusively for the oscilloscope, we can do the following:

.. code-block:: python

   import requests


   def ClientOscilloscope():
      def __init__(self, addr):
         self.addr = addr

      def idn(self):
         r = requests.get(self.addr + '/idn')
         return r.content

   if __name__ == '__main__':
      c = ClientOscilloscope('http://localhost:5000')
      print(c.idn())

The applications of this approach are multiple and not limited to communicating over the network. Imagine that you want to share the information of a device with multiple applications; instead of initializing the communication with the device in each application (that will almost certainly lead to issues), you can communicate through a server, even if on the same computer. You can test this idea if you access ``localhost`` from two different browsers. You can get the ``idn`` of your device twice without issues. You can also run the client script from two different command lines, and you will see that your server can handle several requests at the same time without issues and without blocking the device; the communication is initialized only once, at the beginning of the server script.

Being able to access the server from a different computer depends on the configuration of your network. First, you need to know the ``ip`` address of your computer. Remember that an ip is a unique number that identifies your connection to a network; if you are connected to the Internet, you will have two different numbers, the ip of your computer within a local network, and the public ip that is going to be shared by all the other computers on the same network.

Let's assume that you want to control a device within a local network in your lab. The only thing you need to do is to run the server on the computer you wish to use; most likely you are going to desire a specific port number for the inbound communication. You can do so with this simple command:

.. code-block:: python

   app.run('0.0.0.0', 1234)

which will allow you to run the server on port 1234. You have to check that the port is not used by other processes; for example, port 80 is used by HTTP connections. You can aim for higher numbers like 10000 and above, since those are most likely not used and open within your network. If you now head the browser of another device to ``ip:1234/idn`` you should see the identification number of your device. This procedure is mobile-friendly; you could use your phone to trigger measurements, without developing any apps, just using your mobile browser.

Accessing a computer from outside the local network is possible, but it normally depends on the policy of the institution where you work. The easiest way is to have port forwarding, for example when you access ``public_ip:specific_port``, the connection is forwarded to a specific computer within the local network. To configure it, you need help from the administrator of the network and as a general safety rule, they will never allow such a thing. If you make a mistake, you are giving access to anyone who finds out which port to use.

The possibilities are limitless. If you want to see how to configure a more complex Server/Client strategy that handles any number of devices, you can check `Uetke's Instrument Server <https://github.com/uetke/UUServer>`_. In this project, the server is an extension of Flask; we have defined some common routes to communicate with clients. We have also made use of ``JSON`` as a way of exchanging structured information between client and server. The repository also includes a client and a fake instrument to test the behavior.

The examples we have shown above are very basic but important to understand, if you want to achieve more complex functionality. For example, if you want the server to stay responsive while triggering tasks that take long to execute on a device, you have to implement threads. That is a more extensive discussion than what we can have here, but you can find an implementation example `here <https://github.com/uetke/UUServer/blob/master/instserver/server.py>`_. There are some other packages that can be used for threading on web servers. Those packages were created precisely to handle async tasks. They are aimed at web development but could be useful also for applications with experiments. You can check for example, `Celery <http://docs.celeryproject.org/en/latest/>`_ and `RabbitMQ <https://www.rabbitmq.com>`_, although they are fairly complex, they can be exactly what you are looking for.

If you need help developing a code for communicating over the network, don't hesitate to `contact us <https://www.uetke.com/contact>`_. We can custom build a solution to your problem. If you would like to learn about network communication and much more, you can also consider our `Advanced Python For The Lab Course <https://www.uetke.com/courses/advanced/>`_.

Header photo by `John Carlisle <https://unsplash.com/photos/l090uFWoPaI?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText>`_ on Unsplash
