# Todo functionality
from re import match
from shlex import split
from uuid import uuid4
import todo.parsersDefault as default

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
        s.create = create
        s.read = read
        s.update = update
        s.delete = delete
        # Parsers and Archives
        s.parsers = set()
        s.archive = set()

        s.settings = s.read("TODO_SETTINGS", {})
        s.todos = {} # Store all todos
        s.todoTree = {"None": []} # Store todos in heirarchy for sorting
        for taskID in s.read():
            if match(r"Task_[\w\\-]+", taskID):
                task = s.read(taskID)
                newTodo = s.todoCreate(task, ID=taskID)
                meta = newTodo.getMeta()
                if "Hashtag" in meta:
                    for tag in meta["Hashtag"]:
                        s.todoTree[tag] = taskID
                else:
                    s.todoTree["None"].append(taskID)
                s.todos[taskID] = newTodo
        s.todoGetAll()

    """
    Add a filter for parsing Todos
    """
    def addFilter(s, parser):
        s.parsers.add(parser)

    """
    Add an archive for storing data after task complete
    """
    def addArchive(s, archive):
        s.archive.add(archive)

    """
    Create a Todo
    """
    def todoCreate(s, task, ID=None):
        newTodo = Todo(task, s.parsers)
        if ID:
            newTodo.id = ID
        return newTodo

    """
    Get todo categories
    """
    def getCategories(s):
        return s.todoTree.keys()

    """
    Get a certain Todo
    """
    def getTodo(s, ID):
        return s.todos[ID]


# parser:
# parser(token):
# return token, ("Category", arugments)
class Todo(object):
    """
    Single Todo item
    """
    def __init__(s, task, parsers):
        s.task = task.strip()
        s.parsers = parsers + default.getAllParsers()
        s.label, s.meta = s.parse(s.task)
        s.id = "Task_%s" % uuid4()

    """
    Get Metadata
    """
    def getMeta(s):
        return s.meta

    """
    Parse out specific information from todo task
    """
    def parse(s, task):
        if task:
            tokens = split(task)
            filtered = []
            metadata = {}
            for token in tokens:
                if s.parsers:
                    for parser in s.parsers:
                        if token:
                            token, meta = parser(token)
                            if meta:
                                tokenName, tokenArgs = meta
                                metadata[tokenName] = tokenArgs
                    if token:
                        filtered.append(token)
            return " ".join(filtered), metadata
        return "", {}
