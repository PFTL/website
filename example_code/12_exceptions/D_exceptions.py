try:
    file = open('my_file.dat')
    data = file.readfile()
    print('Data Loaded')
except FileNotFoundError:
    file = open('my_file.dat', 'w')
    print('File created')
file.close()