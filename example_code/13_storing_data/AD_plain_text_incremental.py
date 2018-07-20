import numpy as np
from time import sleep

x = np.linspace(0, 1, 201)
y = np.random.random(201)


header = "X-Column, Y-Column\n"
header += "This is a second line"
f = open('AD_data.dat', 'wb')
np.savetxt(f, [], header=header)
for i in range(201):
    data = np.column_stack((x[i], y[i]))
    np.savetxt(f, data)
    f.flush()
    sleep(0.1)

f.close()