# Controls for the settings panel
import maya.cmds as cmds
import element as element

class CheckSection(element.MayaElement):
    """
    A checkboxed section. Enable/Disable depending on the checked state.
    Attributes:
        checked     : Checkbox state. True/False
        label       : Name of the section
        annotation  : Description of the section in detail
    Events:
        change : Checkbox changing state
    """
    def _GUI_Create(s, parent):
        change = s._events["change"]
        s._root = cmds.columnLayout(adj=True, p=parent)
        s._box = cmds.checkBox(cc=s.checkChanged)
        s._attach = cmds.columnLayout(adj=True)
    def _GUI_Update(s, attr):
        checked = s._attr["checked"]
        cmds.checkBox(
            s._box,
            e=True,
            v=checked,
            l=s._attr["label"]
            )
        cmds.columnLayout(
            s._root,
            e=True,
            bgc=[0.4, 0.4, 0.4] if checked else [0.2, 0.2, 0.2],
            ann=s._attr["annotation"]
            )
        cmds.columnLayout(
            s._attach,
            e=True,
            en=checked
            )
    def checkChanged(s, state):
        s.checked = state
        s._events["change"](s)
