def test_function(first, second, *args):
    print(first)
    print(second)
    for arg in args:
        print(arg)

test_function('first', 2, 'a', 'b', 'c')
test_function('first', 2)
test_function('first')