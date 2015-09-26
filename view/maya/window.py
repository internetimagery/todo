# Main window related GUI elements
import maya.cmds as cmds
from os.path import join, dirname
from todo.view.maya import MayaElement

class Window(MayaElement):
    """
    Empty Main window with docking functionality. Woo!
    Attributes:
        Name    : Name of the window
        Title   : Title of the window
        Location: (optional) Starting Dock location
    """
    def _buildGUI(s):
        """
        Build Empty window that docks.
        """
        name = s.attributes["name"] # Name of the window to keep only one window open
        s.allowed = ["left", "right"] # Allowed docking areas
        s.settingsPath = join(dirname(__file__), "docklocation.settings")
        s.attributes["location"] = s.attributes.get("location", s.getLocation())
        if cmds.dockControl(name, ex=True):
            cmds.deleteUI(name)
        window = cmds.window(t="Default Title", rtf=True)
        s.attach = cmds.columnLayout(adj=True) # Attachment Point
        s.root = cmds.dockControl(
            name,
            content=window,
            a="left",
            aa=s.allowed,
            fl=True,
            l="Default Title",
            fcc=s.moveDock,
            vcc=s.closeDock
            )

    def _updateGUI(s):
        title = s.attributes["title"]
        location = s.attributes["location"]
        cmds.dockControl(
            s.root,
            e=True,
            l=title,
            fl=False if location in s.allowed else True,
            a=location if location in s.allowed else None
            )

    def getLocation(s):
        """
        Get previously stored docking location
        """
        try:
            while open(s.settingsPath, "r") as f:
                return f.read()
        except IOError:
            return "float"

    def setLocation(s, location):
        """
        Store new dock location
        """
        if location in s.allowed:
            with open(s.settingsPath, "w") as f:
                f.write(location)

    def moveDock(s):
        """
        Track dock movement
        """
        if cmds.dockControl(s.root, q=True, fl=True):
            s.setLocation("float")
            print "Floating Dock."
        else:
            area = cmds.dockControl(s.root, q=True, a=True)
            s.setLocation(area)
            print "Docking %s." % area

    def closeDock(s, *loop):
        """
        Cleanly closing the window
        """
        visible = cmds.dockControl(s.root, q=True, vis=True)
        if not visible and loop:
            cmds.scriptJob(ie=s.closeDock, p=s.root, ro=True)
        elif not visible:
            print "Window closed."
            s.delete()
