# Main controller
# Created 30/09/15 Jason Dixon
# http://internetimagery.com

import re
import random

import todo.quotes

import todo.controller._todo as cTodo
import todo.controller.todoContainer as cTodoContainer
import todo.controller.todoScroller as cTodoScroller
import todo.controller.settings as cSettings

import todo.controller.panel as cPanel

class Main(object):
    def __init__(s, software):
        # Set up our interfaces
        if software == "maya":
            import todo.model.maya as model
            import todo.view.maya as view
        else:
            raise RuntimeError, "Unknown Software: %s." % software
        title = random.choice(todo.quotes.quotes)
        s.model = model
        s.view = view
        s.settings = cSettings.Settings(view)
        s.container = [cTodo.Todo(
            CRUD=s.model.CRUD,
            id=t,
            parsers=[]
            ) for t in s.model.CRUD.read() if re.match(r"^TODO_[\d\.]+", t)]
        s.window = s.view.Window(
            attributes={
                "title": title
            }
        )
        # Handle the Todo and Settings page changes
        cPanel.Panel(
            s.window, # Parent
            s.view, # Interface
            s.buildTodo, # Todo Page
            s.buildSettings # Settings Page
            )

    def buildTodo(s, element):
        wrapper = s.view.TextButtonVertical(
            attributes={
                "label"     : "Create a new TODO",
                "annotation": "Type a task into the box.",
            },
            events={
                "trigger"   : s.createTodo
            },
            parent=element
        )
        s.scroller = cTodoScroller.TodoScroller(
            wrapper, # parent
            s.view, # view
            s.settings, # settings
            s.container # container
        )

    def createTodo(s, element):
        try:
            s.container.append(cTodo.Todo(
                task=element.text,
                CRUD=s.model.CRUD,
                parsers=[] # TODO. Add in parsers
            ))
            element.text = ""
            print s.container
            s.scroller.refresh(s.container)
        except AttributeError as e:
            s.view.Notice(
                attributes={
                    "title"     : "Uh oh...",
                    "message"   : str(e)
                }
            )

    def buildSettings(s, element):
        s.view.Title(
            attributes={
                "title"     : "Settings are unique to each Maya scene."
            },
            parent=element
        )



Main("maya")
