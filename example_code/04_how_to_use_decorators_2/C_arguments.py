from functools import wraps


def check_above(threshold):
    print('Threshold: ', threshold)
    def wrap(func):
        @wraps(func)
        def func_wrapper(x, y):
            if x < threshold or y < threshold:
                raise Exception("Both x and y have to be larger than {} for function {} to work".format(threshold, func.__name__))
            res = func(x, y)
            return res
        return func_wrapper
    return wrap

@check_above(2)
def average(x, y):
    """Calculates the average of two numbers.
    """
    return (x + y)/2


# print(help(average))
# print(average(3, 4))
# print(average(1, 2))
