from threading import Thread, Event
from queue import Queue
from time import sleep, time

event = Event()
queue1 = Queue()
queue2 = Queue()


def modify_variable(queue_in: Queue, queue_out: Queue):
    while True:
        if not queue_in.empty():
            var = queue_in.get()
            var += 1
            queue_out.put(var)
        if event.is_set():
            break
    print('Stop printing')


def modify_variable2(queue: Queue):
    while True:
        if not queue.empty():
            var = queue.get()
            var += 1
            queue.put(var)
        if event.is_set():
            break
    print('Stop printing')


my_var = 1
queue1.put(my_var)
queue3 = Queue()
queue3.put(my_var)
t = Thread(target=modify_variable2, args=(queue3,))
t2 = Thread(target=modify_variable2, args=(queue3,))
t.start()
t2.start()
t0 = time()
while time()-t0 < 5:
    try:
        sleep(1)
    except KeyboardInterrupt:
        break

event.set()
t.join()
t2.join()
if not queue1.empty():
    print(queue1.get())
if not queue2.empty():
    print(queue2.get())
if not queue3.empty():
    print(queue3.get())