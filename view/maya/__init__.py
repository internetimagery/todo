# Gathering all the GUI elements into one place!
# Created 30/09/15 Jason Dixon
# http://internetimagery.com

import re
import sys as _sys
reg = re.compile(r"([A-Z])")
class Package(object):
    def __init__(s, local):
        import os.path
        s.cache = {}
        s.local = local
        s.reg = reg
        s.root = os.path.realpath(os.path.dirname(s.local["__file__"]))
    def __getattr__(s, k):
        if k in s.local: return s.local[k]
        if k in s.cache: return s.cache[k]
        path = list(s.local["_sys"].path)
        s.local["_sys"].path.insert(0, s.root)
        try:
            module = __import__(k)
            name = s.reg.sub(r"_\1", k).title()
            s.cache[k] = getattr(module, name) if hasattr(module, name) else module
        finally: s.local["_sys"].path[:] = path
        return s.cache[k]
_sys.modules[__name__] = Package(locals())
