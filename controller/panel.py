# Panel functionality
import todo.images as img
import maya.cmds as cmds

class Panel(object):
    """
    Cotnrol the two panels, Todo and Settings
    """
    def __init__(s, window, gui, todoCallback, settingsCallback):
        s.window = window
        s.gui = gui
        s.todoCallback = todoCallback
        s.settingsCallback = settingsCallback
        s.panel = None
        s.buildTodo()
    def buildSettings(s):
        if s.panel:
            s.panel.delete()
        s.panel = s.gui.Panel(
            attributes={
                "label"     : "<- Todo",
                "annotation": "Click to return to your Todo list.",
                "image"     : img.icon.get("settings_22")
            },
            events={
                "trigger"   : s.buildTodo
            },
            parent=s.window
            )
        s.gui.Title(
            attributes={
                "title"     : "Settings are unique to each Maya scene."
            }
        )
        s.settingsCallback(s.panel)
    def buildTodo(s):
        if s.panel:
            s.panel.delete()
        s.panel = s.gui.Panel(
            attributes={
                "label"     : "Settings ->",
                "annotation": "Click to view the Todo scripts settings. Settings are saved with the Maya scene, so you will need to set them for each scene.",
                "image"     : img.icon.get("todo_22")
            },
            events={
                "trigger"   : s.buildSettings
            },
            parent=s.window
            )
        s.todoCallback(s.panel)
