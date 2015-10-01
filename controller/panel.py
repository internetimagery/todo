# Panel functionality
import todo.images as img
import maya.cmds as cmds

class Panel(object):
    """
    Cotnrol the two panels, Todo and Settings
    """
    def __init__(s, window, view, model, todoCallback, settingsCallback):
        s.window = window
        s.view = view
        s.model = model
        s.todoCallback = todoCallback
        s.settingsCallback = settingsCallback
        s.panel = None
        s.buildTodo()
    def buildSettings(s):
        if s.panel:
            s.panel.delete()
        s.panel = s.view.Panel(
            attributes={
                "label"     : "<- Todo",
                "annotation": "Click to return to your Todo list.",
                "image"     : s.model.icon["panel.todo"]
            },
            events={
                "trigger"   : s.buildTodo
            },
            parent=s.window
            )
        s.settingsCallback(s.panel)
    def buildTodo(s):
        if s.panel:
            s.panel.delete()
        s.panel = s.view.Panel(
            attributes={
                "label"     : "Settings ->",
                "annotation": "Click to view the Todo scripts settings. Settings are saved with the Maya scene, so you will need to set them for each scene.",
                "image"     : s.model.icon["panel.settings"]
            },
            events={
                "trigger"   : s.buildSettings
            },
            parent=s.window
            )
        s.todoCallback(s.panel)
