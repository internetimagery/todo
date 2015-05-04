# Archive options for Git
#
# Created by Jason Dixon
# 04/05/2015
import subprocess as sub
import maya.cmds as cmds
import os


# Settings menu
def settings_archive(mayaFile, todo, gui, settings):
    if not Git().version()[1]:
        git = settings.get("GitArchive.active", False)
        cmds.columnLayout(
            adjustableColumn=True,
            bgc=[0.5, 0.5, 0.5] if git else [0.2, 0.2, 0.2])
        cmds.checkBox(
            l="Use Git archive",
            v=git,
            cc=lambda x: settings.set("GitArchive.active", x))
        cmds.setParent("..")


def archive(mayaFile, todo, gui, settings):
    if settings.get("GitArchive.active", False) and mayaFile:
        check = Git().status(mayaFile)
        if check[1]:
            print "Cannot commit file: %s" % check[1]
        else:
            Git().commit(mayaFile, todo["label"])


def hooks():
    return {
        "settings.archive": settings_archive,
        "todo.complete": archive
        }


class Git(object):
    """
    Control Git
    """
    def __init__(s, *args, **kwargs):
        if args or kwargs:
            return s._git(*args, **kwargs)

    def _git(s, *args, **kwargs):
        """
        git command line function
        """
        try:
            return sub.Popen(["git"] + list(args), stdout=sub.PIPE, stderr=sub.PIPE, **kwargs).communicate()
        except OSError as e:
            return ("", e.__str__())

    def commit(s, path, comment):
        if not s._git("add", os.path.basename(path), cwd=os.path.dirname(path))[1]:
            if not s._git("commit", "--only", "--quiet", "--message", comment, os.path.basename(path), cwd=os.path.dirname(path))[1]:
                print "File committed"

    def status(s, path):
        return s._git("status", "--porcelain", os.path.basename(path), cwd=os.path.dirname(path))

    def version(s):
        return s._git("--version")
