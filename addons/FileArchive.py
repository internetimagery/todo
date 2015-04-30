# File Archiving
import maya.cmds as cmds
import zipfile
import time
import os

#debug = True  # Reload module each time is is used.


# Settings
def settings_archive(getter, setter):

    def filepicker():
        result = cmds.fileDialog2(ds=2, cap="Select a Folder.", fm=3, okc="Select")
        return result[0] if result else ""

    archive = getter("FileArchive.active", False)
    # Use File Archiving
    cmds.columnLayout(
        adjustableColumn=True,
        bgc=[0.5, 0.5, 0.5] if archive else [0.2, 0.2, 0.2])
    cmds.checkBox(
        l="Use File Archive",
        v=archive,
        cc=lambda x: setter("FileArchive.active", x))
    # File archive path
    cmds.rowLayout(nc=2, ad2=2)
    cmds.text(label=" - ")
    path = getter("FileArchive.path", "")
    cmds.iconTextButton(
        en=archive,
        image="fileOpen.png",
        l=path if path else "Pick archive folder.",
        style="iconAndTextHorizontal",
        c=lambda: setter("FileArchive.path", filepicker()))  # TODO errors when no folder is chosen because of 0 index
    cmds.setParent("..")
    cmds.setParent("..")


# Archive file
def archive(mayaFile, todo, settings):
    archive = settings("FileArchive.active", False)
    path = settings("FileArchive.path", "")
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


# Clean up anything that needs cleaning
def cleanup():
    pass
