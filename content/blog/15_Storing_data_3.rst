Storing Data with SQLite
========================

:date: 2018-08-12
:author: Aquiles Carattino
:subtitle: Learn different ways of storing data in your projects
:header: {attach}tobias-fischer-185901-unsplash.jpg
:tags: Data, Storing, SQLite, HDF5, ascii, json, Data Storage
:description: Learn different ways of storing data in your projects

This article is part of a series of articles relating to data storage with Python. The other articles are:

* `Introduction to Storing Data in Files <{filename}13_storing_data.rst>`_
* `Storing Binary Data and Serializing <{filename}14_Storing_data_2.rst>`_
* `Using Databases to Store Data <{filename}15_Storing_data_3.rst>`_
* `Using HDF5 Files with Python <{filename}02_HDF5_python.rst>`_

Using databases for storing data may sound much more complicated than what it actually is. In this article, we are going to cover how to use databases to store different types of data. We will quickly review how you can search for specific parameters and how to get exactly what you want.

In the previous articles, we have seen how to store data into plain text files, which is nothing more than a particular way of serializing our objects. On the second release, we have seen how to serialize complex objects using Python's built-in tools to save them as binary files. In this article, we are going to explore another very useful module called **SQLite** which will allow us to store data in databases.

.. contents::

Databases
---------
Most likely you have heard about databases in the context of websites. It is where your username, email, and password are stored. It is where the government saves all the information it has about you. However, databases can also be used for smaller scale projects, such as a software for controlling devices in the laboratory or for data analysis.

The simplest form of a database can be thought as a table with columns and rows. If you have ever used a spreadsheet, it looks exactly like that. Pandas' Data Frames have the same format. Tables with a header for each column and a different entry on each row. This really forces you to be systematic in the way in which you store your information.

Interacting with databases is a complex subject because it normally involves learning a new scripting language in order to store and retrieve information. In this tutorial, you are going to learn the basics of one of these languages called SQL. Just with the basics, there is a lot that you can achieve.

Something important to point out is that normally you need to install more software in order to use a database. If you have ever heard of MySQL or Postgres, you are probably aware that those are big libraries that need an entire course on themselves. However, Python bundles SQLite, a very simple, single-file database. No extra software needed to run the examples here.

Creating a Table
----------------
Let's start quickly with SQLite. The first thing you need to do to work with databases is to create the database itself. In the case of SQLite, this is going to be a file. It is as easy as this:

.. code-block:: python

    import sqlite3

    conn = sqlite3.connect('AA_db.sqlite')
    conn.close()

When you use ``connect``, SQLite will try to open the file that you are specifying and if it doesn't exist, it will create a new one. Once you have the database, you need to create a table in it. This is where the SQL language that I mentioned before comes into play. Let's assume you want to create a table that stores two variables, the description of an experiment and the name of the person who performed it. You would do the following:

.. code-block:: python

    import sqlite3

    conn = sqlite3.connect('AA_db.sqlite')
    cur = conn.cursor()
    cur.execute('CREATE TABLE experiments (name VARCHAR, description VARCHAR)')
    conn.commit()

    conn.close()

After opening (or creating) the database, we have to create a cursor. The cursor is going to allow you to execute the SQL code. To create a table, we need to use the following command:

.. code-block:: sql

    CREATE TABLE experiments (name VARCHAR, description VARCHAR)

It is quite descriptive: you are creating a table called experiments with two columns: ``name`` and ``description``. Each one of those columns will be of type ``VARCHAR``. Don't worry too much about it right now. The ``commit`` command saves the changes to the database and then you close the connection. Congratulations, you have created your first table!

The problem right now is that there is no feedback on what you have done. If you are using PyCharm, for example, it comes with a built-in SQLite implementation. Therefore, you can just click on the file and you will be able to navigate through the contents of the database. You can also try an application like `SQLite browser <https://sqlitebrowser.org/>`_ to visualize the files. There is also a `Firefox Add-On <https://addons.mozilla.org/en-US/firefox/addon/sqlite-manager/?src>`_.

.. note:: The extension .sqlite is not mandatory. If you use it, many higher level programs will identify it as a database and will be able to open it with a double-click. You can also use the .db extension, which is more common if following Flask or Django tutorials.

Adding Data to a Database
-------------------------
Now that you have a database, is time to store some data into it. All the examples always start by creating a connection and a cursor, which we are going to skip from now on, but you should include in your code. Adding information to a database also involves the use of SQL. You will need to do the following:

.. code-block:: python

    cur.execute('INSERT INTO experiments (name, description) values ("Aquiles", "My experiment description")')
    conn.commit()

You can run this command as many times as you want, and if you are checking your database with an external tool, you will see that you keep adding rows to the table. As you see above, the SQL code can give rise to problems if you are using variables instead of plain text.

Imagine that you try to save a string that includes the character ``"``. SQL will think that the ``"`` from your variable is actually closing the argument and it will give an error. Even worse, if it is a variable submitted by someone else, this can give rise to something called SQL injection. In the same way, in which Pickle can be used to run arbitrary code, SQL can be tricked to perform unwanted operations. Soon enough you will be able to understand the `XKCD SQL injection joke <https://xkcd.com/327/>`_.

A proper way of adding new values to a table is:

.. code-block:: python

    cur.execute('INSERT INTO experiments (name, description) VALUES (?, ?)',
                ('Another User', 'Another Experiment, even using " other characters"'))
    conn.commit()

Assuming that the access to the database is only yours, i.e. you are not going to take variables from the public, you shouldn't worry too much about safety. In any case, it is important to be aware.

.. newsletter::

Retrieving Data
---------------
Now that you have some data stored in the database, we need to be able to retrieve it. You can do the following:

.. code-block:: python

    cur.execute('SELECT * FROM experiments')
    data = cur.fetchall()

The first line is asking for all the columns from experiments. That is what the ``*`` means. The second line is actually getting the values. We have used ``fetchall()``, but you could have also used ``fetchone()`` to get just one element.

So far, nothing particularly special. Imagine that you want to get only the entries where a particular user was involved. You can do the following:

.. code-block:: python

    cur.execute('SELECT * FROM experiments WHERE name="Aquiles"')
    data_3 = cur.fetchall()

.. note:: SQL is not case sensitive for its commands. SELECT or select or Select mean the same. However, if you change Aquiles for aquiles, the results are going to be different.

Of course, it can also happen that there are no entries matching your criteria and therefore the result is going to be an empty list. Again, remember that what we are looking for, ``Aquiles`` may be a variable, and again you are exposed to SQL errors if you have special characters.

At this point, there are two concerns that may have come up to your mind. On one hand, there is no way to refer to specific entries in the database. Two different entries, with the same content, are indistinguishable from each other.

The other is more of a feature request. Imagine that you would like to store more information about the user, not just the name. It doesn't make sense to add extra columns to the experiments database, because we would be duplicating a lot of information. Ideally, we would start a new table, just to register users and their information.

Adding a Primary Key
--------------------
If you have ever seen any spreadsheet program or even a Pandas Data Frame, you have probably noticed that every row is identified with a number. This is very handy because once you learn that the important information is on line N, you just remember that number and retrieve the data specifically.

The table that we have created does not include this numbering, also known as a primary key. Adding a new column is normally not a problem, but since we are dealing with a primary key, SQLite does not allow us to do it in a single step. We should create a new table, copy the contents of the old one, etc. Since we only have toy data, we can start from scratch.

First, we will remove the table from the database, losing all its contents. Then we will create a new table, with its primary key and we will add some content to it. We can do everything with a very long SQL command instead of running multiple ``cur.execute()``. For that, we use the triple-quote notation of Python:

.. code-block:: python

    sql_command = """
    DROP TABLE IF EXISTS experiments;
    CREATE TABLE experiments (
        id INTEGER,
        name VARCHAR,
        description VARCHAR,
        PRIMARY KEY (id));
    INSERT INTO experiments (name, description) values ("Aquiles", "My experiment description");
    INSERT INTO experiments (name, description) values ("Aquiles 2", "My experiment description 2");
    """
    cur.executescript(sql_command)
    conn.commit()

The important part here is the SQL command. First, we drop the table if it exists. If it doesn't exist, it will throw an error and the rest of the code will not be executed. Then, we create a new table, with one new column called ``id``, of type integer. At the end of the statement, we defined that ``id`` as the primary key of the table. Finally, we add two elements to the table.

If you run the retrieval code again, you will notice that each element has a unique number that identifies it. If we want to fetch the first (or the second, etc.) element, we can simply do the following:

.. code-block:: python

    cur.execute('SELECT * FROM experiments WHERE id=1')
    data = cur.fetchone()

Notice that we are using ``fetchone`` instead of ``fetchall`` because we know that the output should be only one element. Check what is the difference if you use one or the other command in the data that you get from the database.

Adding a primary key is fundamental to decrease the time it takes to fetch the data that you are looking for. Not only because it allows you to refer to specific entries, but also because of how databases work, it is much faster addressing data by their key.

Default Values for Fields
-------------------------
So far we have used only two types of variables: ``VARCHAR`` and ``INTEGER``. The varchar has been used for the name of the person doing the experiment and its description, while the integer is used only for the ``id`` number. However, we can develop much more complex tables. For example, we can specify not only the type but also limits to the length. We can also specify default values, simplifying the operations when storing new entries to a table. One of the advantages of doing this is that our data is going to be very consistent.

Imagine that you want to store also the date at which the experiment is run, you could add an extra field and every time you create a new experiment, you also add a field with the date, or you instruct the database to automatically add the date. At the moment of creating the table, you should do the following:

.. code-block:: sql

    DROP TABLE IF EXISTS experiments;
    CREATE TABLE experiments (
        id INTEGER,
        name VARCHAR,
        description VARCHAR,
        perfomed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (id));
    INSERT INTO experiments (name, description) values ("Aquiles", "My experiment description");
    INSERT INTO experiments (name, description) values ("Aquiles 2", "My experiment description 2");

Note the new field called ``performed_at``, which uses ``TIMESTAMP`` as its type, and it also specifies a ``DEFAULT`` value. If you check the two inserted experiments (you can use the code of the previous example) you will see that there is a new field with the current date and time. You can also add default values for other fields, for example:

.. code-block:: sql

    CREATE TABLE experiments (
        id INTEGER,
        name VARCHAR DEFAULT "Aquiles",
        description VARCHAR ,
        perfomed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (id));

Next time you add a new experiment, if you don't specify the user who performed it, it will default to ``Aquiles`` (my name). Specifying defaults is a very useful way of avoiding missing information. For example, the ``performed_at`` will always be added. This ensures that even if someone forgets to explicitly declare the time of an experiment, at least a very reasonable assumption has been made.

SQLite Data Types
-----------------
SQLite is different from other database managers, such as MySQL or Postgres because of its flexibility regarding data types and lengths. SQLite defines only `4 types of fields <https://www.sqlite.org/datatype3.html>`_:

* NULL. The value is a NULL value.
* INTEGER. The value is a signed integer, stored in 1, 2, 3, 4, 6, or 8 bytes depending on the magnitude of the value.
* REAL. The value is a floating point value, stored as an 8-byte IEEE floating point number.
* TEXT. The value is a text string, stored using the database encoding (UTF-8, UTF-16BE or UTF-16LE).
* BLOB. The value is a blob of data, stored exactly as it was input.

And then it defines something called affinities, which specifies the preferred type of data to be stored in a column. This is very useful to maintain compatibility with other database sources and can generate some headaches if you are following tutorials designed for other types of databases. The type we have used, ``VARCHAR`` is not one of the specified datatypes, but it is supported through the affinities. It will be treated as a ``TEXT`` field.

The way SQLite manages data types, if you are new to databases, is not important. If you are not new to databases, you should definitely look at the `official documentation <https://www.sqlite.org/datatype3.html>_` in order to understand the differences and make the best out of the capabilities.

Relational Databases
--------------------
Perhaps you have already heard about relational databases. So far, in the way we have used SQLite, it is hard to see advantages compared to plain CSV files, for example. If you are just storing a table, then you could perfectly do the same with a spreadsheet or a Pandas Data Frame. The power of databases is much more noticeable when you start making relationships between fields.

In the examples that we have discussed earlier, you have seen that when you run an experiment you would like to store who was to the user performing the measurement. The number of users is most likely going to be limited and perhaps you would like to keep track of some information, such as the name, email and phone number.

The way to organize all of this information is by creating a table in which you store the users. Each entry will have a primary key. From the table experiments, instead of storing the name of the user, you store the key of the user. Moreover, you can specify that, when creating a new experiment, the user associated with the experiment already exists. All this is achieved through the use of foreign keys, like this:

.. code-block:: sql

    DROP TABLE IF EXISTS experiments;
    DROP TABLE IF EXISTS users;
    CREATE TABLE  users(
        id INTEGER,
        name VARCHAR,
        email VARCHAR,
        phone VARCHAR,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (id));
    CREATE TABLE experiments (
        id INTEGER,
        user_id INTEGER,
        description VARCHAR ,
        perfomed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (id)
        FOREIGN KEY (user_id) REFERENCES users(id));

.. warning:: depending on your installation of SQLite, you may need to add support for foreign keys. Run the following command when creating the database to be sure: ``cur.execute("PRAGMA foreign_keys = ON;")``

First, you need to create a new user, for example:

.. code-block:: sql

    INSERT INTO users (name, email, phone) values ("Aquiles", "example@example.com", "123456789");

And then you can create a new experiment:

.. code-block:: sql

    INSERT INTO experiments (user_id, description) values (1, "My experiment description");

Note that if you try to add an experiment with a user_id that does not exist, you will get an error:

.. code-block:: sql

    INSERT INTO experiments (user_id, description) values (2, "My experiment description");

When you run the code above using Python, you will get the following message:

.. code-block:: bash

    sqlite3.IntegrityError: FOREIGN KEY constraint failed

Which is exactly what we were expecting. Note, however, that if you leave the ``user_id`` out, i.e., if you don't specify a value, it will default to ``Null``, which is valid (an experiment without a user). If you would like to prevent this behavior, you will need to specify it explicitly:

.. code-block:: sql

    CREATE TABLE experiments (
        id INTEGER,
        user_id INTEGER NOT NULL ,
        description VARCHAR ,
        perfomed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (id)
        FOREIGN KEY (user_id) REFERENCES users(id));

Now we have specified that the ``user_id`` is ``NOT NULL``. If we try to run the following code:

.. code-block:: sql

    INSERT INTO experiments (description) values ("My experiment description 2");

It will raise the following error:

.. code-block:: bash

    sqlite3.IntegrityError: NOT NULL constraint failed: experiments.user_id

Storing Numpy Arrays into Databases
-----------------------------------
Storing complex data into databases is not a trivial task. Databases specify only some data types and numpy arrays are not between them. This means that we have to convert the arrays into something that can be stored in a database. Since SQLite specifies only 4 major data types, we should stick to one of them. In the `previous article <{filename}14_Storing_data_2.rst>`_ we have discussed a lot about serialization. The same ideas can be used to store an array in a database.

For example, you can use Pickle in order to transform your data into bytes and store them using base64 as a ``TEXT`` field. You could also store the Pickle object directly into a ``BLOB``field. You can convert your array into a list and separate its values with ``,`` or use a specific notation to separate rows and columns, etc. However, SQLite offers also the possibility of registering new data types. As explained in `this answer on Stack Overflow <https://stackoverflow.com/a/18622264/4467480>`_ we need to create an adapter and a converter:

.. code-block:: python

    import sqlite3
    import numpy as np
    import io

    def adapt_array(arr):
        out = io.BytesIO()
        np.save(out, arr)
        out.seek(0)
        return sqlite3.Binary(out.read())

    def convert_array(text):
        out = io.BytesIO(text)
        out.seek(0)
        return np.load(out)

    sqlite3.register_adapter(np.ndarray, adapt_array)
    sqlite3.register_converter("array", convert_array)

What we are doing in the code above is to tell SQLite what to do when a field of type ``array`` is declared. When we are storing the field, it will be transformed into bytes, that can be stored as a BLOB in the database. When retrieving the data, we are going to read the bytes and transform them into a numpy array. Note that this is possible because the methods ``save`` and ``load`` know how to deal with bytes when saving/loading.

It is important to note that it is not necessary to register both adapter and converter. The first one is responsible for transforming a specific data type into an SQLite-compatible object. You could do this to automatically serialize your own classes, etc. The converter is responsible for converting back into your object. You can play around and see what happens when you don't register one of the two.

When you define your table, you can use your newly created 'array' data type:

.. code-block:: sql

    DROP TABLE IF EXISTS measurements;
    CREATE TABLE measurements (
        id INTEGER PRIMARY KEY,
        description VARCHAR ,
        arr array);

It is important to note that for the above code to work when you start the connection with the database, you should add the following:

.. code-block:: python

    conn = sqlite3.connect('AI_db.sqlite', detect_types=sqlite3.PARSE_DECLTYPES)

The option ``PARSE_DECLTYPES`` is telling SQLite to use the registered adapters and converters. If you don't include that option, it will not use what you have registered and will default to the standard data types.

To store the array, you can do the following:

.. code-block:: python

    x = np.random.rand(10,2)
    cur.execute('INSERT INTO measurements (arr) values (?)', (x,))
    cur.execute('SELECT arr FROM measurements')
    data = cur.fetchone()
    print(data)

This will transform your array into bytes, and it will store it in the database. When you read it back, it will transform the Bytes back into an array.

What you have to keep in mind is that when you store numpy arrays (or any non-standard object) into a database, you lose the intrinsic advantages of databases, i.e. the capabilities to operate on the elements. What I mean is that with SQL it is very easy to replace a field in all the entries that match a criterion, for example, but you won't be able to do that for a numpy array, at least with SQL commands.

Combining Information
---------------------
So far, we have seen how to create some tables with values, and how to relate them through the use of primary and foreign keys. However, SQL is much more powerful than that, especially when retrieving information. One of the things that you can do is to join the information from different tables into a single table. Let's see quickly what can be done. First, we are going to re-create the tables with the experiments and the users, as we have seen before. You can check the `code in here <https://github.com/PFTL/website/blob/master/example_code/15_databases/AH_foreign_key.py>`_. You should have two entries for users and two entries for the experiments.

You can run the following code:

.. code-block:: python

    import sqlite3

    conn = sqlite3.connect('AH_db.sqlite')
    cur = conn.cursor()

    sql_command = """
    SELECT users.id, users.name, experiments.description
    FROM experiments
    INNER JOIN users ON experiments.user_id=users.id;
    """
    cur.execute(sql_command)
    data = cur.fetchall()

    for d in data:
        print(d)

What you will see printed is the id of the user, the name and the description of the experiment. This is much handier than just seeing the id of the user because you immediately see the information that you need. Moreover, you can filter the results based on the properties of either of the tables. Imagine you want to get the experiments performed by ``'Aquiles'``, but you don't know its user id. You can change the command above to the following:

.. code-block:: sql

    SELECT users.id, users.name, experiments.description
        FROM experiments
        INNER JOIN users ON experiments.user_id=users.id
        WHERE users.name="Aquiles";

And you will see that only the data related to that user is retrieved.

Join statements are complex and very flexible. You probably noticed that we have used the ``INNER JOIN`` option, but it is not the only possibility. If you want to combine tables that are not related through a foreign key, for example, you would like to combine data from different sources that belong to the same day, you can use other types of joins. The diagram in `this website <https://www.w3schools.com/sql/sql_join.asp>`_ is very explicit, but going through the details exceeds the capabilities of an introductory tutorial.

How to Use Databases in Scientific Projects
-------------------------------------------
Leveraging the power of databases is not obvious for first-time developers, especially if you don't belong to the web-development realm. One of the main advantages of databases is that you don't need to keep in memory the entire structure. For example, Imagine that you would have a very large project, with millions of measurements of thousands of experiments with hundreds of users. Most likely you can't load all the information as in memory variables.

By using databases, you will be able to filter the measurements done by a specific user in a given time frame, or that match a specific description without actually loading everything into memory. Even if simple, this example already shows you a very clear use case where Data Frames or numpy arrays would fail.

Databases are used in many large-scale scientific projects, such as astronomical observations, simulations, etc. By using databases, different groups are able to give users access to filtering and joining capabilities, getting the desired data and not the entire collection. Of course, for small groups, it may look like an overshoot. But imagine that you could filter through your data, acquired during years, to find a specific measurement.

Conclusions
-----------
One of the main challenges of using databases is that they require learning a new language called SQL. In this article we have tried to point to the most basic concepts, that would allow anyone to get started and build his/her way up through clever Google searches.

Python has built-in support for SQLite, a file-based database that is ideal for getting started. There is no further setting up involved, everything works out of the box, and many of the tutorials that can be found online relating to SQL will also work with SQLite.

Using databases for one-off projects may be an overkill, but for long-running programs, such as software for controlling setups or custom data analysis it may open the door to very creative solutions. Combining databases for metadata and files for data has the added advantage of a high portability (sharing data is sharing just a file) and an easy way to search through the collection of metadata stored onto a database.

This article is part of a series of articles relating to data storage with Python. The other articles are:

* `Introduction to Storing Data in Files <{filename}13_storing_data.rst>`_
* `Storing Binary Data and Serializing <{filename}14_Storing_data_2.rst>`_
* `Using Databases to Store Data <{filename}15_Storing_data_3.rst>`_
* `Using HDF5 Files with Python <{filename}02_HDF5_python.rst>`_

Header photo by `Tobias Fischer <https://unsplash.com/photos/PkbZahEG2Ng?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText>`_ on Unsplash