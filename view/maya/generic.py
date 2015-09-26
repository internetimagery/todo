# Generic Elements
import maya.cmds as cmds
from todo.view.maya import MayaElement

class PlaceHolder(MayaElement):
    """
    An empty placeholder
    """
    def _buildGUI(s):
        s.root = cmds.columnLayout(adj=True)
        s.attach = s.root

class Title(MayaElement):
    """
    A title underlined. Striking!
    Attributes:
        title   : The title text. Duh!
        align   : (optional) Where is the text? "left" , "right" , "center"
    """
    def _buildGUI(s):
        s.attributes["align"] = s.attributes.get("align", "center")
        s.root = cmds.columnLayout(adj=True)
        s.title = cmds.text()
        cmds.separator()
    def _updateGUI(s, attr):
        align = s.attributes["align"]
        cmds.text(
            s.title,
            e=True,
            al=align if align in ["left", "right", "center"] else "center",
            l=s.attributes["title"]
            )
