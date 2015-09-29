# Base Todo Classes
# Created Jason Dixon 29/09/15
# http:internetimagery.com

import time
import shlex
import collections


class TodoContainer(collections.MutableSequence):
    """
    A container for Todos. Sorts them and groups them.
    (optional) callback triggered on each change
    """
    def __init__(s, todos=[], callback=None):
        s.callback = callback
        s._todos = list(todos)
        s.groups = {}
    def __getitem__(s, k): return s._todos[k]
    def __len__(s): return len(s._todos)
    def __str__(s): return str(s._todos)
    def __delitem__(s, k):
        try:
            for g in s.groups:
                s.groups[g].remove(s._todos[k])
            s.callback(s.groups)
        except (TypeError, ValueError):
            pass
        del s._todos[k]
    def __setitem__(s, k, v):
        s._addTodo(v)
        s._todos[k] = v
    def insert(s, k, v):
        s._addTodo(v)
        s._todos.insert(k, v)
    def _addTodo(s, todo):
        try:
            groups = todo.metadata["Group"]
            if not groups:
                groups = ["none"]
            for g in groups:
                    s.groups[g] = s.groups.get(g, [])
                    if todo not in s.groups[g]:
                        s.groups[g].append(todo)
                        s.groups[g].sort(key=lambda x: x.label)
            s.callback(s.groups)
        except (AttributeError, TypeError):
            pass

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

class CRUD(object):
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

class Element(object):
    """
    Interface for GUI elements / compound elements
    Override all with "GUI" in the name.
    """
    def __init__(s, attributes={}, events={}, parent=None):
        if parent:
            s._parent = parent
            parent._children.append(s)
        else:
            s._parent = None
        s._children = []
        s._attr = attributes
        s._events = events
        s._root = None # Base of the element, for removal procedures
        s._attach = None # Attachment point for children where applicable
        s._GUI_Create()
    def delete(s):
        """
        Remove element
        """
        if s._parent:
            s._parent._children.remove(s)
        if s._children:
            for child in s._children:
                child._parent = None
        s._GUI_Delete(s)
    def _GUI_Create(s):
        """
        Build the gui given attributes, events and a parent
        """
        pass
    def _GUI_Read(s, k):
        """
        Get attribute value from GUI
        """
        return s._attr[k]
    def _GUI_Update(s, attr, value):
        """
        Update GUI value given an attribute
        """
        pass
    def _GUI_Delete(s):
        """
        Remove gui element
        """
        pass
    def __getattr__(s, k):
        if s._attr.has_key(k):
            return s._GUI_Read(k)
        else:
            raise AttributeError, "No attribute exists named %s." % k
    def __setattr__(s, k, v):
        s._attr[k] = v
        s._GUI_Update(k, v)
