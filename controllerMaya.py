# Controller for Maya
import maya.cmds as cmds
import todo.viewMaya as view

class Start(object):
    """
    Application
    """
    def __init__(s, location=None):
        if not location:
            location = "float" # TODO retrieve this from file

        windowOptions = {
            "title"                    : "grab from file",
            "location"                 : location,
            "moveCallback"             : s.test,
            "closeCallback"            : s.test,
            "buildTodoCallback"        : s.test,
            "buildSettingsCallback"    : s.test,
            "newTodoCallback"          : s.test
        }
        s.window = view.MainWindow(
            "Todo_window_Temporaryname",
            "",
            title                 = "grab from file",
            location              = location,
            moveCallback          = s.test,
            closeCallback         = s.test,
            buildTodoCallback     = s.test,
            buildSettingsCallback = s.test,
            newTodoCallback       = s.test
            )

    def test(s, *args):
        print args

Start()

# options:
# title = window title
# location = "float" or "left" or "right"
# moveCallback(location) = run when docked or undocked
# closeCallback = run when window closed
# buildTodoCallback(parent) = run when switching to main todo window
# buildSettingsCallback(parent) = run when switching to settings window
# newTodoCallback(text) = run when creating a new todo
