# collapsable group
# Created 30/09/15 Jason Dixon
# http://internetimagery.com

import element
import maya.cmds as cmds

class Collapsable_Group(element.MayaElement):
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
            s._events["position"](s)
