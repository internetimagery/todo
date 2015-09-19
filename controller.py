# Todo functionality
from re import match
from shlex import split
from uuid import uuid4
from os.path import dirname, join, realpath
from json import load, dump

# Provide functions for:
# create(key, value) returns value
# read(key, defaultValue) returns value if present or defaultValue
# read() returns [all, keys, ...]
# update(key, value) returns value
# delete(key) returns None
class Controller(object):
    """
    Todo storage etc
    """
    def __init__(s, create, read, update, delete):
        # Set up our CRUD
        s._create = create
        s._read = read
        s._update = update
        s._delete = delete
        # Parsers and Archives
        s._parsers = set()
        s._archive = set()
        s.addParser(parseCategory) # Default "always on" parser
        # Settings
        s._settingsName = "TODO_SETTINGS"
        s._settings = s._read(s._settingsName, {})
        # Global Settings
        s._globalSettingsName = join(dirname(realpath(__file__)), "settings.json")
        try:
            with open(s._globalSettingsName, "r") as f:
                s._globalSettingsName = load(f)
        except (IOError, ValueError, KeyError):
            s._globalSettings = {}
        # Todos
        s._todos = {} # Store all todos
        s._todoTree = {"None": set()} # Store todos in heirarchy for sorting
        for taskID in s._read():
            if match(r"Task_[\w\\-]+", taskID):
                task = s._read(taskID)
                s.todoCreate(task, ID=taskID)

    """
    Add a filter for parsing Todos
    """
    def addParser(s, parser):
        s._parsers.add(parser)

    """
    Add an archive for storing data after task complete
    """
    def addArchive(s, archive):
        s._archive.add(archive)

    """
    Validate a todos text (placeholder)
    """
    def todoValidate(s, task):
        ok = True # TODO add validation rules or override in subclass
        return task if ok else False

    """
    Create a Todo
    """
    def todoCreate(s, task, ID=None):
        if s.todoValidate(task):
            newTodo = Todo(task, s._parsers, ID=ID)
            if not ID:
                s._create(newTodo.id, newTodo.label)
            s._todos[newTodo.id] = newTodo
            if "Category" in newTodo.meta:
                for tag in newTodo.meta["Category"]:
                    s._todoTree[tag] = s._todoTree.get(tag, set())
                    s._todoTree[tag].add(newTodo.id)
            else:
                s._todoTree["None"].add(newTodo.id)
            return newTodo
    """
    Remove a Todo
    """
    def todoRemove(s, ID):
        if ID in s._todos:
            del s._todos[ID]
            s._delete(ID)
            for cat in s._todoTree:
                if ID in s._todoTree[cat]:
                    del s._todoTree[cat][ID]
    """
    Get a todo from its ID
    """
    def todoGetID(s, ID):
        return s._todos[ID] if ID in s._todos else None
    """
    Get todo category tree
    """
    def todoGetTree(s):
        return s._todoTree
    """
    Archive file completing a todo
    """
    def todoArchive(s, ID):
        if s._archive and ID in s._todos:
            for arch in s._archive:
                arch(s.todoGet(ID))
    """
    Get settings
    """
    def settingsGet(s, key=None, default=None):
        if key:
            return s._settings[key] if key in s._settings else default
        else:
            return s._settings
    """
    Set settings parameter
    """
    def settingsSet(s, key, value):
        s._settings[key] = value
        s._update(s._settingsName, s._settings)
        return value
    """
    Get global settings
    """
    def globalSettingsGet(s, key=None, default=None):
        if key:
            return s._globalSettings[key] if key in s._globalSettings else default
        else:
            return s._globalSettings
    """
    Set global settings
    """
    def globalSettingsSet(s, key, value):
        s._globalSettings[key] = value
        with open(s._globalSettingsName, "w") as f:
            dump(s._globalSettings, f)
        return value

"""
Common parser, parsing categories
"""
def parseCategory(tokens):
    tags = set()
    filteredToken = []
    for token in tokens:
        # Check for #Hashtags
        if 1 < len(token) and token[:1] = "#":
            tags.add(token[1:])
        else:
            filteredToken.append(token)
    return token, {"Category": tags} if tags else None


# parser:
# parser(token):
# return filteredToken, {"Category": arugments}
class Todo(object):
    """
    Single Todo item
    """
    def __init__(s, task, parsers, ID=None):
        s.parsers = parsers
        s.id = ID if ID else "Task_%s" % uuid4()
        s.parse(task)

    """
    Parse out specific information from todo task
    """
    def parse(s, task):
        task = task.strip()
        s.label = ""
        s.meta = {}
        if task and s.parsers:
            s.task = task
            tokens = split(task)
            for parse in s.parsers:
                tokens, meta = parse(tokens)
                if meta:
                    s.meta = dict(s.meta, **meta) # Join metadata
            if tokens:
                s.label = " ".join(tokens)
