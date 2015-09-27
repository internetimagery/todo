# Main controller running the Todo program!

class Main(object):
    """
    Start the app here!
    """
    def __init__(s, controllers={}):
        s.controllers = controllers
        s.window = s.controllers["window"](

        )

from todo.controller.inherit.window import Window
from todo.view.maya.window import Window as WinView
from todo.view.maya.panel import Panel as PanView

Main({
    "window": Window
})



# TEMP! For testing!
from todo.view.maya.window import Window as El_window
from todo.view.maya.panel import Panel as El_panel


Window(
    elements={
        "window": El_window,
        "panel" : El_panel,
        },
    events={
        "todo": todoA,
        "settings": setA
        }
)
