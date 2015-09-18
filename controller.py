# Todo functionality

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
        s.todos = {}
        for todoID in s.read():
            

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
