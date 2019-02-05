Introduction to Storing Data in Files
=====================================

:date: 2018-08-10
:author: Aquiles Carattino
:subtitle: Learn different ways of storing data in your projects
:header: {attach}pietro-jeng-266017-unsplash.jpg
:tags: Data, Storing, SQLite, HDF5, ascii, json, Data Storage
:description: Learn different ways of storing data in your projects

This is the first of a series of articles relating to data storage with Python. The other articles are:

* `Storing Binary Data and Serializing Objects <{filename}14_Storing_data_2.rst>`_
* `Using Databases to Store Data <{filename}15_Storing_data_3.rst>`_
* `Using HDF5 Files with Python <{filename}02_HDF5_python.rst>`_

Storing data to reuse it later is a central part in most Python applications. Whether you are doing a measurement in the lab or developing a web application, you will need to save information in a persistent way. For example, you would like to analyze your results after you have performed an experiment. Or you would like to keep a list of e-mails of people who registered on your website.

Even if storing data is of utmost importance, every application will require different strategies. You have to take into account different factors, such as the volume of data being generated, how self-descriptive the data is, how are you going to use it later, etc. In this article, we are going to start exploring different ways of storing data.

.. contents::

Plain Text Files with Numpy
---------------------------
When storing data on the hard drive, a common option is to use plain text files. Let's start with a simple example, a ``numpy`` array of a given length. We can generate such an array in the following way:

.. code-block:: python

    import numpy as np

    data = np.linspace(0,1,201)

Which will generate an array of 201 values equally spaced between 0 and 1. This means that the elements will look like ``0, 0.005, 0.01, ..``. If you want to save the data to a file, numpy allows you to do it very easily with the ``savetxt`` method, like this:

.. code-block:: python

    np.savetxt('A_data.dat', data)

Go ahead and open the file **a_data.dat** with any text editor. You will see that you have a column of all the values in your array. This is very handy because the file can be read with any other program that supports reading text files. So far, this example is very simplistic because it stores only one array. Imagine that you want to store two arrays, like the ones needed to make a simple plot. First, let's generate both arrays:

.. code-block:: python

    x = np.linspace(0, 1, 201)
    y = np.random.random(201)

You can store them very easily by doing the following:

.. code-block:: python

    np.savetxt('AA_data.dat', [x, y])

If you open the file, you will see that instead of having two columns, the file has only two very long lines. This is normally not a problem, but it makes your file very hard to read if you open it with a text editor or with other programs. If you want to save the data as two (or several) columns, you need to stack them. The code would look like this:

.. code-block:: python

    data = np.column_stack((x, y))
    np.savetxt('AA_data.dat', data)

Check the file again, you will see that you have the x values on the column on the left and the y values on the other. A file like this is easier to read and, as we will see later, allows you to do partial reads. However, there is something very important missing. If someone opens the file, there is no information on what each column means. The easier solution, in this case, is to add a header describing each column:

.. code-block:: python

    header = "X-Column, Y-Column"
    np.savetxt('AB_data.dat', data, header=header)

Check the file again, you will see a nice header explaining what each column is. Note that the first character of the line is a ``#``. This is very standard in order to easily identify which lines belong to the header and not to the data itself. If you want to add a multi-line header, you can do the following:

.. code-block:: python

    header = "X-Column, Y-Column\n"
    header += "This is a second line"
    np.savetxt('AB_data.dat', data, header=header)

The important element to note in the code above is the ``\n`` added at the end of the first line. This is the new line character, which is equivalent to pressing ``enter`` in your keyboard when typing a document. This character tells Python to go to the line below when writing information to a file.

Loading Saved Data with Numpy
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Of course, saving to a file is only half what you have to do. The other half is reading it. Fortunately, this is very easy with numpy:

.. code-block:: python

    data = np.loadtxt('AB_data.dat')
    x = data[:, 0]
    y = data[:, 1]

Note that it automatically discards the headers. The advantage of using always the same library (in this case numpy) is that it makes it incredibly easy to go through the write/read cycle. If you are trying to read data from a file that was generated with another program and that uses another character for starting comments, you can very easily adapt the code above:

.. code-block:: python

    data = np.loadtxt('data.dat', comments='@')

In the example above, the code will skip all the lines that start with an ``@`` symbol.

.. newsletter::

Saving Partial Files with Numpy
-------------------------------
One common situation is to save to file while the data acquisition or generation is happening. This allows you, for example, to monitor the progress of an experiment and to have the data safe even if something goes wrong with your program. The code is very similar to what we have done earlier, but not exactly the same:

.. code-block:: python

    import numpy as np

    x = np.linspace(0, 1, 201)
    y = np.random.random(201)

    header = "X-Column, Y-Column\n"
    header += "This is a second line"
    f = open('AD_data.dat', 'wb')
    np.savetxt(f, [], header=header)
    for i in range(201):
        data = np.column_stack((x[i], y[i]))
        np.savetxt(f, data)

    f.close()

The first thing you have to notice is that we are explicitly opening the file with the command ``open``. The important portion of information here is the ``wb`` that we added at the end. The ``w`` stands for *writing* mode, i.e. the file will be created if it doesn't exist, and if it already exists it will be erased and started from scratch. The second letter, the ``b`` is for binary mode, which is needed for letting numpy append data to a file. In order to generate the header, we first save an empty list with the header. Within the for-loop, we save every value to the file, line by line.

With the example above, if you open the file you will see it exactly as earlier. However, if you add a ``sleep`` statement within the for-loop, and open the file, you will see the partial saves. Remember that not all operating systems allow you to open the file in two different programs at the same time. Moreover, not all text editors are able to notice changes to the file from outside themselves, meaning that you won't see the changes to the file unless you re-open it.

Flushing Changes
~~~~~~~~~~~~~~~~
If you start saving partial data often, you will notice that, especially when your program crashes, some of the data points may be missing. Writing to disk is a step that is handled by the operating system, and therefore its behavior can be very different depending on which one you use and how busy the computer is. Python puts the writing instructions into a queue, which means that the writing itself can be executed much later in time. If you want to be sure that changes are being written, especially when you are aware that your program may give rise to `unhandled exceptions <{filename}12_handling_exceptions.rst>`_, you can add the ``flush`` command. Simply like this:

.. code-block:: python

    f = open('AD_data.dat', 'wb')
    for i in range(201):
        [...]
        f.flush()

This will guarantee that you are writing to disk every single time. Python normally relies on the operating system defaults for handling buffering of writing events. However, when trying to push the limits, it is very important to regain control and be aware of what the consequences may be.

The With Statement
~~~~~~~~~~~~~~~~~~
When working with files, it is important to ensure that you are closing it when you finish with it. If you don't do it, you may end up with corrupted data. In the example above, you can see that if an error appears within the ``for``, the line ``f.close()`` will never be executed. In order to avoid this kind of issues, Python provides the ``with`` statement. You can use it like this:

.. code-block:: python

    with open('AE_data.dat', 'wb') as f:
        np.savetxt(f, [], header=header)
        for i in range(201):
            data = np.column_stack((x[i], y[i]))
            np.savetxt(f, data)
            f.flush()
            sleep(0.1)

The first line is the key element here. Instead of doing ``f=open()``, we use the ``with`` statement. The file will be open while we are inside the block. As soon as the block finishes, the file will be closed, even if there is an exception within the block. The ``with`` allows you to save a lot of typing since you don't need to handle exceptions nor to close the file afterward. It may seem like a small gain at the beginning, but the conscious developer should use it extensively.

The details of the ``with`` statement deserve their own article, which is in the pipeline for the future. For the time being, remember what it means when you see it.

Lower-level Writing to Text Files
---------------------------------
Up to here, we have seen how to use numpy to save data because it is a standard in many applications. However, it may not fit all the applications. Python has its own method for writing to and reading from, files. Let's start writing to a file. The pattern is very simple:

.. code-block:: python

    f = open('BA_data.dat', 'w')
    f.write('# This is the header')
    f.close()

Or with the ``with``:

.. code-block:: python

    with open('BA_data.dat', 'w') as f:
        f.write('# This is the header')

The ``open`` command takes at least one argument, the filename. The second argument is the mode with which the file is opened. Basically, there are three: ``r`` for reading, not modifying, ``a`` for appending or creating the file if it doesn't exist, ``w`` for creating an empty file, even if it already exists. If no mode is given, ``r`` is assumed, and if the file doesn't exist, a ``FileNotFound`` exception will be raised.

Now that we have the header written to the file, we want to write some data to it. For example, we can try the following:

.. code-block:: python

    x = np.linspace(0,1,201)
    with open('BB_data.dat', 'w') as f:
        f.write('# This is the header')
        for data in x:
            f.write(data)

However, you will see an error, ``TypeError``, because you are trying to write something that is not a string, in this case, a numpy number. Therefore, first, you have to transform whatever you want to write to a string. For numbers, it is very easy, you only need to replace one line:

.. code-block:: python

    f.write(str(data))

If you open the file, you will notice something very strange. The header and all the elements of your array were written to the same line, no separation whatsoever between them. This is actually expected if you think about it. Because you are using lower level commands, you have a much more precise control over what and how you write to a file.

If you remember from the previous section, you can use the ``\n`` character to generate a new line after writing to a file. Your code will look like the following:

.. code-block:: python

    x = np.linspace(0,1,201)
    with open('BB_data.dat', 'w') as f:
        f.write('# This is the header\n')
        for data in x:
            f.write(str(data)+'\n')

If you open the file again, you will see that all your data points are nicely stacked on top of each other. You will also notice that not all values have the same length. For example, you will find elements such as ``0.01``, ``0.005``, and ``0.17500000000000002``. The first two make sense, however, the third one may seem odd. The last digit in that number is given because of floating-point errors. You can read more about it in the `Oracle website <https://docs.oracle.com/cd/E19957-01/806-3568/ncg_goldberg.html>`_ (more technical) or `on Wikipedia <https://en.wikipedia.org/wiki/Floating-point_arithmetic#Floating-point_numbers>`_ (more general public-oriented).

Formatting the output
---------------------
One of the most important things to consider when writing data to disk is how to structure it in order to make it easy to read afterward. In the section above, we have seen that if you don't append a newline character after every value, they get printed one after the other, on the same line. This makes your data almost impossible to read back. Since every number has a different length, you can't break the line into smaller information blocks, etc.

Formatting the output is therefore very important to give sense to your data in the long run. Python offers different ways for formatting strings. I will choose the one I normally employ, but you are free to explore other alternatives. Let's first adapt the example above, with ``format``. You can print every value to a different line like this:

.. code-block:: python

    x = np.linspace(0,1,201)
    with open('BC_data.dat', 'w') as f:
        f.write('# This is the header\n')
        for data in x:
            f.write('{}\n'.format(data))

If you run the code, the output file will be the same. When you use ``format``, the ``{}`` gets replaced by the data. It is equivalent to the ``str(data)`` that we have used before. However, imagine that you want to output all the values with the same amount of characters, you can replace that last line by:

.. code-block:: python

    f.write('{:.2f}\n'.format(data))

which will give you values like ``0.00``, ``0.01``, etc. What you put in between the ``{}`` is the format string, which instructs Python how to transform your numbers into strings. In this case, it is telling it to treat the numbers as fixed point with 2 decimals. In principle, it looks very nice, but notice that you are losing information. The values like ``0.005`` are rounded to ``0.01``. Therefore, you have to be very certain about what do you want to achieve, in order not to lose important information. If you are performing an experiment with 0.1 precision, you don't care about 0.005, but if it is not the case, you have lost half your information.

Proper formatting takes a bit of tinkering. Since we want to store at least three decimals, we should change the line to:

.. code-block:: python

    f.write('{:.3f}\n'.format(data))

Now you are storing all the decimals up to the third place. Formatting strings deserve a post on its own. But you can see the basic options here. If you are working with integers, for instance, or with larger floating point numbers (not between 0 and 1), you may want to specify how much space the numbers are going to take. For instance, you can try:

.. code-block:: python

    import numpy as np

    x = np.linspace(0,100,201)
    with open('BC_data.dat', 'w') as f:
        for data in x:
            f.write('{:4.1f}\n'.format(data))

This command is letting Python know that each number should be allocated 4 spaces in total, with only one decimal place. Since the first numbers have only 3 characters (``0.5``), there will be a space preceding the number. Later on, ``10.0`` will start right from the beginning, and the decimals will be nicely aligned. However, you will notice that ``100.0`` is displaced by one position (it takes 5, not 4 spaces).

You can play a lot with the formatting. You can align the information to the left or to the right, adding spaces or any other character on either side, etc. I promise to cover this topic later on. But for now it is enough, let's keep storing data to a file.

Storing Data in Columns
-----------------------
Let's recover the example from before, where we stored two columns of data. We would like to do the same, without the use of numpy's ``savetxt``. With what we know of formatting we can already do this:

.. code-block:: python

    import numpy as np

    x = np.linspace(0,100,201)
    y = np.random.random(201)

    with open('BD_data.dat', 'w') as f:
        for i in range(len(x)):
            f.write('{:4.1f} {:.4f}\n'.format(x[i], y[i]))

Check the saved file, you will see the two columns of data, separated by a space. You can change the ``write`` line in different ways, for example, you could have:

.. code-block:: python

    f.write('{:4.1f}\t{:.4f}\n'.format(x[i], y[i]))

which will add a tab between the columns, and not a space. You can structure your file as you like. However, you have to be careful and think ahead about how you are going to retrieve the data in case an inconsistency appears.

Reading the data
----------------
After we have saved the data to a file, it is very important to be able to read it back into our program. The first approach is unorthodox, but it will prove a point. You can read the data generated with the ``write`` method using numpy's ``loadtxt``:

.. code-block:: python

    import numpy as np

    data = np.loadtxt('BD_data.dat')

One of the advantages of writing text files is that they are relatively easy to read from any other program. Even your text editor can make sense of what is inside one of such files. Of course, you can also read the file without using numpy, just with Python's built-in methods. The easiest would be:

.. code-block:: python

    with open('BD_data.dat', 'r') as f:
        data = f.read()

However, if you look into data, you will notice that it is a string. After all, plain text files are just strings. Depending on how you have structured the file, transforming the data into an array, a list, etc. may be more or less simple. However, before going into those details, another way of reading the file is line by line:

.. code-block:: python

    with open('BD_data.dat', 'r') as f:
        data = f.readline()
        data_2 = f.readline()

In this case, ``data`` will hold the header, because it is the first line of the file, while ``data_2`` will hold the first line of data. Of course, this only reads the first two lines of the file. To read all the lines, we can do the following:

.. code-block:: python

    with open('BD_data.dat', 'r') as f:
        line = f.readline()
        header = []
        data = []
        while line:
            if line.startswith('#'):
                header.append(line)
            else:
                data.append(line)
            line = f.readline()

Now you see that things are getting more complicated. After opening the file, we read the first line and then we enter into a loop, that will keep running while there are more lines in the file. We start two empty lists to hold the header and the data information. For each line, we check whether it starts with ``#``, which would correspond to the header (or comment). We append the rest of the lines to ``data``.

If you look into the ``data`` variable, you will notice that it is not very usable. If you are reading the example with the two columns, you will see that ``data`` is a list in which every element looks like `` 0.0\t0.02994\n``. If we want to reconstruct the information we had before, we have to reverse the procedure of writing. The first thing to note is that both values are separated by a ``\t``, therefore our code would look like the following:

.. code-block:: python

    with open('BD_data.dat', 'r') as f:
        line = f.readline()
        header = []
        x = []
        y = []
        while line:
            if line.startswith('#'):
                header.append(line)
            else:
                data = line.split('\t')
                x.append(float(data[0]))
                y.append(float(data[1]))
            line = f.readline()

The beginning looks the same, but we have separated the data into ``x`` and ``y``. The biggest modification, in this case, is that we apply the method ``split`` to separate a string. Since our columns are delimited by a tab, we use the character ``\t``. Data will have two elements, i.e. two columns, and we append each to x and y. Of course, we don't want the strings, but the numbers. That is why we transform ``data`` into floats.

With the steps above you can see that it is possible to recover the functionality of the ``loadtxt`` of numpy, but with a lot of effort. The code above works only if you have two columns if you had a file with just 1 column, or with more than 2 it would fail. ``loadtxt`` didn't ask explicitly how many columns to expect, it just parsed the text and found out by itself. However, you will not always have numpy available, or sometimes you require a higher level of control on how your data is being read or written.

Learning From Others
--------------------
One of the main advantages of open-source software is that you are free to look into their code in order to understand what they do and learn from them. In the example above, we have developed a very specialized solution that is able to handle two columns, but not more nor less. However, when we are using ``loadtxt``, we don't need to specify how many columns there are, the method will find out by itself. Let's look at the `loadtxt code <https://github.com/numpy/numpy/blob/v1.15.0/numpy/lib/npyio.py#L773-L1149>`_ to try to understand how it works and improve our own code.

The first you have to notice is that the method ``loadtxt``, including comments, is 376 lines long, quite a big difference with our 10-line-long method for reading two columns. In `line 1054 <https://github.com/numpy/numpy/blob/v1.15.0/numpy/lib/npyio.py#L1054>`_ you can find ``first_vals = split_line(first_line)``, which sends you to `line 991 <https://github.com/numpy/numpy/blob/v1.15.0/numpy/lib/npyio.py#L991>`_, in which numpy defines how to split the lines. You see that it is simply doing ``line.split(delimiter)`` and ``delimiter`` could be ``None`` (it comes from the very line where ``loadtxt`` is defined). Looking at that line takes you to the official Python docs, in which you can see the `documentation for split <https://docs.python.org/3.6/library/stdtypes.html#str.split>`_.

What we could do is to look for the first line with data, split it either with a fixed delimiter or we can let Python do its best by using ``None``. Once we read the first line, we will know how many columns are present, and we assume that all the other lines will have the same number. If it is not the case, we could raise an exception because of malformed data. Note that ``loadtxt`` also takes care of parsing the element as the proper data type. We assume we are dealing with floats, and we have used ``float(data[0])``, which will fail if we try to load a string.

Loading data in a flexible way such as what numpy does is relatively complex. The advantage of looking at code developed by others is that you can learn a lot from seasoned developers, you can see that they anticipate problems you perhaps never thought about. You could also implement the same method, without relying on having numpy on the same computer. Whenever you think you are doing something that it was already solved, try to leverage from that experience. Reading code is a great resource for learning.

Saving Non-Numeric Data
-----------------------
So far we have dealt only with numbers, that is why using numpy provides such a big advantage. However, a lot of applications need to deal with different types of data. Let's start with the easiest one: storing strings. There is a very popular dataset for people learning machine learning, known as the Iris Dataset. It consists of observations of several parameters of three different types of flowers.

I am not going to recreate the dataset here, but I will just use it as inspiration. Imagine you make several observations, each corresponding to a specific flower out of three options. However, not all of the observations are real, some were labeled as fake ones. We can create a file very easily, with some random data:

.. code-block:: python

    import random

    observations = ['Real', 'Fake']
    flowers = ['Iris setosa', 'Iris virginica', 'Iris versicolor']

    with open('DA_data.dat', 'w') as f:
        for _ in range(20):
            observation = random.choice(observations)
            flower = random.choice(flowers)
            f.write('{} {}\n'.format(observation, flower))

There are two types of observations, with three different types of flowers. You pick one random type of observation and one random flower and you write it to the file. Of course, we don't need to limit ourselves to string data. We can also save numeric values. The original dataset includes four numeric values: the length and the width of the sepals and petals. We can include some fake data modifying the script:

.. code-block:: python

    import random

    observations = ['Real', 'Fake']
    flowers = ['Iris setosa', 'Iris virginica', 'Iris versicolor']

    with open('DB_data.dat', 'w') as f:
        for _ in range(20):
            observation = random.choice(observations)
            flower = random.choice(flowers)
            sepal_width = random.random()
            sepal_length = random.random()
            petal_width = random.random()
            petal_length = random.random()

            f.write('{} {} {:.3f} {:.3f} {:.3f} {:.3f}\n'.format(
                observation,
                flower,
                sepal_length,
                sepal_width,
                petal_length,
                petal_width))

If you look at the file, you will see that you have the same information as before, plus the extra four numeric fields. Probably, you are already seeing the limitations of the approach. But let's see it in more detail.

Reading Non-Numeric Data
------------------------
Just as before, reading non-numeric data is as easy as reading numeric data. For example, you can do the following:

.. code-block:: python

    with open('DB_data.dat', 'r') as f:
        line = f.readline()
        data = []
        while line:
            data.append(line.split(' '))
            line = f.readline()
    print(data)

You see that we are splitting the spaces, which seemed like a good idea in the examples above. However, if you look closely at the data, you will notice that the names of the flowers are split, and we end up with lines of 6 elements instead of 5 as expected. This is a simple example because every field has exactly one space, and therefore we can merge together the two that belong to the name.

More complicated data, like sentences, for example, will require a more careful handling. In a sentence, you will have a variable number of spaces and therefore you are going to have a hard time figuring out what parts belong to which data column. You can replace the space by a comma when you save the file and it is going to work, provided that there are no commas in the data you are saving.

If you delimit your data with commas you will have a file commonly referred to as Comma Separated Values, or **csv**. You can see the output of `the file I have generated <https://github.com/PFTL/website/blob/master/example_code/13_storing_data/DB_data.csv>`_ on Github. This kind of files can be interpreted not only by text readers but also by numeric programs such as Excel, Libre Office, Matlab, etc. You can even see that if you look at the file on Github it appears nicely formatted. There are several standards around, and you can try to reproduce them.

Of course, if your data has a comma in it, the file will be broken. The integrity of your data will be fine, but it is going to be very hard to specify how to read it back without errors. The idea of storing data is that you can read back, and if there are exceptions in the process, you will not be certain about what your data means. You don't need to use commas, nor single characters. You can separate your data with a dot and a comma, for instance.

When you store data, you have to think not only about the process of storing but also in the process of reading it back in an unambiguous way. If you store only numeric data, choosing a letter for separating values may seem like a good idea. Using a comma may seem correct until you realize that in some countries commas separate the decimal part of numbers.

Is this all regarding how to store data? Of course, not, there is much more to come.

As always, `the example code can be found here <https://github.com/PFTL/website/tree/master/example_code/13_storing_data>`_ and `the source code for this article here <https://github.com/PFTL/website/blob/master/content/blog/13_storing_data.rst>`_.

Header photo by `Pietro Jeng <https://unsplash.com/photos/n6B49lTx7NM?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText>`_ on Unsplash

This article is part of a series of articles relating to data storage with Python. The other articles are:

* `Introduction to Storing Data in Files <{filename}13_storing_data.rst>`_
* `Storing Binary Data and Serializing <{filename}14_Storing_data_2.rst>`_
* `Using Databases to Store Data <{filename}15_Storing_data_3.rst>`_
* `Using HDF5 Files with Python <{filename}02_HDF5_python.rst>`_