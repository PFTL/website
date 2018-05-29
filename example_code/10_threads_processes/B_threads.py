import numpy as np
from time import sleep

class OhmLaw:
    def make_measurement(self, start, stop, num_points, delay):
        x_axis = np.linspace(start, stop, num_points)
        data = []
        for i in x_axis:
            # Acquire fake data
            data.append(np.random.random())
            print(i)
            sleep(delay)

        return data


if __name__ == "__main__":
    import threading
    ohm = OhmLaw()

    t = threading.Thread(target=ohm.make_measurement, args=(0,1,11,1))
    t.start()
    print('Triggered measurement')
    i = 0
    while t.is_alive():
        i += 1
        print('Acquiring {}\r'.format('.'*i), end=' ')
        sleep(0.5)
