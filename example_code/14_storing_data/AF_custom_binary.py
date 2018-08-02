from array import array

data = array('d', [3.15, 2.15, 1.28])

with open('AF_custom_binary.dat', 'wb') as f:
    f.write(data)


with open('AF_custom_binary2.dat', 'w') as f:
    f.write(data)