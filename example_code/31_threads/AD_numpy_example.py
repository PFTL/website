import numpy as np


def increase_by_one(array):
    array += 1

data = np.ones((100,1))
increase_by_one(data)

print(data[0])