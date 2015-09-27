# The main window!
from todo.controller.inherit import Control
from todo.quotes import quotes
from random import choice


class Window(Control):
    """
    Create the main window! Two Panels: Todo / Settings
    Override functions beginning with "_"
    Elements:
        window          : The Main window!
        todoPanel       : Todo panel
        settingsPanel   : Settings panel
    Events:
        todo            : Todo panel active
        settings        : Settings panel active
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
        s.buildTodo()
    def buildTodo(s):
        if s.panel:
            s.panel.delete()
        s.panel = s.elements["todoPanel"](
            attributes={
                "label"     : "Settings ->",
                "annotation": "Click to view the Todo scripts settings. Settings are saved with the Maya scene, so you will need to set them for each scene.",
            },
            events={
                "trigger"   : s.buildSettings
            }
        )
        s.window.parent(s.panel)
        s.events["todo"](s.panel)
    def buildSettings(s):
        if s.panel:
            s.panel.delete()
        s.panel = s.elements["settingsPanel"](
            attributes={
                "label"     : "<- Todo",
                "annotation": "Click to return to your Todo list.",
            },
            events={
                "trigger"   : s.buildTodo
            }
        )
        s.window.parent(s.panel)
        s.events["settings"](s.panel)

def setA(*Arg):
    print "settings"
def todoA(*arg):
    print "todo"

# TEMP! For testing!
from todo.view.maya.window import Window as El_window
from todo.view.maya.panel import TodoPanel as El_todoPanel
from todo.view.maya.panel import SettingsPanel as El_settingsPanel


Window(
    elements={
        "window": El_window,
        "todoPanel" : El_todoPanel,
        "settingsPanel" : El_settingsPanel
        },
    events={
        "todo": todoA,
        "settings": setA
        }
)
