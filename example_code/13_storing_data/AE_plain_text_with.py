import numpy as np
from time import sleep

x = np.linspace(0, 1, 201)
y = np.random.random(201)


header = "X-Column, Y-Column\n"
header += "This is a second line"
with open('AE_data.dat', 'wb') as f:
    np.savetxt(f, [], header=header)
    for i in range(201):
        data = np.column_stack((x[i], y[i]))
        np.savetxt(f, data)
        f.flush()
