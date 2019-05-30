from threading import Thread
from time import sleep


def print_numbers(number, delay=1):
    for i in range(number):
        print(i)
        sleep(delay)


t = Thread(target=print_numbers, args=(10,), kwargs={'delay': .2})
t.start()
print('Thread started')
t.join()
print('Thread finished')