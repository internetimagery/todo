# Generic Elements
import maya.cmds as cmds
from todo.view.maya.base import MayaElement

class PlaceHolder(MayaElement):
    """
    An empty placeholder
    """
    def _GUI_Create(s, parent):
        s._root = cmds.columnLayout(adj=True, p=parent)
        s._attach = s._root

class Title(MayaElement):
    """
    A title underlined. Striking!
    Attributes:
        title   : The title text. Duh!
        align   : (optional) Where is the text? "left" , "right" , "center"
    """
    def _GUI_Create(s, parent):
        s._attr["align"] = s._attr.get("align", "center")
        s._root = cmds.columnLayout(adj=True, p=parent)
        s._textfield = cmds.text()
        cmds.separator()
    def _GUI_Update(s, attr):
        align = s._attr["align"]
        cmds.text(
            s._textfield,
            e=True,
            al=align if align in ["left", "right", "center"] else "center",
            l=s._attr["title"]
            )
