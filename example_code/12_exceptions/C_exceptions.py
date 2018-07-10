try:
    file = open('my_data.dat')
    data = file.readfile()
    print('Data Loaded')
except Exception as e:
    print(e)

