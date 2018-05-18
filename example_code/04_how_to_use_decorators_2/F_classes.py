class Decorator:
    def __init__(self, func):
        print('Decorating {}'.format(func.__name__))
        self.func = func

    def __call__(self, *args, **kwargs):
        return self.func(*args)

@Decorator
def average(x, y):
    return (x + y) / 2

res = average(1, 2)
print(res)

print(type(average))