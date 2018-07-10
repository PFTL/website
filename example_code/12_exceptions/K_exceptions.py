def average(x, y):
    if x <= 0 or y <= 0:
        raise Exception('Both x and y should be positive')
    return (x + y) / 2

print(average(1, 2))
print(average(2, -1))