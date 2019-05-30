from threading import Thread
import numpy as np


def increase_by_one(array):
    for i in range(10000):
        array += 1


def divide(array):
    for i in range(10000):
        array /= 1.1


data = np.ones((100,1))

t = Thread(target=increase_by_one, args=(data,))
t2 = Thread(target=divide, args=(data,))
t.start()
t2.start()
t.join()
t2.join()
print(data[0])
print(np.mean(data))
