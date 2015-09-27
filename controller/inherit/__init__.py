# Giving the GUI some functionality!

class Control(object):
    """
    Piece together elements to control them. Keeping data and visuals in sync.
    Override functions beginning with "_"
    view = view for the required GUI
    events = fired upon things happening
    data = data needed to build out the control
    """
    def __init__(s, elements={}, events={}, data={}):
        s.elements = elements
        s.events = events
        s.data = data
        s.root = ""
        s._buildCtrl()
    def delete(s):
        """
        Delete the Control
        """
        pass
    def _buildCtrl(s):
        """
        Begin making the control
        """
        pass
    def _deleteCtrl(s):
        """
        Remove all gui elements etc to delete the control
        """
        pass
