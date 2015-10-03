# Todo data persistence
# Created 30/09/15 Jason Dixon
# http://internetimagery.com

import time
import shlex
import todo.parsers.group as defaultParser

class Todo(object):
    """
    A Todo
    task = the task to complete, as raw text
    CRUD = software specific data interface
    id = id following format "TODO_123456"
    parsers = functions to parse out metadata from task
    """
    def __init__(s, view, model, data, id=None, task="", parsers=[]):
        s.view = view
        s.model = model
        s.data = data
        s.parsers = [defaultParser.Group] + parsers
        s.label = ""
        s.groups = set()
        s.special = None
        s.id = id if id else "TODO_%s" % time.time()
        if task: # We're given a task. Parse it out.
            s._task = task
            s.parseTask(task)
            if not id: # No id provided. Expected to create Task
                s.data[s.id] = task
                print "Creating %s: %s." % (s.id, task)
        elif id: # No task provided, but ID provided
            s._task = s.data.get(id, "")
            print "Loaded task %s: %s." % (id, s._task)
            s.parseTask(s._task)
        else: # Neither task nor ID provided
            raise AttributeError, "No task provided."

    def parseTask(s, task):
        """
        Parse out metadata from the task
        """
        if task:
            if 255 < len(task): # 255 character limit!
                raise AttributeError, "Task is too long."
            parsers = [p(s.view, s.model, s.data) for p in s.parsers] # init parsers
            label = ""
            tokens = shlex.split(task) # break into tokens
            filteredTokens = []
            for token in tokens:
                for p in parsers:
                    token = p.update(token) if token else None
                if token:
                    filteredTokens.append(token)
            if filteredTokens:
                s.label = " ".join(filteredTokens)
                s.groups = parsers[0].tags # Get groups
                trimmed = [p for p in parsers if 0 < p.priority]
                s.special = sorted(trimmed, key=lambda x: x.priority)[-1] if trimmed else None
                return
        raise AttributeError, "Task is empty."

    def delete(s):
        """
        Delete the Todo.
        """
        del s.data[s.id]

    def task():
        doc = "A single todo Task"
        def fget(s):
            return s._task
        def fset(s, value):
            value = value.strip()
            s._task = value
            s.parseTask(value)
            s.data[s.id] = value
            print "Updated %s: %s." % (s.id, value)
        def fdel(s):
            del s.data[s.id]
            del s._task
        return locals()
    task = property(**task())
