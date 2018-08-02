import numpy as np


a = np.linspace(0,65535,65535, dtype=np.uint16)

np.save('AE_binay', a)

with open('AE_ascii.dat', 'w') as f:
    for i in a:
        f.write(str(i)+'\n')