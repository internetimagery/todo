# Controls for the Todo Panel
import maya.cmds as cmds
from todo.view.maya import MayaElement

class HeroTextField(MayaElement):
    """
    A Fancy large text field for creating new Todos.
    Attributes:
        label       : Button Name.
        annotation  : Description of what the control will do.
        text        : (optional) Current text in the field
    Events:
        trigger     : Triggered when new text is entered or button is pressed.
    """
    def _buildGUI(s):
        trigger = s.events["trigger"]
        s.attributes["text"] = s.attributes.get("text", "")
        s.root = cmds.columnLayout(adj=True)
        s.textfield = cmds.textFieldGrp(
            h=30,
            tcc=s.updateText
            cc=trigger
            )
        s.button = cmds.button(
            h=20,
            c=lambda x: trigger(s.attributes["text"])
            )
    def _updateGUI(s, attr):
        annotation = s.attributes["annotation"]
        cmds.textFieldGrp(
            s.textfield,
            e=True,
            tx=s.attributes["text"]
            ann=annotation,
            )
        cmds.button(
            s.button,
            e=True,
            label=s.attributes["label"],
            ann=annotation,
            )
    def updateText(s, text):
        s.attributes["text"] = text

class HeroScrollBox(MayaElement):
    """
    The main scroll box. Inserting todo groups into.
    """
    def _buildGUI(s):
        s.root = cmds.scrollLayout(
            bgc=[0.2, 0.2, 0.2],
            cr=True,
            h=400
            )
        s.attach = s.root

class CollapsableGroup(MayaElement):
    """
    A collapsable grouping. Sort todos by their group and hide them away.
    Attributes:
        label       : Group name
        position    : Is the group open or closed? Open = True
    Events:
        position    : Triggerd on position change.
    """
    def _buildGUI(s):
        position = s.events["position"]
        s.root = cmds.frameLayout(
            cll=True,
            cc=lambda: s.positionChange(False),
            ec=lambda: s.positionChange(True)
        )
        s.attach = s.root
    def _updateGUI(s, attr):
        cmds.frameLayout(
            s.root,
            e=True,
            l=s.attributes["label"],
            cl=False if s.attributes["position"] else True
            )
    def positionChange(s, pos):
        s.attributes["position"] = pos
        s.events["position"](pos)
