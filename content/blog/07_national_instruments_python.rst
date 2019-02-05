Controlling a National Instruments Card with Python
===================================================

:date: 2018-02-21
:author: Aquiles Carattino
:subtitle: Don't depend on Labview; learn how to control National Instruments cards directly with Python.
:header: {attach}writing-machine.jpg
:tags: National Instruments, DAQ, Control, NI DAQ, PyDAQmx
:description: Don't depend on Labview; learn how to control National Instruments cards directly with Python.

One of the most common devices in a lab is a National Instruments acquisition card, also called a DAQ. As you probably know by now, the default programming environment for such cards is Lab View, but what you may not be aware is that there are libraries for interfacing with other languages. NI provides a common driver to all of their devices called *NI-DAQmx* and how to use their hardware through the C programming language is `well documented <http://zone.ni.com/reference/en-XX/help/370471AA-01/>`_.

Once there is good documentation for one programming language, there are no limits for developers to expand the toolbox into other languages. For National Instruments devices, there is a project called `PyDAQmx <https://pythonhosted.org/PyDAQmx/>`_ that ported all the functions to be Python compatible. Since it is a port of the C code, what you should always bear in mind is that you have to check the `National Instruments documentation <http://zone.ni.com/reference/en-XX/help/370471AA-01/>`_ and adapt the code to Python.

.. note:: since the writing of this article, a new Python package supporting NI-DAQmx was released by National Instruments itself. You can see the `documentation here <https://nidaqmx-python.readthedocs.io/en/latest/>`_. I didn't have time to test it yet, but looks very promising. Keep an eye on the `bugs and issues <https://github.com/ni/nidaqmx-python/issues>`_ because they may be a good source of information.

Let's see how to get started. Remember that each card has different specifications and therefore some of the options may not be present in your current configuration. Let's assume we want to read an analog input from our device; you need to know the number that was assigned to your card in order to communicate with it; normally you should have National Instruments software that allows you to configure the number of your card.

.. code-block:: python

   import PyDAQmx as nidaq


   t = nidaq.Task()
   t.CreateAIVoltageChan("Dev1/ai0", None, nidaq.DAQmx_Val_Diff, 0, 10, nidaq.DAQmx_Val_Volts, None)
   t.CfgSampClkTiming("", 1000, nidaq.DAQmx_Val_Rising, nidaq.DAQmx_Val_FiniteSamps, 5000)
   t.StartTask()

In these few lines of code we have created a new Task and called it ``t``; we have defined an analog input channel for ``Dev1`` and port number ``ai0``. We also configured the timing to be internal, with 1000 samples per second and in total, we want to acquire 5000 samples. We finally trigger the task to start acquiring samples. It is interesting to compare our code to what is documented, so you can learn how to adapt the code to Python.

We first go to the documentation of the method `CreateAIVoltageChan <http://zone.ni.com/reference/en-XX/help/370471AA-01/daqmxcfunc/daqmxcreateaivoltagechan/>`_ and the first thing you should notice is that the name is actually different; it is **DAQmxCreateAIVoltageChan**. The first thing to note is that the *DAQmx* prefix is dropped in PyDAQmx. Then we can see the arguments that the function takes:

.. code-block:: c

   int32 DAQmxCreateAIVoltageChan (
      TaskHandle taskHandle,
      const char physicalChannel[],
      const char nameToAssignToChannel[],
      int32 terminalConfig,
      float64 minVal,
      float64 maxVal,
      int32 units,
      const char customScaleName[]);

Since we are using the task as Python object, we drop the first argument of the function; PyDAQmx takes care of it (notice that we are using the syntax ``t.CreateAIVoltageChan``. Then we have to pass all the other arguments, paying attention to their types. So, where it says ``char`` we should pass a ``String``; that is what we do for the channel. In this example, we don't assign a name to the channel and therefore we leave it as ``None``. Next, we have to define the ``terminalConfig``; if you look at the documentation, you will see that there are different options, for example ``DAQmx_Val_RSE``, ``DAQmx_Val_Diff``, etc. PyDAQmx has all these configurations already defined and we can use them directly as in the example above: ``nidaq.DAQmx_Val_Diff``.

Then it asks for the limits of our analog input; remember that the DAQmx works with units that can be different from volts and that will be defined later on; the limits that we establish here are in those specific units. Setting the limits allows the DAQ card to automatically set a gain to our measurement, therefore increasing the effective resolution of the measurement. The values are automatically converted to the requested type, provided that they are numbers.

.. newsletter::

When performing a measurement with an NI Card we have to explicitly set its units; it may very well be that you have a thermocouple connected to the analog input and therefore you want to measure Kelvins instead of Volts, or that you have any other transducer plugged. Defining custom scales is an entire chapter and therefore it is much easier to leave them here as volts and do the transformation directly in our code. We use again a built-in option of DAQmx, the ``nidaq.DAQmx_Val_Volts`` and the last option is left to ``None`` because it is what the documentation asks for in case we set the scale to Volts.

.. note:: Converting variable types from Python to C or the other way around is handled in different ways by different libraries. PyDAQmx is doing all the work under to hood and that is why we can use an integer instead of a float, for example. But be aware that it will not always be the same; some libraries require to define very specific types.

The other method, `CfgSampClkTiming <http://zone.ni.com/reference/en-XX/help/370471AA-01/daqmxcfunc/daqmxcfgsampclktiming/>`_ is used for configuring the clock used to acquire the samples. I leave it up to you to check the documentation and to understand what each argument of the function is doing. In short, I set it to use an internal clock at a rate of 1000 samples per second for a total of 5000 samples (i.e. 5 seconds total acquisition time). The last line simply triggers the task.

The next step is to read the data that was acquired. Remember that it takes 5 seconds for the acquisition to complete; the DAQmx functions are non-blocking, meaning that the execution of your program will not halt at each execution. For reading from the card we will use another method defined within the Task object; you will also need to use numpy for this example to work.

.. code-block:: python

   import numpy as np

   [...]

   data = np.zeros((5000,), dtype=np.float64)
   read = nidaq.int32()
   t.ReadAnalogF64(5000, 5, nidaq.DAQmx_Val_GroupByChannel,
      data, len(data), nidaq.byref(read), None)

Reading from the NI DAQ has a structure more similar to how proper C code looks like and is quite different from how Python code works. The first thing to note is that there is no return; we are not doing anything like ``data = t.ReadAnalogF64()``. Let's see it step by step. The `documentation <http://zone.ni.com/reference/en-XX/help/370471AA-01/daqmxcfunc/daqmxreadanalogf64/>`_ is useful but doesn't explain how the actual syntax works. Again, we skip the first argument, the ``task handler`` because we are using the object-oriented-style.

We define how many data points *per channel* we want to read; if we were acquiring more than one channel, it is important to notice that it is not the total number of points. We set the timeout in seconds, in order for the function to stop waiting in case there are not enough data points available. Then we set how to group the values in case we are reading from more than one channel. Remember that each channel is read sequentially, so it would be Chan1_1 -> Chan2_1 -> Chan3_1 -> Chan1_2 -> Chan2_2 -> Chan3_2 -> Chan1_3 -> etc. If we group them by channel, they will be returned as all the measurements from Chan1, all the measurements from Chan2, etc. I prefer it this way because it works well with numpy's reshape.

Now, the interesting part; we pass as an argument ``data``, which was defined few lines before as an empty numpy array. In the documentation, it is defined as `The array to read samples into`. This is a very common way of working with functions in C; we first create the memory structure that will hold the output of the function, in this case, a numpy array with 5000 elements. Whatever is present in the array will be overwritten by the read function. The next argument is the `actual number of samples read from each channel`; in other words, the length of the data array.

The final argument is the ``read`` integer, that was also defined few lines before. It will hold the total number of data points read per channel. Note that we are not simply passing the read integer as an argument to the function, but we are using a method called ``byref``. This is typical when working with external libraries written in C. It basically means that you are passing the reference to an object and not the object itself; you are letting the function know where in the memory is located that specific variable. In the end, the effect is the same: the variable will hold the information you need.

Now you can plot your ``data``, save it or do whatever you like with it. The read function has a lot of options that I haven't fully covered, but that you can easily check the documentation. The complexity arises because the function covers a lot of different scenarios with few inputs. For example, when you are continuously acquiring and you wish to download as many data points as there are available but you cannot know beforehand how many. It can also take care when you use an external trigger and you don't know how long it will take to complete an acquisition.

Even though National Instruments cards were not designed to be used with Python, there can still be used in a variety of projects without many complications. The use of a common API for all the cards makes them ideal because exchanging them doesn't require a single change in the code. However, each card can have very different capabilities, for example, the acquisition rate or the number of simultaneous tasks that it can handle.

More Information: `PyDAQmx Tutorial <https://pythonhosted.org/PyDAQmx/usage.html>`_, `NI-DAQmx C Reference Help <http://zone.ni.com/reference/en-XX/help/370471AA-01/>`_