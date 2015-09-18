# Todo
from shlex import split
from todo.parsersDefault import getAllParsers

class Todo(object):
    """
    Single Todo item
    """
    def __init__(s, task, parsers=[]):
        s.task = task.strip()
        s.parsers = parsers + getAllParsers()
        s.label, s.meta = s.parse(s.task)

    """
    Get label
    """
    def getLabel(s):
        return s.label

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
                if parsers:
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
