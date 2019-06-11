import numpy as np

def increase_by_one(value):
    if isinstance(value, int) or isinstance(value, float):
        return value + 1

var1 = np.array((0, 1, 2))

print(increase_by_one(var1))


def increase_by_one(value):
    return value + 1

print(increase_by_one(var1))