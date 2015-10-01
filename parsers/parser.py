# Base parser Class to be overridden
# Created 01/10/15 Jason Dixon
# http://internetimagery.com

class Parser(object):
    """
    Single parser with requried information
    """
    description = "Replace this description with a relevant one."
    icon = "replaceme.png"
    name = "Base Parser. Replace me."
    priority = 0 # Set at 0 and replace if token found
    def update(s, token):
        """
        Parse a single token and return what should be displayed.
        Otherwise return token untouched.
        """
        return token
    def run(s):
        """
        Perform function
        """
        pass
