class MyClass:
    var = []

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
MyClass.var.append(2)
print(my_class)
print(my_class_2)

my_class_2.var += [3]

print(my_class)
print(my_class_2)
