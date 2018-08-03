Store Data in Your Python Applications Part 3
=============================================

:status: draft
:date: 2018-07-23
:author: Aquiles Carattino
:subtitle: Learn different ways of storing data in your projects
:header: {attach}tom-hermans-642319-unsplash.jpg
:tags: Data, Storing, sqlite, HDF5, ascii, json
:description: Learn different ways of storing data in your projects

Using databases for storing data may sound much more complicated that what it actually means. In this article we are going to cover how to use databases to store different types of data. We will quickly review how you can search for specific parameters and how to get exactly what you want.

In the previous articles we have seen how to store data to plain text files, which is nothing more than a particular way of serializing our objects. On the second release we have seen how to serialize complex objects using Python's built-in tools. In this article we are going to explore another very useful module called SQLite.

.. contents::

Databases
---------
Most likely you have heard about databases in the context of websites. It is where your username, email and password are stored. It is where the government saves all the information it has about you. However, databases can also be used for smaller scale projects, such as a software for controlling devices in the lab or for data analysis.

The simplest form of a database can be thought as a table with columns and rows. If you have ever used a spreadsheet, it looks exactly like that. Pandas' Data Frames have the same format. Tables with a header for each column and a different entry on each row. This really forces you to be systematic in the way in which you store your information.

There are also databases that store information in completely different ways. Those platforms are normally referred to as non-relational databases. Since Python doesn't support that kind of databases out of the box, we are not going to cover them in this tutorial, but it is important for you to know that there are alternatives out there.

Interacting with databases is a complex subject, because it normally involves learning a new scripting language in order to store and retrieve information. In this tutorial you are going to learn the basics of one of these languages called SQL. Just with the basics there is a lot that you can achieve.

Something important to point out is that normally you need to install more software in order to use a database. If you have ever heard of MySQL or Postgres, you are probable aware that those are big libraries that need an entire course on themselves. However, Python bundles SQLite, a very simple, single-file database. No extra software needed to run the examples here.

Creating a Table
----------------
Let's start quickly with SQLite. The first thing you need to do to work with databases is to create a database itself. In the case of SQLite, this is going to be a file. It is as easy as this:

.. code-block:: python

    import sqlite3

    conn = sqlite3.connect('AA_db.sqlite')
    conn.close()

We you use connect, sqlite will try to open the file that you are specifying and if it doesn't exist, it will create a new one. Once you have the database, you need to create a table in it. This is where the SQL language that I mentioned before comes into play. Let's assume you want to create a table that stores two variables, the description of an experiment and the name of the person who performed it. You would do the following:

.. code-block:: python

    import sqlite3

    conn = sqlite3.connect('AA_db.sqlite')
    cur = conn.cursor()
    cur.execute('CREATE TABLE experiments (name STRING, description STRING)')
    conn.commit()

    conn.close()

After opening (or creating) the database, we have to create a cursor. The cursor is going to allow you to execute the SQL code. To create a table, we need to use the following command:

.. code-block:: sql

    CREATE TABLE experiments (name STRING, description STRING)

It is quite descriptive: you are creating a table called experiments with two columns: ``name`` and ``description``. Each one of those columns will be of type ``STRING``. Don't worry to much about it right now. Right after you run the ``commit`` command in order to save the changes to the database and you close the connection. The problem right now is that there is no feedback on what you have done.

If you are using PyCharm, for example, it comes with a built-in sqlite implementation. Therefore, you can just click on the file and you will be able to navigate through the contents of the database. You can also try an application like `sqlite browser <https://sqlitebrowser.org/>`_ to visualize the files. There is also a `Firefox Add-On <https://addons.mozilla.org/en-US/firefox/addon/sqlite-manager/?src>`_ that works very well.  Congratulations, you have created your first table!

Adding Data to a Database
-------------------------
Now that you have a database, is time to store some data into it. All the examples always start by creating a connection and a cursor, which we are going to skip from now on, but you should include in your code. Adding information to a database also involves the use of SQL. You will need to do the following:

.. code-block:: python

    cur.execute('INSERT INTO experiments (name, description) values ("Aquiles", "My experiment description")')
    conn.commit()

You can run this command as many times as you want, and if you are checking your database, you will see that you keep adding rows to the table. As you see above, the SQL code can give rise to problems if you are using variables instead of plain text.

Imagine that you try to save a string that includes the character ``"``. SQL will think that the ``"`` from your variable is actually closing the argument and it will give an error. Even worse, if it is a variable submitted by someone else, this can give rise to something called SQL injection. In the same way in which Pickle can be used to run arbitrary code, SQL can be tricked to perform unwanted operations. Soon enough you will be able to understand the `XKCD SQL injection joke <https://xkcd.com/327/>`_.

A proper way of adding new values to a table is:

.. code-block:: python

    cur.execute('INSERT INTO experiments (name, description) VALUES (?, ?)',
                ('Another User', 'Another Experiment'))
    conn.commit()

Assuming that the access to the database is only yours, i.e. you are not going to take variables from the public, you shouldn't worry too much about safety. In any case, it is important to be aware.

Retrieving Data
---------------
Now that you have some data stored in the database, we need to be able to retrieve it. You can do the following:

.. code-block:: python

    cur.execute('SELECT * FROM experiments')
    data = cur.fetchall()

The first line is asking all the columns from experiments. That is what the ``*`` means. The second line is actually getting the values. We have used ``fetchall``, but you could have also used ``fetchone()`` to get just one element.

So far, nothing particularly special. Imagine that you want to get only the entries where a particular user was involved. You can do the following:

.. code-block:: python

    cur.execute('SELECT * FROM experiments WHERE name="Aquiles"')
    data_3 = cur.fetchall()

.. note:: SQL is not case sensitive for its commands. SELECT or select or Select mean the same. However, if you change Aquiles for aquiles, the results are going to be different.

Of course, it can also happen that there are no entries matching your criteria and therefore the result is going to be an empty list. Again, remember that what we are looking for, ``Aquiles`` may be a variable, and again you are exposed to SQL errors if you have special characters.

At this point there are two concerns that may have come up to your mind. On one hand, there is no way to reference to specific entries in the database. Two different entries, with the same content are indistinguishable from each other.

The other is more of a feature request. Imagine that you would like to store more information about the user, not just the name. It doesn't make sense to add extra columns to the experiments database, because we would be duplicating a lot of information. Ideally, we would start a new table, just to register users and their information.

Adding a Primary Key
--------------------
If you have ever seen any spreadsheet program or even Pandas you probably have noticed that every row is identified with a number. This is very handy, because once I learn that the important information is on line N, I just remember that number and retrieve the data specifically.

The table that we have created does not include this numbering, also known as primary key. Adding a new column is normally not a problem, but since we are dealing with a primary key, sqlite does not allow us to do it in a single step. We should create a new table, copy the contents of the old one, etc. Since we only have toy data, we can start from scratch.

First, we will remove the table from the database, losing all its contents. Then we will create a new tample, with its primary key and we will add some content to it. We can do everything with a very long SQL command instead of running multiple ``cur.execute()``. For that, we use the triple-quote notation of Python.

.. code-block:: python

    sql_command = """
    DROP TABLE IF EXISTS experiments;
    CREATE TABLE experiments (
        id INTEGER,
        name STRING,
        description STRING,
        PRIMARY KEY (id));
    INSERT INTO experiments (name, description) values ("Aquiles", "My experiment description");
    INSERT INTO experiments (name, description) values ("Aquiles 2", "My experiment description 2");
    """
    cur.executescript(sql_command)
    conn.commit()

The important part here is the SQL command. First, we drop the table if it exists. If it doesn't exist, it will throw an error and the rest of the code will not execute. Then we create a new table, with one new column called ``id``, of type integer. At the end of the statement, we defined that ``id`` as the primary key of the table. Finally, we add two elements.

If you run the retrieval code again, you will notice that each element has a unique number that identifies it. If we want to fetch the first (or the second, etc.) element, we can simply do the following:

.. code-block:: python

    cur.execute('SELECT * FROM experiments WHERE id=1')
    data = cur.fetchone()

Notice that we are using ``fetchone`` instead of ``fetchall`` because we know that the output should be only one element. Check what is the difference if you use one or the other command in the data that you get from the database.