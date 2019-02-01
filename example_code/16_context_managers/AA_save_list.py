from time import sleep

file = open('My_File.txt', 'w')
file.write('This is the first line\n')

sleep(600)
file.close()

