# Base class element to be inherited on various GUI interfaces.
try:
    from cPickle import dumps
except ImportError:
    from pickle import dumps

class Element(object):
    """
    Override all functions starting with "O_"
    Attributes: Dict with keys and values corresponding to GUI elements.
    Events: Callback functions that fire on user input.
    """
    def __init__(s, attributes={}, events={}):
        # Format
        s.attributes = attributes # This elements attributes
        s._attributeCache = dict((k, dumps(s.attributes[k])) for k in s.attributes)
        s.events = events # GUI events triggered by this element
        s._isVisible = True # GUI visibility
        s._isEnabled = True # GUI enability ... not a word?
        # Hierarchy
        s._children = set() # Children of this element
        s._parent = None # Parent of this element
        # Sctructure
        s.attach = None # Attachment point where applicable for children
        s.O_buildGUI()
        s.O_updateGUI()
    def update(s, key=None, value=None):
        """
        Update changes to the information on the GUI element.
        """
        if key in s.attributes:
            check = dumps(value)
            if s.attributesCache[key] != value:
                s._attributeCache[key] = check
                s.attributes[key] = value
                s.O_updateGUI(key)
            else:
                print "%s's value unchanged. Skipping update." % key.title()
        else:
            s._updateGUI(None)
        return s
    def delete(s):
        """
        Delete element from the GUI
        """
        if s._parent and s in s._parent.children:
            s._parent.children.remove(s)
            s._children = []
        s.O_deleteGUI()
        return s
    def parent(s, element):
        """
        Attach another element to this one
        """
        if s.attach:
            s._children.add(element)
            element.O_parent(s.attach)
        return s
    def unparent(s, element):
        """
        Detatch an element from this one
        """
        if element in s._children:
            s._children.remove(element)
            element.delete()
        return s
    def show(s):
        """
        Make element visible
        """
        if not s._isVisible:
            s._isVisible = True
            s.O_visible(True)
        return s
    def hide(s):
        """
        Make element invisible
        """
        if s._isVisible:
            s._isVisible = False
            s.O_visible(False)
        return s
    def enabled(s):
        """
        Enable element
        """
        if not s._isEnabled:
            s._isEnabled = True
            s.O_active(True)
        return s
    def disable(s):
        """
        Disable element
        """
        if s._isEnabled:
            s._isEnabled = False
            s.O_active(False)
        return s
    def O_buildGUI(s):
        """
        Build out the gui framework bare bones.
        Bind events from s._events
        """
        pass
    def O_updateGUI(s, attribute):
        """
        Either update a single attribute if provided, or the whole thing.
        Using s.attributes to get information
        """
        pass
    def O_deleteGUI(s):
        """
        Remove GUI element
        """
        pass
    def O_parentGUI(s, structure):
        """
        Attach this element to another GUI element
        """
        pass
    def O_visibleGUI(s, show):
        """
        Make element visible or invisible. True = visible
        """
        pass
    def O_enableGUI(s, enable):
        """
        Make element active/enabled or not. True = active
        """
        pass
