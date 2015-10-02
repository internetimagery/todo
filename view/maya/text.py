# A generic text label
# Created 30/09/15 Jason Dixon
# http://internetimagery.com

import element
import maya.cmds as cmds

class Text(element.MayaElement):
    """
    Text!
    Attributes:
        text    : The text. Duh!
        align   : (optional) Where is the text? "left" , "right" , "center"
    """
    def _GUI_Create(s, parent):
        s._attr["align"] = s._attr.get("align", "center")
        s._root = cmds.text(
            p=parent
        )
    def _GUI_Update(s, attr):
        align = s._attr["align"]
        cmds.text(
            s._root,
            e=True,
            al=align if align in ["left", "right", "center"] else "center",
            l=s._attr["text"]
            )
