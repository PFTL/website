import traceback


filename = 'my_datas.dat'

try:
    file = open(filename)
    data = file.read()
except FileNotFoundError:
    traceback.print_exc()