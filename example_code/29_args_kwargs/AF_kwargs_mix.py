def test_function(first, **kwargs):
    print(first)
    print('Number kwargs: ', len(kwargs))

test_function(1)
test_function(1, second=2, third=3)