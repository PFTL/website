Context Managers: The 'with' command
====================================

:status: draft
:date: 2018-08-12
:author: Aquiles Carattino
:subtitle: Using the with command and developing classes that support it
:header: {attach}tobias-fischer-185901-unsplash.jpg
:tags: Data, Storing, SQLite, HDF5, ascii, json, Data Storage
:description: Using the with command and developing classes that support it

There is a common pattern when programming that is opening a resource, doing something with it and closing it. However, if something goes wrong in your program, for example an exception is raised, you may end up with a resource that is not closed. This is a common scenario when you open files, a network connection or when you communicate with devices.

Python has a command that allows you to open a resource, work with it and guarantee that it is going to be properly closed, even if exceptions arise in your program. In this article I will show you how to use the ``with`` statement with common objects such as files, but also how to develop classes that are able to be instantiated in a ``with`` block.

Opening and Closing Files
-------------------------
If you would like to write a string to a file, you can do the following:

.. code-block:: python

    f = open('My_File.txt', 'w')
    f.write('This goes to the file\n')
    f.close()

The lines above will create a new file every time you run them, and will write a line to it. When the program is done, it closes the file. However, let's consider this other scenario: you have a list and you would like to save each element to a new line. You develop a function for it:

.. code-block:: python

    def save_list_to_file(filename, list):
        f = open(filename, 'w')
        for element in list:
            f.write('{}\n'.format(element))
        f.close()