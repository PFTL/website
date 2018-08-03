import yaml

with open('AM_example.yml', 'r') as f:
    data = yaml.load(f)

print(data)