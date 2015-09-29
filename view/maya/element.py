# Maya GUI Base

import todo.base as base
import maya.cmds as cmds

class MayaElement(base.GUIElement):
    """
    Maya Gui base
    """
    def _GUI_Delete(s):
        try:
            cmds.deleteUI(s.root)
        except RuntimeError:
            pass
    def _GUI_Visible(s, state):
        if cmds.layout(s.root, ex=True):
            cmds.layout(s.root, e=True, m=state)
        elif cmds.conrol(s.root, ex=True):
            cmds.control(s.root, e=True, m=state)
    def _GUI_Enable(s, state):
        if cmds.layout(s.root, ex=True):
            cmds.layout(s.root, e=True, en=state)
        elif cmds.conrol(s.root, ex=True):
            cmds.control(s.root, e=True, en=state)
