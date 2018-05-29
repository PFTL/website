import numpy as np
from time import sleep
from threading import Thread

class Worker(Thread):
    def __init__(self):
        super().__init__()
        self.queue = []
        self.keep_running = True

    def add_to_queue(self, target, args=None):
        print('Adding to queue')
        self.queue.append((target, args))

    def stop_thread(self):
        self.keep_running = False

    def run(self):
        while self.keep_running:
            if self.queue:
                func, args = self.queue.pop(0)
                func(*args)

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
    ohm = OhmLaw()

    worker = Worker()
    worker.start()
    worker.add_to_queue(ohm.make_measurement, args=(0, 1, 11, .1))
    worker.add_to_queue(ohm.make_measurement, args=(0, 1, 11, .1))
    worker.add_to_queue(ohm.make_measurement, args=(0, 1, 11, .1))
    while worker.queue:
        print('Queue length: {}'.format(len(worker.queue)))
        sleep(1)
    worker.stop_thread()
    worker.join()
    print('Finishing')
