from multiprocessing import Process, Queue
import random
from time import sleep

def move_from_in_to_out(q_in, q_out):
    while not q_in.empty():
        data = q_in.get()
        q_out.put(data)
        sleep(random.uniform(0,.01))
        if data is None:
            break

def print_len_queue(q_in, q_out):
    while not q_in.empty() or not q_out.empty():
        space = int(q_in.qsize() / (q_in.qsize() + q_out.qsize()) * 50)
        output = str(q_in.qsize())+ '||' + space * ' '+ '|' + (50-space) * ' ' + '||' + str(q_out.qsize()) + '\r'
        print(output, end=' ')

q_in = Queue()
q_out = Queue()

for i in range(50):
    q_in.put(i)
    q_out.put(i)

p = Process(target=move_from_in_to_out, args=(q_in, q_out))
p2 = Process(target=move_from_in_to_out, args=(q_out, q_in))
p3 = Process(target=print_len_queue, args=(q_in, q_out))
p3.start()
p2.start()
p.start()
p.join()
p2.join()
p3.join()