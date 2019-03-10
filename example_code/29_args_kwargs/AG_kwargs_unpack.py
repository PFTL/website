def test_unpack(first, second, third):
    print(first)
    print(second)
    print(third)

vars = {'second': 2,
        'first': 1,
        'third': 3}

test_unpack(**vars)

vars = (2, 1, 3)
test_unpack(*vars)