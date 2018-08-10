def save_list_to_file(filename, data):
    f = open(filename, 'w')
    for element in data:
        f.write(element)
    f.close()

my_list = ['First line\n', 'Second Line\n', 3]

save_list_to_file('AA_save_list.dat', my_list)