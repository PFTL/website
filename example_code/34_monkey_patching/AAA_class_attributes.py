class MyClass:
    def __init__(self):
        self.a = 1
        self.b = '2'


var1 = MyClass()
var2 = MyClass()
MyClass.a = 3
MyClass.b = '4'

print(var1.a)
print(var2.a)
