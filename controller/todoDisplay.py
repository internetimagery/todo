# Manage todo display

class TodoDisplay(object):
    """
    Manage placement of Todos in display
    """
    def __init__(s, parent, gui, todoContainer):
        s.parent = parent
        s.gui = gui
        s.container = todoContainer
