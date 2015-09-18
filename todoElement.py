# Todo
from shlex import split
from uuid import uuid4
import todo.parsersDefault as default

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
