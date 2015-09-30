# Todo containment
# Created 30/09/15 Jason Dixon
# http://internetimagery.com

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
