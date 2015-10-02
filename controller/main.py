# Main controller
# Created 30/09/15 Jason Dixon
# http://internetimagery.com

import re
import random
import threading

import todo.quotes

import todo.archivers

import todo.controller.todoContainer as cTodoContainer
import todo.controller.todoScroller as cTodoScroller
import todo.controller.settings as cSettings
import todo.controller.panel as cPanel
import todo.controller._todo as cTodo


class Main(object):
    def __init__(s, software):
        # Set up our interfaces
        if software == "maya":
            import todo.model.maya as model
            import todo.view.maya as view
            from todo.parsers.maya import parsers
        else:
            raise RuntimeError, "Unknown Software: %s." % software
        title = random.choice(todo.quotes.quotes)
        s.model = model
        s.view = view
        s.parsers = parsers
        s.settings = cSettings.Settings(s.model.CRUD)
        # Set up our archivers
        s.archives = [a(
            s.view, # view
            s.model, # model
            s.settings # settings
        ) for a in todo.archivers.Archives]
        s.daemonArchive = True # Daemonize archives

        s.window = s.view.Window(
            attributes={
                "name"  : "TODO_WINDOW",
                "title" : title
            }
        )
        # Handle the Todo and Settings page changes
        cPanel.Panel(
            s.window, # Parent
            s.view, # view Interface
            s.model, # model interface
            s.buildTodo, # Todo Page
            s.buildSettings # Settings Page
            )

    def buildTodo(s, element):
        s.view.TextButtonVertical(
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
            element, # parent
            s.view, # view
            s.model, # model
            s.settings, # settings
            s.parsers, # parsers
            s.completeTodo # Todo complete callback
        )
        container = []
        keys = s.model.CRUD.read() # Initialize our Todos
        if keys:
            for key in keys:
                if re.match(r"^TODO_[\d\.]+", key):
                    try:
                        container.append(cTodo.Todo(
                            view=s.view,
                            model=s.model,
                            id=key,
                            parsers=s.parsers
                            )
                        )
                    except AttributeError as e:
                        print "Error loading %s: %s" % (key, e)
        s.scroller.refresh(container)

    def createTodo(s, element):
        """
        Run when creating a new todo
        """
        try:
            s.scroller.todoCreate(element.text)
            element.text = ""
        except AttributeError as e:
            s.view.Notice(
                attributes={
                    "title"     : "Uh oh...",
                    "message"   : str(e)
                }
            )

    def completeTodo(s, todo):
        """
        Todo complete.
        """

        return s.model.File.save(
            todo=todo,
            archive=lambda x: s.archiveTodo(todo, x)
            )

    def archiveTodo(s, todo, path):
        """
        Fire off the file archive routines!
        """
        threads = []
        for a in s.archives:
            if s.daemonArchive:
                print "threadding"
                th = threading.Thread(
                    target=a.runArchive,
                    args=(todo, path)
                    )
                th.daemon = True
                th.start()
                threads.append(th)
            else:
                a.runArchive(todo, path)

    def buildSettings(s, element):
        s.view.Title(
            attributes={
                "title"     : "Settings are unique to each Maya scene."
            },
            parent=element
        )
        for archive in s.archives:
            archive.buildSettings(element)
Main("maya")
