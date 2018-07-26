import codecs

data_to_save = 'Data to Save'
with codecs.open('AB_unicode.dat', 'w', 'utf-32') as f:
    f.write(data_to_save)