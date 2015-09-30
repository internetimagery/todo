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
        label           : Name displayed on the Todo
        annotation      : Description of the Todo
        icon            : Icon for the main button
        editIcon        : Icon for the edit button
        editAnnotaion   : Description of the edit button
        delIcon         : Icon for the delete button
        delAnnotation   : Description of the delete button
        specialIcon     : (optional) Icon for the special button
        specialAnn      : (optional) Description for the special button
    Events:
        complete    : Triggered when todo is marked off as complete
        special     : Triggered when the special button is pressed
        edit        : Triggered when the edit button is pressed
        delete      : Triggered when the delete button is pressed
    """
    def _GUI_Create(s, parent):
        s._attr["specialIcon"] = s._attr.get("specialIcon", None)
        s._attr["specialAnn"] = s._attr.get("specialAnn", None)
        complete = s._events["complete"]
        special = s._events["special"]
        delete = s._events["delete"]
        edit = s._events["edit"]
        s._root = cmds.rowLayout(nc=4, ad4=1, p=parent)
        s._labelBtn = cmds.iconTextButton(
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
            style="iconOnly",
            w=30,
            c=lambda: edit(s)
            )
        s._deleteBtn = cmds.iconTextButton(
            style="iconOnly",
            w=30,
            c=lambda: delete(s)
            )
    def _GUI_Update(s, attr):
        if attr == "label" or attr == "annotation" or attr == "icon" or attr == None:
            cmds.iconTextButton(
                s._labelBtn,
                e=True,
                l=s._attr["label"],
                ann=s._attr["annotation"],
                image=s._attr["icon"]
            )
        if attr == "specialIcon" or attr == "specialAnn" or attr == None:
            managed = True if s._attr["specialIcon"] and s._attr["specialAnn"] else False
            cmds.iconTextButton(
                s._specialBtn,
                e=True,
                m=managed,
                image=s._attr["specialIcon"] if s._attr["specialIcon"] else"vacantCell.png",
                ann=s._attr["specialAnn"] if s._attr["specialAnn"] else "You cannot use this button."
                )
        if attr == "editAnnotaion" or attr == "editIcon" or attr == None:
            cmds.iconTextButton(
                s._editBtn,
                e=True,
                ann=s._attr["editAnnotaion"],
                image=s._attr["editIcon"]
            )
        if attr == "delAnnotation" or attr == "delIcon" or attr == None:
            cmds.iconTextButton(
                s._deleteBtn,
                e=True,
                ann=s._attr["delAnnotation"],
                image=s._attr["delIcon"]
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
        label   : Name on the button
    Events:
        edit    : Triggered on text edit
    """
    def _GUI_Create(s, parent):
        edit = s._events["edit"]
        s._root = cmds.rowLayout(nc=2, adj=1, p=parent)
        s._txt = cmds.textField(
            h=30
        )
        s._btn = cmds.button(
            c=lambda x: s._events["edit"](s)
        )
    def _GUI_Update(s, attr):
        if attr == "text" or attr == None:
            cmds.textField(
                s._txt,
                e=True,
                tx=s._attr["text"]
            )
        if attr == "label" or attr == None:
            cmds.button(
                s._btn,
                e=True,
                l=s._attr["label"]
            )
    def _GUI_Read(s, attr):
        if attr == "text":
            return cmds.textField(s._txt, q=True, tx=True)
        else:
            return s._attr[attr]
