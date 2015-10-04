# Data persistence in the scene. Override "_DATA_" methods
# Created 03/10/15 Jason Dixon
# http://internetimagery.com

import collections

class Data(collections.MutableMapping):
    def __init__(s, *args):
        s.data = s._DATA_Retrieve(*args)
    def set(s, k, v): return s.__setitem__(k, v)
    def __setitem__(s, k, v):
        s.data[k] = v
        s._DATA_Store(s.data)
    def __getitem__(s, k): return s.data[k]
    def __len__(s): return len(s.data)
    def __iter__(s): return iter(s.data)
    def __str__(s): return str(s.data)
    def has_key(s, k): return s.data.has_key(k)
    def __delitem__(s, k):
        del s.data[k]
        s._DATA_Store(s.data)
    def _DATA_Retrieve(s, *args):
        """
        Set inital settings.
        Take all data from store. Return as dict.
        """
        return {}
    def _DATA_Store(s, data):
        """
        Store all data.
        """
        pass
