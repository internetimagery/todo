# Data persistence in the scene
# Created 03/10/15 Jason Dixon
# http://internetimagery.com

import maya.cmds as cmds
import json

class Data(dict):
    def __init__(s, node):
        s.node = node
        s._check()
        data = cmds.getAttr(s.node+".notes")
        try:
            dict.__init__(s, **json.loads(data.decode("unicode_escape")))
        except (TypeError, ValueError, AttributeError):
            dict.__init__(s)
    def _check(s):
        if not cmds.objExists(s.node):
            cmds.createNode("unknown", n=s.node, ss=True)
        if not cmds.attributeQuery("notes", n=s.node, ex=True):
            cmds.addAttr(s.node, ln="notes", sn="nts", dt="string")
    def __setitem__(s, k, v):
        dict.__setitem__(s, k, v)
        s._check()
        print "Storing", k, v
        cmds.setAttr(s.node+".notes", json.dumps(s), type="string")
    def __delitem__(s, k, v):
        dict.__delitem__(s, k, v)
        s._check()
        print "Removing", k, v
        cmds.setAttr(s.node+".notes", json.dumps(s), type="string")
