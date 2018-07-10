filename = 'my_data.dat'

try:
    file = open(filename)
    data = file.read()
    important_data = data[0]
except Exception as e:
    print('Unhandled exception')
    print(e)