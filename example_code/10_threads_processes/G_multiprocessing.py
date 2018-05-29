import numpy as np


def calculate_random(number_points):
    if number_points<=10:
        number_points = 10

    for i in range(10, number_points):
        data = np.random.random(i)
        fft = np.fft.fft(data)
    return fft

if __name__ == "__main__":
    from time import time
    from multiprocessing import Process, Pool

    # t0 = time()
    # d = calculate_random(5000)
    # print('Total time: {:2.2f} seconds'.format(time() - t0))

    t0 = time()
    t1 = Process(target=calculate_random, args=(5000,))
    t2 = Process(target=calculate_random, args=(5000,))
    t3 = Process(target=calculate_random, args=(5000,))
    t1.start()
    t2.start()
    t3.start()
    t1.join()
    t2.join()
    t3.join()
    print('Total time: {:2.2f} seconds'.format(time()-t0))

    t0 = time()
    with Pool(4) as p:
        print(p.map(calculate_random, [5000, 5000, 5000, 5000 ]))
    print('Total time: {:2.2f} seconds'.format(time() - t0))