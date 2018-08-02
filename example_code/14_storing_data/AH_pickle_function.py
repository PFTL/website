import pickle


def my_function(var):
    new_str = '='*len(var)
    print(new_str+'\n'+var+'\n'+new_str)

my_function('Testing')

with open('AH_pickle_function.dat', 'wb') as f:
    pickle.dump(my_function, f)

with open('AH_pickle_function.dat', 'rb') as f:
    new_function = pickle.load(f)

new_function('New Test')