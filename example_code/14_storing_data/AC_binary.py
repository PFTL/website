import numpy as np


a = np.linspace(0, 1000, 1024, dtype=np.uint8)

np.save('AC_binay', a)

with open('AC_ascii.dat', 'w') as f:
    for i in a:
        f.write(str(i)+'\n')