try:
    f = open('my_file.dat')
    f.readfile()
    print('Loaded data')
except:
    print('Data not loaded')

f = open('my_data.dat')
f.readfile()
print('Loaded data')