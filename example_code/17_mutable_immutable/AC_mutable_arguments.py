def divide_and_average(var1):
    var = var1
    for i in range(len(var)):
        var[i] /= 2
    avg = sum(var)/len(var)
    return avg

my_list = [1, 2, 3]
print(divide_and_average(my_list))
print(my_list)

import copy

def divide_and_average(var1):
    var = copy.copy(var1)
    for i in range(len(var)):
        var[i] /= 2
    avg = sum(var)/len(var)
    return avg

my_list = [1, 2, 3]
print(divide_and_average(my_list))
print(my_list)