Why (not) Handling Exceptions
=============================

:date: 2018-06-04
:author: Aquiles Carattino
:subtitle: Learn how to dealing with exceptions in Python
:header: {attach}chuttersnap-553860-unsplash.jpg
:tags: Threads, Processes, Parallel, Speed, Async, Advanced
:description: Why you should not catch exceptions in your programs
:status: draft

When you develop code, it is almost impossible not to run into an error. Some problems are going to arise as soon as you start your program, for example if you forgot to close a parenthesis, or forgot the ``:`` after an if-statement. However, errors at runtime are also very frequent and harder to anticipate. Imagine that you develop a function to calculate the geometric average of two numbers, i.e. the square root of the product between them.