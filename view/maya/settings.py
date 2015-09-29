# Controls for the settings panel
import maya.cmds as cmds
from todo.view.maya import MayaElement

class CheckSection(MayaElement):
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
        s._box = cmds.checkBox(cc=change)
        s._attach = cmds.columnLayout(adj=True)
    def O_updateGUI(s, attr):
        checked = s._attr["checked"]
        if attr == "checked" or attr == "label" or attr == None:
            cmds.checkBox(
                s._box,
                e=True,
                v=checked,
                l=s._attr["label"]
                )
        if attr == "checked" or attr == "annotation" or attr == None:
            cmds.columnLayout(
                s._root,
                e=True,
                bgc=[0.5, 0.5, 0.5] if checked else [0.2, 0.2, 0.2],
                ann=s._attr["annotation"]
                )
        if attr == "checked" or attr == None:
            cmds.columnLayout(
                s._attach,
                e=True,
                en=checked
                )
