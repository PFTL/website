def increase_values(var1=[1, 1], value=1):
    var1[0] += value
    var1[1] += value
    return var1

print(increase_values())
print(increase_values())

var2 = [1, 2]
var3 = increase_values(var2, 2)
print(var3)
print(var2)

print(id(var2))
print(id(var3))