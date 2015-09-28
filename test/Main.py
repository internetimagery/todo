# Todo app functionality

from time import time

class Main(object):
    """
    Run the Todo App
    """
    def __init__(s):
        pass


class Todo(object):
    """
    A Todo
    """
    def __init__(s, id=None, task="", parsers=[]):
        s.id = id if id else "TODO_%s" % time() # Unique ID for Todo
        s.realTask = task if task else "No task given." # Task to complete pre-parse
        s.parsers = parsers # functions to run that parse out metadata from todo
        s.metadata = {} # Metadata taken from parsers
        pass
