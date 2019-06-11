class AddOne:
    def __init__(self, value):
        self.value = str(value)

    def __add__(self, other):
        self.value += str(other)
        return self

    def __str__(self):
        return self.value

def increase_by_one(value):
    try:
        value += 1
    except TypeError:
        return None
    return value

var1 = AddOne('This is a string')
print(increase_by_one(var1))
