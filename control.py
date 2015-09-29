# Control the app

import re
import random

import todo.base as base
import todo.quotes as quotes

# import sys
# for mod in sys.modules.values():
#     if type(mod) == "module":
#         print "reloading %s" % mod
#         reload(mod)

class Main(object):
    def __init__(s, software):
        # Set up our interfaces
        if software == "maya":
            # Set up Crud
            from todo.mayaInterface.crud import CRUD
        else:
            raise RuntimeError, "Unknown Software: %s." % software
        title = random.choice(quotes.quotes)
        s.crud = CRUD()
        s.settings = base.Settings(s.crud)
        s.todos = base.TodoContainer([t for t in s.crud.read() if re.match(r"^TODO_\d+", t)])



Main("maya")
