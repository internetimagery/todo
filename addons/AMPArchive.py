# Import AMP support
import am.client.cmclient.config as config
import am.client.cmclient.manager as manager
import maya.cmds as cmds
import os

debug = True


# Settings menu
def settings_archive(getter, setter):
    amp = getter("AMPArchive.active", False)
    cmds.columnLayout(
        adjustableColumn=True,
        bgc=[0.5, 0.5, 0.5] if amp else [0.2, 0.2, 0.2])
    cmds.checkBox(
        l="Use AMP archive",
        v=amp,
        cc=lambda x: setter("AMPArchive.active", x))
    cmds.setParent("..")


# File Archive
def archive(mayaFile, comment, settings):
    amp = settings("AMPArchive.active", False)
    if amp:
        AMPArchive().archive(mayaFile, comment)
        print "Committing file to AMP"


# Cleanup stuff
def cleanup():
    pass


class AMPArchive(object):
    """
    Archive using AMP
    """
    def __init__(s):
        s.config = config.Configurator()
        s.manager = manager.getShotManager(config=s.config)
        s.root = s.manager.contentRoot
        s.working = s._walk(s.root, [], "working")

    def archive(s, path, comment):
        """
        Save off file.
        """
        if os.path.isfile(path) and any(p in path for p in s.working):
            if s._status(path):
                s._checkIn(path, comment)
                s._checkOut(path)
                return True
            elif "Confirm" == cmds.confirmDialog(title="Hold up...", message="You need to check out the file first.\nWould you like to do that now?"):
                s._checkOut(path)
                s._checkIn(path, comment)
                s._checkOut(path)
                return True
        return False

    def _walk(s, path, paths, stop):
        """
        Search files for working dir
        """
        for d in os.listdir(path):
            p = os.path.join(path, d)
            if os.path.isdir(p):
                if d == stop:
                    paths.append(p)
                else:
                    s._walk(p, paths, stop)
        return paths

    def _checkIn(s, path, comment):
        """
        Check in the file to lock in changes.
        """
        s.manager.checkinViewItemByPath(path, comment=comment)

    def _checkOut(s, path):
        """
        Check out file for editing.
        """
        s.manager.checkoutViewItemByPath(path)

    def _revert(s, path):
        """
        Revert file back to the most recent state.
        """
        s.manager.revertViewItemByPath(path)

    def _status(s, path):
        """
        Check the locked status of a file.
        """
        return os.access(path, os.W_OK)  # True = Checked out. False = Checked in.
