# Two main pages of the GUI.
# Todo layout, and settings layout
import maya.cmds as cmds
from todo.view.maya import MayaElement

class Panel(MayaElement):
    """
    Base layout for both Todo and Settings pages of the GUI
    Attributes:
        label       : Name for the panel switching button
        annotation  : Description of what the main button does
        image       : Image to place on the button
    Events:
        trigger     : Triggered when panel switching button is pressed
    """
    def _GUI_Create(s, parent):
        """
        Build the window.
        """
        trigger = s._events["trigger"]
        s._root = cmds.columnLayout(adj=True, p=parent)
        s._button = cmds.iconTextButton(
            h=30,
            ann="Default Description",
            image="vacantCell.png",
            label="<-- Go where? -->",
            style="iconAndTextHorizontal",
            c=trigger
            )
        cmds.separator()
        s._attach = cmds.columnLayout(adj=True)

    def _GUI_Update(s, attr):
        """
        Set the windows information
        """
        cmds.iconTextButton(
            s._button,
            e=True,
            label=s._attr["label"],
            ann=s._attr["annotation"],
            image=s._attr["image"]
            )
