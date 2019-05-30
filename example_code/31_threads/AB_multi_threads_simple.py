from threading import Thread, current_thread
from time import sleep


def print_numbers(number, delay=1):
    for i in range(number):
        print(current_thread(), i)
        sleep(delay)


t1 = Thread(target=print_numbers, args=(10,), kwargs={'delay':.5})
t2 = Thread(target=print_numbers, args=(5,))
t1.start()
t2.start()

t1.join()
t2.join()
