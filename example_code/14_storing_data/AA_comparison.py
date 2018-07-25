import sys
import numpy as np

x = np.linspace(0, 255, 256, dtype=np.uint8)

with open('AA_data.dat', 'w') as f:
    for data in x:
        f.write(str(data)+'\n')

print(sys.getsizeof(x))

print(type(x[0]))