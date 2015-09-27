# Base class for GUI elements for Maya
from todo.view.inherit import Element
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
    def O_parentGUI(s, structure):
        """
        Reparent the layout or control element to the provided one.
        """
        if s.root:
            if cmds.layout(s.root, ex=True):
                cmds.layout(s.root, e=True, p=structure)
            elif cmds.conrol(s.root, ex=True):
                cmds.control(s.root, e=True, p=structure)
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
