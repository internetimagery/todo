# Check for objects and select one if found
# Created 01/10/15 Jason Dixon
# http://internetimagery.com

from todo.parsers.parser import Parser
import maya.cmds as cmds

class Object(Parser):
    def start(s):
        s.icon = "centerCurrentTime.png"
        s.name = "object"
        s.objects = []
    def update(s, token):
        obj = cmds.ls(token, r=True)
        if obj:
            s.objects += obj
            s.priority = 5
            s.description = "Select objects:%s" % "".join(["\n* %s" % o for o in s.objects])
        return token
    def run(s):
        if s.objects:
            def select(objs):
                cmds.select(objs, r=True)
            if 1 < len(s.objects):
                query(s.objects)
            else:
                select(s.objects)

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
            print "Selecting %s" obj
        cmds.deleteUI(window)
        callback(o)
    def addPicker(o):
        cmds.button(
            l="Select object: %s" % o,
            c=lambda x: pick(o)
            )
    window = cmds.window(t="Which range would you like?", rtf=True)
    cmds.columnLayout(adj=True)
    for o in objects:
        addPicker(o)
    cmds.button(
        l="Select All!",
        c=lambda x: pickAll(objects)
    )
    cmds.showWindow(window)
