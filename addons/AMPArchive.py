# Import AMP support
import am.client.cmclient.config as config
import am.client.cmclient.manager as manager
import am.client.gui.utils as utils
import maya.cmds as cmds
import maya.utils as Mutil
import os

#debug = True


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
def archive(mayaFile, todo, settings):
    comment = todo["label"]
    amp = settings("AMPArchive.active", False)
    if amp:
        if Mutil.executeInMainThreadWithResult(lambda: AMPArchive().archive(mayaFile, comment)):
            print "Checking file into AMP."
        else:
            print "Couldn't check in file to AMP."


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

    def archive(s, path, comment):
        """
        Save off file.
        """
        if os.path.isfile(path) and s.login() and s.manager.isClientPathManaged(path):
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

    def _checkLogin(s):
        """
        Check login status. Return True for logged in.
        """
        return s.manager.checkSessionToken()

    def _checkIn(s, path, comment):
        """
        Check in the file to lock in changes.
        """
        if not s.manager.checkinViewItemByPath(path, comment=comment):
            s.manager.addViewItemByPath(path, comment=comment)

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

    def login(s):
        """
        Check if we are logged in. If not, try to log in.
        """
        s.loggingin = True
        def cancel():
            """
            Cancel out of the login loop
            """
            s.loggingin = False

        def ok():
            """
            Try to sign in
            """
            s.config.setDefaultServer(d.server_name)
            s.manager.login(unicode(d.username), unicode(d.password))

        for i in range(10):
            if s.manager.checkSessionToken():  # Check if we are logged in.
                print "Signed into AMP."
                return True
            elif not s.loggingin:
                break
            else:
                print "Login attempt %s of 10." % str(i + 1)
                d = utils.LoginDialog(
                    message_to_user="Can't archive your file to AMP.\nYou are not logged in.\nLets log in now. :)",
                    server_config=s.config)
                d.set_click_handler("ok", ok)
                d.set_click_handler("cancel", cancel)
                d.draw()
                d.exec_()
        return False
