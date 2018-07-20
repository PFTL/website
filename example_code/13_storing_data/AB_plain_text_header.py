import numpy as np

x = np.linspace(0, 1, 201)
y = np.random.random(201)

data = np.column_stack((x, y))
header = "X-Column, Y-Column\n"
header += "This is a second line"
np.savetxt('AB_data.dat', data, header=header)