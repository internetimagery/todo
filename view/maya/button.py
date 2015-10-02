# Controls for the settings panel
import maya.cmds as cmds
import element as element

class Button(element.MayaElement):
    """
    A button
    Attributes:
        label       : name on button
        image       : (optional) Image for button
        annotation  : Description of button
    Events:
        pressed     : Button pressed
    """
    def _GUI_Create(s, parent):
        s._image = True if s._attr.has_key("image") else False # pick button type
        if s._image:
            s._root = cmds.iconTextButton(
                h=30,
                style="iconAndTextHorizontal",
                c=lambda: s._events["pressed"](s)
                )
        else:
            s._root = cmds.button(
                h=30,
                c=lambda x: s._events["pressed"](s)
            )
    def _GUI_Update(s, attr):
        if s._image:
            cmds.iconTextButton(
                s._root,
                e=True,
                ann=s._attr["annotation"],
                image=s._attr["image"],
                label=s._attr["label"],
                )
        else:
            cmds.button(
                s._root,
                e=True,
                ann=s._attr["annotation"],
                label=s._attr["label"]
            )
