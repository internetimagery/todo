# Main window
import c4d
from c4d import gui

class Window(gui.GeDialog):

    def __init__(s):
        s.events = {}
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
        s.AddButton(1013, c4d.BFV_MASK, initw=145, name="Tab one")
        s.GroupEnd()

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
        s.AddButton(1013, c4d.BFV_MASK, initw=145, name="Tab two")
        s.GroupEnd()

    def Command(s, id, msg):
        if id in s.events and s.events[id]:
            s.events[id]()
        return True

    def getId(s):
        start = 1050
        ids = s.events.keys()
        while True:
            if start not in ids:
                s.events[start] = None
                return start
            start += 1

    def bind(s, id, function):
        s.events[id] = function

    def unbind(s, id):
        if id in s.events:
            del s.events[id]

if __name__ == '__main__':
    w = Window()
    w.Open()
