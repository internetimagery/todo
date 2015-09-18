# Controller for Maya
import maya.cmds as cmds
import todo.viewMaya as view

# Begin Application
class Start(object):
    """
    Application
    """
    def __init__(s, location=None):
        if not location:
            location = "float" # TODO retrieve this from file

        s.window = view.MainWindow(
            "Todo_window_Temporaryname",
            "",
            title                 = "grab from file",
            location              = location,
            moveCallback          = s.moveUpdate,
            closeCallback         = s.closeUpdate,
            buildTodoCallback     = s.buildTodo,
            buildSettingsCallback = s.buildSettings,
            newTodoCallback       = s.newTodo
            )

    """
    Build out todo page
    """
    def buildTodo(s, parent):
        s.todoContainer = cmds.scrollLayout(bgc=[0.2, 0.2, 0.2], cr=True, p=parent)
        cmds.text(l="Added in controller")
        s.todoContainerSections = cmds.columnLayout(adj=True, p=s.todoContainer)
        s.todoContainerUnsectioned = cmds.columnLayout(adj=True, p=s.todoContainer)


    """
    Build out settings page
    """
    def buildSettings(s, parent):
        cmds.text(l="Todo: Insert settings stuff in here!", p=parent)

    """
    New todo requested
    """
    def newTodo(s, text):
        print "new todo:", text

    """
    Update window position
    """
    def moveUpdate(s, location):
        print "moved", location
        print "todo, store this info in preferences"

    """
    No real functionality
    """
    def closeUpdate(s):
        print "closed"


Start()
