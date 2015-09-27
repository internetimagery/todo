# Generic Elements
import maya.cmds as cmds
from todo.view.maya import MayaElement

class PlaceHolder(MayaElement):
    """
    An empty placeholder
    """
    def O_buildGUI(s):
        s.root = cmds.columnLayout(adj=True, p=s.parent)
        s.attach = s.root

class Title(MayaElement):
    """
    A title underlined. Striking!
    Attributes:
        title   : The title text. Duh!
        align   : (optional) Where is the text? "left" , "right" , "center"
    """
    def O_buildGUI(s):
        s.attributes["align"] = s.attributes.get("align", "center")
        s.root = cmds.columnLayout(adj=True, p=s.parent)
        s.title = cmds.text()
        cmds.separator()
    def O_updateGUI(s, attr):
        align = s.attributes["align"]
        cmds.text(
            s.title,
            e=True,
            al=align if align in ["left", "right", "center"] else "center",
            l=s.attributes["title"]
            )
