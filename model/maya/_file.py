# Maya specific file functionality
# Created 01/10/15 Jason Dixon
# http://internetimagery.com

import maya.cmds as cmds
import todo.model._file as _file
import os.path

class File(_file.File):
    """
    File functionality
    """
    def _FILE_Setup(s):
        s.extensions = [".ma", ".mb"]

    def _FILE_Running(s):
        f = cmds.file(q=True, sn=True)
        return f if f else ""

    def _FILE_Load(s, path):
        if path:
            realpath = os.path.realpath(path)
            if os.path.isfile(realpath):
                if cmds.file(mf=True, q=True):  # File is modified. Need to prompt a save.
                    answer = cmds.confirmDialog(
                        t="Save Changes",
                        m="Save changes to %s" % "file",
                        b=["Save", "Don't Save", "Cancel"],
                        db="Save",
                        cb="Cancel",
                        ds="Cancel"
                        )
                    if answer == "Save":
                        if not path:
                            loc = cmds.fileDialog2(ds=2, sff="Maya ASCII", ff="Maya Files (*.ma *.mb);;Maya ASCII (*.ma);;Maya Binary (*.mb);;")
                            if loc:
                                cmds.file(rn=loc[0])
                            else:
                                return
                        s._FILE_Save(None)
                    elif answer == "Cancel":
                        return
                cmds.file(path, o=True, f=True)
                return
        print "Could not open file: \"%s\"" % path

    def _FILE_Save(s, todo):
        path = s._FILE_Running()
        if path:
            realpath = os.path.realpath(path)
            cmds.file(save=True)
        else:
            "Could not save scene."

    def _FILE_SaveAs(s, todo, path):
        if path:
            cmds.file(rn=path)
            s._FILE_Save(todo)
        else:
            print "No path given to save."
