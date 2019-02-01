class SimpleClass:
    def simple_method(self):
        print('Simple Method')

    def finalize(self):
        print('Finalizing the Class')

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.finalize()
        print(exc_type)
        print(exc_val)
        print(exc_tb)

    def __enter__(self):
        return self

with SimpleClass() as sc:
    sc.simple_method()
    # raise Exception('This is an Exception')

sc.simple_method()


with open('test', 'w') as f:
    f.write('test')

f.write('test')