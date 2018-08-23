class MyClass:
    def __init__(self, var):
        self.var = var

    def __hash__(self):
        return int(self.var)

    def __str__(self):
        return 'MyClass'

    def __repr__(self):
        return 'MyClass {}'.format(self.var)

    def __eq__(self, other):
        return True

my_obj = MyClass(1)
var = MyClass(2)
print(var == my_obj)
var2 = {my_obj: 'my_obj'}
var2[var] = 'var'
print(var2)