class MyClass:
    a = 1
    b = '2'


var1 = MyClass()
var2 = var1

var1.a = 2
var1.b = '3'

print(var2.a)
print(var2.b)

var1 = MyClass()
var2 = MyClass()
MyClass.a = 3
MyClass.b = '4'

print(var1.a)
print(var2.a)

var1 = MyClass()
var2 = var1

var3 = var1.a

var1.a = 2
var1.b = '3'

MyClass.a = 3

print(var1.a)
# 2
print(var2.a)
# 2
print(var3)