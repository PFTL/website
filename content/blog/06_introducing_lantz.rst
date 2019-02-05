How to Write a Driver with Lantz
================================

:date: 2018-02-23
:author: Aquiles Carattino
:subtitle: Simplifying the task of writing new drivers thanks to a lot of built-in features
:header: {attach}toolbox.jpg
:tags: Lantz, Beginner, Drivers, Devices
:description: Writing your own drivers is easy thanks to Lantz, a Python package that handles different communication standards, limits, and even units.

Lantz is a package written by several researchers who wanted to have a framework to build instrumentation on Python. It is open source and hosted `on Github <https://github.com/LabPy/lantz>`_. Their description is very clear:

   Lantz is an automation and instrumentation toolkit with a clean, well-designed and consistent interface. It provides a core of commonly used functionalities for building applications that communicate with scientific instruments allowing rapid application prototyping, development and testing. Lantz benefits from Python's extensive library flexibility as a glue language to wrap existing drivers and DLLs.

Lantz was built with one objective in mind: make easier to researchers the development of drivers for their devices. With time the Lantz group has built an entire framework that handles different types of connections, such as GPIB, Serial, Ethernet, etc. and much more. The values generated are kept in a cache that prevents unnecessary communications with the devices. Plus, the syntax is simple and allows to check for limits and units before sending commands to the real device.

Let's see step by step how to build a driver for a common device, for instance, a `Tektronics Oscilloscope <https://www.tek.com/oscilloscope/tds1000-manual>`_. The first thing we need to do is to import the needed modules from Lantz.

.. code-block:: python

   from lantz.feat import Feat
   from lantz.action import Action
   from lantz.messagebased import MessageBasedDriver

We will see how to use each one of them. We first define the class:

.. code-block:: python

   class TDS1012(MessageBasedDriver):

   MANUFACTURER_ID = '0x699'
   DEFAULTS = {'USB': {'write_termination': '\n',
                           'read_termination': '\n',
                           'timeout': 5000,
                           'encoding': 'ascii'
               }}

We inherit from the general ``MessageBasedDriver`` because the Oscilloscope communicates through an exchange of text commands. We define the `Manufacturer Id` because it is one of the easiest ways of identifying USB devices. Beware that if there were two different Tektronix devices connected, the program will not be able to differentiate between them, you should provide more information as I will show below.

The second important step is to define the defaults for the communications. In this case, we are setting the defaults for a USB communication. The write and read terminations are the new line character and we set the encoding to `ascii`; all this information can be found in the manual. We set the timeout to 5 seconds; if a command takes longer than that to execute it will stop it.

Now we are ready to start developing some more interesting code for our driver. Normally, one of the first commands we can exchange with a device is to ask for its identification. We can achieve it like so:

.. code-block:: python

   @Feat()
   def idn(self):
      return self.query('*IDN?')

Now we see the use of the first decorator, called ``Feat``. Decorators in Python are complex, but they can be described mainly as functions that take as arguments other functions. When we use the ``Feat`` decorator a lot of things are going to happen internally in Lantz, but we shouldn't worry too much for the time being. What you should remember is that Features are all those elements in a device that will return a value or that can be set to a value. The identification of the oscilloscope is one of such features. Now we can already use the class:

.. code-block:: python

   with TDS1012.via_usb() as osc:
      print(os.idn)

And now we see the magic of Lantz happening. First, the fact that we can use the ``with`` statement means that some methods were defined for us under the hood; these methods are in charge of initializing and finalizing the communication with the device, in order to free the resource right after the statement finishes. The second important thing to notice is that we initialize the device with the ``via_usb()`` method. Of course, it could have been ``via_serial()``, for example, but let's keep with the USB for now.

.. newsletter::

The second important thing to note is that the method ``idn`` is treated as a property of the device itself. This is achieved through the ``Feat`` decorator. If you are an experienced Python programmer you probably know how to achieve this behavior for your own classes; in Lantz, you shouldn't worry too much about understanding it, but you have to learn just how to use them.

Now, imagine you want to trigger the device; that doesn't count as a Feature because you are not setting a specific value nor getting a value. That is the situation where you would use an ``Action`` decorator:

.. code-block:: python

   @Action()
   def trigger(self):
      self.write('*TRG')

In this case, we are only writing to the oscilloscope and therefore we are not awaiting any output value after the action. ``Action`` decorators don't have much magic behind; they can be thought as the buttons on a device; a button is pressed and an action is triggered.

We have so far only discussed a passive ``Feat``, or better called, a *read-only* only feature. But what happens when we have a feature that actually accepts values; the oscilloscope, for example, can be set to acquire one of two different channels. First, we define the *feature* to read which channel is going to be read, in exactly the same way than for the ``idn`` feature.

.. code-block:: python

   @Feat(limits=(1,2))
   def datasource(self):
      return self.query('DAT:SOU?')

The first difference to note here is that we have added limits to the feature, in this case, the value it will output will be in the range from 1 to 2 (1 and 2 included). While reading from a device it is not important to know the limits, but when we write, it becomes crucial. The way of setting the value of the data source is like this:

.. code-block:: python

   @datasource.setter
   def datasource(self,value):
      self.write('DAT:SOU CH{}'.format(value))

Again, if you have ever worked with properties of classes the syntax may result familiar, but if you haven't don't worry too much. Once we have defined the method ``datasource`` as a ``Feat``, we can change its value by defining a ``setter``. Now, pay attention here, the decorator we use is ``@datasource.setter``, because the function that comes after is exactly that, instructions on how to set the ``datasource`` feature. The method defined right after is the function that is going to be called when we do something like:

.. code-block:: python

   dev.datasource = 1
   print(dev.datasource)
   dev.datasource = 2
   print(dev.datasource)
   dev.datasource = 3 # This will raise an Exception

Note that it takes one argument, value. The value will be first checked against the limits we established in the ``Feat`` declaration, i.e. it should be between 1 and 2. That is why if you try to assign the value 3 to it, it will fail. Because of how we did things, if you send the value 1.5 to the datasource, it won't fail, but it is not a valid command.

Using Units
^^^^^^^^^^^
One of the most useful utilities of Lantz is the built-in units. The oscilloscope doesn't provide a lot of good opportunities to work with units but trust me when you are working with other devices they are going to be very handy. When you are reviewing old code it is always hard to remember if the values should be set in nanometers, centimeters and sometimes you don't want to dig up the manual from an obscure website or cupboard in your lab. Let's imagine we have a tunable laser, and we want to set the output wavelength to it. Our code would become:

.. code-block:: python

   @Feat(units='nm', limits=(1480, 1640, 0.0001))
   def wavelength(self):
      return self.query('WA')

   @wavelength.setter
   def wavelength(self, value):
      self.query('WA%.4f' % value)

We begin by declaring a feature, with units nanometers and some limits. Importantly, we set the step at which we can change the wavelength: 0.1pm. Now, the wavelength setter looks exactly the same as with the oscilloscope. All the magic is going to happen thanks to the ``Feat`` decorator at the beginning, converting to the proper units before actually sending the command to the device. To use it, you can just do:

.. code-block:: python

   from lantz import Q_

   wl = Q_('1500nm')
   dev.wavelength = wl
   print(dev.wavelength)
   wl = 1510
   dev.wavelength = wl
   print(dev.wavelength)
   um = Q_('um')
   wl = 1.520*um
   dev.wavelength = wl
   print(dev.wavelength)
   wrong = Q_('1500V')
   dev.wavelength = wrong

The first thing we have to do is to import the module `Quantity` directly from Lantz, which is basically the unit registry from Pint; if this is the first time you hear about Pint, I really suggest that you check out `that project <http://pint.readthedocs.io/en/latest/>`_. We then define a variable ``wl`` as a 1500nm quantity and set the laser wavelength to it. The rest of the commands are just to test the different scenarios; for example, when you don't specify units, Lantz will automatically assume the default units (the ones you set in the ``@Feat``). You can, of course, use other units; I've chosen micrometers, but anything that is distance-related would have just worked fine. You could have even used inches. Of course, the program will raise an Exception if you try to pass the wrong units to the wavelength.

The advantage of using units so early in the code (at driver development) is that it will make it clear for the rest of our programs what units are we supposed to use. We don't need to worry about a user (or even ourselves) confusing nanometers with micrometers, the conversion will happen under the hood. In my experience, however, few people are used to the Pint package and get slightly confused when they have to work with a new type of variable that has both a number and a unit. Anyways, a bit of practice doesn't heart.

Conclusions
^^^^^^^^^^^
Lantz has seen a rollercoaster of development cycles, from very active to almost abandoned. Lately, it has been hibernating, as you can see by the number of merge requests and issues open that no one has replied to. In any case, the package works reasonably well, but what is more important is that you can learn a lot from their ideas. The use of decorators for communicating with devices, for example, is a great way of simplifying a lot of actions, like checking the limits and the units.

I try to implement the new drivers that I write in Lantz, but I am also realistic and know that for some devices it is better not to depend on it, especially when dealing with very complex systems such as cameras. If you want to explore more I suggest you check also:

   * `Instrumental, from Mabuchi Lab <http://instrumental-lib.readthedocs.io/en/stable/>`_.
   * `Storm Control, from Zhuang Lab <https://github.com/ZhuangLab/storm-control>`_.
   * `Experimentor, by Uetke <https://github.com/uetke/experimentor/tree/develop>`_.


Header photo by `Philip Swinburn <https://unsplash.com/@pjswinburn>`_ on Unsplash