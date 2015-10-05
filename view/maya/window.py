# Main window related GUI elements
import maya.cmds as cmds
import os.path
import element

class window(element.MayaElement):
    """
    Empty Main window with docking functionality. Woo!
    Attributes:
        name    : Name of the window element
        title   : Title of the window
        location: (optional) Starting Dock location
    """
    def _GUI_Create(s, parent):
        """
        Build Empty window that docks.
        """
        name = s._attr["name"]
        s.allowed = ["left", "right"] # Allowed docking areas
        s.settingsPath = os.path.join(os.path.dirname(__file__), "docklocation.settings")
        s._attr["location"] = s._attr.get("location", s.getLocation())
        if cmds.dockControl(name, ex=True):
            print "WINDOW EXISTS. REPLACING!"
            cmds.deleteUI(name)
        window = cmds.window(rtf=True)
        s._attach = cmds.columnLayout(adj=True) # Attachment Point
        s._root = cmds.dockControl(
            name,
            content=window,
            a="left",
            aa=s.allowed,
            fl=True,
            fcc=s.moveDock,
            vcc=s.closeDock
            )

    def _GUI_Update(s, attr):
        """
        Update Gui information
        """
        location = s._attr["location"]
        cmds.dockControl(
            s._root,
            e=True,
            l=s._attr["title"],
            fl=False if location in s.allowed else True,
            a=location if location in s.allowed else None
            )

    def getLocation(s):
        """
        Get previously stored docking location
        """
        try:
            with open(s.settingsPath, "r") as f:
                return f.read()
        except IOError:
            return "float"

    def setLocation(s, location):
        """
        Store new dock location
        """
        with open(s.settingsPath, "w") as f:
            f.write(location)

    def moveDock(s):
        """
        Track dock movement
        """
        if cmds.dockControl(s._root, q=True, fl=True):
            s.setLocation("float")
            print "Floating Dock."
        else:
            area = cmds.dockControl(s._root, q=True, a=True)
            s.setLocation(area)
            print "Docking %s." % area

    def closeDock(s, *loop):
        """
        Cleanly closing the window
        """
        visible = cmds.dockControl(s._root, q=True, vis=True)
        if not visible and loop:
            cmds.scriptJob(ie=s.closeDock, p=s._root, ro=True)
        elif not visible:
            print "Window closed."
            s.delete()
