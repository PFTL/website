class MyException(BaseException):
    pass

class NonPositiveIntegerError(MyException):
    def __init__(self, x, y):
        super(NonPositiveIntegerError, self).__init__()
        if x<=0 and y<=0:
            self.msg = 'Both x and y are negative: x={}, y={}'.format(x, y)
        elif x<=0:
            self.msg = 'Only x is negative: x={}'.format(x)
        elif y<=0:
            self.msg = 'Only y is negative: y={}'.format(y)

    def __str__(self):
        msg = self.msg
        return msg


def average(x, y):
    if x<=0 or y<=0:
        raise NonPositiveIntegerError(x, y)
    return (x+y)/2

try:
    average(1, -1)
except MyException as e:
    print(e)
