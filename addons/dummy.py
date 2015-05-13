# Dummy addon. Doesn't do anything, but is something to build off of.
#
# Created by Jason Dixon
# 02/05/15

debug = True  # Add this to override caching. So changes can be observed while testing.


def run_hook(mayaFile, todo, settings):
    """
    Run hook for whatever event is fired.
    mayaFile = path to scene.
    todo = todo metadata (optional).
    settings = get() and set() settings. !!Beware setting the settings in hooks other than ones denoted with "settings" ie "settings.archive"!!
    
    """
    pass


def hooks():
    return {
        "settings.archive": run_hook,
        "todo.complete": run_hook,
        "todo.delete": run_hook,
        "todo.create": run_hook,
        "todo.edit": run_hook
        }
