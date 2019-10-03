from ..mod_a.file_a import function_a
from mod_a.file_c import function_c

def function_b():
    print('This is function_b')
    function_c()

function_b()