# Check for objects and select one if found
# Created 01/10/15 Jason Dixon
# http://internetimagery.com

from todo.parsers.parser import Parser
import maya.cmds as cmds

class Object(Parser):
    def start(s):
        s.icon = "todo.object"
        s.name = "object"
        s.objects = set()
    def update(s, token):
        try:
            obj = cmds.ls(token, r=True)
            if obj:
                s.objects |= set(obj)
                s.priority = 5
                if 1 < len(s.objects):
                    s.description = "Select objects:" + "\n- ".join(["\n* %s" % o for o in s.objects])
                else:
                    s.description = "Select object: %s" % s.objects[0]
        except RuntimeError:
            pass
        return token
    def run(s):
        print "RUNNING", s.objects
        if s.objects:
            def select(objs):
                cmds.select(objs, r=True)
            if 1 < len(s.objects):
                query(s.objects, select)
            else:
                select(list(s.objects))

def query(objects, callback):
    """
    Ask user to pick desired range
    """
    def pick(o):
        print "Selecting object: %s" % o
        cmds.deleteUI(window)
        callback(o)
    def pickAll(o):
        for obj in o:
            print "Selecting %s" % obj
        cmds.deleteUI(window)
        callback(list(o))
    def addPicker(o):
        cmds.button(
            l="Select object: %s" % o,
            c=lambda x: pick(o)
            )
    window = cmds.window(t="Which Object would you like?", rtf=True)
    cmds.columnLayout(adj=True)
    for o in objects:
        addPicker(o)
    cmds.button(
        l="Select All!",
        c=lambda x: pickAll(objects)
    )
    cmds.showWindow(window)
