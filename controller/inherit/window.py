# The main window!
from todo.controller.inherit import Control
from todo.quotes import quotes
from random import choice

import todo.view.maya as view # import view specific to the GUI needed


class Window(object):
    """
    Create the main window! Two Panels: Todo / Settings
    Override functions beginning with "_"
    """
    def __init__(s, view):
        quote = choice(quotes)
        s.window = s.view.window.Window(
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
    def _getImage(s, name):
        """
        Override this to get images for the GUI elements
        """
        if name == "todo":
            return "revealSelected.png" # temporary
        if name == "settings":
            return "attributes.png"

Window(view)
