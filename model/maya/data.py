# Data persistence in the scene
# Created 03/10/15 Jason Dixon
# http://internetimagery.com

import maya.cmds as cmds
import todo.model.data
import json


class Data(todo.model.data.Data):
    def _DATA_Retrieve(s, node):
        s.node = node
        s._check()
        data = cmds.getAttr(s.node + ".notes")
        try:
            return json.loads(data.decode("unicode_escape"))
        except (TypeError, ValueError, AttributeError):
            return {}
    def _DATA_Store(s, data):
        s._check()
        cmds.setAttr(s.node + ".notes", json.dumps(data), type="string")
    def _check(s):
        if not cmds.objExists(s.node):
            sel = cmds.ls(sl=True)
            cmds.group(n=s.node, em=True)
            cmds.select(sel, r=True)
        if not cmds.attributeQuery("notes", n=s.node, ex=True):
            cmds.addAttr(s.node, ln="notes", sn="nts", dt="string")
