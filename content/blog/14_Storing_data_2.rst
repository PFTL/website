Store Data in Your Python Applications Part 2
=============================================

:status: draft
:date: 2018-07-23
:author: Aquiles Carattino
:subtitle: Learn different ways of storing data in your projects
:header: {attach}tom-hermans-642319-unsplash.jpg
:tags: Data, Storing, sqlite, HDF5, ascii, json
:description: Learn different ways of storing data in your projects

Last week we have seen how to store data into plain text files that can be read by any editor and by other programs. We have also seen that if you separate your data with commas your file will be compatible with other programs, mainly spread sheets. One of the main limitations of this strategy is that if your data contains a comma, your file will not be readable anymore.

In this article we are going to discuss about encoding of data, basically to understand how come that what you save with Python can be read by a normal text editor or your web browser. We will also see that you can save space if you encode your data in the proper way. In the end what you will have is a clear picture of the difference between saving text files and binary data.

.. contents::

What does it really mean to save text files
-------------------------------------------
Last week you have seen different ways of saving text files. One of the most noticeable attributes is that those files can be opened with any basic text editor, you don't need Python to read them. This already should indicate that there is an underlying property that allows programs to share files with each other.

As you have probably heard already, computers don't understand about letters, or colors, they only understand about 1's and 0's. So, there should be a way of translating that information into a letter (or a number, or a color). That is called an encoding. Probably we have already heard about ascii or unicode. Those are standards that specify how to translate from a stream of bytes (i.e. 1's and 0's) to the letters you are seeing now on the screen.

ASCII stands for American Standard Code for Information Interchange. It is a standard that specifies how to translate numbers to characters. If you look at the `ASCII table <https://www.asciitable.com/>`_, you see that it specifies how to translate from 0 to 127 to characters. 128 options is not a random choice, it is 7-bit, or all the combinations that a sequence of 7 1's and 0's can generate. You can see also the extended ascii table, which adds all the characters up to a number of 255 (i.e. 8-bit).

Let's do a quick test. We can create an array of integers between 0 and 255 (8-bit) and store it to a file, and then compare the size of that file with the size of the array. The code will look like this:

.. code-block:: python

    import sys
    import numpy as np

    x = np.linspace(0, 255, 256, dtype=np.uint8)

    with open('AA_data.dat', 'w') as f:
        for data in x:
            f.write(str(data)+'\n')


Each element of the array is 8-bits long (or 1 byte). We are storing 256 elements, and therefore we expect the file to be 256 bytes in size. However, if you check it, you will see that it is bigger than that: around 914 bytes. This difference is not negligible, so where is it coming from?

We have stored 256 elements, but there more numbers in the file. 10 elements are 1-digit long, 90 are 2-digits and 156 are 3-digits long. In total, there are 658 digits, plus 256 new line characters. If you add them up you get exactly 914. This means that each character is taking exactly 1 byte, or 8 bits. If you are on Windows, there is an extra consideration, because the new line character gets replaced by two characters and therefore you need to add 512 characters instead of 256.

When you want to write a ``1``, it takes 1 byte. However, when you store a ``10`` it will take 2 bytes. You have to remember that, in the space of integer numbers of 8 bits, they both take the same amount of memory. With this simple example you start seeing that there are a lot of small issues that you have to take into account when saving data.

Different encodings for text data
---------------------------------
You may have realized in the previous section that ASCII is limited to a special set of characters. If you want to write characters of other languages, for example, such as ñ from Spanish, you will need to resort to other standards. This gave raise to a myriad of different encodings, with a small degree of compatibility between them.

When you open a text file, the program needs to translate from bytes to characters, basically by looking up on a table. If you change the table, you change the output. If you use text editors such as Notepad ++ you will see that you can specify the encoding of the file. If you play with it, you will see that the output may change, especially if there are special characters from other languages.

The problem got worst with websites having users from different countries expecting to use different characters. That is why a superseding standard appeared, called `Unicode <https://en.wikipedia.org/wiki/Unicode>`_. Unicode includes and expands the ascii table up to 32-bit characters, which is billions of different choices. Unicode includes thousands of symbols from modern and ancient languages, plus all the emojis you are already familiar with.

If you want to specify the encoding used while saving a file, you can do the following:

.. code-block:: python

    import codecs

    data_to_save = 'Data to Save'
    with codecs.open('AB_unicode.dat', 'w', 'utf-8') as f:
        f.write(data_to_save)

In the code above, the important part is the line that says ``utf-8``. Unicode has different implementations; each use a different amount of bits per character. You can choose 8, 16 and 32. You can also change the encoding to ``ascii``. Compare how much space it takes every time you save the data. Open the file being saved with a text editor and check if you can see the message.

Saving Numpy Arrays
-------------------
Last week we have seen that it is possible to save numpy arrays into text files that can be read by any editor. This means that the information will be converted to ascii (or unicode) and then written to a file. It is very easy to calculate how much space it will take, based on the number of digits that you are storing. Numpy also offer another way of storing data, in binary format.

Let's start by creating an array and then we save it both as numpy binary and as ascii:

.. code-block:: python

    import numpy as np

    a = np.linspace(0, 1000, 1024, dtype=np.uint8)

    np.save('AC_binay', a)

    with open('AC_ascii.dat', 'w') as f:
        for i in a:
            f.write(str(i)+'\n')

You will end up with two different files, one called 'AC_binary.npy' and the other called 'AC_ascii.dat'. The latter can be opened with any text editor, while the first one will give you a very weird looking file. If you compare the size, you will notice that the binary file is using less memory than the ascii file.

First, you have to note something strange about the code above. We are specifying the type of our array to ``np.uint8``, which means that we are using 8-bit integers. With 8-bits you can go up to ``2^8-1``, or ``255``. Moreover, since we are generating a linear space between 0 and 1000 with 1024 elements, each one is going to be rounded off. Anyways, this discussion is for you to start thinking about different data types and what do they mean. If you inspect the ascii file, you will notice that the numbers increase up to 255 and then they start again from 0.

So, we have 1024 numbers, each one taking 8-bits, or equivalently 1 byte. The array therefore will take 1KB (1 kilobyte), but the file we are saving is larger than that (around 1.12KB). You can do the math for the ascii file and see that you can predict its size. Let's create, instead, a file with an array of ones:

.. code-block:: python

    import numpy as np

    a = np.ones((1024), dtype=np.uint8)

    np.save('AD_binay', a)

    with open('AD_ascii.dat', 'w') as f:
        for i in a:
            f.write(str(i)+'\n')

First thing to notice is that the ascii file is now smaller than in the example above. You are saving two characters per element (the 1 and the newline character), while before you could have up to 4 characters per line. However, the numpy binary file has exactly the same size. What happens if you run the code above, but specifying the type of the array as ``np.uint16``?

You will see that the ascii file is still taking the same space, exactly 2KB (or 3KB on Windows). However, the numpy binary format is taking more space, exactly 1KB more. The array itself takes 2KB of memory, and there is an extra 0.12KB, exactly as before. This already gives us a hint of what is going on, but you can keep testing. Change the type to ``np.uint32`` and you will see that the ascii files is still at the same size, but the binary file is taking 2KB more than before. Again, you are saving 4KB to a file that takes 4.12KB.

Those extra .12KB that numpy is saving are equivalent to the header we were generating in the previous article. Binary files also need to store context information in order to be interpreted. You also have to notice that what you are storing is not 'just' a number, you are storing also its data type. Next time you read that file, you will have an 8, 16 or 32-bit variable. The ascii file, on the other hand, doesn't have that information.

With this examples, it may even seem that saving ascii files is more efficient than saving binary files. Let's see what happens if you have more than just 1's in your array:

.. code-block:: python

    import numpy as np

    a = np.linspace(0,65535,65535, dtype=np.uint16)
    np.save('AE_binay', a)
    with open('AE_ascii.dat', 'w') as f:
        for i in a:
            f.write(str(i)+'\n')

Compare the sized of the two files and try to understand why are they so different.

