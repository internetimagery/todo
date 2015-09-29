# CRUD Interface to override for Todo persistance
# Created 30/09/15 Jason Dixon
# http://internetimagery.com

class CRUD_Manager(object):
    """
    Override with software specific data operations
    """
    def __init__(s):
        """
        Probably retrive information here
        """
        pass
    def create(s, k, v):
        """
        Create data given a key and value
        """
        pass
    def read(s, k=None, default=None):
        """
        Read data.
        If no key is given, return all data keys.
        If a key is requested and no data exists, return default.
        """
        pass
    def update(s, k, v):
        """
        Update an existing key, value pair
        """
        pass
    def delete(s, k):
        """
        Delete an existing key
        """
        pass
