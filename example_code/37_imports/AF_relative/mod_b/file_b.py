from ..mod_a.file_a import function_a
from AF_relative.mod_b.mod_a.file_c import function_c

def function_b():
    print('This is function_b')
    function_c()

function_b()
