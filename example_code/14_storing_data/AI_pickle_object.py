import pickle
from time import time
from datetime import datetime

class MyClass:
    def __init__(self):
        self.init_time = time()

    def __str__(self):
        dt = datetime.fromtimestamp(self.init_time)
        return 'MyClass created at {:%H:%M:%S on %m-%d-%Y}'.\
            format(dt)

if __name__ == '__main__':
    my_class = MyClass()
    print(my_class)

    with open('AI_pickle_object.dat', 'wb') as f:
        pickle.dump(my_class, f)
#
# with open('AI_pickle_object.dat', 'rb') as f:
#     new_class = pickle.load(f)
#
# print(new_class)