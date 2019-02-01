class SimpleClass:
    def __init__(self):
        print('Init')

    def simple_method(self):
        print('Simple Method')

    def finalize(self):
        print('Finalizing the Class')

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('Exit')
        self.finalize()

    def __enter__(self):
        print('enter')
        return self

with SimpleClass() as sc:
    sc.simple_method()
