from threading import Thread
import numpy as np


def increase_by_one(array):
    array += 1


data = np.ones((100,1))


t = Thread(target=increase_by_one, args=(data,))
t.start()
t.join()
print(data[0])
