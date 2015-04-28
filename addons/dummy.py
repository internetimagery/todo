# Dummy addon. Doesn't do anything, but is something to build off of.

debug = True  # Add this to override caching. So changes can be observed while testing.


def settings_archive(getter, setter):
    """
    Create some GUI elements that will be placed in the settings window.
    Use the getter and setter to get and retrieve settings info ie:
    getter("key", "default value")
    setter("key", "new value")
    """
    pass


def archive(mayaFile, todo, settings):
    """
    Perform an archive action on the maya file when todo is checked off.
    It's a good idea to check for a previously set up setting before doing anything so users have a choice in what is happening.
    mayaFile = path to the current Maya scene
    todo = the metadata from the todo
    settings = getter for settings information. ie: settings("key", "default value")
    """
    pass


def cleanup():
    """
    Run after any other action is taken. Use for cleaning up anything that may need it.
    Delete temp files etc. This will run even if an error occurs.
    """
    pass
