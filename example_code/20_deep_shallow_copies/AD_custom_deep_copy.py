import copy

class MyClass:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.other = [1, 2, 3]

    def __deepcopy__(self, memodict={}):
        new_instance = MyClass(self.x, self.y)
        new_instance.__dict__.update(self.__dict__)
        new_instance.x = copy.deepcopy(self.x, memodict)
        new_instance.y = copy.deepcopy(self.y, memodict)
        return new_instance

my_class = MyClass([1, 2], [3, 4])
my_new_class = copy.deepcopy(my_class)

print(id(my_class))
print(id(my_new_class))

my_class.x[0] = 0
my_class.y[0] = 0
my_class.other[0] = 0
print(my_new_class.x)
print(my_new_class.y)
print(my_new_class.other)