from threading import Thread, Lock
import numpy as np

lock = Lock()


def increase_by_one(array):
    with lock:
        for i in range(len(array)):
            array[i] += 1

def divide(array):
    with lock:
        for i in range(len(array)):
            array[i] /= 1.1


lock.acquire()
data = np.ones((100000,1))
t = Thread(target=increase_by_one, args=(data,))
t2 = Thread(target=divide, args=(data,))
t2.start()
t.start()
increase_by_one(data)
lock.release()
t.join()
t2.join()
print(data[0])
print(np.mean(data))
