import numpy as np
from time import sleep

class OhmLaw:
    def __init__(self):
        self.data = np.zeros(0)  # To store the data of the measurement
        self.step = 0  # To keep track of the step

    def make_measurement(self, start, stop, num_points, delay):
        x_axis = np.linspace(start, stop, num_points)
        self.data = np.zeros(num_points)
        self.step = 0
        for i in x_axis:
            # Acquire fake data
            self.data[self.step] = np.random.random()
            self.step += 1
            sleep(delay)

        return self.data


if __name__ == "__main__":
    import threading
    ohm = OhmLaw()

    t = threading.Thread(target=ohm.make_measurement, args=(0,1,11,1))
    t.start()
    print('Triggered measurement')
    i = ohm.step
    while t.is_alive():
        if i != ohm.step:
            print('Number of points acquired: {}'.format(ohm.step-1))
            i = ohm.step
        sleep(2)
