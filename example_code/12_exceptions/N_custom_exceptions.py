class MyException(BaseException):
    pass

class NonPositiveIntegerError(MyException):
    pass

class TooBigIntegerError(MyException):
    pass

def average(x, y):
    if x<=0 or y<=0:
        raise NonPositiveIntegerError('Either x or y is not positive')

    if x>=10 or y>=10:
        raise TooBigIntegerError('Either x or y is too large')
    return (x+y)/2

try:
    average(1, -1)
except MyException as e:
    print(e)

try:
    average(11, 1)
except MyException as e:
    print(e)

try:
    average('a', 'b')
except MyException as e:
    print(e)
    # print(dir(e))

print('Done')