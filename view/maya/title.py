# A Generic Title
# Created 30/09/15 Jason Dixon
# http://internetimagery.com

import element
import maya.cmds as cmds

class Title(element.MayaElement):
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
