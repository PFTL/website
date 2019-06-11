import numpy as np


def increase_by_one(value):
    try:
        value += 1
    except TypeError:
        return None
    return value

var1 = np.array((0, 1, 2))
print(increase_by_one(var1))
var1 = 2
print(increase_by_one(var1))
var1 = 'This is a string'
print(increase_by_one(var1))
