# Allow for imports
import sys
import os.path
sys.path.append(os.path.realpath(os.path.dirname(__file__)))

import view.c4d as view
view.window()
