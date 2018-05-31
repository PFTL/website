"""
Module factorial
================
This module supplies one function, factorial() to calculate the factorial of an integer.
"""
import math


def factorial(n):
    """Function to calculate the factorial of a number.
    For example:

    >>> factorial(5)
    120

    >>> factorial(-1)
    Traceback (most recent call last):
        ...
    ValueError: n must be >= 0
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