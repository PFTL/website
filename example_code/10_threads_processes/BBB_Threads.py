import numpy as np
from time import sleep


class OhmLaw:
    def __init__(self):
        self.data = np.zeros(0)  # To store the data of the measurement
        self.step = 0  # To keep track of the step
        self.running = False

    def make_measurement(self, start, stop, num_points, delay):
        if self.running:
            raise Exception("Can't trigger two measurements at the same time")

        self.running = True
        x_axis = np.linspace(start, stop, num_points)
        self.data = np.zeros(num_points)
        self.step = 0
        for i in x_axis:
            # Acquire fake data
            self.data[self.step] = np.random.random()
            self.step += 1
            sleep(delay)
        self.running = False
        return self.data


if __name__ == "__main__":
    import threading

    ohm = OhmLaw()

    meas_1 = threading.Thread(target=ohm.make_measurement, args=(0, 1, 11, 1))
    meas_1.start()
    meas_2 = threading.Thread(target=ohm.make_measurement, args=(0, 1, 21, 1))
    meas_2.start()
    print('Triggered measurement')
    i = ohm.step
    while meas_1.is_alive() or meas_2.is_alive():
        if i != ohm.step:
            print('Number of points acquired: {}'.format(ohm.step - 1))
            i = ohm.step
        sleep(2)
