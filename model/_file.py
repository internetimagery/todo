# Override with software specific file functionality
# Created 01/10/15 Jason Dixon
# http://internetimagery.com

import os
import sys
import os.path
import webbrowser
import subprocess

class File(object):
    """
    File functionality
    Override "_FILE_" prefixes
    """
    def __init__(s, path=None):
        s.extensions = [] # extensions to check for compatability
        s._FILE_Setup()
    def load(s, path=None):
        if path and os.path.exists(path):
            name, ext = os.path.splitext(path)
            if ext in s.extensions:
                return s._FILE_Load(s, path) # Load file with software
            else: # Try opening the file with OS's software
                try:
                    if sys.platform == "win32": # Window
                        os.startfile(path)
                    elif sys.platform == "darwin": # Mac
                        subprocess.Popen(["open", path])
                    else: # Others, probably Linux
                        for com in ["xdg-open", "gnome-open", "kde-open", "exo-open"]:
                            try:
                                return subprocess.Popen([com, path])
                            except OSError:
                                pass
                            raise OSError, "No commands worked. :("
                except Exception as e:
                    print "Trouble: %s" % str(e)
                    webbrowser.open(path)
        else:
            print "Could not load file: \"%s\"" % path
    def save(s, todo=None, path=None, archive=None):
        """
        Save file. If todo, then archive the file too.
        """
        curr = s._FILE_Running()
        if not path or curr == path: #saving over the same file
            return s._FILE_Save(todo, archive)
        else: # Saving as a new file.
            return s._FILE_SaveAs(todo, path, archive)

    def _FILE_Setup(s):
        """
        Init any variables, such as extensions
        """
        pass
    def _FILE_Running(s):
        """
        Get the currently active filename or return if unsaved.
        """
        pass
    def _FILE_Load(s, path):
        """
        Load a given file from a pathname
        """
        pass
    def _FILE_Save(s, todo, archive):
        """
        Save currently open scene
        """
        pass
    def _FILE_SaveAs(s, todo, path, archive):
        """
        Save currently open scene as a new file
        """
        pass
