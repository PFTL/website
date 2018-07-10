filename = 'my_datas.dat'

try:
    file = open(filename)
    data = file.read()
    important_data = data[0]
except Exception as e:
    if isinstance(e, IndexError):
        print(e)
        data = 'Information'
        important_data = data[0]
    else:
        print('Unhandled exception')

print(important_data)