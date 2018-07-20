with open('DB_data.dat', 'r') as f:
    line = f.readline()
    data = []
    while line:
        data.append(line.split(' '))
        line = f.readline()
print(data)