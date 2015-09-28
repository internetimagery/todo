# Maya version of Window Controller

from todo.controller.inherit.window import Window as ctrlWindow
from todo.view.maya.window import Window as viewWindow
from todo.view.maya.panel import Panel as viewPanel

class Window(ctrlWindow):
    """
    Main window
    Events:
        todo            : Todo panel active
        settings        : Settings panel active
    """
    def _buildCtrl(s):
        s.elements = {
            "window"    : viewWindow,
            "panel"     : viewPanel
        }
        ctrlWindow._buildCtrl(s)
