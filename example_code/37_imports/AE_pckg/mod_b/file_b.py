import os
import sys

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_PATH)

from mod_a.file_a import simple


def bsimple():
    print('This is simple B')
    simple()