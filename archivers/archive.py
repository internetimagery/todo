# Base archive to be overridden
# Created 02/10/15 Jason Dixon
# http://internetimagery.com

class Archive(object):
    def __init__(s, view, model, settings):
        """
        Archive tool. Save the file off in various places to backup.
        """
        # Store our interfaces
        s.view = view
        s.model = model
        s.settings = settings
        s.start()
    def start(s):
        """
        Add custom init code here.
        """
        pass
    def buildSettings(s, parent):
        """
        Build the settings for this archive into the settings panel
        """
        pass
    def runArchive(s, todo, filename):
        """
        Archive the file given the todo and filename
        """
        pass
