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
    def _GUI_Create(s, parent):
        trigger = s._events["trigger"]
        s._attr["text"] = s._attr.get("text", "")
        s._root = cmds.columnLayout(adj=True, p=parent)
        s._textfield = cmds.textFieldGrp(
            h=30,
            tcc=s.updateText,
            cc=trigger
            )
        s._button = cmds.button(
            h=20,
            c=lambda x: trigger(s._attr["text"])
            )
    def _GUI_Update(s, attr):
        annotation = s._attr["annotation"]
        cmds.textFieldGrp(
            s._textfield,
            e=True,
            tx=s._attr["text"],
            ann=annotation,
            )
        cmds.button(
            s._button,
            e=True,
            label=s._attr["label"],
            ann=annotation,
            )
    def updateText(s, text):
        s._attr["text"] = text

class HeroScrollBox(MayaElement):
    """
    The main scroll box. Inserting todo groups into.
    """
    def _GUI_Create(s, parent):
        s._root = cmds.scrollLayout(
            p=parent,
            bgc=[0.2, 0.2, 0.2],
            cr=True,
            h=400
            )
        s._attach = s._root

class CollapsableGroup(MayaElement):
    """
    A collapsable grouping. Sort todos by their group and hide them away.
    Attributes:
        label       : Group name
        position    : Is the group open or closed? Open = True
    Events:
        position    : (optional) Triggerd on position change.
    """
    def _GUI_Create(s, parent):
        s._root = cmds.frameLayout(
            p=parent,
            cll=True,
            cc=lambda: s._positionChange(False),
            ec=lambda: s._positionChange(True)
        )
        s._attach = s._root
    def _GUI_Update(s, attr):
        cmds.frameLayout(
            s._root,
            e=True,
            l=s._attr["label"],
            cl=False if s._attr["position"] else True
            )
    def _positionChange(s, pos):
        s._attr["position"] = pos
        if s._events.has_key("position"):
            s._events["position"](pos)

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
    def _GUI_Create(s, parent):
        complete = s._events["complete"]
        special = s._events["special"]
        delete = s._events["delete"]
        edit = s._events["edit"]
        s._root = cmds.rowLayout(nc=4, ad4=1, p=parent)
        s._labelBtn = cmds.iconTextButton(
            image="fileSave.png",
            h=30,
            style="iconAndTextHorizontal",
            fn="fixedWidthFont",
            c=complete
            )
        s._specialBtn = cmds.iconTextButton(
            style="iconOnly",
            w=30,
            m=False,
            c=special
            )
        s._editBtn = cmds.iconTextButton(
            image="setEdEditMode.png",
            style="iconOnly",
            w=30,
            ann="Edit Todo.",
            c=edit
            )
        s._deleteBtn = cmds.iconTextButton(
            image="removeRenderable.png",
            style="iconOnly",
            w=30,
            ann="Delete Todo without saving.",
            c=delete
            )
    def _GUI_Update(s, attr):
        if attr == "label" or attr == "annotation" or attr == None:
            cmds.iconTextButton(
                s._labelBtn,
                e=True,
                l=s._attr["label"],
                ann=s._attr["annotation"]
            )
        if attr == "specialIcon" or attr == "specialAnn" or attr == None:
            cmds.iconTextButton(
                s._specialBtn,
                e=True,
                image=s._attr.get("specialIcon", "vacantCell.png"),
                ann=s._attr["specialAnn"]
                )
    def _GUI_Delete(s):
        """
        Overriding deletion for a fancy removal animation.
        """
        if cmds.layout(s._root, ex=True):
            height = cmds.layout(s._root, q=True, h=True)
            for i in range(20):
                i = (100 - i*5) / 100.0
                cmds.layout(s._root, e=True, h=height * i)
                cmds.refresh()
                sleep(0.01)
            MayaElement._GUI_Delete(s)

class TodoEdit(MayaElement):
    """
    A todo in edit mode. Letting you edit inline.
    Attributes:
        text    : Text in the text box
    Events:
        edit    : Triggered on text edit
    """
    def _GUI_Create(s, parent):
        edit = s._events["edit"]
        s._root = cmds.textFieldButtonGrp(
            p=parent,
            bl="Update",
            h=30,
            tcc=s.updateText,
            cc=edit, # TODO THIS MIGHT CAUSE A CRASH IF REMOVED ON THIS FUNCTION
            bc=lambda: edit(s._attr["text"])
        )
    def updateText(s, text):
        s._attr["text"] = text
    def _GUI_Update(s, attr):
        cmds.textFieldButtonGrp(
            s._root,
            e=True,
            tx=s._attr["text"]
            )
