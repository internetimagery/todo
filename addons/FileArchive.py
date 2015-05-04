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
def settings_archive(mayaFile, todo, gui, settings):

    def filepicker():
        result = cmds.fileDialog2(ds=2, cap="Select a Folder.", fm=3, okc="Select")
        return result[0] if result else ""

    archive = settings.get("FileArchive.active", False)
    path = settings.get("FileArchive.path")
    # Use File Archiving
    cmds.columnLayout(
        adjustableColumn=True,
        bgc=[0.5, 0.5, 0.5] if archive else [0.2, 0.2, 0.2],
        p=gui)
    cmds.checkBox(
        l="Use File Archive",
        v=archive,
        cc=lambda x: settings.set("FileArchive.active", x))
    # File archive path
    cmds.rowLayout(nc=2, ad2=2)
    cmds.text(label=" - ")
    cmds.iconTextButton(
        en=archive,
        image="fileOpen.png",
        l=path if path else "Pick archive folder.",
        style="iconAndTextHorizontal",
        c=lambda: settings.set("FileArchive.path", filepicker()))  # TODO errors when no folder is chosen because of 0 index
    cmds.setParent("..")


# Archive file
def archive(mayaFile, todo, gui, settings):
    archive = settings.get("FileArchive.active", False)
    path = settings.get("FileArchive.path", False)
    if archive:
        if path and os.path.isdir(path):
            basename = os.path.basename(mayaFile)
            name = "%s_%s_%s.zip" % (os.path.splitext(basename)[0], int(time.time() * 100), todo["label"])
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
        "archive": archive
        }
