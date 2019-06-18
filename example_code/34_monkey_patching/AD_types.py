import types


class MyClass:
    a = 1
    b = '2'

    def get_value(self):
        return self.a


def get_new_value(cls):
    return cls.b


var1 = MyClass()
var2 = MyClass()
var1.get_value = types.MethodType(get_new_value, var1)
print(var1.get_value())
print(var2.get_value())