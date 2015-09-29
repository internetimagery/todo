# Text field with a button below
# Created 30/09/15 Jason Dixon
# http://internetimager.com

import element

class TextButtonVertical(element.MayaElement):
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
            cc=lambda x: trigger(s)
            )
        s._button = cmds.button(
            h=20,
            c=lambda x: trigger(s)
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
