filename = 'my_data.dat'

try:
    file = open(filename)
    data = file.read()
    important_data = data[0]
except FileNotFoundError:
    file = open(filename, 'w')
    print('Created file')
except AttributeError:
    print('Attribute Error')
except Exception:
    print('Unhandled exception')