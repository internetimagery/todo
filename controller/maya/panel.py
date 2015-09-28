# Panels for settings and todo pages

from todo.controller.inherit.panel import TodoPanel as ctrlTodoPanel
from todo.view.maya.todos import HeroTextField, HeroScrollBox

class TodoPanel(ctrlTodoPanel):
    """
    Todo window
    Events:
        new         : Triggered when a new todo is being requested.
    """
    def _buildGUI(s):
        s.attributes = {
            "newtodo"   : HeroTextField,
            "scrollbox" : HeroScrollBox
        }
        ctrlTodoPanel._buildGUI(s)
