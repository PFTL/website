class MyClass:
    def __init__(self, var=[]):
        self.var = var

    def append(self, value):
        self.var.append(value)

    def __str__(self):
        return str(self.var)

my_class = MyClass()
print(my_class)
my_class.append(1)
print(my_class)
my_class_2 = MyClass()
print(my_class_2)

my_class_2.append(2)
print(my_class)

print(id(my_class.var))
print(id(my_class_2.var))

print(id(my_class))
print(id(my_class_2))

my_list = [1, 2, 3]
my_class = MyClass(my_list)
my_class.append(4)
print(my_list)