def check_positive(func):
    """Checks that the inputs of a function are positive.
    """
    def func_wrapper(x, y):
        """Function wrapper"""
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

a = average(1, 2)
print(a)
b = average(1, -1)
print(b)

