# Maya Gui

import maya.cmds as cmds
import os.path


class GUI(object):
    """
    Gui for Maya
    """
    def __init__(s, title):
        name = "window_%s" % title
        s._allowed = ["left", "right"] # Allowed docking areas
        s._dockMemory = os.path.join(os.path.dirname(__file__), "docklocation.settings")
        try:
            with open(s._dockMemory) as f:
                loc = f.read()
        except IOError:
            loc = "float"
        s._dockLocation = loc if loc in s._allowed else "float"
        window = cmds.window(rtf=True)
        cmds.columnLayout(adj=True) # Base Attachment Point
        s._dock = cmds.dockControl(
            name,
            l=title,
            content=window,
            a="left",
            aa=s._allowed,
            fl=True,
            fcc=s._moveDock,
            vcc=s._closeDock
            )

    def _dockMemorySave(s, loc):
        """
        Remember last position of dock
        """
        with open(s._dockMemory, "r") as f:
            f.write(loc)

    def _moveDock(s):
        """
        Track dock movement
        """
        if cmds.dockControl(s._dock, q=True, fl=True):
            s._dockMemorySave("float")
            print "Floating Dock."
        else:
            area = cmds.dockControl(s._dock, q=True, a=True)
            s._dockMemorySave(area)
            print "Docking %s." % area

    def _closeDock(s, *loop):
        """
        Cleanly closing the window
        """
        visible = cmds.dockControl(s._dock, q=True, vis=True)
        if not visible and loop:
            cmds.scriptJob(ie=s._closeDock, p=s._dock, ro=True)
        elif not visible:
            print "Window closed."
            cmds.deleteUI(s._dock)
