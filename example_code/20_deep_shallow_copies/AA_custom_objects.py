class MyClass:
    def __init__(self, x, y):
        self.x = x
        self.y = y



my_class = MyClass([1, 2], [3, 4])
my_new_class = my_class

print(id(my_class))
print(id(my_new_class))

my_class.x[0] = 0
print(my_new_class.x)

