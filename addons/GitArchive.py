# coding: utf-8
# Archive options for Git
#
# Created by Jason Dixon
# 04/05/2015
import subprocess as sub
import maya.cmds as cmds
import os


# Settings menu
def settings_archive(mayaFile, todo, settings):

    def getInput():
        result = cmds.promptDialog(
            title="Optional Branch",
            message="Enter Branch Name:",
            button=["OK", "Cancel"],
            defaultButton="OK",
            cancelButton="Cancel",
            dismissString="Cancel")
        if result == "OK":
            return cmds.promptDialog(q=True, text=True)
        return ""

    def update(yesno):
        settings.GitArchiveActive = yesno
        cmds.columnLayout(col, e=True, bgc=[0.5, 0.5, 0.5] if yesno else [0.2, 0.2, 0.2])
        cmds.checkBox(activeButton, e=True, v=yesno)
        cmds.rowColumnLayout(row, e=True, en=yesno)
        cmds.text(vers, e=True, en=yesno)

    def updatePush(yesno):
        settings.GitArchivePush = yesno
        cmds.checkBox(pushButton, e=True, v=yesno)
        cmds.iconTextButton(branchButton, e=True, en=yesno)

    def updateBranch(text):
        settings.GitArchiveBranch = text
        cmds.iconTextButton(branchButton, e=True, l=text if text else "Enter remote branch name.")

    version = Git().version()
    if not version[1]:
        col = cmds.columnLayout(
            adjustableColumn=True,
            ann="Commit the Maya file into Git (if the file is located in a valid repo) upon each Todo task completion.")
        activeButton = cmds.checkBox(
            l="Use Git archive",
            cc=update)
        row = cmds.rowColumnLayout(nc=2)
        cmds.text(label=" - ")
        pushButton = cmds.checkBox(
            l="Automatically PUSH changes.",
            cc=updatePush)
        cmds.text(label=" - ")
        branchButton = cmds.iconTextButton(
            image="createContainer.png",  # "publishNamedAttribute.png" "channelBoxHyperbolicOn.png"  "createContainer.png"
            style="iconAndTextHorizontal",
            c=lambda: updateBranch(getInput()))
        cmds.setParent("..")
        vers = cmds.text(
            l="%s found." % version[0].capitalize().replace("\n", ""))
        updatePush(settings.GitArchivePush)
        updateBranch(settings.GitArchiveBranch)
        update(settings.GitArchiveActive)


def archive(mayaFile, todo, settings):
    if settings.GitArchiveActive and mayaFile:
        check = Git().status(mayaFile)
        if check[1]:
            print "Cannot commit file: %s." % check[1]
        else:
            if Git().commit(mayaFile, todo["label"]) and settings.GitArchivePush:
                print "Pushing update"
                pushed = Git().push(mayaFile, settings.GitArchiveBranch)
                print pushed[1] if pushed[1] else pushed[0]


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

    def push(s, path, dest):
        return s._git("push", dest, cwd=os.path.dirname(path))

    def commit(s, path, comment):
        if not s._git("add", os.path.basename(path), cwd=os.path.dirname(path))[1]:
            if not s._git("commit", "--quiet", "--message", comment, "--only", os.path.basename(path), cwd=os.path.dirname(path))[1]:
                print "File committed"
                return True

    def status(s, path):
        return s._git("status", "--porcelain", os.path.basename(path), cwd=os.path.dirname(path))

    def version(s):
        return s._git("--version")
