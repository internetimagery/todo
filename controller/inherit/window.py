# The main window!
from todo.controller.inherit import Control
from todo.quotes import quotes
from random import choice

# TEMP! For testing!
from todo.view.maya.window import Window as El_window

class Window(Control):
    """
    Create the main window! Two Panels: Todo / Settings
    Override functions beginning with "_"
    Elements:
        window  : The Main window!
        panel   : Settings / Todo panel
    """
    def _buildCtrl(s):
        quote = choice(quotes)
        s.window = s.elements["window"](
            attributes={
                "name"      : "TODO_MAIN_WINDOW",
                "title"     : quote
            }
        )
        s.panel = None
    def buildTodo(s):
        if s.panel:
            s.panel.delete()
        s.panel = s.view.panel.Panel(
            attributes={
                "label"     : "Settings ->",
                "annotation": "Click to view the Todo scripts settings. Settings are saved with the Maya scene, so you will need to set them for each scene.",
                "image"     : s._getImage("settings")
            },
            events={
                "trigger"   : s.buildSettings
            }
        )
        s.panel.attach(s.window)
    def buildSettings(s):
        if s.panel:
            s.panel.delete()
        s.panel = s.view.panel.Panel(
            attributes={
                "label"     : "<- Todo",
                "annotation": "Click to return to your Todo list.",
                "image"     : s._getImage("todo")
            },
            events={
                "trigger"   : s.buildTodo
            }
        )
        s.panel.attach(s.window)
    def _getImage(s, name):
        """
        Override this to get images for the GUI elements
        """
        if name == "todo":
            return "revealSelected.png" # temporary
        if name == "settings":
            return "attributes.png"

Window(
    elements={"window": El_window}
)
