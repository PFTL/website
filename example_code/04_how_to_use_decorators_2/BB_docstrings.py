from functools import wraps


def check_positive(func):
    @wraps(func)
    def func_wrapper(x, y):
        if x < 0 or y < 0:
            raise Exception("Both x and y have to be positive for function {} to work".format(func.__name__))
        res = func(x, y)
        return res

    return func_wrapper


@check_positive
def average(x, y):
    """Calculates the average of two numbers.
    """
    return (x + y) / 2
