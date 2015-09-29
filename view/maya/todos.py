# Controls for the Todo Panel
import maya.cmds as cmds
from time import sleep
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
    def _GUI_Create(s):
        trigger = s.events["trigger"]
        s.attributes["text"] = s.attributes.get("text", "")
        s.root = cmds.columnLayout(adj=True, p=s.parent.attach)
        s.textfield = cmds.textFieldGrp(
            h=30,
            tcc=s.updateText,
            cc=trigger
            )
        s.button = cmds.button(
            h=20,
            c=lambda x: trigger(s.attributes["text"])
            )
    def O_updateGUI(s, attr):
        annotation = s.attributes["annotation"]
        cmds.textFieldGrp(
            s.textfield,
            e=True,
            tx=s.attributes["text"],
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
    def O_buildGUI(s):
        s.root = cmds.scrollLayout(
            p=s.parent.attach,
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
    def O_buildGUI(s):
        s.root = cmds.frameLayout(
            p=s.parent.attach,
            cll=True,
            cc=lambda: s.positionChange(False),
            ec=lambda: s.positionChange(True)
        )
        s.attach = s.root
    def O_updateGUI(s, attr):
        cmds.frameLayout(
            s.root,
            e=True,
            l=s.attributes["label"],
            cl=False if s.attributes["position"] else True
            )
    def positionChange(s, pos):
        s.attributes["position"] = pos
        s.events["position"](pos)

class Todo(MayaElement):
    """
    The real hero of the show. The humble todo!
    Attributes:
        label       : Name displayed on the Todo
        annotation  : Description of the Todo
        specialIcon : (optional) Icon for the special button
        specialAnn  : (optional) Description for the special button
    Events:
        complete    : Triggered when todo is marked off as complete
        special     : Triggered when the special button is pressed
        edit        : Triggered when the edit button is pressed
        delete      : Triggered when the delete button is pressed
    """
    def O_buildGUI(s):
        complete = s.events["complete"]
        special = s.events["special"]
        delete = s.events["delete"]
        edit = s.events["edit"]
        s.root = cmds.rowLayout(nc=4, ad4=1, p=s.parent.attach)
        s.labelBtn = cmds.iconTextButton(
            image="fileSave.png",
            h=30,
            style="iconAndTextHorizontal",
            fn="fixedWidthFont",
            c=complete
            )
        s.specialBtn = cmds.iconTextButton(
            style="iconOnly",
            w=30,
            m=False,
            c=special
            )
        s.editBtn = cmds.iconTextButton(
            image="setEdEditMode.png",
            style="iconOnly",
            w=30,
            ann="Edit Todo.",
            c=edit
            )
        s.deleteBtn = cmds.iconTextButton(
            image="removeRenderable.png",
            style="iconOnly",
            w=30,
            ann="Delete Todo without saving.",
            c=delete
            )
    def O_updateGUI(s, attr):
        if attr == "label" or attr == "annotation" or attr == None:
            cmds.iconTextButton(
                s.labelBtn,
                e=True,
                l=s.attributes["label"],
                ann=s.attributes["annotation"]
            )
        if attr == "specialIcon" or attr == "specialAnn" or attr == None:
            cmds.iconTextButton(
                s.specialBtn,
                e=True,
                image=s.attributes.get("specialIcon", "vacantCell.png"),
                ann=s.attributes["specialAnn"]
                )
    def O_deleteGUI(s):
        """
        Overriding deletion for a fancy removal animation.
        """
        if cmds.layout(s.root, ex=True):
            height = cmds.layout(s.root, q=True, h=True)
            for i in range(20):
                i = (100 - i*5) / 100.0
                cmds.layout(s.root, e=True, h=height * i)
                cmds.refresh()
                sleep(0.01)
            MayaElement.O_deleteGUI(s)

class TodoEdit(MayaElement):
    """
    A todo in edit mode. Letting you edit inline.
    Attributes:
        text    : Text in the text box
    Events:
        edit    : Triggered on text edit
    """
    def O_buildGUI(s):
        edit = s.events["edit"]
        s.root = cmds.textFieldButtonGrp(
            p=s.parent.attach,
            bl="Update",
            h=30,
            tcc=s.updateText,
            cc=edit, # TODO THIS MIGHT CAUSE A CRASH IF REMOVED ON THIS FUNCTION
            bc=lambda: edit(s.attributes["text"])
        )
    def updateText(s, text):
        s.attributes["text"] = text
    def O_updateGUI(s, attr):
        cmds.textFieldButtonGrp(
            s.root,
            e=True,
            tx=s.attributes["text"]
            )
