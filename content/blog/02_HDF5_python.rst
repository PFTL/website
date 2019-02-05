How to use HDF5 files in Python
===============================

:date: 2018-03-19
:author: Aquiles Carattino
:subtitle: HDF5 allows you to store large amounts of data efficiently
:header: {attach}samuel-zeller-118195-unsplash.jpg
:tags: HDF5, Python, Data, Data Storage, h5py
:description: Learn how to use the HDF5 format to store large amounts of data and read it back with Python

This article is part of a series of articles relating to data storage with Python. The other articles are:

* `Introduction to Storing Data in Files <{filename}13_storing_data.rst>`_
* `Storing Binary Data and Serializing <{filename}14_Storing_data_2.rst>`_
* `Using Databases to Store Data <{filename}15_Storing_data_3.rst>`_
* `Using HDF5 Files with Python <{filename}02_HDF5_python.rst>`_

When dealing with large amounts of data, either experimental or simulated, saving it to several text files is not very efficient.  Sometimes you need to access a very specific subset of data and you want to do it fast. In these situations, the HDF5 format solves both issues thanks to a very optimized underlying library. HDF5 is broadly used in scientific environments and has a great implementation in Python, designed to work with numpy out of the box.

The HDF5 format in principle supports files of any size, each file has an internal structure that allows you to search for a specific dataset. You can think of it as a single file with its own hierarchical structure, just like a collection of folders and subfolders. By default, the data is stored in binary format and the library is compatible with different data types. One of the most important options of the HDF5 format is that it allows attaching metadata to every element in the structure, making it ideal for generating self-contained files.

In Python, the interface with the HDF5 format can be achieved through a package called **h5py**. One of the most interesting features of the h5py package is that data is read from the file only when it is needed. Imagine you have a very large array that doesn't fit in your available RAM memory. You could have generated the array, for example, in a computer with different specifications than the one you are using to analyze the data. The HDF5 format allows you to choose which elements of the array to read with a syntax equivalent to numpy. You can then work with the data stored on a hard drive rather than in the RAM memory without much modifications to your existent code.

In this article, we are going to see how you can use **h5py** to store and retrieve data from a hard drive. We are going to discuss different ways of storing data and how to optimize the reading process. All the examples that appear in this article are also `available on our Github repository <https://github.com/uetke/website_content/tree/master/example_code/HDF_Examples>`_.

.. contents::

Installing
**********
The HDF5 format is supported by the `HDF Group <https://www.hdfgroup.org/>`_, and it is based on open source standards, meaning that your data will always be accessible, even if the group disappears. Support for Python is given through the `h5py package <https://www.h5py.org/>`_ that can be installed through ``pip``. Remember that you should be using a `virtual environment <{filename}03_Virtual_Environment.rst>`_ to perform tests:

.. code-block:: shell

   pip install h5py

the command will also install numpy in case you don't have it already in your environment.

If you are looking for a graphical tool to explore the contents of your HDF5 files, you can install the `HDF5 Viewer <https://support.hdfgroup.org/products/java/hdfview/>`_. It is written in Java so it should work on almost any computer.

Basic Saving and Reading Data
*****************************
Let's go straight to using the HDF5 library. We will create a new file and save a numpy random array to it.

.. code-block:: python

   import h5py
   import numpy as np

   arr = np.random.randn(1000)

   with h5py.File('random.hdf5', 'w') as f:
       dset = f.create_dataset("default", data=arr)

The first few lines are quite straightforward, we import the packages h5py and numpy and create an array with random values. We open a file called `random.hdf5` with write permission, ``w`` , which means that if there is already a file with the same name it is going to be overwritten. If you would like to preserve the file and still be able to write to it, you can open it with the ``a`` attribute instead of ``w``.  We create a `dataset` called ``default`` and we set the data as the random array created earlier. Datasets are holders of our data, basically the building blocks of the HDF5 format.

.. note:: If you are not familiar with the ``with`` statement, I shall say that it is a convenient way of opening and closing a file. Even if there is an error within the ``with``, the file is going to be closed. If for some reason you don't use the ``with``, never forget to add the command ``f.close()`` at the end. The with statement works with any kind of file, not necessarily an HDF file.

To read the data back, we can do it in a very similar way to when we read a numpy file:

.. code-block:: python

   with h5py.File('random.hdf5', 'r') as f:
      data = f['default']
      print(min(data))
      print(max(data))
      print(data[:15])

We open the file with a read attribute, ``r`` , and we recover the data by directly addressing the dataset called `default`. If you are opening a file and you are not sure which data sets are available, you can retrieve them:

.. code-block:: python

   for key in f.keys():
      print(key)

Once you have read the data set that you want, you can use it as you would use any numpy array. For example, you can check the maximum and minimum values in the array, or you can select the first 15 values of it. These simple examples, however, are hiding a lot of the things that happen under the hood and that need to be discussed in order to understand the full potential of HDF5.

In the example above, you can use ``data`` as an array. You can, for example, address the third element by typing ``data[2]``, or you could get a range of values with ``data[1:3]``. Note that ``data`` is not an array but a dataset. You can see it by typing ``print(type(data))``. Datasets work in a completely different way than arrays because their information is stored on the hard drive and they don't load it to RAM memory if we don't use them. The following code, for example, will not work:

.. code-block:: python

   f = h5py.File('random.hdf5', 'r')
   data = f['default']
   f.close()
   print(data[1])

The error that appears is a bit lengthy, but the last line is very helpful:

.. code-block:: shell

   ValueError: Not a dataset (not a dataset)

The error means that we are trying to access a dataset to which we have no longer access. It is a bit confusing, but this happens because we closed the file, and therefore we are no longer allowed to access the second value in data. When we assigned ``f['default']`` to the variable ``data`` we are not actually reading the data from the file, instead, we are generating a pointer to where the data is located on the hard drive. On the other hand, this code will work:

.. code-block:: python

   f = h5py.File('random.hdf5', 'r')
   data = f['default'][:]
   f.close()
   print(data[10])

If you pay attention, the only difference is that we added ``[:]`` after reading the dataset. Many other guides stop at these sort of examples, without ever really showing the full potential of the HDF5 format with the h5py package. Because of the examples that we did up to now, you could wonder why using HDF5, if saving numpy files gives you the same functionality. Let's dive into the specifics of the HDF5 format.

.. newsletter::

Selective Reading from HDF5 files
*********************************
So far we have seen that when we read a dataset we are not yet reading data from the disk, instead, we are creating a link to a specific location on the hard drive. We can see what happens if, for example, we explicitly read the first 10 elements of a dataset:

.. code-block:: python
   :hl_lines: 2

   with h5py.File('random.hdf5', 'r') as f:
      data_set = f['default']
      data = data_set[:10]

   print(data[1])
   print(data_set[1])

We are splitting the code into different lines to make it more explicit, but you can be more synthetic in your projects. In the lines above we first read the file, and we then read the `default` dataset. We assign the first 10 elements of the dataset to a variable called ``data``. After the file closes (when the ``with`` finishes), we can access the values stored in ``data``, but ``data_set`` will give an error. Note that we are only reading from the disk when we explicitly access the first 10 elements of the data set. If you print the type of ``data`` and of ``data_set`` you will see that they are actually different. The first is a **numpy array** while the second is an **h5py DataSet**.

The same behavior works in more complex scenarios. Let's create a new file, this time with two data sets, and let's select the elements of one based on the elements of the other. Let's start by creating a new file and storing data; that part is the easiest one:

.. code-block:: python

   import h5py
   import numpy as np

   arr1 = np.random.randn(10000)
   arr2 = np.random.randn(10000)

   with h5py.File('complex_read.hdf5', 'w') as f:
       f.create_dataset('array_1', data=arr1)
       f.create_dataset('array_2', data=arr2)

We have two datasets called ``array_1`` and ``array_2``, each has a random numpy array stored in it. We want to read the values of ``array_2`` that correspond to the elements where the values of ``array_1`` are positive. We can try to do something like this:

.. code-block:: python

   with h5py.File('complex_read.hdf5', 'r') as f:
       d1 = f['array_1']
       d2 = f['array_2']

       data = d2[d1>0]

but it will not work. ``d1`` is a dataset and can't be compared to an integer. The only way is to actually read the data from the disk and then compare it. Therefore, we will end up with something like this:

.. code-block:: python

   with h5py.File('complex_read.hdf5', 'r') as f:
       d1 = f['array_1']
       d2 = f['array_2']

       data = d2[d1[:]>0]

The first dataset, ``d1`` is completely loaded into memory when we do ``d1[:]``, but we grab only some elements from the second dataset ``d2``. If the ``d1`` dataset would have been too large to be loaded into memory all at once, we could have worked inside a loop.

.. code-block:: python

   with h5py.File('complex_read.hdf5', 'r') as f:
       d1 = f['array_1']
       d2 = f['array_2']

       data = []

       for i in range(len(d1)):
           if d1[i] > 0:
               data.append(d2[i])

   print('The length of data with a for loop: {}'.format(len(data)))

Of course, there are efficiency concerns regarding reading an array element by element and appending it to a list, but it is a very good example of one of the greatest advantages of using HDF5 over text or numpy files. Within the loop, we are loading into memory only one element. In our example, each element is just a number, but it could have been anything, from a text to an image or a video.

As always, depending on your application, you will have to decide if you want to read the entire array into memory or not. Sometimes you run simulations on a specific computer with loads of memory, but you don't have the same specifications in your laptop and you are forced to read chunks of your data. Remember that reading from a hard drive is relatively slow, especially if you are using HDD instead of SDD disks or even more if you are reading from a network drive.

Selective Writing to HDF5 Files
*******************************
In the examples above we have appended data to a data set as soon as this was created. For many applications, however, you need to save data while it is being generated. HDF5 allows you to save data in a very similar way to how you read it back. Let's see how to create an empty `dataset` and add some data to it.

.. code-block:: python

   arr = np.random.randn(100)

   with h5py.File('random.hdf5', 'w') as f:
      dset = f.create_dataset("default", (1000,))
      dset[10:20] = arr[50:60]

The first couple of lines are the same as before, with the exception of ``create_dataset``. We don't append data when creating it, we just create an empty dataset able to hold up to 1000 elements. With the same logic as before, when we read specific elements from the dataset, we are actually writing to disk only when we assign values to specific elements of the ``dset`` variable. In the example above we are assigning values just to a subset of the array, the indexes 10 to 19.

.. warning:: It is not entirely true that you write to disk when you assign values to a dataset. The precise moment depends on several factors, including the state of the operating system. If the program closes too early, it may happen that not everything was written. It is very important to always use the ``close()`` method, and in case you write in stages, you can also use ``flush()`` in order to force the writing. Using ``with`` prevents a lot of writing issues.

If you read the file back and print the first 20 values of the dataset, you will see that they are all zeros except for the indexes 10 to 19. There is a **common mistake** that can give you a lot of headaches. The following code will not save anything to disk:

.. code-block:: python

   arr = np.random.randn(1000)

   with h5py.File('random.hdf5', 'w') as f:
      dset = f.create_dataset("default", (1000,))
      dset = arr

This mistake always gives a lot of issues, because you won't realize that you are not saving anything until you try to read it back. The problem here is that you are not specifying where you want to store the data, you are just overwriting the ``dset`` variable with a numpy array. Since both the dataset and the array have the same length, you should have used ``dset[:] = arr``. This mistake happens more often than you think, and since it is technically not wrong, you won't see any errors printed to the terminal, but your data will be just zeros.

So far we have always worked with 1-dimensional arrays but we are not limited to them. For example, let's assume we want to use a 2D array, we can simply do:

.. code-block:: python

   dset = f.create_dataset('default', (500, 1024))

which will allow us to store data in a 500x1024 array. To use the dataset, we can use the same syntax as before, but taking into account the second dimension:

.. code-block:: python

   dset[1,2] = 1
   dset[200:500, 500:1024] = 123


Specify Data Types to Optimize Space
************************************
So far, we have covered only the tip of the iceberg of what HDF5 has to offer. Besides the length of the data you want to store, you may want to specify the type of data in order to optimize the space. The `h5py documentation <http://docs.h5py.org/en/latest/faq.html>`_ provides a list of all the supported types, here we are going to show just a couple of them. We are going to work with several datasets in the same file at the same time.

.. code-block:: python

   with h5py.File('several_datasets.hdf5', 'w') as f:
      dset_int_1 = f.create_dataset('integers', (10, ), dtype='i1')
      dset_int_8 = f.create_dataset('integers8', (10, ), dtype='i8')
      dset_complex = f.create_dataset('complex', (10, ), dtype='c16')

      dset_int_1[0] = 1200
      dset_int_8[0] = 1200.1
      dset_complex[0] = 3 + 4j

In the example above, we have created three different datasets, each with a different type. Integers of 1 byte, integers of 8 bytes and complex numbers of 16 bytes. We are storing only one number, even if our datasets can hold up to 10 elements. You can read the values back and see what was actually stored. The two things to note here are that the integer of 1 byte should have been rounded to 127 (instead of 1200), and the integer of 8 bytes should have been rounded to 1200 (instead of 1200.1).

If you have ever programmed in languages such as C or Fortran, you probably are aware of what different data types mean. However, if you have always worked with Python, perhaps you haven't faced any issues by not declaring explicitly the type of data you are working with. The important thing to remember is that the number of bytes tells you how many different numbers you can store. If you use 1 byte, you have 8 bits and therefore you can store 2^8 different numbers. In the example above, integers are both positive, negative, and 0. When you use integers of 1 byte you can store values from -128 to 127, in total they are 2^8 possible numbers. It is equivalent when you use 8 bytes, but with a larger range of numbers.

The type of data that you select will have an impact on its size. First, let's see how this works with a simple example. Let's create three files, each with one dataset for 100000 elements but with different data types. We will store the same data to them and then we can compare their sizes. We create a random array to assign to each dataset in order to fill the memory. Remember that data will be converted to the format specified in the dataset.

.. code-block:: python

   arr = np.random.randn(100000)

   f = h5py.File('integer_1.hdf5', 'w')
   d = f.create_dataset('dataset', (100000,), dtype='i1')
   d[:] = arr
   f.close()

   f = h5py.File('integer_8.hdf5', 'w')
   d = f.create_dataset('dataset', (100000,), dtype='i8')
   d[:] = arr
   f.close()

   f = h5py.File('float.hdf5', 'w')
   d = f.create_dataset('dataset', (100000,), dtype='f16')
   d[:] = arr
   f.close()

If you check the size of each file you will get something like:

========= ========
File      Size (b)
--------- --------
integer_1 102144
integer_8 802144
float     1602144
========= ========

The relation between size and data type is quite obvious. When you go from integers of 1 byte to integer of 8 bytes, the size of the file increases 8-fold, similarly, when you go to 16 bytes it takes approximately 16 times more space. But space is not the only important factor to take into account, you should also consider the time it takes to write the data to disk. The more you have to write, the longer it will take. Depending on your application it may be crucial to optimize the reading and writing of data.

Note that if you use the wrong data type, you may also lose information. For example, if you have integers of 8 bytes and you store them as integers of 1 byte, their values are going to be trimmed. When working in the lab, it is very common to have devices that produce different types of data. Some DAQ cards have 16 bits, some cameras work with 8 bits but some can work with 24. Paying attention to data types is important, but is also something that Python developers may not take into account because you don't have to explicitly declare a type.

It is also interesting to remember that when you initialize an array with numpy it will default to float 8 bytes (64 bits) per element. This may be a problem if, for example, you initialize an array with zeros to hold data that is going to be only 2 bytes. The type of the array itself is not going to change, and if you save the data when creating the dataset (adding ``data=my_array``) it will default to the format ``'f8'``, which is the one the array has but not your real data.

Thinking about data types is not something that happens on a regular basis if you work with Python on simple applications. However, you should know that data types are there and the impact they can have on your results. Perhaps you have large hard drives and you don't care about storing files a bit larger, but when you care about the speed at which you save, there is no other workaround but to optimize every aspect of your code, including the data types.

Compressing Data
****************
When saving data, you may opt for compressing it using different algorithms. The package h5py supports a few compression filters such as `GZIP`, `LZF`, and `SZIP`. When using one of the compression filters, the data will be processed on its way to the disk and it will be decompressed when reading it. Therefore, there is no change in how the code works downstream. We can repeat the same experiment, storing different data types, but using a compression filter. Our code looks like this:

.. code-block:: python

   import h5py
   import numpy as np

   arr = np.random.randn(100000)

   with h5py.File('integer_1_compr.hdf5', 'w') as f:
       d = f.create_dataset('dataset', (100000,), dtype='i1', compression="gzip", compression_opts=9)
       d[:] = arr

   with h5py.File('integer_8_compr.hdf5', 'w') as f:
       d = f.create_dataset('dataset', (100000,), dtype='i8', compression="gzip", compression_opts=9)
       d[:] = arr

   with h5py.File('float_compr.hdf5', 'w') as f:
       d = f.create_dataset('dataset', (100000,), dtype='f16', compression="gzip", compression_opts=9)
       d[:] = arr

We chose gzip because it is supported in all platforms. The parameters ``compression_opts`` sets the level of compression. The higher the level, the less space data takes but the longer the processor has to work. The default level is 4. We can see the differences in our files based on the level of compression:

========= ============== ============= ==============
Type      No Compression Compression 9 Compression 4
--------- -------------- ------------- --------------
integer_1 102144         28016         30463
integer_8 802144         43329         57971
float     1602144        1469580       1469868
========= ============== ============= ==============

The impact of compression on the integer datasets is much more noticeable than with the float dataset. I leave it up to you to understand why the compressing worked so well in the first two cases and not in the other. As a hint, you should inspect what kind of data you are actually saving.

Reading compressed data doesn't change any of the code discussed above. The underlying HDF5 library will take care of extracting the data from the compressed datasets with the appropriate algorithm. Therefore, if you implement compression for saving, you don't need to change the code you use for reading.

Compressing data is an extra tool that you have to consider, together with all the other aspects of data handling. You should consider the extra processor time and the effective compressing rate to see if the tradeoff between both compensates within your own application. The fact that it is transparent to downstream code makes it incredibly easy to test and find the optimum.

Resizing Datasets
*****************
When you are working on an experiment, it may be impossible to know how big your data is going to be. Imagine you are recording a movie, perhaps you stop it after one second, perhaps after an hour. Fortunately, HDF5 allows resizing datasets on the fly and with little computational cost. Datasets can be resized once created up to a maximum size. You specify this maximum size when creating the dataset, via the keyword ``maxshape``:

.. code-block:: python

   import h5py
   import numpy as np

   with h5py.File('resize_dataset.hdf5', 'w') as f:
       d = f.create_dataset('dataset', (100, ),  maxshape=(500, ))
       d[:100] = np.random.randn(100)
       d.resize((200,))
       d[100:200] = np.random.randn(100)

   with h5py.File('resize_dataset.hdf5', 'r') as f:
       dset = f['dataset']
       print(dset[99])
       print(dset[199])

First, you create a dataset to store 100 values and set a maximum size of up to 500 values. After you stored the first batch of values, you can expand the dataset to store the following 100. You can repeat the procedure up to a dataset with 500 values. The same holds true for arrays with different shapes, any dimension of an N-dimensional matrix can be resized. You can check that the data was properly stored by reading back the file and printing two elements to the command line.

You can also resize the dataset at a later stage, don't need to do it in the same session when you created the file. For example, you can do something it like this (pay attention to the fact that we open the file with an ``a`` attribute in order not to destroy the previous file):

.. code-block:: python

   with h5py.File('resize_dataset.hdf5', 'a') as f:
       dset = f['dataset']
       dset.resize((300,))
       dset[:200] = 0
       dset[200:300] = np.random.randn(100)

   with h5py.File('resize_dataset.hdf5', 'r') as f:
       dset = f['dataset']
       print(dset[99])
       print(dset[199])
       print(dset[299])

In the example above you can see that we are opening the dataset, modifying its first 200 values, and appending new values to the elements in the position 200 to 299. Reading back the file and printing some values proves that it worked as expected.

Imagine you are acquiring a movie but you don't know how long it will be. An image is a 2D array, each element being a pixel, and a movie is nothing more than stacking several 2D arrays. To store movies we have to define a 3-dimensional array in our HDF file, but we don't want to set a limit to the duration. To be able to expand the  third axis of our dataset without a fixed maximum, we can do as follows:

.. code-block:: python

   with h5py.File('movie_dataset.hdf5', 'w') as f:
      d = f.create_dataset('dataset', (1024, 1024, 1),  maxshape=(1024, 1024, None ))
      d[:,:,0] = first_frame
      d.resize((1024,1024,2))
      d[:,:,1] = second_frame

The dataset holds square images of 1024x1024 pixels, while the third dimension gives us the stacking in time. We assume that the images don't change in shape, but we would like to stack one after the other without establishing a limit. This is why we set the third dimension's ``maxshape`` to ``None``.

Save Data in Chunks
*******************
To optimize the storing of data you can opt to do it in chunks. Each chunk will be contiguous on the hard drive and will be stored as a block, i.e. the entire chunk will be written at once. When reading a chunk, the same will happen, entire chunks are going to be loaded. To create a `chunked` dataset, the command is:

.. code-block:: python

    dset = f.create_dataset("chunked", (1000, 1000), chunks=(100, 100))

The command means that all the data in ``dset[0:100,0:100]`` will be stored together. It is also true for ``dset[200:300, 200:300]``, ``dset[100:200, 400:500]``, etc. According to h5py, there are some performance implications while using `chunks`:

    Chunking has performance implications. It is recommended to keep the total size of your chunks between 10 KiB and 1 MiB, larger for larger datasets. Also keep in mind that when any element in a chunk is accessed, the entire chunk is read from disk.

There is also the possibility of enabling auto-chunking, that will take care of selecting the best size automatically. Auto-chunking is enabled by default if you use compression or ``maxshape``. You enable it explicitly by doing:

.. code-block:: python

   dset = f.create_dataset("autochunk", (1000, 1000), chunks=True)

Organizing Data with Groups
***************************
We have seen a lot of different ways of storing and reading data. Now we have to cover one of the last important topics of HDF5 that is how to organize the information in a file. Datasets can be placed inside `groups`, that behave in a similar way to how directories do. We can create a group first and then add a dataset to it:

.. code-block:: python

   import numpy as np
   import h5py

   arr = np.random.randn(1000)

   with h5py.File('groups.hdf5', 'w') as f:
       g = f.create_group('Base_Group')
       gg = g.create_group('Sub_Group')

       d = g.create_dataset('default', data=arr)
       dd = gg.create_dataset('default', data=arr)

We create a group called ``Base_Group`` and within it, we create a second one called ``Sub_Group``. In each one of the groups, we create a dataset called ``default`` and save the random array into them. When you read back the files, you will notice how data is structured:

.. code-block:: python

   with h5py.File('groups.hdf5', 'r') as f:
      d = f['Base_Group/default']
      dd = f['Base_Group/Sub_Group/default']
      print(d[1])
      print(dd[1])

As you can see, to access a `dataset` we address it as a folder within the file: ``Base_Group/default`` or ``Base_Group/Sub_Group/default``. When you are reading a file, perhaps you don't know how groups were called and you need to list them. The easiest way is using ``keys()``:

.. code-block:: python

   with h5py.File('groups.hdf5', 'r') as f:
       for k in f.keys():
           print(k)

However, when you have nested groups, you will also need to start nesting for-loops. There is a better way of iterating through the tree, but it is a bit more involved. We need to use the ``visit()`` method, like this:

.. code-block:: python

   def get_all(name):
      print(name)

   with h5py.File('groups.hdf5', 'r') as f:
      f.visit(get_all)

Notice that we define a function ``get_all`` that takes one argument, ``name``. When we use the ``visit`` method, it takes as argument a function like ``get_all``. ``visit`` will go through each element and while the function doesn't return a value other than ``None``, it will keep iterating. For example, imagine we are looking for an element called `Sub_Group` we have to change ``get_all``:

.. code-block:: python

   def get_all(name):
       if 'Sub_Group' in name:
           return name

   with h5py.File('groups.hdf5', 'r') as f:
       g = f.visit(get_all)
       print(g)

When the method ``visit`` is iterating through every element, as soon as the function returns something that is not ``None`` it will stop and return the value that ``get_all`` generated. Since we are looking for the `Sub_Group`, we make the ``get_all`` return the name of the group when it finds `Sub_Group` as part of the name that is analyzing. Bear in mind that ``g`` is a string, if you want to actually get the group, you should do:

.. code-block:: python

   with h5py.File('groups.hdf5', 'r') as f:
      g_name = f.visit(get_all)
      group = f[g_name]

And you can work as explained earlier with groups. A second approach is to use a method called ``visititems`` that takes a function with two arguments: name and object. We can do:

.. code-block:: python

   def get_objects(name, obj):
      if 'Sub_Group' in name:
         return obj

   with h5py.File('groups.hdf5', 'r') as f:
      group = f.visititems(get_objects)
      data = group['default']
      print('First data element: {}'.format(data[0]))

The main difference when using ``visititems`` is that we have accessed not only the name of the object that is being analyzed but also the object itself. You can see that what the function returns is the object and not the name. This pattern allows you to achieve more complex filtering. For example, you may be interested in the groups that are empty, or that have a specific type of dataset in them.

Storing Metadata in HDF5
************************
One of the aspects that are often overlooked in HDF5 is the possibility to store metadata attached to any group or dataset. Metadata is crucial in order to understand, for example, where the data came from, what were the parameters used for a measurement or a simulation, etc. Metadata is what makes a file self-descriptive. Imagine you open older data and you find a 200x300x250 matrix. Perhaps you know it is a movie, but you have no idea which dimension is time, nor the timestep between frames.

Storing metadata into an HDF5 file can be achieved in different ways. The official one is by adding attributes to groups and datasets.

.. code-block:: python
   :hl_lines: 14

   import time
   import numpy as np
   import h5py
   import os

   arr = np.random.randn(1000)

   with h5py.File('groups.hdf5', 'w') as f:
       g = f.create_group('Base_Group')
       d = g.create_dataset('default', data=arr)

       g.attrs['Date'] = time.time()
       g.attrs['User'] = 'Me'

       d.attrs['OS'] = os.name

       for k in g.attrs.keys():
           print('{} => {}'.format(k, g.attrs[k]))

       for j in d.attrs.keys():
         print('{} => {}'.format(j, d.attrs[j]))

In the code above you can see that the ``attrs`` is like a dictionary. In principle, you shouldn't use attributes to store data, keep them as small as you can. However, you are not limited to single values, you can also store arrays. If you happen to have metadata stored in a dictionary and you want to add it automatically to the attributes, you can use ``update``:

.. code-block:: python

   with h5py.File('groups.hdf5', 'w') as f:
      g = f.create_group('Base_Group')
      d = g.create_dataset('default', data=arr)

      metadata = {'Date': time.time(),
         'User': 'Me',
         'OS': os.name,}

      f.attrs.update(metadata)

      for m in f.attrs.keys():
         print('{} => {}'.format(m, f.attrs[m]))

Remember that the data types that hdf5 supports are limited. For example, dictionaries are not supported. If you want to add a dictionary to an hdf5 file you will need to serialize it. In Python, you can serialize a dictionary in different ways. In the example below, we are going to do it with JSON because it is very popular in different fields, but you are free to use whatever you like, including `pickle`.

.. code-block:: python

   import json

   with h5py.File('groups_dict.hdf5', 'w') as f:
       g = f.create_group('Base_Group')
       d = g.create_dataset('default', data=arr)

       metadata = {'Date': time.time(),
                   'User': 'Me',
                   'OS': os.name,}

       m = g.create_dataset('metadata', data=json.dumps(metadata))

The beginning is the same, we create a group and a dataset. To store the metadata we define a new dataset, appropriately called `metadata`. When we define the data, we use ``json.dumps`` that will transform a dictionary into a long string. We are actually storing a string and not a dictionary into HDF5. To load it back we need to read the data set and transform it back to a dictionary using ``json.loads``:

.. code-block:: python

   with h5py.File('groups_dict.hdf5', 'r') as f:
       metadata = json.loads(f['Base_Group/metadata'][()])
       for k in metadata:
           print('{} => {}'.format(k, metadata[k]))

When you use `json` to encode your data, you are defining a specific format. You could have used YAML, XML, etc. Since it may not be obvious how to load the metadata stored in this way, you could add an attribute to the ``attr`` of the dataset specifying which way of serializing you have used.

Final thoughts on HDF5
**********************
In many applications, text files are more than enough and provide a simple way to store data and share it with other researchers. However, as soon as the volume of information increases, you need to look for tools that are better suited than text files. One of the main advantages of the HDF format is that it is self-contained, meaning that the file itself has all the information you need to read it, including metadata information to allow you to reproduce results. Moreover, the HDF format is supported in different operating systems and programming languages.

HDF5 files are complex and allow you to store a lot of information in them. The main advantage over databases is that they are stand-alone files that can be easily shared. Databases need an entire system to manage them, they can't be easily shared, etc. If you are used to working with SQL, you should check `the HDFql project <https://www.hdfgroup.org/2016/06/hdfql-new-hdf-tool-speaks-sql/>`_ which allows you to use SQL to parse data from an HDF5 file.

Storing a lot of data into the same file is susceptible to corruption. If your file loses its integrity, for example, because of a faulty hard drive, it is hard to predict how much data is going to be lost. If you store years of measurements into one single file, you are exposing yourself to unnecessary risks. Moreover, backing up is going to become cumbersome because you won't be able to do incremental backups of a single binary file.

HDF5 is a format that has a long history and that many researchers use. It takes a bit of time to get used to, and you will need to experiment for a while until you find a way in which it can help you store your data. HDF5 is a good format if you need to establish transversal rules in your lab on how to store data and metadata.

Header photo by `Samuel Zeller <https://www.samuelzeller.ch>`_ on `Unsplash <https://unsplash.com/photos/JuFcQxgCXwA?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText>`_

This article is part of a series of articles relating to data storage with Python. The other articles are:

* `Introduction to Storing Data in Files <{filename}13_storing_data.rst>`_
* `Storing Binary Data and Serializing <{filename}14_Storing_data_2.rst>`_
* `Using Databases to Store Data <{filename}15_Storing_data_3.rst>`_
* `Using HDF5 Files with Python <{filename}02_HDF5_python.rst>`_