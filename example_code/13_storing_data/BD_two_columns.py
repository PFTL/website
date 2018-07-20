import numpy as np

x = np.linspace(0,100,201)
y = np.random.random(201)

with open('BD_data.dat', 'w') as f:
    f.write('# This is the header\n')
    for i in range(len(x)):
        f.write('{:4.1f}\t{:.4f}\n'.format(x[i], y[i]))