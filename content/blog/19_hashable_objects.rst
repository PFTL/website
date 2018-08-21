What are Hashable Objects
-------------------------

:status: draft
:date: 2018-08-12
:author: Aquiles Carattino
:subtitle: Understanding how tuples which are immutable, may seem to change.
:header: {attach}tobias-fischer-185901-unsplash.jpg
:tags: Data, Types, Mutable, Immutable, Tuples
:description: Understanding how tuples which are immutable, may seem to change.

To understand hashable objects in Python, it is important to review what a hash table is. Following `the article on Wikipedia <https://en.wikipedia.org/wiki/Hash_table>`_, a hash table is a data structure that can map keys to values and that implements a hash function to compute the index to an array of buckets or slots. Heavy words, I know.

The idea behind a hash table is that in the end you can reduce a complex object to an index in an array. The analogy with the phone book may be appropriate. Imagine you have a collection of names of people and their e-mail address. You store each e-mail as soon as you meet a new person, one under the other. A hash table in such case will be responsible for transforming a name to a number that corresponds to the row in which their e-mail is written.

If you have enough experience with Python, the first thing that probably came to mind is a dictionary. That would be the easiest way of storing e-mails for people that you meet, and that you can easily retrieve by looking up their names. Even if dictionaries are a general concept in which keys are associated to values, Python in fact implements a hash table by default (which doesn't mean this cannot change in the future without affecting how dictionaries work).

One of the complications of hash tables is how to implement the hash function in a reliable way. Immutable data types in Python come with a built-in method for computing their hash value, which is called ``__hash__``. Let's see for example what happens with strings or tuples:

.. code-block:: pycon

    >>> a = '123'
    >>> a.__hash__()
    4031090051524460767
    >>> b = (1, 2, 3)
    >>> b.__hash__()
    2528502973977326415

You see that strings and lists are reduced to integers. If you would use numbers instead:

.. code-block:: pycon

    >>> c = 1
    >>> c.__hash__()
    1
    >>> d = 1.1
    >>> d.__hash__()
    230584300921369601

However, mutable objects such as lists and dictionaries do not have a hash method.


