Building a CRM with Jupyter Notebooks
=====================================

:status: draft
:date: 2019-02-04
:author: Aquiles Carattino
:subtitle: Send and receive emails from Jupyter notebooks, keep track of people
:header: {attach}rebecca-georgia-269933-unsplash.jpg
:tags: Data, Types, Mutable, Immutable, Tuples
:description: Send and receive emails from Jupyter notebooks, keep track of people


This tutorial is going to be off-topic compared to the others on the website. It was born out of a question regarding how to send personalized e-mail to several people on a list, and I thought it could be useful to post a tutorial online. This will help people interested in building a simple Customer Relationship Manager (CRM) and it will also show scientists that the skills they develop while working in the lab can be used in various contexts.

Let's first discuss what we want to achieve. A CRM is a tool that allows users to send e-mails to customers and keep track of their answers. It could be much more complex than that, integrating with phone, social media, billing platforms, etc. but for our purposes we will keep it to what a normal person (like me) needs. It should be able to send the same e-mail to several people but with a certain degree of personalization, for example saying *Dear John* instead of a generic *Dear Customer*.

The CRM should prevent me from sending the same e-mail twice to the same person and should be able to show me all the e-mails I have exchanged with that person. It should also allow me to segment customers, making it possible for me to send e-mails just to groups of people, for example the ones who took the Python For The Lab course and those who are interested. The ones who bought the book and those who only asked for the free chapter, etc. Let's get started!

.. contents::

The Choices
-----------
First, we will need a way of sending and receiving e-mail. If you are a GMail user, you can check `this guide <https://support.google.com/mail/answer/7104828?hl=en>`_ and `this other one <https://www.digitalocean.com/community/tutorials/how-to-use-google-s-smtp-server>`_ on how to setup the server (you will need this information later on, so keep it in hand). If you want ot use a custom domain to send and receive e-mail, I strongly suggest you to use `Dreamhost <https://www.dreamhost.com/r.cgi?181470/promo/dreamsavings50/>`_ which is what I use myself (if you use the link, you will get 50U$ discount and at the same time you will help me keep this website running). If you expect to send more than 100 e-mails per hour, I suggest you to check `Amazon SES <https://aws.amazon.com/ses/>`_ which is very easy to setup and has a reasonable pricing.

Next, we need to define how to send the e-mails. That we are going to use Python is out of question. But here we have several choices to make. I believe the best is to use Jupyter notebooks. They have the advantage of allowing you to run different pieces of code, see the output inline, etc. It is easier to have interaction through a Jupyter notebook than through plain scripts. Building a user interface (either a desktop app or a web app) would be too time consuming for a minimum increase in usability.

We have now a web server, a platform, we only need to define how to store the data. For this I will choose SQLite. I have written in the past about how to `store data using SQLite <15_Storing_data_3.rst>`_, but in this article we are going one step further by introducing an ORM, or Object Relational Mapping, which will greatly simplify our work when defining tables, accessing data, etc.

Jupyter Notebooks
-----------------
If you are familiar with the Jupyter notebooks, just skip this section and head to the next one. If you are not familiar with them, I will give you a very quick introduction. First, you need to install the needed package. If you are an Anaconda user, you have Jupyter by default. If you are not, you should start by creating a `Virtual Environment <03_Virtual_Environment.rst>`_, and then do the following:

.. code-block:: bash

    pip install jupyter

The installation will take some time because there are many packages to download, but don't worry, it will be over soon. Then, you can simply run the following command:

.. code-block:: bash

    jupyter notebook

If you are not inside a virtual environment, or the command above fails, you can also try the following command, directly on your terminal:

.. code-block:: bash

    python -m jupyter notebook

After you run the command, your web browser should open. Bear in mind that you will use as base folder the folder where you run the command above. Just select new from the top-right button and start a new Python 3 notebook.

You should be welcomed by a screen like this:

.. image:: /images/27_images/01_jupyter.jpg
    :alt: Empty Jupyter Notebook
    :class: center-img

The arrow indicates the name of the notebook. You can edit it to something more descriptive than Untitled. For example, **Test_Notebook**. The line that you see in green is where your input should go. Let's try a simple print statement, like what you see in the image below. To run the code, you can either press Shift+Enter, or click the play button that says run, while the cursor is still in the cell.

.. image:: /images/27_images/02_jupyter.jpg
    :alt: First Cell
    :class: center-img

The advantage of Jupyter notebooks is that they also keep the output when you share them. You can see `this example notebook <https://github.com/PFTL/website/blob/master/example_code/27_CRM/Test_Notebook.ipynb>`_ on Github. And they allow you to embed markdown text in order to document what you are doing.

If you haven't used Jupyter notebooks before, now it is a great chance to get started. They are very useful for prototyping code that later can became an independent program. From now on, I will not stress every single time that the code should go into a notebook, but you should assume it.

As always, all the code for this project `can be found here <https://github.com/PFTL/website/tree/master/example_code/27_CRM>`_. The majority of the code that goes into the Jupyter notebooks can also be copy-pasted into plain Python script files. Just keep in mind that the order in which you can run cells is up to you and not necessarily from top to bottom as is the case for scripts.

Sending Email
-------------
The most basic function of any customer relationship manager is to be able to send e-mails. Having just this functionality is already useful in a lot of different situations, not only professionally but also for private tasks. For example, you can invite your friends to a party by addressing them by name: '*Dear Brian,*'. In order to be able to send e-mails, you need to be able to configure an SMTP server.

If you are a Google User you can check `this guide <https://www.digitalocean.com/community/tutorials/how-to-use-google-s-smtp-server>`_, or you can `sign up to Dreamhost <https://www.dreamhost.com/r.cgi?181470/promo/dreamsavings50/>`_ or `Amazon Services <https://aws.amazon.com/ses/>`_. If you want to use a custom domain, the Dreamhost way is the easiest and quickest. You can read the `documentation for configuring your e-mail <https://help.dreamhost.com/hc/en-us/articles/214918038-Email-client-configuration-overview>`_.

Let's start by creating a configuration file in which we will store some useful parameters. Create an empty file in the same directory where you will be working and call it **config.yml**. You can use Jupyter to create this file, just select *Text File* after clicking on *New*. And in the file, put the following:

.. code-block:: yaml

    EMAIL:
      username: my_username
      password: my_password
      port: 1234
      smtp_server: smtp.server

The format of this file is called YAML, which is a very simple markup language in which blocks are indented by **2 spaces**. Replace the different variables by what you need, i.e., replace ``my_username`` with the username of your server, etc.

Receiving Email
---------------

Using a Database
----------------

Sending To All Customers
------------------------

Storing Email
-------------

Sending to a Group of Customers
-------------------------------

Conclusions
-----------