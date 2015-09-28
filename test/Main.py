# Todo app functionality

import time
import shlex


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
        s.id = id if id else "TODO_%s" % time.time() # Unique ID for Todo
        s.label = "" # Task formatted for display
        s.task = task # Task to complete pre-parse
        s.parsers = [parseGroups] + parsers # functions to run that parse out metadata from todo
        s.metadata = {} # Metadata taken from parsers
    def parseTask(s, task):
        task = split(task)
        s.label = ""
        s.metadata = {}
        if task and s.parsers:
            tokens = shlex.split(task)
            for parse in s.parsers:
                tokens, meta = parse(tokens)
                if meta:
                    s.metadata = dict(s.metadata, **meta)
            if tokens:
                s.label = " ".join(tokens)
    def task():
        doc = "A single todo Task"
        def fget(s):
            return s._task
        def fset(s, value):
            value = value.strip()
            s._task = value
            s.parseTask(value)
        def fdel(s):
            del s._task
        return locals()
    task = property(**task())

def parseGroups(tokens):
    """
    Parse out groups from tasks. Also serves as an example parser...
    """
    tags = set()
    filteredToken = []
    for token in tokens:
        # Pull out #hashtags
        if 1 < len(token) and token[:1] == "#":
            tags.add(token[1:])
        else:
            filteredToken.append(token)
    return filteredToken, {"Group": tags}
