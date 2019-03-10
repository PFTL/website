def test_kwargs(**kwargs):
    print(type(kwargs))
    for key, value in kwargs.items():
        print(key, '=>', value)


test_kwargs(first=1, second=2)