from threading import Thread, Event
from time import sleep

import numpy as np

event = Event()


def increase_by_one(array):
    print('Starting to increase by one')
    while True:
        if event.is_set():
            break
        for i in range(len(array)):
            array[i] += 1
        sleep(0.1)
    print('Finishing')


data = np.ones((10000, 1))
t = Thread(target=increase_by_one, args=(data,))
t.start()
print('Going to sleep')
sleep(1)
print('Finished sleeping')
event.set()
t.join()
print(data[0])
