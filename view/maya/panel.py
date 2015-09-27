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
    def O_buildGUI(s):
        """
        Build the window.
        """
        trigger = s.events["trigger"]
        s.root = cmds.columnLayout(adj=True)
        s.button = cmds.iconTextButton(
            h=30,
            ann="Default Description",
            image="revealSelected.png",
            label="<-- Go where? -->",
            style="iconAndTextHorizontal",
            c=trigger
            )
        cmds.separator()
        s.attach = cmds.columnLayout(adj=True)

    def O_updateGUI(s, attr=None):
        """
        Set the windows information
        """
        cmds.iconTextButton(
            s.button,
            e=True,
            label=s.attributes["label"],
            ann=s.attributes["annotation"],
            image=s.attributes["image"]
            )
