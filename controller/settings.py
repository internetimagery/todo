# Settings storage
# Created Jason Dixon 29/09/15
# http:internetimagery.com

class Settings(object):
    """
    Settings interface
    """
    def __init__(s, CRUD):
        s.crud = CRUD
        s.name = "TODO_SETTINGS"
        s.data = s.crud.read(s.name, {})
    def get(s, k, default): return s.data[k] if s.data.has_key(k) else default
    def set(s, k, v):
        s.data[k] = v
        try:
            s.crud.update(s.name, s.data)
        except:
            s.crud.create(s.name, s.data)
