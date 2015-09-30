# Notice / Warning popup
# Created 30/09/15 Jason Dixon
# http://internetimagery.com

import element
import maya.cmds as cmds

class Notice(element.MayaElement):
    """
    Warning / Notice popup
    Attributes:
        title   : Title at the top of the window
        message : Message in the window
    Events:
        answer  : (optional) The result of the popup
    """
    def _GUI_Create(s, parent):
        answer = cmds.confirmDialog(
            t=s._attr["title"],
            m=s._attr["message"]
        )
    def _GUI_Update(s, attr):
        pass
