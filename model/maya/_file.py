# Maya specific file functionality
# Created 01/10/15 Jason Dixon
# http://internetimagery.com

import maya.cmds as cmds
import todo.model._file as _file

class File(_file.File):
    """
    File functionality
    """
    def _FILE_Setup(s):
        s.extensions = [".ma", ".mb"]

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
    def _FILE_Save(s, todo):
        """
        Save currently open scene
        """
        pass
    def _FILE_SaveAs(s, todo, path):
        """
        Save currently open scene as a new file
        """
        pass
