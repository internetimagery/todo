# Maya element base

class Element(object):
    """
    Base object definition
    """
    def __init__(s, attributes={}, events={}, parent=None):
        s._attr = attributes
        s._events = events
        s._parent = parent.root if parent else None
        s._root = None # base of control
        s._attach = None # attachment point if applicable
        s._build(s._parent)
    def _build(s, parent):
        """
        Build Element
        """
    def _update(s, attr, value):
        """
        Update Elements attributes
        """
        pass

a=Element()
a.something
test = a.test
a.somethingelse = "this"
print a.somethingelse
