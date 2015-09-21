# Todo functionality
from re import match
from shlex import split
from uuid import uuid4
from os.path import dirname, join, realpath
from json import load, dump
from random import choice

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
        s._parsers = []
        s._archive = []
        s.addParser(parseCategory) # Default "always on" parser
        # Path
        localPath = dirname(realpath(__file__))
        # Settings
        s._settingsName = "TODO_SETTINGS"
        s._settings = s._read(s._settingsName, {})
        # Global Settings
        s.globalSettingsFile = join(localPath, "settings.json")
        try:
            with open(s.globalSettingsFile, "r") as f:
                s._globalSettings = load(f)
        except (IOError, ValueError, KeyError):
            s._globalSettings = {}
        # Quotes
        try:
            with open(join(localPath, "quotes.json"), "r") as f:
                quotes = load(f)
        except (IOError, ValueError, KeyError):
            quotes = ["What will we do today?"]
        s.quote = choice(quotes)
        # Todos
        s._todos = set() # Store all todos
        s._todoTree = {"None": []} # Store todos in heirarchy for sorting
        for taskID in s._read():
            if match(r"Task_[\w\\-]+", taskID):
                task = s._read(taskID)
                s.todoCreate(task, ID=taskID)

    """
    Add a filter for parsing Todos
    """
    def addParser(s, parser):
        s._parsers.append(parser)

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
                s._create(newTodo.id, newTodo.task)
            s._todos.add(newTodo)
            if "Category" in newTodo.meta:
                for tag in newTodo.meta["Category"]:
                    s._todoTree[tag] = s._todoTree.get(tag, [])
                    s._todoTree[tag].append(newTodo)
            else:
                s._todoTree["None"].append(newTodo)
            return newTodo

    """
    Remove a Todo
    """
    def todoRemove(s, task):
        try:
            s._delete(task.id)
            s._todos.remove(task)
        except (KeyError, RuntimeError):
            print "Task not found for removal"
        s._todoTree = dict((cat, filter(lambda x: x != task, s._todoTree[cat])) for cat in s._todoTree)

    """
    Get a todo from its ID
    """
    def todoGetID(s, ID):
        pass
        # return s._todos[ID] if ID in s._todos else None

    """
    Get todo category tree
    """
    def todoGetTree(s):
        return dict((k, sorted(s._todoTree[k])) for k in s._todoTree)

    """
    Archive file completing a todo
    """
    def todoArchive(s, task, filename):
        if s._archive and filename:
            for arch in s._archive:
                arch(task)

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
        with open(s.globalSettingsFile, "w") as f:
            dump(s._globalSettings, f)
        return value

"""
Common parser, parsing categories
"""
def parseCategory(tokens):
    tags = set(["None"])
    filteredToken = []
    for token in tokens:
        # Check for #Hashtags
        if 1 < len(token) and token[:1] == "#":
            tags.add(token[1:])
        else:
            filteredToken.append(token)
    return filteredToken, {"Category": tags}

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
