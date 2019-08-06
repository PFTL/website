Introduction to Threads in Python: Part 3
=========================================

:status: draft
:date: 2019-03-17
:author: Aquiles Carattino
:subtitle: Learn how to share data between threads
:header: {attach}ivana-cajina-324103-unsplash.jpg
:tags: functions, methods, arguments, packing, unpacking, args, kwargs
:description: Learn how to share data between threads

We have seen in the previous articles how you can use threads to run several tasks at the same time. We have also explored some of the limitations and risks when you share data between different threads. With the set of tools that we have presented earlier, it is possible to start developing programs with a range of functionalities that are not possible in single-threaded applications.

In this article we are going to explore how to create a website crawler which follows links. This is an ideal example to use queues, shared memory, threads, and most of the tools we have shown in the previous articles. In this article we are going to create a set of routines to explore the relationship between articles in Wikipedia. Our goal is to start with an entry point, check what articles are linked, and visit them to see what other articles are linked, etc.

.. warning:: Since we will be downloading data from websites, it is important to be polite with the server. If we crawl a website, we will be creating a load on the server much higher than what a normal user would.

Downloading and Parsing a Website
---------------------------------
The core of our program will be the possibility of downloading a page and getting the important information from the page. To that end, we are going to use urllib, which comes installed with Python, and `Beautiful Soup <https://www.crummy.com/software/BeautifulSoup/bs4/doc/>`_ which can be installed like this:

.. code-block:: bash

    pip install beautifulsoup4

Let's quickly review how we can get information from a website and find the elements we care about. We would like to collect all the links to other articles on a given Wikipedia article. Downloading and printing to screen a page, can be done like this:

.. code-block:: python

    from bs4 import BeautifulSoup
    from urllib import request

    response = request.urlopen('https://en.wikipedia.org/wiki/Shergar')
    data = response.read().decode('utf-8')

    soup = BeautifulSoup(data, 'html.parser')
    print(soup.prettify())

First, we open the page we want, in this case a random Wikipedia article. We read the response and decode it (this step is important, since responses are binary by default). We then use Beautiful Soup to create a tree out of the page, and print it to screen. It is hard to make anything out of what you see. However, we can explore the article to understand where the important information lives.

Let's use Firefox to explore the structure of a Wikipedia article. If you wonder why I point you to Firefox and not Chrome, you can check `this article <https://www.fastcompany.com/90174010/bye-chrome-why-im-switching-to-firefox-and-you-should-too>`__, or you can do a quick search online. If you open `the article <https://en.wikipedia.org/wiki/Shergar>`__, you can explore its structure by pressing **Ctrl**+**Shift**+**I**. A toolbar like the one shown below will appear:

.. image:: /images/35_images/01_firefox.png
    :alt: Firefox with developers tools
    :class: center-img

If you go with the mouse through the elements, you will see that they light up on the main window. If you expand the ``div`` element with id ``content``, you can go through its children. You will see that there is one specifically which selects the entire article, but not the elements around:

.. image:: /images/35_images/02_firefox.png
    :alt: Selecting the appropriate div
    :class: center-img

As you can see in the image above, the ``div`` element we care about has ``id=bodyContent``. In properly formatted HTML, ``id``s should be unique, and therefore they are ideal for selecting elements within a page. Without entering too much into the details of how Beautiful Soup works, we want to select the links which appear only within that specific ``div``. We can achieve that by doing:

.. code-block:: python

    body = soup.find('div', id='bodyContent')
    for link in body.find_all('a'):
        print(link.get('href'))

If you look at the output, you will see that a lot of links start with ``/wiki/``, and a lot with ``#``. Those starting with ``#`` can be discarded, because they are internal links. Then, we have all the external links, which normally start with ``http``. If we want to crawl through the articles, we need to filter only the internal links, i.e. those starting with ``wiki``. If we want to skip links to categories, we should drop those starting with ``/wiki/Category``, etc. We can improve our code to look like this:

.. code-block:: python

    for alink in body.find_all('a'):
        link = alink.get('href')
        if link and link.startswith('/wiki'):
            if not any(x in link for x in ('Category:', 'File:', 'Help:', 'Special:')):
                print(link)

You see that we filter links which do not contain those four special words, but we may add others if we need to. Of course, printing a link is not useful. Let's change our code to make it a recursive function. We have to be careful because if we make a recursive function to crawl to a website, we may end up downloading all the website. We have to limit the depth of our crawl:

.. code-block:: python

    def get_pages(url, level=0, max_depth=1):
        print(f'{level} Getting pages for {url}')
        response = request.urlopen('https://en.wikipedia.org'+url)
        data = response.read().decode('utf-8')
        soup = BeautifulSoup(data, 'html.parser')
        body = soup.find('div', id='bodyContent')
        pages = []
        for alink in body.find_all('a'):
            link = alink.get('href')
            if link and link.startswith('/wiki'):
                if not any(x in link for x in ('Category:', 'File:', 'Help:', 'Special:')):
                    pages.append(link)
                    if level < max_depth:
                        pages += get_pages(link, level=level+1)
        return pages


    url = '/wiki/Shergar'
    pages = get_pages(url)
    print(len(pages))

There are few things to note. The first is that we assume Wikipedia urls. This means that we add the base url ``https://en.wikipedia.org`` to every URL provided. There are, of course, more flexible ways to work with crawlers. The first part of the crawler is the same we have seen earlier. The main difference is that when we go through the links, we append each link to a list called ``pages``. And then we check whether we are below or above our max depth. If we are below, then we call the same function again to check for the links, increasing the level by one. The result of the function is then concatenated to the pages list.

If you run the code above, you will download a total of ``199948`` pages from Wikipedia. Bear in mind that this number is gigantic for most websites. For you to have an idea, Python for the Lab website is receiving around 1000 visits per day. Therefore, you have to be responsible when creating such a strain on somebody's web server. One way to be transparent about what we are doing, is to specify a header for our requests.

For example, we can change one line in the above code in order to give the server the chance to filter our requests, either for the statistics or to balance the load:

.. code-block:: python


    headers = {'User-Agent': 'Mozilla/5.0 (compatible; PFTLBot/1.0)'}
    req = request.Request('https://en.wikipedia.org'+url, headers=headers)
    response = request.urlopen(req)

In this way, every time we download a page, we are going to identify the request as the PFTLBot version 1.0, and the website owner is free to decide what to do with our request. Ideally, the User Agent should also allow the website owner to see who we are. The string PFTLBot will not allow the operator of the website to find us back, and therefore something more descriptive can be a good idea. I hope you get the point.

Threading the Requests
----------------------
In the approach above you can see plenty of problems. The most obvious one is that we may be downloading the same page more than once. For example, if A links to B, and B links back to A, we may end up downloading 2 (or more) times both pages. Improving the code in the previous section is therefore left as an exercise to the reader.

We are going to focus now on how to use threads to perform the same task. Our core strategy would be to have a main thread that synchronizes the behavior of the children threads. From the main thread we will keep track of the pages visited. We are going to use all the strategies learned in the previous two articles, even if perhaps not completely needed.

The first thing to do when dealing with threads is to decide what we want to parallelize. We would like to download pages from different threads, but just that. The handling of the information would happen on the main thread. Moreover, threads should pull data from a Queue. Whenever there is a new page available, the thread will download it. Let's quickly adapt the code from the previous section:

.. code-block:: python

    def download_page(queue_downloads, queue_pages, event):
        while not event.is_set():
            try:
                url = queue_downloads.get(timeout=0.5)
            except Empty:
                continue
            print(f'Getting pages for {url}')
            headers = {'User-Agent': 'Mozilla/5.0 (compatible; PFTLBot/1.0)'}
            req = request.Request('https://en.wikipedia.org'+url, headers=headers)
            response = request.urlopen(req)
            data = response.read().decode('utf-8')
            soup = BeautifulSoup(data, 'html.parser')
            body = soup.find('div', id='bodyContent')
            links = []
            for alink in body.find_all('a'):
                link = alink.get('href')
                if link and link.startswith('/wiki'):
                    if not any(x in link for x in ('Category:', 'File:', 'Help:', 'Special:')):
                        links.append(link)
            queue_pages.put({url: links})

We use a queue to get the data into the thread. We use a timeout of half a second while waiting for data from the queue. This will allow the program to verify whether the event was set and stop the loop. If after the timeout there is no new data, we just skip the rest and wait for new data. The rest is quite similar to the function of the previous section. The only different part is at the end, in which instead of returning the list of pages, we add them to an output queue. This will allow us to build the tree of links, and limit the depth of the crawling from the main thread.