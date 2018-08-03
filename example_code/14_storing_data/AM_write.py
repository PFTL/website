import yaml
from time import time

data = {
    'values': [1, 2, 3, 4, 5],
    'creation_date': time(),
}

with open('AM_data.yml', 'w') as f:
    yaml.dump(data, f)