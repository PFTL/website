def area(base, height):
    return base*height/2

print(area(1,2))

print(area(-1, 2))

from functools import wraps


def check_positive(func):
    @wraps(func)
    def func_wrapper(*args):
        for arg in args:
            if type(arg) is int or type(arg) is float:
                if arg < 0:
                    raise Exception("Function {} takes only positive arguments".format(func.__name__))
            else:
                raise Exception("Arguments of {} must be numbers".format(func.__name__))
        return func(*args)

    return func_wrapper


@check_positive
def area_positive(base, height):
    return base*height/2

print(area_positive(1, 2))
print(area_positive(-1, 2))