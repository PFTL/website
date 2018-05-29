import numpy as np


class TestRand:
    def calculate_random(self, number_points):
        if number_points<=10:
            number_points = 10

        for i in range(10, number_points):
            data = np.random.random(i)
            fft = np.fft.fft(data)
        return fft

if __name__ == "__main__":
    from time import time
    from threading import Thread

    t = TestRand()
    # t0 = time()
    # d = calculate_random(5000)
    # print('Total time: {:2.2f} seconds'.format(time() - t0))

    t0 = time()
    t1 = Thread(target=t.calculate_random, args=(5000,))
    t2 = Thread(target=t.calculate_random, args=(5000,))
    t3 = Thread(target=t.calculate_random, args=(5000,))
    t1.start()
    t2.start()
    t3.start()
    t1.join()
    t2.join()
    t3.join()
    print('Total time: {:2.2f} seconds'.format(time()-t0))