# Scroll Field for Maya
# Created 30/09/15 Jason Dixon
# http://internetimagery.com

import element
import maya.cmds as cmds

class Scroll_Field(element.MayaElement):
    """
    The main scroll box. Inserting todo groups into.
    """
    def _GUI_Create(s, parent):
        s._root = cmds.scrollLayout(
            p=parent,
            bgc=[0.2, 0.2, 0.2],
            cr=True,
            h=500
            )
        s._attach = s._root
