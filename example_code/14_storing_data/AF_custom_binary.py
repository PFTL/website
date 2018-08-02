import pickle

data = [1, 1.2, 'a', 'b']

with open('AF_custom.dat', 'wb') as f:
    pickle.dump(data, f)

with open('AF_custom.dat', 'rb') as f:
    new_data = pickle.load(f)

print(new_data)