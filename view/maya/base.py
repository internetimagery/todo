# Maya GUI Base

from todo.base import GUIElement
import maya.cmds as cmds

class MayaElement(GUIElement):
    """
    Maya Gui base
    """
    def _GUI_Delete(s):
        if s.root:
            try:
                cmds.deleteUI(s.root)
            except RuntimeError:
                pass
        else:
            print "Missing s.root!"



# Base class for GUI elements for Maya
from todo.view import Element
import maya.cmds as cmds

class MayaElement(Element):
    """
    Use s.root to store the outermost gui element. Be it a layout or control
    """
    def O_deleteGUI(s):
        """
        Remove the s.root element.
        """
        if s.root:
            if cmds.layout(s.root, ex=True) or cmds.window(s.root, ex=True) or cmds.control(s.root, ex=True):
                cmds.deleteUI(s.root)
    def O_visibleGUI(s, show):
        """
        Make element visible or invisible
        """
        if s.root:
            if cmds.layout(s.root, ex=True):
                cmds.layout(s.root, e=True, m=show)
            elif cmds.conrol(s.root, ex=True):
                cmds.control(s.root, e=True, m=show)
    def O_enableGUI(s, enable):
        """
        Enable or disable the element
        """
        if s.root:
            if cmds.layout(s.root, ex=True):
                cmds.layout(s.root, e=True, en=enable)
            elif cmds.conrol(s.root, ex=True):
                cmds.control(s.root, e=True, en=enable)
