# Data management in Maya

import maya.cmds as cmds
from json import dumps, loads

class Store(object):
    """
    Store information in a Maya scene
    """
    def __init__(s):
        s.cache = {}
        for k, v in (lambda x: zip(x[::2], x[1::2]))(cmds.fileInfo(q=True)):
            v = v.decode("unicode_escape")
            try:
                s.cache[k] = loads(v)
            except ValueError:
                s.cache[k] = v

    """
    Get data
    """
    def get(s, k, default):
        return s.cache[k] if k in s.cache else default

    """
    Set data
    """
    def set(s, k, v):
        if type(v) == str:
            cmds.fileInfo(k, v)
        else:
            cmds.fileInfo(k, dumps(v))
        s.cache[k] = v

    """
    Remove data
    """
    def rm(s, k):
        cmds.fileInfo(rm=k)
        del s.cache[k]
