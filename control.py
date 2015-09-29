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
            from todo.mayaInterface.gui import GUI
            from todo.mayaInterface.crud import CRUD
        else:
            raise RuntimeError, "Unknown Software: %s." % software
        title = random.choice(quotes.quotes)
        s.gui = GUI(title)
        s.crud = CRUD()
        s.settings = base.Settings(s.crud)
        s.todos = base.TodoContainer([t for t in s.crud.read() if re.match(r"^TODO_\d+", t)])
        s.gui = GUI(title, {
            "Panel.Btn": s.switchPanel
        })
        s.panel = "Todo"
        s.buildTodo()
    def switchPanel(s):
        if s.panel = "Todo":
            s.buildTodo()
        else:
            s.buildSettings()
    def buildTodo(s):
        print "building todo"
        pass
    def buildSettings(s):
        pass

Main("maya")
