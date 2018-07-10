filename = 'my_data.dat'

try:
    file = open(filename)
    data = file.readfile()
except FileNotFoundError:
    file = open(filename, 'w')
    print('Created file')
except AttributeError:
    print('Attribute Error')
