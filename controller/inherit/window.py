# The main window!
from todo.view import Element
from todo.quotes import quotes
from todo.images import icon
from random import choice


class Window(Element):
    """
    Create the main window! Two Panels: Todo / Settings
    Attributes:
        window          : The Main window!
        panel           : Todo / Settings panels
    Events:
        todo            : Todo panel active
        settings        : Settings panel active
    """
    def _buildGUI(s):
        quote = choice(quotes)
        s.window = s.attributes["window"](
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
        s.panel = s.attributes["panel"](
            attributes={
                "label"     : "Settings ->",
                "annotation": "Click to view the Todo scripts settings. Settings are saved with the Maya scene, so you will need to set them for each scene.",
                "image"     : icon.get("settings_22")
            },
            events={
                "trigger"   : s.buildSettings
            },
            parent=s.window
        )
        s.events["todo"](s.panel)
    def buildSettings(s):
        if s.panel:
            s.panel.delete()
        s.panel = s.attributes["panel"](
            attributes={
                "label"     : "<- Todo",
                "annotation": "Click to return to your Todo list.",
                "image"     : icon.get("todo_22")
            },
            events={
                "trigger"   : s.buildTodo
            },
            parent=s.window
        )
        s.events["settings"](s.panel)
