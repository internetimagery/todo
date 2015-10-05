# Gathering all the GUI elements into one place!
# Created 30/09/15 Jason Dixon
# http://internetimagery.com

import re
import sys
import os.path
root = os.path.realpath(os.path.dirname(__file__))
reg = re.compile(r"([A-Z])")

class Package(object):
    def __init__(s, local):
        s.cache = {}
        s.sys = sys
        s.root = root
        s.reg = reg
        s.local = local
    def __getattr__(s, k):
        if k in s.local: return s.local[k]
        if k in s.cache: return s.cache[k]
        path = list(s.sys.path)
        s.sys.path.insert(0, s.root)
        try:
            module = __import__(k)
            s.cache[k] = getattr(module, s.reg.sub(r"_\1", k).title())
        finally:
            s.sys.path[:] = path
        return s.cache[k]
sys.modules[__name__] = Package(locals())
