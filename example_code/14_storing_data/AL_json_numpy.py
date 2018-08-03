import pickle
import json
import numpy as np
import time
import base64

np_array = np.ones((1000, 2), dtype=np.uint8)

array_bytes = pickle.dumps(np_array)

data = {
    'array': base64.b64encode(array_bytes).decode('ascii'),
    'time': time.time(),
}

with open('AL_json_numpy.dat', 'w') as f:
    json.dump(data, f)