# Main controller running the Todo program!

class Main(object):
    """
    Start the app here!
    Controllers:
        "window"    : Main window
        "todopanel" : Todo panel
    """
    def __init__(s, controllers={}):
        s.controllers = controllers
        s.window = s.controllers["window"](
            events={
                "todo"      : s.requestTodo,
                "settings"  : s.requestSettings
            }
        )
    def requestTodo(s, panel):
        s.panel = s.controllers["todopanel"](
            events={
                "new"   : ""
                },
            parent=panel
            )
        print "todo"
    def requestSettings(s, panel):
        print "settings"

from todo.controller.maya.window import Window as ctrlWindows
from todo.controller.maya.panel import TodoPanel as ctrlTodoPanel

Main({
    "window"    : ctrlWindows,
    "todopanel" : ctrlTodoPanel
})
