with open('BD_data.dat', 'r') as f:
    line = f.readline()
    header = []
    data = []
    while line:
        if line.startswith('#'):
            header.append(line)
        else:
            data.append(line)
        line = f.readline()

print(header)
print(data)