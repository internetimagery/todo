# Base GUI Element Overridden with Maya settings.

import maya.cmds as cmds
import todo.view.element

class MayaElement(todo.view.element.Element):
    """
    Maya Gui base
    """
    def _GUI_Delete(s):
        try:
            cmds.deleteUI(s._root)
        except RuntimeError:
            pass
    def _GUI_Visible(s, state):
        if cmds.layout(s._root, ex=True):
            cmds.layout(s._root, e=True, m=state)
        elif cmds.control(s._root, ex=True):
            cmds.control(s._root, e=True, m=state)
    def _GUI_Enable(s, state):
        if cmds.layout(s._root, ex=True):
            cmds.layout(s._root, e=True, en=state)
        elif cmds.control(s._root, ex=True):
            cmds.control(s._root, e=True, en=state)
