import numpy as np


a = np.ones((1024), dtype=np.uint32)

np.save('AD_binay', a)

with open('AD_ascii.dat', 'w') as f:
    for i in a:
        f.write(str(i)+'\n')