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
        s.metadata = {}
        s.label = ""
        s.id = id if id else "TODO_%s" % time.time()
        if task: # We're given a task. Parse it out.
            s._task = task
            s.parseTask(task)
            if not id: # No id provided. Expected to create Task
                s.crud.create(s.id, task)
                print "Creating %s: %s." % (s.id, task)
        elif id: # No task provided, but ID provided
            s._task = s.crud.read(id, "")
            print "Loaded task %s: %s." % (id, s._task)
            s.parseTask(s._task)
        else: # Neither task nor ID provided
            raise AttributeError, "No task provided."

    def parseTask(s, task):
        """
        Parse out metadata from the task
        """
        if task:
            metadata = {}
            label = ""
            tokens = shlex.split(task) # break into tokens
            for parse in s.parsers:
                tokens, meta = parse(tokens)
                if meta:
                    metadata = dict(metadata, **meta)
            if tokens:
                label = " ".join(tokens)
            if label:
                s.label = label
                s.metadata = metadata
                return
        raise AttributeError, "Task is empty"

    def delete(s):
        """
        Delete the Todo.
        """
        s.crud.delete(s.id)

    def task():
        doc = "A single todo Task"
        def fget(s):
            return s._task
        def fset(s, value):
            value = value.strip()
            s._task = value
            s.crud.update(s.id, value)
            s.parseTask(value)
            print "Updated %s: %s." % (s.id, value)
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
    return filteredToken, {"group": tags}
