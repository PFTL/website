import numpy as np
from time import sleep

class OhmLaw:
    def make_measurement(self, start, stop, num_points, delay):
        x_axis = np.linspace(start, stop, num_points)
        data = []
        for i in x_axis:
            # Acquire fake data
            data.append(np.random.random())
            sleep(delay)

        return data


if __name__ == "__main__":
    ohm = OhmLaw()
    result = ohm.make_measurement(0,1,11,0.01)
    print(result)