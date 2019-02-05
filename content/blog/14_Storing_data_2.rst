Storing Binary Data and Serializing
===================================

:date: 2018-08-11
:author: Aquiles Carattino
:subtitle: Learn different ways of storing data in your projects
:header: {attach}joshua-sortino-215039-unsplash.jpg
:tags: Data, Storing, SQLite, HDF5, ascii, json, Data Storage
:description: Learn different ways of storing data in your projects

This article is part of a series of articles relating to data storage with Python. The other articles are:

* `Introduction to Storing Data in Files <{filename}13_storing_data.rst>`_
* `Storing Binary Data and Serializing <{filename}14_Storing_data_2.rst>`_
* `Using Databases to Store Data <{filename}15_Storing_data_3.rst>`_
* `Using HDF5 Files with Python <{filename}02_HDF5_python.rst>`_

Last week we have seen how to store data into plain text files that can be read by any editor or by other programs. We have also seen that if you separate your data with commas your file will follow a standard and it will be automatically compatible with other applications, such as spreadsheets. One of the main limitations of this strategy is that if the data itself contains a comma, your file will not be readable anymore.

In this article, we are going to discuss the encoding of data. This will allow us to understand how come that what you save with Python can be read by a normal text editor or your web browser. We will also see that you can save space on your disk if you encode your data in the proper way. In the end what you will have is a clear picture of the difference between saving plain text files and binary data.

.. contents::

What does it really mean to save text files
-------------------------------------------
Last week you have seen different ways of saving text files. One of the most noticeable attributes is that those files can be opened with any basic text editor, you don't need Python to read them. This already should indicate that there is an underlying property that allows programs to share files with each other.

As you have probably heard already, computers don't understand about letters or colors, they only understand about 1's and 0's. This means that there should be a way of translating that kind of information into a letter (or a number, or a color). The way of converting from one to another type of representation is called an encoding. Probably you have already heard about ascii or Unicode. Those are standards that specify how to translate from a stream of bytes (i.e. 1's and 0's) to the letters you are seeing now on the screen.

ASCII stands for American Standard Code for Information Interchange. It is a specification on how to translate bytes to characters and vice-versa. If you look at the `ASCII table <https://www.asciitable.com/>`_, you see that it specifies how to translate numbers from 0 to 127 to characters. 128 options is not a random choice, it is 7-bit or all the combinations that a sequence of 7 1's and 0's can generate. You can see also the extended ascii table, which adds all the characters up to a number of 255 (i.e. 8-bit).

Let's do a quick test. We can create an array of integers between 0 and 255 (8-bit) and store it to a file, and then compare the size of that file with the size of the array. The code will look like this:

.. code-block:: python

    import sys
    import numpy as np

    x = np.linspace(0, 255, 256, dtype=np.uint8)

    with open('AA_data.dat', 'w') as f:
        for data in x:
            f.write(str(data)+'\n')


Each element of the array is 8-bits long (or 1 byte). We are storing 256 elements, and therefore we expect the file to be 256 bytes in size. However, if you check it, you will see that it is bigger than that: around 914 bytes. This difference is not negligible, so where is it coming from?

We have stored 256 elements, but there more numbers in the file. 10 elements are 1-digit long, 90 are 2-digits and 156 are 3-digits long. In total, there are 658 digits, plus 256 newline characters. If you add them up you get exactly 914. This means that each character is taking exactly 1 byte or 8 bits. If you are on Windows, there is an extra consideration, because the new line character gets replaced by two characters and therefore you need to add 512 characters instead of 256.

When you want to write a ``1``, it takes 1 byte. However, when you store a ``10`` it will take 2 bytes. You have to remember that, in the space of integer numbers of 8 bits, they both take the same amount of memory. With this simple example, you start seeing that there are a lot of small details that you have to take into account when saving data.

.. newsletter::

Different encodings for text data
---------------------------------
You may have realized in the previous section that ASCII is limited to a special set of characters. If you want to write characters of other languages, for example, such as the Spanish ñ, you will need to resort to other standards. This gave rise to a myriad of different encodings, with a small degree of compatibility between them. If you are `Notpad++ <https://notepad-plus-plus.org/>`_ user you can see on the menu that you can select the *encoding* for the file.

When you open a text file, the program needs to translate from bytes to characters, basically by looking up on a table. If you change that table, you change the output. If you use text editors such as `Notpad++ <https://notepad-plus-plus.org/>`_ you will see that you can specify the encoding of the file. Select *encoding* on the menu and then *character sets* and you will find tons of options. If you play with it, you will see that the output may change, especially if there are special characters from other languages.

The problem got worst with websites having users from different countries expecting to use different character sets. That is why a superseding standard appeared, called `Unicode <https://en.wikipedia.org/wiki/Unicode>`_. Unicode includes and expands the ascii table with up to 32-bit characters, which is billions of different choices. Unicode includes thousands of symbols from modern and ancient languages, plus all the emojis you are already familiar with.

If you want to specify the encoding used while saving a file, you can do the following:

.. code-block:: python

    import codecs

    data_to_save = 'Data to Save'
    with codecs.open('AB_unicode.dat', 'w', 'utf-8') as f:
        f.write(data_to_save)

In the code above, the important part is the line that says ``utf-8``. Unicode has different implementations, and each one uses a different amount of bits per character. You can choose between 8, 16 and 32. You can also change the encoding to ``ascii``. As an exercise, compare how much space it takes every time you save the data. Open the file being saved with a text editor and check if you can see the message.

Saving Numpy Arrays
-------------------
Last week we have seen that it is possible to save numpy arrays into text files that can be read by any editor. This means that the information will be converted to ascii (or Unicode) and then written to a file. It is very easy to calculate how much space it will take, based on the number of digits that you are storing. Numpy also offers another way of storing data, in binary format.

What we have done in the past was transforming a number to its representation as characters, which will allow us to read it back on the screen. However, sometimes we don't want to read back, we just want our programs to be able to load the information back. Therefore, we could store directly the bytes to disk and not their representation as strings.

Let's start by creating an array and then we save it both as numpy binary and as ascii to compare between them:

.. code-block:: python

    import numpy as np

    a = np.linspace(0, 1000, 1024, dtype=np.uint8)

    np.save('AC_binay', a)

    with open('AC_ascii.dat', 'w') as f:
        for i in a:
            f.write(str(i)+'\n')

You will end up with two different files, one called 'AC_binary.npy' and the other called 'AC_ascii.dat'. The latter can be opened with any text editor, while the first one will give you a very weird looking file. If you compare the size, you will notice that the binary file is using less memory than the ascii file.

First, you have to note something strange about the code above. We are specifying the type of our array to ``np.uint8``, which means that we are using 8-bit integers. With 8-bits you can go up to ``2^8-1``, or ``255``. Moreover, since we are generating a linear space between 0 and 1000 with 1024 elements, each one is going to be rounded off. Anyways, this discussion is for you to start thinking about different data types and what do they mean. If you inspect the ascii file, you will notice that the numbers increase up to 255 and then they start again from 0.

So, we have 1024 numbers, each one taking 8-bits, or equivalently 1 byte. The array, therefore, will take 1KB (1 kilobyte), but the file we are saving is larger than that (around 1.12KB). You can do the math for the ascii file and see that you can predict its size. Let's create, instead, a file with an array of ones:

.. code-block:: python

    import numpy as np

    a = np.ones((1024), dtype=np.uint8)

    np.save('AD_binay', a)

    with open('AD_ascii.dat', 'w') as f:
        for i in a:
            f.write(str(i)+'\n')

The first thing to notice is that the ascii file is now smaller than in the example above. You are saving two characters per element (the 1 and the newline character), while before you could have up to 4 characters per line. However, the numpy binary file has exactly the same size. What happens if you run the code above, but specifying the type of the array as ``np.uint16``?

You will see that the ascii file is still taking the same space, exactly 2KB (or 3KB on Windows). However, the numpy binary format is taking more space, exactly 1KB more. The array itself takes 2KB of memory, and there is an extra 0.12KB, exactly as before. This already gives us a hint of what is going on, but you can keep testing. Change the type to ``np.uint32`` and you will see that the ascii files are still the same size, but the binary file is taking 2KB more than before. Again, you are saving 4KB to a file that takes 4.12KB.

Those extra .12KB that numpy is saving are equivalent to the header we were generating in the previous article. Binary files also need to store context information in order to be interpreted. You also have to notice that what you are storing is not 'just' a number, you are storing also its data type. Next time you read that file, you will have an 8, 16 or 32-bit variable. The ascii file, on the other hand, doesn't have that information.

With these examples, it may even look like that saving ascii files is more efficient than saving binary files. Let's see what happens if you have more than just 1's in your array:

.. code-block:: python

    import numpy as np

    a = np.linspace(0,65535,65536, dtype=np.uint16)
    np.save('AE_binay', a)
    with open('AE_ascii.dat', 'w') as f:
        for i in a:
            f.write(str(i)+'\n')

Compare the size of the two files and try to understand why are they so different.

Intro to Pickle
---------------
So far we have discussed how to save strings or numpy arrays to a file. However, Python allows you to define several types of data structures, such as lists, dictionaries, custom objects, etc. You can think about how to transform a list into a series of strings and use the opposite operation to recover the variable. This is what we have done when writing arrays to plain text files.

However, this is very cumbersome, because is very susceptible to small changes. For example, it is not the same saving a list of numbers than a list that mixes numbers and strings. Fortunately, Python comes with a package that allows us to save almost everything we want, called **Pickle**. Let's first see it in action and then discuss how it works.

Imagine you have a list that mixes some numbers and some strings and you want to save them to a file, you can do the following:

.. code-block:: python

    import pickle

    data = [1, 1.2, 'a', 'b']

    with open('AF_custom.dat', 'wb') as f:
        pickle.dump(data, f)

If you try to open the file *AF_custom.dat* with a text editor you will see a collection of strange characters. It is important to note that we have opened the file as ``wb``, meaning that we are writing just as before, but that the file is opened in binary format. This is what allows Python to write a stream of bytes to a file.

If you want to load the data back into Python, you can do the following:

.. code-block:: python

    with open('AF_custom.dat', 'rb') as f:
        new_data = pickle.load(f)

    print(new_data)

Again, check that we have used ``rb`` instead of just ``r`` for opening the file. Then you just load the contents of ``f`` into a variable called ``new_data``.

Pickle is transforming an object, in the example above a list, into a series of bytes. That procedure is called serialization. The algorithm responsible for serializing the information is particular to Python and therefore it is not compatible out of the box with other programming languages. In the context of Python, serializing an object is called *pickling* and when you deserialize it is called *unpickling*.

Pickling numpy arrays
---------------------
You can use Pickle to save other kinds of variables. For example, you can use it to store a numpy array. Let's compare what happens when you use the default numpy ``save`` method and Pickle:

.. code-block:: python

    import numpy as np
    import pickle

    data = np.linspace(0, 1023, 1000, dtype=np.uint8)

    np.save('AG_numpy', data)

    with open('AG_pickle.dat', 'wb') as f:
        pickle.dump(data, f)

As in the examples earlier, the numpy file will take exactly 1128 bytes. 1000 are for the data itself and 128 are for the extra information. The pickle file will take 1159 bytes, which is not bad at all, considering that it is a general procedure and not specific to numpy.

To read the file, you do exactly the same as before:

.. code-block:: python

    with open('AG_pickle.dat', 'rb') as f:
        new_data = pickle.load(f)

    print(new_data)

If you check the data you will see that it is actually a numpy array. If you run the code in an environment in which numpy is not installed, you will see the following error:

.. code-block:: bash

    Traceback (most recent call last):
      File "AG_pickle_numpy.py", line 14, in <module>
        new_data = pickle.load(f)
    ModuleNotFoundError: No module named 'numpy'

So, you already see that pickle is doing a lot of things under the hood, like trying to import numpy.

Pickling Functions
------------------
To show you that Pickle is very flexible, you will see how you can store functions. Probably you already heard that everything in Python is an object, and Pickle is, in fact, a way of serializing objects. Therefore it doesn't really matter what it actually is that you are storing. For a function, you would have something like this:

.. code-block:: python

    def my_function(var):
        new_str = '='*len(var)
        print(new_str+'\n'+var+'\n'+new_str)

    my_function('Testing')

Which is a simple example of a function. It surrounds the text with ``=`` signs. Storing this function is exactly the same as storing any other object:

.. code-block:: python

    import pickle

    with open('AH_pickle_function.dat', 'wb') as f:
        pickle.dump(my_function, f)

And to load it and use it you would do:

.. code-block:: python

    with open('AH_pickle_function.dat', 'rb') as f:
        new_function = pickle.load(f)

    new_function('New Test')

Limitations of Pickle
---------------------
In order for Pickle to work, you need to have available the definition of the object you are pickling. In the examples above, you have seen that you need to have numpy installed in order to unpickle an array. However, if you try to unpickle your function from a different file than the one you used to create it, you will get the following error:

.. code-block:: bash

    Traceback (most recent call last):
      File "<stdin>", line 2, in <module>
    AttributeError: Can't get attribute 'my_function' on <module '__main__' (built-in)>

If you want to unpickle a function in a different file (as most likely is going to be the case), you can do the following:

.. code-block:: python

    import pickle
    from AH_pickle_function import my_function

    with open('AH_pickle_function.dat', 'rb') as f:
        new_function = pickle.load(f)

Now, of course, you can wonder what is the use of this. If you imported ``my_function``, you don't need to load the pickled file. And this is true. Storing a function or a class doesn't make a lot of sense, because in any case, you have it defined. The biggest difference is when you want to store an instance of a class. Let's define a class that stores the time at which it is instantiated:

.. code-block:: python

    import pickle
    from time import time
    from datetime import datetime

    class MyClass:
        def __init__(self):
            self.init_time = time()

        def __str__(self):
            dt = datetime.fromtimestamp(self.init_time)
            return 'MyClass created at {:%H:%M on %m-%d-%Y}'.\
                format(dt)

    my_class = MyClass()
    print(my_class)

    with open('AI_pickle_object.dat', 'wb') as f:
        pickle.dump(my_class, f)

If you do this, you will have an object that stores the time at which it was created and if you ``print`` that object, you will see the date nicely formatted. Pay attention also to the fact that that you are saving ``my_class`` and not ``MyClass`` to the pickled file. This means that you are saving an instance of your class, with the attributes that you have defined.

From a second file, you would like to load what you have saved. You need to import the ``MyClass`` class, but the instance itself will be what you saved:

.. code-block:: python

    import pickle
    from AI_pickle_object import MyClass


    with open('AI_pickle_object.dat', 'rb') as f:
        new_class = pickle.load(f)

    print(new_class)

Notice that we are not importing ``time`` nor ``datetime``, just ``pickle`` for loading the object and the class itself. Pickle is a great tool when you want to save the specific state of an object in order to keep up with the work later.

Risks of Pickle
---------------
If you look around, you will definitely find a lot of people warning the Pickle is not safe to use. The main reason is that when you unpickle, arbitrary code could be executed on the machine. If you are the only one using the files, or you definitely trust the one who gave you the file, there will be no problems. If you are building an online service, however, unpickling data that was sent by a random user may have consequences.

When Pickle runs, it will look for a special method on the class called ``__reduce__`` that specifies how an object is pickled and unpickled. Without entering too much into detail, you can specify a callable that will be executed while unpickling. In the example above, you can add the extra method to ``MyClass``:

.. code-block:: python

    class MyClass:
        def __init__(self):
            self.init_time = time()

        def __str__(self):
            dt = datetime.fromtimestamp(self.init_time)
            return 'MyClass created at {:%H:%M:%S on %m-%d-%Y}'.\
                format(dt)

        def __reduce__(self):
            return (os.system, ('ls',))

Run the code again to save the pickled file. If you run the file to load the pickled object you will see that all the contents of the folder in which you executed the script are shown. **Windows** users may not see it happening because depending on whether you use Power Shell or CMD, the command ``ls`` is not defined.

This is a very naïve example. Instead of ``ls`` you could erase a file, open a connection to an external attacker, send all the files to a server, etc. You can see that if you open the door to others to execute commands in your computer, eventually something very bad is going to happen.

The scenario of a security risk with Pickle is extremely low for the vast majority of end users. The most important thing is to trust the source of your pickled files. If it is yourself, a colleague, etc. then you should fine. If the source of your pickled files is not trustworthy, you should be aware of the risks.

You may wonder why Python opens this security risk. The answer is that by being able to define how to unpickle an object, you can become much more efficient at storing data. The idea is that you can define how to reconstruct an object and not necessarily all the information that it contains. In the case of the numpy arrays, imagine you define a matrix of 1024X1024 elements, all ones (or zeroes). You can store each value, which will take a lot of memory, or you can just instruct Python to run numpy and create the matrix, which doesn't take that much space (is only one line of code).

Having control is always better. If you want to be sure that nothing bad is going to happen, you have to find other ways of serializing data.

.. note:: If you are using Pickle as in the examples above, you should consider changing ``pickle`` for ``cPickle`` which is the same algorithm but written directly in C and runs much faster.

Serializing with JSON
---------------------
The main idea behind serialization is that you transform an object into something else, that can be 'easily' stored or transmitted. Pickle is a very convenient way but with some limitations regarding security. Moreover, the results of Pickle are not human readable, so it makes it harder to explore the contents of a file.

JavaScript Object Notation, or JSON for short, became a popular standard for exchanging information with web services. It is a definition on how to structure strings that can be later converted to variables. Let's first see a simple example with a dictionary:

.. code-block:: python

    import json

    data = {
        'first': [0, 1, 2, 3],
        'second': 'A sample string'
    }

    with open('AK_json.dat', 'w') as f:
        json.dump(data, f)

If you open the file you will notice that the result is a text file that can be easily read with a text editor. Moreover, you can quickly understand what the data is just by looking at the contents of the file. You can also define more complex data structures, such as a combination of lists and dictionaries, etc. To read back a json file, you can do the following:

.. code-block:: python

    with open('AK_json.dat', 'r') as f:
        new_data = json.load(f)

Json is very handy because it can structure the information in such a way that can be shared with other programming languages, transmitted over the network and easily explored if saved to a file. However, if you try to save an instance of a class, you will get an error like this:

.. code-block:: bash

    TypeError: Object of type 'MyClass' is not JSON serializable

JSON will not work with numpy arrays out of the box either.

Combining JSON and Pickle
-------------------------
As you have seen, JSON is a way of writing text to a file, structured in a way that makes it easy to load back the information and transform it to a list, a dictionary, etc. On the other hand, Pickle transforms objects into bytes. It would be great to combine both, to write the bytes to a text file. Combining plain text and bytes can be a good idea if you would like to explore parts of the file by eye while keeping the possibility of saving complex structures.

What we are after is not that complex. We need a way of transforming bytes into an ASCII string. If you remember the discussion at the beginning of this article, there is a standard called ASCII that transforms bytes into characters that you can read. When the internet started to catch up, people needed to transfer more than just plain words. Therefore, a new standard appeared, in which you can translate bytes into characters. This is called ``Base64`` and is supported by most programming languages, not just Python.

As an example, we will generate a numpy array, we will pickle it and then we are going to create a dictionary that holds that array and the current time. The code looks like this:

.. code-block:: python

    import pickle
    import json
    import numpy as np
    import time
    import base64

    np_array = np.ones((1000, 2), dtype=np.uint8)
    array_bytes = pickle.dumps(np_array)
    data = {
        'array': base64.b64encode(array_bytes).decode('ascii'),
        'time': time.time(),
    }

    with open('AL_json_numpy.dat', 'w') as f:
        json.dump(data, f)

.. note:: In the example above, we are using ``pickle.dumps`` instead of ``pickle.dump``, which returns the information instead of writing it to a file.

You can go ahead and look at the file. You will see that you can read some parts of it, like the words 'array' and the time at which it was created. However, the array itself is a sequence of characters that don't make much sense. If you want to load the data back, you need to repeat the steps in the opposite order:

.. code-block:: python

    import pickle
    import base64
    import json

    with open('AL_json_numpy.dat', 'r') as f:
        data = json.load(f)


    array_bytes = base64.b64decode(data['array'])

    np_array = pickle.loads(array_bytes)
    print(data['time'])
    print(np_array)
    print(type(np_array))

The first step is to open the file and read it. Then, you grab the base64 encoded pickle and decode it. The output is directly the pickled array, which you proceed to unpickle. You can print the values and see that effectively you have recovered the numpy array.

At this point, there are two questions that you may be asking yourself. Why going through the trouble of pickling, encoding and serializing through json instead of just pickling the ``data`` dictionary. And why have we pickled first the array and then encoded in base 64 instead of writing the output of pickle.

First, going to the trouble is justified if you look at your data with other programs. Having files which store extra information that can be easily read is very handy to quickly decide if it is the file you want to read or not. For example, you can open the file with a text editor, see that the date is not the one you were interested in and move forward.

The second question is a bit deeper. Remember that when you are writing to a plain text file, you are assuming a certain encoding. The most common one nowadays being utf-8. This limits a lot the way in which you can write bytes to disk because you have only a finite set of characters you can use. Base64 takes care of using just the allowed characters.

However, you have to remember that base64 was developed to transmit data over the network a long time ago. That makes base64 slower and less memory efficient than what it could be. Nowadays you don't need to be limited by the ascii specification thanks to Unicode. However, sticking to standards is a good practice if you want compatibility of your code in different systems.

Other Serialization Options
---------------------------
We have seen how to serialize objects with Pickle and JSON, however, they are not the only two options. There are no doubts that they are the most popular ones, but you may face the challenge of opening files generated by other programs. For instance, LabView normally uses XML instead of JSON to store data.

While JSON translates very easily to python variables, XML is a bit more complicated. Normally, XML files come from an external source, such as a website or another program. To load the data on those files, you need to rely on `ElementTree <https://docs.python.org/3/library/xml.etree.elementtree.html>`_. Check the link to see the official documentation to see how it works.

Another option is YAML. It is a simple markup language that, such as Python, uses spaces to delimit blocks of content. The advantage of YAML is that it is easy to type. For instance, imagine that you are using text files as input for your program. While you respect the tabbing, the file will be easily parsed. A YAML file looks like this:

.. code-block:: yaml

    data:
      creation_date: 2018-08-08
      values: [1, 2, 3, 4]

To read the file, you need to install a package called PyYAML, simply with ``pip``:

.. code-block:: bash

    pip install pyyaml

And the script to read looks like this:

.. code-block:: python

    import yaml

    with open('AM_example.yml', 'r') as f:
        data = yaml.load(f)

    print(data)

You can also write a yaml file:

.. code-block:: python

    import yaml
    from time import time

    data = {
        'values': [1, 2, 3, 4, 5],
        'creation_date': time(),
    }

    with open('AM_data.yml', 'w') as f:
        yaml.dump(data, f)

It is beyond the scope of this article to discuss YAML, but you can find a lot of information online. YAML is still not a standard, but it is gaining traction. Writing configuration files in YAML feels very natural. There is much less typing involved than with XML and it looks more organized, at least to me than JSON.

Conclusions
-----------
In this article, we have discussed serialization of objects and how to store them on the hard drive. We have started discussing what an encoding is, and started to think about converting from and to bytes. This opened the door to understand what Pickle does and how to save the data to disk.

Remember that Pickle is not perfect and you have to be aware of its limitations, especially if you are going to deal with user submitted files, such as what happens on a web server. On the other hand, if you are using it for storing data for yourself, it is a very efficient way.

We have also discussed how to use JSON, a very popular tool for web technologies. The limit of JSON is, however, that you have to store data as text files, thus limiting its native capabilities. Fortunately, combining ``Pickle`` and ``base64``, you can transform bytes to an ascii string and save it next to easy to read metadata.

This article has gone much more in depth regarding how to store data in different formats, but the topic is far from complete. Keep tuned to find more articles regarding how to save data with Python.

This article is part of a series of articles relating to data storage with Python. The other articles are:

* `Introduction to Storing Data in Files <{filename}13_storing_data.rst>`_
* `Storing Binary Data and Serializing <{filename}14_Storing_data_2.rst>`_
* `Using Databases to Store Data <{filename}15_Storing_data_3.rst>`_
* `Using HDF5 Files with Python <{filename}02_HDF5_python.rst>`_


Header photo by `Joshua Sortino <https://unsplash.com/photos/LqKhnDzSF-8?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText>`_ on Unsplash