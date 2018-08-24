class MyClass:
    var = 1

    def increase(self):
        self.var += 1

    def __str__(self):
        return str(self.var)

my_class = MyClass()
print(my_class)
my_class_2 = MyClass()
print(my_class_2)
print(id(my_class_2.var))
print(id(my_class.var))
print(id(MyClass.var))
MyClass.var += 1
print(my_class)
print(my_class_2)
print(id(my_class_2.var))
print(id(my_class.var))
print(id(MyClass.var))

my_class.var += 1
print(id(my_class_2.var))
print(id(my_class.var))
print(id(MyClass.var))

my_class_2.var = 0
print(my_class_2)
print(my_class)

my_class = MyClass()
my_class_2 = MyClass()
print(my_class)
my_class.var += 1
print(my_class)
print(my_class_2)