# Horizonal layout
# Created 01/10/15 Jason Dixon
# http://internetimagery.com

import element
import maya.cmds as cmds

class HorizontalLayout(element.MayaElement):
    """
    An empty placeholder
    """
    def _GUI_Create(s, parent):
        s._root = cmds.columnLayout(adj=True, p=parent)
        s._attach = s._root
