Accessing a Raspberry Pi from Anywhere
======================================

:status: draft
:date: 2018-10-05
:author: Aquiles Carattino
:subtitle: Learn how to configure Digital Ocean to access your RasPi
:header: {attach}yeo-khee-793533-unsplash.jpg
:tags: Network, Firewall, Raspberry Pi, Raspi, Digital Ocean, Floating IP
:description: Learn how to configure Digital Ocean to access your RasPi

Raspberry Pi's are tiny and cheap computers that can easily run Linux on them. They are ideal to learn how to program, how to setup a web server, and how to administer a Linux machine. You can also use them to host your personal website, or a custom installation of any web service. However, accessing a Raspberry Pi from anywhere in the world can look harder than what it really is.

This tutorial is **not** aimed a complete beginners. You should already have a Raspberry Pi set up and you should know how to access it through SSH within your own network. What we are going to cover in this tutorial is how to set up the RasPi in order to give it a fixed IP-address within the local network and how to configure your router and Digital Ocean in order to give your Raspberry a fixed address on the internet.

.. contents::

Understanding the Network
-------------------------
The Internet is basically a lot of computers connected together through different relays. In order for information to flow from one computer to another, the structure of the network has to be such that two distant computers are discoverable to each other. One of the ways to do such a thing is through the use of a number called the IP number of a computer.

The IP number identifies any device connected to a network, and networks can be connected to each other. Most likely all the devices in your home or at work are connected to a router, and the router is connected to the internet. Therefore, your device is going to have a unique number within your home (or work) network, and the entire network will have a unique number on the internet.

The quickest way of knowing your IP is to visit `ifconfig.co <https://ifconfig.co/>`_. Try to go to the website from two different devices connected to the same router, you will see that the IP number is the same. That is the public IP of your router. However, within your home network, both devices are going to have different IP addresses. On Linux, you can run:

.. code-block:: bash

    ifconfig

And look for the information that corresponds to ``inet``. You will see that it is completely different from the public IP of your network.

On Windows you can run the following on the terminal:

.. code-block:: cmd

    ifconfig \all

You will also see that different devices have different numbers within the network. Another important thing to note is that when you disconnect and connect again devices, or when the router is rebooted, the IP address assigned can change. Also, for security reasons, the public IP of your router can also be changed periodically by your Internet Service Provider (ISP).

If all the devices connected to one router have the same public IP, you may wonder how come that communication is established. The reality is that connections are always started from your devices and never to them. Even when you receive a Whatsapp message, it is actually your phone connecting to the Whatsapp server and asking whether there is a new message available.

.. newsletter::

The DNS Infrastructure
----------------------
If every computer connected to the internet gets one number assigned to it, you may wonder how come that you can visit this website by entering into the browser wwww.pythonforthelab.com. Connected to the internet you have several services that are so ubiquitous normally no one thinks about them. In order to have websites and not plain IP addresses, there are distributed lookup tables hooked to the internet.

When you visit a website, your browser automatically checks one (or several) of those tables and in return gets the IP address associated. The infrastructure associated to maintaining those lookup tables is called DNS. Browsers come normally preconfigured to use some of those DNS servers and you are free to change them. DNS are normally a privacy concern, because it allows to monitor who visits what.

It is important to note that the DNS infrastructure is highly distributed, there are different servers all around the world and in order to speed things up browsers tend to cache the DNS information. When you want to change the information of a website, for instance that a given address points to a new location, there will be a time for that new data to propagate through the network.

If you are a website with heavy traffic, you can't afford to update your DNS records often, because a lot of your visits will be redirected to your old or someone else's server. That is why commercial infrastructure normally counts with fixed IP addresses. If you pay engouh you could have one fixed IP at your home, but that is not a normal residential deal.

Therefore, if you would like to have a fixed address online (either an IP or a domain) you will need to perform some extra steps. Mainly, you will need to update the DNS records associated with your Rasperry Pi every time the public IP of your router changes.

Static IP and Port Forwarding
-----------------------------
When you have control over the network, as is normally the case at your own home, you can assign static IP addresses to your devices. This means that your Raspberry Pi (or any other computer) will have always the same IP address within your own network. This is very handy, because you will know how to access each of the devices.

Some institutions such as universities or big companies, assign the IP address to the computers in a very systematic way. For example, if you are on the 4th floor in office 26 and your computer is number 17, you could be assigned an IP such as ``192.4.26.17``. If you know where you work, you will be able to find your computer, right?

To set up a static IP for your Raspberry Pi, there are two things to consider. First, routers assign random addresses within a range to all the devices that connect to them. The range can be set by the user. My suggestions is for you to Google around the brand of your router and the keywords ``DHCP configuration``.

Most online guides on this topic fail at telling you that if you assign a static IP to your raspberry, but that IP is in the pool of those that can be randomly assigned, when you reboot the device, the router, etc. there is no guarantee that that same address will be available for your RasPi. It is not very likely for small networks, but can be problematic for larger ones.

Therefore, you should limit the range of IP addresses in your router, for instance, you can set them from ``192.168.1.0`` to ``192.168.1.50``, and when setting static IP addresses, you can use from ``51`` onward. Now, the part of setting up the Pi. Regardless of whether you have remote access to it through SSH or Putty, or you have a keyword/screen connected to it, you will need to edit some text files.

