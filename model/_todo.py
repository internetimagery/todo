# Todo data persistence
# Created 30/09/15 Jason Dixon
# http://internetimagery.com

import time
import shlex

class Todo(object):
    """
    A Todo
    task = the task to complete, as raw text
    CRUD = software specific data interface
    id = id following format "TODO_123456"
    parsers = functions to parse out metadata from task
    """
    def __init__(s, CRUD, id=None, task="", parsers=[]):
        s.crud = CRUD
        s.parsers = [parseGroups] + parsers
        s.id = id if id else "TODO_%s" % time.time()
        if id: # ID provided. Working with an exiting Todo
            if task: # Task also provided... ok nice. Set it up.
                s._task = task
            else: # No task provided. Cool, we can load it ourselves
                s._task = s.crud.read(id, "")
        else: # No ID provided. We must be creating a new Todo
            s._task = task
            s.crud.create(s.id, task)
        s.parseTask(s._task) # Grab our metadata

    def parseTask(s, task):
        """
        Parse out metadata from the task
        """
        s.label = ""
        s.metadata = {}
        if task and s.parsers:
            tokens = shlex.split(task) # break into tokens
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
            s.crud.update(s.id, value)
            s.parseTask(value)
        def fdel(s):
            s.crud.delete(s.id)
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
