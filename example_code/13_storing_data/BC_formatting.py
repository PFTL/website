import numpy as np

x = np.linspace(0,100,201)
with open('BC_data.dat', 'w') as f:
    f.write('# This is the header\n')
    for data in x:
        f.write('{:4.1f}\n'.format(data))