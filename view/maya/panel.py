# Two main pages of the GUI.
# Todo layout, and settings layout
import maya.cmds as cmds
from todo.view.maya import MayaElement

class Panel(MayaElement):
    """
    Base layout for both Todo and Settings pages of the GUI
    Attributes:
        label       : Name for the panel switching button
        Annotation  : Description of what the main button does
        image       : Image to place on the button
    Events:
        Switch      : Triggered when panel switching button is pressed
    """
    def _buildGUI(s):
        """
        Build the window.
        """
        switch = s.events["switch"]
        s.root = cmds.columnLayout(adj=True)
        s.button = cmds.iconTextButton(
            h=30,
            ann="Default Description",
            image="revealSelected.png",
            label="<-- Go where? -->",
            style="iconAndTextHorizontal",
            c=switch
            )
        cmds.separator()
        s.attach = cmds.columnLayout(adj=True)

    def _updateGUI(s, attribute, value):
        """
        Set the windows information
        """
        if attribute == "label":
            cmds.iconTextButton(
                s.button,
                e=True,
                label=value,
                )
        if attribute == "annotation":
            cmds.iconTextButton(
                s.button,
                e=True,
                ann=value,
                )
        if attribute == "image":
            cmds.iconTextButton(
                s.button,
                e=True,
                image=image,
                )
