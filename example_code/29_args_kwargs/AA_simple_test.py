def test_function(*args):
    print(type(args))
    for arg in args:
        print(arg)


test_function('a', 'b', 1, 2)