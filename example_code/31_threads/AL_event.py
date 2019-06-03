from threading import Thread, Event
import numpy as np

evnt = Event()

def increase_by_one(array):
    print('Waiting for event')
    l = evnt.wait()
    print('Increasing by one')
    for i in range(len(array)):
        array[i] += 1

data = np.zeros((100000,1))

t = Thread(target=increase_by_one, args=(data,))
t2 = Thread(target=increase_by_one, args=(data,))
t.start()
t2.start()
for i in range(len(data)):
    data[i] += 1
print('Data Ready. Setting event')
evnt.set()
t.join()
t2.join()
print(data[0])
print(np.mean(data))
