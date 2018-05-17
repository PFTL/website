def check_positive(func):
    """Decorator to check that input values are positive.
    """
    def func_wrapper(x, y):
        if x < 0 or y < 0:
            raise Exception("Both x and y have to be positive for function {} to work".format(func.__name__))
        res = func(x, y)
        return res

    func_wrapper.__name__ = func.__name__
    func_wrapper.__doc__ = func.__doc__
    return func_wrapper


@check_positive
def average(x, y):
    """Calculates the average of two numbers.
    """
    return (x + y) / 2