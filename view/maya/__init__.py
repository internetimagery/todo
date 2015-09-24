# Base element for maya GUI
import todo.view as view
import maya.cmds as cmds

class Element(view.Element):
    """
    Base class to derive gui elements from
    """
    def parent(s, element):
        if cmds.layout(element.wrapper, ex=True) and cmds.layout(s.attach, ex=True):
            cmds.layout(element.wrapper, e=True, p=s.attach)
    def remove(s):
        if cmds.layout(s.wrapper, ex=True):
            cmds.deleteUI(s.wrapper)
