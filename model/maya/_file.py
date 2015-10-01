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
                return True
        print "Could not open file: \"%s\"" % path

    def _FILE_Save(s, todo):
        path = s._FILE_Running()
        if path:
            # realpath = os.path.realpath(path)
            try:
                cmds.file(save=True)
                return True
            except RuntimeError:
                pass
        else:
            "Could not save scene."

    def _FILE_SaveAs(s, todo, path):
        if path:
            cmds.file(rn=path)
            return s._FILE_Save(todo)
        else:
            print "No path given to save."
File = File()

class safeOut(object):
    """
    Protect output during threads
    """
    def __init__(s):
        s.oldOut = sys.stdout
        sys.stdout = s

    def write(s, *t):
        t = "".join(t)
        if len(t.rstrip()):
            utils.executeDeferred(lambda: s.oldOut.write("%s\n" % t))

    def __enter__(s):
        return s

    def __exit__(s, errType, errVal, trace):
        sys.stdout = s.oldOut
        if errType:
            s.write("Uh oh... there was a problem. :(")
            s.write("%s :: %s" % (errType.__name__, errVal))
            for t in traceback.format_tb(trace):
                s.write(t)
        return True

class Popup(object):
    """
    Create a one time popup
    """
    def __init__(s, message):
        s.uid = "TODO_POPUP_%s" % int((time.time() * 100))  # Generate unique ID
        s.message = message

    def stringify(s, data):
        return "python(\"%s\");" % data.replace("\\", "\\\\").replace("\"", "\\\"").replace("\n", r"\n")

    def __enter__(s):
        s.job = cmds.scriptNode(n=s.uid, st=2, bs="")
        s.code = """
import maya.cmds as cmds
uid = "%(uid)s"
job = "%(job)s"
if cmds.fileInfo(uid, q=True) == ["ok"]:
    def makepopup():
        p = cmds.setParent(q=True)
        cmds.rowLayout(nc=2, ad2=2, p=p)
        cmds.columnLayout()
        %(image)s
        cmds.setParent("..")
        cmds.columnLayout(adj=True)
        cmds.text(al="left", hl=True, l=\"\"\"%(message)s\"\"\", h=70)
        cmds.button(l="Thanks", c="cmds.layoutDialog(dismiss=\\"gone\\")", h=30)
        cmds.setParent("..")
    cmds.layoutDialog(ui=makepopup, t="Welcome Back")
if cmds.objExists(job):
    cmds.delete(job)
cmds.fileInfo(rm=uid)
""" % {"uid": s.uid, "job": s.job, "image": embedImage(), "message": s.message}
        cmds.scriptNode(s.job, e=True, bs=s.stringify(s.code))
        cmds.fileInfo(s.uid, "ok")
        return s

    def __exit__(s, err, val, trace):
        """
        Remove those things from the scene
        """
        cmds.fileInfo(rm=s.uid)
        if cmds.objExists(s.job):
            cmds.delete(s.job)


#             process = cmds.scriptJob(e=['SceneSaved', performArchive], ro=True)
#             try:
#                 message = """
# <div>- This Scene was last saved on <em>%(time)s</em>.</div>
# <div>- Completing the task: <code>%(todo)s</code></div>
# <div>- The file <strong>has not been modified since.</strong></div><br>
# """ % {"time": time.ctime(), "todo": tempmeta["label"]}
#                 with Popup(message):
#                     cmds.file(save=True)  # Save the scene
#             except RuntimeError:  # If scene save was canceled or failed. Reset everything
#                 if cmds.scriptJob(ex=process):
#                     cmds.scriptJob(kill=process)
#                 s.data[uid] = temp
