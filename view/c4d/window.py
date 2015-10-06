# Main window
import c4d
from c4d import gui

class Window(gui.GeDialog):

    def __init__(s):
        s.elements = {} # Keep track of elements and their associative functions
        s.requestSettings = None # Callback to get settings built
        s.requestTodos = None # Callback to get todos information
        gui.GeDialog.__init__(s)

    def Open(s):
        gui.GeDialog.Open(
            s,
            dlgtype=c4d.DLG_TYPE_ASYNC,
            defaultw=500,
            defaulth=500
            )

    def CreateLayout(s):
        s.SetTitle("Todo window")
        s.TabGroupBegin(
            id=s.getId(),
            flags=c4d.BFH_SCALEFIT|c4d.BFV_SCALEFIT
            )
        s.buildTodo()
        s.buildSettings()
        s.GroupEnd()
        return True

    def buildTodo(s):
        """
        Build the todo page
        """
        s.GroupBegin(
            id=s.getId(),
            flags=c4d.BFH_SCALEFIT|c4d.BFV_SCALEFIT,
            cols=1,
            title="Tasks",
            groupflags=c4d.BFV_CMD_EQUALCOLUMNS
            )
        textfield = s.getId()
        button = s.getId()
        s.AddEditText(
            id=textfield,
            flags=c4d.BFH_SCALEFIT,
        )
        s.AddButton(
            id=button,
            flags=c4d.BFH_SCALEFIT,
            name="ADD A TODO IN HERE, ALSO REPLACE THIS TEXT"
            )
        s.GroupEnd()
        def newTask(id):
            print s.GetString(textfield)
        s.bind(button, newTask)

    def buildSettings(s):
        """
        Build the todo page
        """
        s.GroupBegin(
            id=s.getId(),
            flags=c4d.BFH_SCALEFIT|c4d.BFV_SCALEFIT,
            cols=1,
            title="Settings",
            groupflags=c4d.BFV_CMD_EQUALCOLUMNS
            )
        s.AddButton(1013, c4d.BFV_MASK, initw=145, name="INSERT SETTINGS IN HERE LATER")
        s.GroupEnd()

    def Command(s, id, msg):
        if id in s.elements and s.elements[id]:
            s.elements[id](id)
        return True

    def getId(s):
        start = 1050
        ids = s.elements.keys()
        while True:
            if start not in ids:
                s.elements[start] = None
                return start
            start += 1

    def bind(s, id, function):
        s.elements[id] = function

    def unbind(s, id):
        if id in s.elements:
            del s.elements[id]

if __name__ == '__main__':
    w = Window()
    w.Open()
