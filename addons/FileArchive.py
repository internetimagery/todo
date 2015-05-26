# coding: utf-8
# File Archiving
#
# Created by Jason Dixon
# 02/05/15
import maya.cmds as cmds
import zipfile
import time
import os

#debug = True  # Reload module each time is is used.


# Settings
def settings_archive(mayaFile, todo, settings):

    def filepicker():
        result = cmds.fileDialog2(ds=2, cap="Select a Folder.", fm=3, okc="Select")
        return result[0] if result else ""

    def activate(yesno):
        settings.FileArchiveActive = yesno
        cmds.columnLayout(col, e=True, bgc=[0.5, 0.5, 0.5] if yesno else [0.2, 0.2, 0.2])
        cmds.checkBox(activeButton, e=True, v=yesno)
        cmds.iconTextButton(pathButton, e=True, en=yesno)

    def updatePath(path):
        settings.FileArchivePath = path
        cmds.iconTextButton(pathButton, e=True, l=path if path else "Pick archive folder.")

    # Use File Archiving
    col = cmds.columnLayout(
        adjustableColumn=True,
        ann="Store a backup of the current scene into the provided folder upon each Todo completion.")
    activeButton = cmds.checkBox(
        l="Use File Archive",
        cc=activate)
    # File archive path
    cmds.rowLayout(nc=2, ad2=2)
    cmds.text(label=" - ")
    pathButton = cmds.iconTextButton(
        image="fileOpen.png",
        style="iconAndTextHorizontal",
        c=lambda: updatePath(filepicker()))  # TODO errors when no folder is chosen because of 0 index
    activate(settings.FileArchiveActive)
    updatePath(settings.FileArchivePath)


# Archive file
def archive(mayaFile, todo, settings):
    archive = settings.FileArchiveActive
    path = settings.FileArchivePath
    if archive and mayaFile:
        if path and os.path.isdir(path):
            basename = os.path.basename(mayaFile)
            whitelist = [" ", ".", "_"]  # Strip invalid characters
            label = "".join(ch for ch in todo["label"] if ch.isalnum() or ch in whitelist).rstrip()
            name = "%s_%s_%s.zip" % (os.path.splitext(basename)[0], int(time.time() * 100), label)
            dest = os.path.join(path, name)
            z = zipfile.ZipFile(dest, "w")
            z.write(mayaFile, basename)
            z.close()
            print "File archived to: %s" % dest
        else:
            cmds.confirmDialog(title="Uh oh...", message="Can't save file archive. You need to provide a folder.")


def hooks():
    return {
        "settings.archive": settings_archive,
        "todo.complete": archive
        }
