import numpy as np
from time import sleep
from threading import Thread, Lock

lock = Lock()

class Worker(Thread):
    def __init__(self, target, args=None):
        super().__init__()
        self.target = target
        self.args = args

    def run(self):
        lock.acquire()
        self.target(*self.args)
        lock.release()

class OhmLaw:
    def __init__(self):
        self.data = np.zeros(0)  # To store the data of the measurement
        self.step = 0  # To keep track of the step
        self.running = False
        self.stop = False

    def make_measurement(self, start, stop, num_points, delay):
        if self.running:
            raise Exception("Can't trigger two measurements at the same time")

        x_axis = np.linspace(start, stop, num_points)
        self.data = np.zeros(num_points)
        self.step = 0
        self.stop = False
        self.running = True
        for i in x_axis:
            if self.stop:
                print('Stopping')
                break
            # Acquire fake data
            self.data[self.step] = np.random.random()
            self.step += 1
            sleep(delay)
        self.running = False
        return self.data


if __name__ == "__main__":
    import threading

    ohm = OhmLaw()

    meas_1 = Worker(target=ohm.make_measurement, args=(0, 1, 11, 1))
    meas_1.start()
    meas_2 = Worker(target=ohm.make_measurement, args=(0, 1, 11, 1))
    meas_2.start()
    i = ohm.step
    while meas_1.is_alive() or meas_2.is_alive():
        if i != ohm.step:
            print('Number of points acquired: {}'.format(ohm.step - 1))
            i = ohm.step
        sleep(2)

    print('Finishing')
