import AE_module
import AE_module2

var1 = 1

AE_module.print_variable(var1)

def print_plus_one(var):
    print(var+1)

AE_module.print_variable = print_plus_one

AE_module.print_variable(var1)
AE_module2.another_print(var1)