import os
import sys


CURR_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(CURR_DIR)
for path in sys.path:
    print(path)