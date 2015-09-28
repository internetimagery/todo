# Control the app

import re

from todo.base import Settings, TodoContainer, Todo

# "^TODO_\d+"


class Main(object):
    def __init__(s, software):
        # Set up our interfaces
        s.settings = Settings()
        if software == "maya":
            # Set up Crud
            from todo.maya.crud import CRUD
            s.crud = CRUD()
        else:
            raise RuntimeError, "Unknown Software: %s." % software
        # Initialize our todos
        s.todos = TodoContainer([t for t in s.crud.read() if re.match(r"^TODO_\d+", t)])


Main("maya")
