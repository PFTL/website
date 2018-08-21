a = (1, 2, 3)
print(a.__hash__())
b = (1, 2, 3)
print(b.__hash__())

print(a is b)

class MyClass:
    def __init__(self, var):
        self.var = var

my_class = MyClass(1)
print(my_class.__hash__())
my_new_obj = MyClass(1)
print(my_new_obj.__hash__())