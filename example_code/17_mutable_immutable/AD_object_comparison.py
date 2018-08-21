class MyClass:
    def __init__(self):
        self.var = 1

    def __eq__(self, other):
        return True


my_obj = MyClass()
if my_obj == None:
    print('My object == None')

if my_obj is None:
    print('My Object is None')