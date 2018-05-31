"""
Module factorial
================
This module supplies one function, factorial() to calculate the factorial of an integer.
You can imported like this:

>>> from my_module.factorial import factorial
"""
import math


def factorial(n):
    """Function to calculate the factorial of a number.
    First import, and then use, for example:


    >>> factorial(5)
    120
    >>> factorial(-1)
    Traceback (most recent call last):
        ...
    ValueError: n must be >= 0

    :param n: Number to calculate the factorial
    :type n: int
    :return: The calculated factorial
    :rtype: int
    """

    if not n >= 0:
        raise ValueError("n must be >= 0")
    if math.floor(n) != n:
        raise ValueError("n must be exact integer")
    if n + 1 == n:  # catch a value like 1e300
        raise OverflowError("n too large")
    result = 1
    factor = 2
    while factor <= n:
        result *= factor
        factor += 1
    return result