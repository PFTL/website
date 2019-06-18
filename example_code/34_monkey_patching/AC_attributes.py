class MyClass:
    a = 1
    b = '2'

    def get_value(self):
        return self.a

def get_new_value(cls):
    return cls.b

var1 = MyClass()
var2 = MyClass()

MyClass.get_value = get_new_value
MyClass.b = '3'
print(var1.get_value())
print(var2.get_value())