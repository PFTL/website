import numpy as np

x = np.linspace(0, 1, 201)
y = np.random.random(201)

data = np.column_stack((x, y))

np.savetxt('AA_data.dat', data)