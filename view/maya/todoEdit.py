# Controls for the Todo Panel
# Created 30/09/15
# http://internetimagery.com

import time
import element
import maya.cmds as cmds

class todoEdit(element.MayaElement):
    """
    A todo in edit mode. Letting you edit inline.
    Attributes:
        text    : Text in the text box
        label   : Name on the button
    Events:
        edit    : Triggered on text edit
    """
    def _GUI_Create(s, parent):
        edit = s._events["edit"]
        s._root = cmds.rowLayout(nc=2, adj=1, p=parent)
        s._txt = cmds.textField(
            h=30
        )
        s._btn = cmds.button(
            c=lambda x: s._events["edit"](s)
        )
    def _GUI_Update(s, attr):
        if attr == "text" or attr == None:
            cmds.textField(
                s._txt,
                e=True,
                tx=s._attr["text"]
            )
        if attr == "label" or attr == None:
            cmds.button(
                s._btn,
                e=True,
                l=s._attr["label"]
            )
    def _GUI_Read(s, attr):
        if attr == "text":
            return cmds.textField(s._txt, q=True, tx=True)
        else:
            return s._attr[attr]
