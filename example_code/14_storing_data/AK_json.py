import json


data = {
    'first': [0, 1, 2, 3],
    'second': 'A sample string'
}

data = [1, 2, data]

with open('AK_json.dat', 'w') as f:
    json.dump(data, f)


with open('AK_json.dat', 'r') as f:
    new_data = json.load(f)

print(new_data)