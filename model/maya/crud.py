# CRUD opperations in Maya
# Created 29/09/15 Jason Dixon
# http://internetimagery.com

import json
import maya.cmds as cmds
import todo.model.crud as crud

class CRUD(crud.CRUD):
    """
    Store information in a Maya scene
    """
    def __init__(s):
        s.cache = {}
        for k, v in (lambda x: zip(x[::2], x[1::2]))(cmds.fileInfo(q=True)):
            v = v.decode("unicode_escape")
            try:
                s.cache[k] = json.loads(v)
            except ValueError:
                s.cache[k] = v
    """
    Set data
    """
    def create(s, k, v):
        if type(v) == str:
            cmds.fileInfo(k, v)
        else:
            cmds.fileInfo(k, json.dumps(v))
        s.cache[k] = v
        return v
    """
    Get data
    """
    def read(s, k=None, default=None):
        if k:
            return s.cache[k] if k in s.cache else default
        else:
            return s.cache.keys()
    """
    Update data
    """
    def update(s, k, v):
        return s.create(k, v)

    """
    Remove data
    """
    def delete(s, k):
        cmds.fileInfo(rm=k)
        del s.cache[k]

CRUD = CRUD() # Export out our CRUD
