from threading import Thread
import numpy as np


def increase_by_one(array):
    for i in range(len(array)):
        array[i] += 1


def divide(array):
    for i in range(len(array)):
        array[i] /= 1.1


data = np.ones((100000,1))

t = Thread(target=increase_by_one, args=(data,))
t2 = Thread(target=divide, args=(data,))
t.start()
t2.start()
t.join()
t2.join()
print(np.max(data))
print(np.min(data))