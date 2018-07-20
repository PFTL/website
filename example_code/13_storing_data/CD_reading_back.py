with open('BD_data.dat', 'r') as f:
    line = f.readline()
    header = []
    x = []
    y = []
    while line:
        if line.startswith('#'):
            header.append(line.strip())
        else:
            data = line.split('\t')
            x.append(float(data[0]))
            y.append(float(data[1]))
        line = f.readline()

print(header)
print(x)
print(y)