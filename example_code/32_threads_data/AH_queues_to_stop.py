from threading import Thread, Event
from queue import Queue
from time import sleep, time

event = Event()
queue1 = Queue(1)
queue2 = Queue(1)


def modify_variable(queue_in: Queue, queue_out: Queue):
    internal_t = 0
    while True:
        var = queue_in.get()
        if var is None:
            break
        t0 = time()
        for i in range(len(var)):
            var[i] += 1
        queue_out.put(var)
        internal_t += time()-t0
    sleep(0.1)
    print(f'Running time: {internal_t} seconds\n')


my_var = [1, 2, 3]
queue1.put(my_var)
t = Thread(target=modify_variable, args=(queue1, queue2))
t2 = Thread(target=modify_variable, args=(queue2, queue1))
t.start()
t2.start()
t0 = time()
while time()-t0 < 5:
    try:
        sleep(1)
    except KeyboardInterrupt:
        break
queue1.put(None)
queue2.put(None)
t.join()
t2.join()
if not queue1.empty():
    print(queue1.get())
if not queue2.empty():
    print(queue2.get())