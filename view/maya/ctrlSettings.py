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
    def _buildGUI(s):
        change = s.events["change"]
        s.root = cmds.columnLayout(adj=True)
        s.box = cmds.checkBox(cc=change)
        s.attach = cmds.columnLayout(adj=True)
    def _updateGUI(s, attr):
        checked = s.attributes["checked"]
        if attr == "checked" or attr == "label" or attr == None:
            cmds.checkBox(
                s.box,
                e=True,
                v=checked,
                l=s.attributes["label"]
                )
        if attr == "checked" or attr == "annotation" or attr == None:
            cmds.columnLayout(
                s.root,
                e=True,
                bgc=[0.5, 0.5, 0.5] if checked else [0.2, 0.2, 0.2],
                ann=s.attributes["annotation"]
                )
        if attr == "checked" or attr == None:
            cmds.columnLayout(
                s.attach,
                e=True,
                en=checked
                )
