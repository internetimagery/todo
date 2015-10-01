# Parse out files and return a function that opens thems.
# Created 01/10/15 Jason Dixon
# http://internetimagery.com

from todo.parsers.parser import Parser
import maya.cmds as cmds
import webbrowser
import subprocess
import os.path
import os

class File(Parser):
    def start(s):
        s.description = "No files to open."
        s.icon = "openScript.png"
        s.name = "file"
        s.files = set()
        filename = cmds.file(q=True, sn=True)
        s.root = os.path.dirname(filename) if filename else ""
    def update(s, token):
        if "/" in token:
            path = os.path.realpath(os.path.join(s.root, token))
            if os.path.isfile(path):
                s.files.add(path)
                s.description = "Open the files: %s" % ", ".join(s.files)
                s.priority += 2 # Higher priority if more files found
                return os.path.basename(path)
        return token
    def run(s):
        if s.files:
            maya = [f for f in s.files if f[-3:] in [".ma", ".mb"]]
            other = [f for f in s.files if f not in maya]
            if other:
                for f in other:
                    print "Opening: %s" % os.path.basename(f)
                    universalOpen(f)
            if maya: # Only open one maya file
                print "Opening: %s" % os.path.basename(maya[0])
                fileOpen(maya[0])

def fileOpen(path):
    """
    Open a file
    """
    def savePrompt():
        p = cmds.setParent(q=True)
        cmds.columnLayout(adj=True, p=p)
        cmds.rowLayout(nc=2)
        cmds.columnLayout()
        eval(embedImage())
        cmds.setParent("..")
        cmds.columnLayout(adj=True)
        cmds.text(al="left", hl=True, l="""
<h3>There are unsaved changes in your scene.</h3>
<div>Would you like to save before leaving?</div>""", h=70)
        cmds.rowLayout(nc=3, h=30)
        cmds.button(l="Yes please!".center(20), c="cmds.layoutDialog(dismiss=\"yes\")")
        cmds.button(l="No Thanks".center(20), c="cmds.layoutDialog(dismiss=\"no\")")
        cmds.button(l="Cancel".center(20), c="cmds.layoutDialog(dismiss=\"cancel\")")
        cmds.setParent("..")
        cmds.setParent("..")

    if os.path.isfile(path):
        if path[-3:] in [".ma", ".mb"]:  # Make a special exception for maya files.
            if cmds.file(mf=True, q=True):  # File is modified. Need to make some changes.
                answer = cmds.layoutDialog(ui=savePrompt, t="Excuse me one moment...")
                if answer == "yes":
                    if not cmds.file(q=True, sn=True):
                        loc = cmds.fileDialog2(ds=2, sff="Maya ASCII", ff="Maya Files (*.ma *.mb);;Maya ASCII (*.ma);;Maya Binary (*.mb);;")
                        if loc:
                            cmds.file(rn=loc[0])
                        else:
                            return
                    cmds.file(save=True)
                elif answer == "no":
                    pass
                else:
                    return
            cmds.file(path, o=True, f=True)
        else:
            universalOpen(path)


def universalOpen(command):
    """
    Open file in different OS's
    """
    try:
        os.startfile(command)  # Open file on windows
    except AttributeError:  # Open file on anything else
        for com in [["open"], ["xdg-open"], ["gnome-open"], ["kde-open"], ["exo-open"]]:
            try:
                return subprocess.Popen(com + [command])
            except OSError:
                pass
            webbrowser.open(command)
