from threading import Thread, Lock
from time import sleep

import numpy as np

lock = Lock()


def increase_by_one(array):
    l = lock.acquire(timeout=1)
    print('Lock: ', l)
    for i in range(len(array)):
        array[i] += 1

data = np.ones((100000,1))

t = Thread(target=increase_by_one, args=(data,))
lock.acquire()
t.start()
print('Before Sleeping')
sleep(5)
print('After sleeping')
t.join()
print(data[0])
print(np.mean(data))
