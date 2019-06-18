class MyClass:
    a = 1
    b = '2'

    def get_value(self):
        return self.a


var1 = MyClass()
print(var1.get_value())


def get_new_value(cls):
    return cls.b

MyClass.get_value = get_new_value

print(var1.get_value())

var2 = MyClass()
print(var2.get_value())