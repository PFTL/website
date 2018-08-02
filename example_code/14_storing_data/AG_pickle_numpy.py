# import numpy as np
import pickle

#
# data = np.linspace(0, 1023, 1000, dtype=np.uint8)
#
# np.save('AG_numpy', data)
#
# with open('AG_pickle.dat', 'wb') as f:
#     pickle.dump(data, f)
#

with open('AG_pickle.dat', 'rb') as f:
    new_data = pickle.load(f)

print(new_data)