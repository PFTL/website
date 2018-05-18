from functools import wraps

func_registry = []

def register(func):
    func_registry.append(func.__name__)
    @wraps(func)
    def func_wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return func_wrapper

@register
def average(x, y):
    return (x + y)/2

@register
def geom_average(x, y):
    return (x*y)**0.5

