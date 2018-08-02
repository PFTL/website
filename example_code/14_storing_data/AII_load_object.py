import pickle
from AI_pickle_object import MyClass


with open('AI_pickle_object.dat', 'rb') as f:
    new_class = pickle.load(f)

print(new_class)