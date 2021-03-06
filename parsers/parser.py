# Base parser Class to be overridden
# Created 01/10/15 Jason Dixon
# http://internetimagery.com

class Parser(object):
    """
    Single parser with requried information
    """
    def __init__(s, view, model, data):
        s.view = view
        s.model = model
        s.data = data
    def reset(s):
        s.description = "Replace this description with a relevant one."
        s.icon = "replaceme.png"
        s.name = "Base Parser. Replace me."
        s.priority = 0 # Set at 0 and replace if token found
        s.start()
    def start(s):
        """
        Set up everything needed to parse
        Override this
        """
        pass
    def update(s, token):
        """
        Parse a single token and return what should be displayed.
        Otherwise return token untouched.
        Override this.
        """
        return token
    def run(s):
        """
        Perform function relevant to the data aquired.
        Override this.
        """
        pass
