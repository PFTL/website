import numpy as np

x = np.linspace(0,1,201)
with open('BB_data.dat', 'w') as f:
    f.write('# This is the header\n')
    for data in x:
        f.write(str(data)+'\n')