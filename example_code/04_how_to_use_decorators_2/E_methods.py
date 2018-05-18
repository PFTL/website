from functools import wraps


def check_positive(func):
    @wraps(func)
    def func_wrapper(*args):
        for arg in args:
            if type(arg) is int or type(arg) is float:
                if arg < 0:
                    raise Exception("Method {} takes only positive arguments".format(func.__name__))
        return func(*args)

    return func_wrapper


class Operations:
    @check_positive
    def average(self, x, y):
        return (x + y)/2


op = Operations()
res = op.average(1, 2)
print(res)