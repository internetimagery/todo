# A Base GUI Element to build off of!

class GUIElement(object):
    """
    Interface for GUI elements / compound elements
    Override all with "GUI" in the name.
    """
    _attr = {} # Storage of attributes
    _events = {} # Storage of events

    def __init__(s, attributes={}, events={}, parent=None):
        s._attr = attributes
        s._events = events
        if parent:
            s._parent = parent
            parent._children.append(s)
        else:
            s._parent = None
        s._children = []
        s._root = None # Base of the element, for removal procedures
        s._attach = None # Attachment point for children where applicable
        s._enable = True
        s._visible = True
        s._GUI_Create(
            parent._attach if parent else None
            )
        s._GUI_Update(None)
    def delete(s):
        """
        Remove element
        """
        if s._parent:
            s._parent._children.remove(s)
        if s._children:
            for child in s._children:
                child._parent = None
        s._GUI_Delete(s)
    def enable():
        doc = "The enable property."
        def fget(s):
            return s._enable
        def fset(s, value):
            s._enable = value
            s._GUI_Enable(value)
        def fdel(s):
            del s._enable
        return locals()
    enable = property(**enable())
    def visible():
        doc = "The visible property."
        def fget(s):
            return s._visible
        def fset(s, value):
            s._visible = value
            s._GUI_Visible(value)
        def fdel(s):
            del s._visible
        return locals()
    visible = property(**visible())
    def _GUI_Create(s, parent):
        """
        Build the gui given attributes, events and a parent
        """
        pass
    def _GUI_Read(s, k):
        """
        Get attribute value from GUI.
        Only need to override this if the attributes aren't tracking the GUI
        """
        return s._attr[k]
    def _GUI_Update(s, attr):
        """
        Update GUI value given an attribute
        """
        pass
    def _GUI_Delete(s):
        """
        Remove gui element
        """
        pass
    def _GUI_Enable(s, state):
        """
        Enable or Disable the element
        """
        pass
    def _GUI_Visible(s, state):
        """
        Enable or Disable the elements visibility
        """
        pass
    def __getattr__(s, k):
        if s._attr.has_key(k):
            return s._GUI_Read(k)
        else:
            raise AttributeError, "No attribute exists named %s." % k
    def __setattr__(s, k, v):
        if s._attr.has_key(k):
            s._attr[k] = v
            s._GUI_Update(k)
        else:
            object.__setattr__(s, k, v)
