from threading import Thread, current_thread
from time import sleep


def save_strings(number, file):
    string = """Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum"""
    for i in range(number):
        file.write(string)
        # sleep(delay)


f = open('AC_concurrency.txt', 'w')
t1 = Thread(target=save_strings, args=(10, f)) #, kwargs={'delay':.5})
t2 = Thread(target=save_strings, args=(10, f))
t1.start()
t2.start()

t1.join()
t2.join()
