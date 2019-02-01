import copy

class MyClass:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.other = [1, 2, 3]

    def __copy__(self):
        new_instance = MyClass(self.x, self.y)
        new_instance.__dict__.update(self.__dict__)
        new_instance.other = copy.deepcopy(self.other)
        return new_instance

my_class = MyClass([1, 2], [3, 4])
my_new_class = copy.copy(my_class)

print(id(my_class))
print(id(my_new_class))

my_class.x[0] = 0
my_class.y[0] = 0
my_class.other[0] = 0
print(my_new_class.x)
print(my_new_class.y)
print(my_new_class.other)

print(my_new_class.__dict__)
my_new_class.__dict__['y'][0] = 20
print(my_new_class.y)