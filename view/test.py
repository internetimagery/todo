# Testing persistence through object storage

import maya.cmds as cmds
import json

class Store(dict):
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
        cmds.setAttr(s.node+".notes", json.dumps(s), type="string")


s = Store("another")
print len(s.get("long", "not here"))
s["long"] = "b" * 3
