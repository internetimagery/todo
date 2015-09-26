# Base class element to be inherited on various other GUI interfaces.
try:
    from cPickle import dumps
except ImportError:
    from pickle import dumps

class Element(object):
    """
    Override all functions starting with "_"
    Attributes: Dict with keys and values corresponding to GUI elements.
    Events: Callback functions that fire on user input.
    """
    def __init__(s, attributes={}, events={}):
        # Format
        s.attributes = attributes # This elements attributes
        s.attributeCache = dict((k, dumps(s.attributes[k])) for k in s.attributes)
        s.events = events # GUI events triggered by this element
        # Hierarchy
        s.children = set() # Children of this element
        s.parent = None # Parent of this element
        # Sctructure
        s.attach = None # Attachment point where applicable for children
        s._buildGUI()
        s._updateGUI()
    def update(s, key=None, value=None):
        """
        Update changes to the information on the GUI element.
        """
        if key in s.attributes:
            check = dumps(value)
            if s.attributesCache[key] != value:
                s.attributeCache[key] = check
                s.attributes[key] = value
                s._updateGUI(key)
            else:
                print "%s's value unchanged. Skipping update." % key.title()
        else:
            s._updateGUI(None)
    def delete(s):
        """
        Delete element from the GUI
        """
        if s.parent and s in s.parent.children:
            s.parent.children.remove(s)
            s.children = []
        s._deleteGUI()
    def attach(s, element):
        """
        Attach another element to this one
        """
        if s.attach:
            s.children.add(element)
            element._parent(s.attach)
    def detatch(s, element):
        """
        Detatch an element from this one
        """
        if element in s.children:
            s.children.remove(element)
            element.delete()
    def _buildGUI(s):
        """
        Build out the gui framework bare bones.
        Bind events from s._events
        """
        pass
    def _updateGUI(s, attribute):
        """
        Either update a single attribute if provided, or the whole thing.
        Using s.attributes to get information
        """
        pass
    def _deleteGUI(s):
        """
        Remove GUI element
        """
        pass
    def _parentGUI(s, structure):
        """
        Attach this element to another GUI element
        """
        pass
