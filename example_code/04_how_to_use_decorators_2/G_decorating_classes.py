def Decorate(cls):
    print('Decorating {}'.format(cls))
    def class_wrapper(*args):
        print('Arguments, ', args)
        def average(cls, x, y):
            return (x + y) / 2
        setattr(cls, 'average', average)
        return cls(*args)
    return class_wrapper

@Decorate
class MyClass:
    def __init__(self):
        print('MyClass')

print(type(MyClass))
# op = Operations()
# print(type(op))
# print(op.average(1, 2))