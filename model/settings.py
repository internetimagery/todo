# Settings storage
# Created Jason Dixon 29/09/15
# http:internetimagery.com

class Settings(object):
    """
    Interface to get and set settings.
    """
    def __init__(s, CRUD):
        s.crud = CRUD
        s._settings = {}
    def _prefix(s, k): return "setting_%s" % k
    def get(s, k, default): return s.crud.read(s._prefix(k), default)
    def set(s, k, v):
        k = s._prefix(k)
        try:
            s.crud.update(k, v)
        except:
            s.crud.create(k, v)
