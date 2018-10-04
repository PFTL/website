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

If all your devices have the same public IP, you may wonder how to 