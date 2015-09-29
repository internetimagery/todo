# Main controller
# Created 30/09/15 Jason Dixon
# http://internetimagery.com

import re
import random

import todo.quotes

import todo.model._todo as mTodo
import todo.model.todoContainer as mTodoContainer
import todo.model.settings as mSettings

import todo.controller.panel as cPanel

class Main(object):
    def __init__(s, software):
        # Set up our interfaces
        if software == "maya":
            import todo.model.maya as model
            import todo.view.maya as gui
        else:
            raise RuntimeError, "Unknown Software: %s." % software
        title = random.choice(todo.quotes.quotes)
        s.model = model
        s.gui = gui
        s.settings = mSettings.Settings(gui)
        s.todos = mTodoContainer.TodoContainer([t for t in s.model.CRUD.read() if re.match(r"^TODO_\d+", t)])
        s.window = s.gui.Window(
            attributes={
                "title": title
            }
        )
        cPanel.Panel(
            s.window, # Parent
            s.gui, # Interface
            s.test, # Todo Page
            s.test # Settings Page
            )

    def test(s, *args):
        print args



Main("maya")
