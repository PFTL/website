from threading import Thread, Event, Lock
from time import sleep, time

event = Event()
data_lock = Lock()

def modify_variable(var):
    while True:
        for i in range(len(var)):
            with data_lock:
                var[i] += 1
        if event.is_set():
            break
        # sleep(.5)
    print('Stop printing')


def modify_variable2(var):
    while True:
        for i in range(len(var)):
            with data_lock:
                var[i] -= 1
        if event.is_set():
            break
        # sleep(.5)
    print('Stop printing')


my_var = [1, 2, 3]
t = Thread(target=modify_variable, args=(my_var, ))
t2 = Thread(target=modify_variable, args=(my_var, ))
t.start()
t2.start()
t0 = time()
while time()-t0 < 5:
    try:
        print(my_var)
        sleep(1)
    except KeyboardInterrupt:
        event.set()
        break
event.set()
t.join()
t2.join()
print(my_var)
