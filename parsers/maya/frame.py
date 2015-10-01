# Pull out a single frame
# Created 01/10/15 Jason Dixon
# http://internetimagery.com

from todo.parsers.parser import Parser
import maya.cmds as cmds

class Frame(Parser):
    def start(s):
        s.icon = "todo.frame"
        s.name = "frame"
        s.frames = []
    def update(s, token):
        try:
            num = int(token)
            s.frames.append(num)
            s.priority = 1
            s.description = "Go to frame: %s" % "".join(["\n* %s" % f for f in s.frames])
        except ValueError:
            pass
        return token
    def run(s):
        if s.frames:
            def setFrame(f):
                cmds.currentTime(f)
            if 1 < len(s.frames):
                query(s.frames, setFrame)
            else:
                setFrame(s.frames[0])

def query(item, callback):
    """
    Ask user to pick desired item
    """
    def rangePick(i):
        print "Going to frame %s" % i
        cmds.deleteUI(window)
        callback(i)
    def addPicker(i):
        cmds.button(
            l="Go to frame: %s" % i,
            c=lambda x: rangePick(i)
            )
    window = cmds.window(t="Which frame would you like?", rtf=True)
    cmds.columnLayout(adj=True)
    for i in item:
        addPicker(i)
    cmds.showWindow(window)
