# Dummy addon. Doesn't do anything, but is something to build off of.
#
# Created by Jason Dixon
# 02/05/15

#debug = True  # Add this to override caching. So changes can be observed while testing.


def run_hook(mayaFile, todo, gui, settings):
    """
    Run hook for whatever event is fired.
    mayaFile = path to scene.
    todo = todo metadata (optional).
    gui = gui to parent any created gui items to (optional).
    settings = get() and set() settings.
    """
    pass


def hooks():
    return {
        "settings.archive": run_hook,
        "archive": run_hook
        }
