filename = 'my_data.dat'

try:
    print('In the try block')
    file = open(filename)
    data = file.read()
    important_data = data[0]
except FileNotFoundError:
    print('File not found, creating one')
    file = open(filename, 'w')
finally:
    print('Finally, closing the file')
    file.close()
    important_data = 'A'

print(important_data)