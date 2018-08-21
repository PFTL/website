class MyImmutable:
    def __init__(self, var1, var2):
        super().__setattr__('var1', var1)
        super().__setattr__('var2', var2)

    def __setattr__(self, key, value):
        raise TypeError('MyImmutable cannot be modified after instantiation')

    def __str__(self):
        return 'MyImmutable var1: {}, var2: {}'.format(self.var1, self.var2)

my_immutable = MyImmutable(1, 2)
print(my_immutable)
my_immutable.var1 = 2