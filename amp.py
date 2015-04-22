# Wrapper for AMP
import maya.cmds as cmds
import os

tempbase = "/Users/Maczone/Documents/AnimationMentor/Work_on_server/Shots/students/209000/jdixon_209238/_locker/my_locker/working/pose_a_day/April/day_008/"
temppath = os.path.join(tempbase, "day_008.ma")


class AMP(object):
    """
    Wrapper for AMP
    """
    def __init__(self):
        try:
            import am.cmclient.manager
            import am.cmclient.config
            self.config = am.cmclient.config.Configurator()
            self.manager = am.cmclient.manager.getShotManager(self.config)
            self.root = self.manager.contentRoot
            self.working = self._walk(self.root, [], "working")
            self.ok = True
        except ImportError:
            self.ok = False

    def save(self, path, comment):
        """
        Save off file.
        """
        if self.ok and os.path.isfile(path) and self.root in path:
            if self._status(path):
                self._checkIn(path, comment)
                self._checkOut(path)
                return True
            elif "Confirm" == cmds.confirmDialog(title="Hold up...", message="You need to check out the file first.\nWould you like to do that now?"):
                self._checkOut(path)
                self._checkIn(path, comment)
                self._checkOut(path)
                return True
        return False

    def _walk(self, path, paths, stop):
        for d in os.listdir(path):
            p = os.path.join(path, d)
            if os.path.isdir(p):
                if d == stop:
                    paths.append(p)
                else:
                    self._walk(p, paths, stop)
        return paths

    def _checkIn(self, path, comment):
        """
        Check in the file to lock in changes.
        """
        self.manager.checkinViewItemByPath(path, comment=comment)

    def _checkOut(self, path):
        """
        Check out file for editing.
        """
        self.manager.checkoutViewItemByPath(path)

    def _revert(self, path):
        """
        Revert file back to the most recent state.
        """
        self.manager.revertViewItemByPath(path)

    def _status(self, path):
        """
        Check the locked status of a file.
        """
        return os.access(path, os.W_OK)  # True = Checked out. False = Checked in.


am = AMP()
print am.working