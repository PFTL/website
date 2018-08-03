import pickle
import base64
import json

with open('AL_json_numpy.dat', 'r') as f:
    data = json.load(f)


array_bytes = base64.b64decode(data['array'])

np_array = pickle.loads(array_bytes)
print(data['time'])
print(np_array)
print(type(np_array))