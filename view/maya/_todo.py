# Controls for the Todo Panel
# Created 30/09/15
# http://internetimagery.com

import time
import element
import maya.cmds as cmds

class Todo(element.MayaElement):
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
            c=lambda: complete(s)
            )
        s._specialBtn = cmds.iconTextButton(
            style="iconOnly",
            w=30,
            m=False,
            c=lambda: special(s)
            )
        s._editBtn = cmds.iconTextButton(
            image="setEdEditMode.png",
            style="iconOnly",
            w=30,
            ann="Edit Todo.",
            c=lambda: edit(s)
            )
        s._deleteBtn = cmds.iconTextButton(
            image="removeRenderable.png",
            style="iconOnly",
            w=30,
            ann="Delete Todo without saving.",
            c=lambda: delete(s)
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
                time.sleep(0.01)
            element.MayaElement._GUI_Delete(s)

class TodoEdit(element.MayaElement):
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
            cc=lambda x: edit(s), # TODO THIS MIGHT CAUSE A CRASH IF REMOVED ON THIS FUNCTION
            bc=lambda: edit(s)
        )
    def updateText(s, text):
        s._attr["text"] = text
    def _GUI_Update(s, attr):
        cmds.textFieldButtonGrp(
            s._root,
            e=True,
            tx=s._attr["text"]
            )
