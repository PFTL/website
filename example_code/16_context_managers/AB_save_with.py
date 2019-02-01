f = open('my_file.txt', 'w')
try:
    f.write('This is the first line\n')
    raise Exception('This is an exception')
except Exception as e:
    pass
f.close()
raise e