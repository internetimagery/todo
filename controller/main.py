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
        s.scroller = TodoScroller(
            element, # parent
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


class TodoScroller(object):
    """
    Todos displayed in scroll field
    view = GUI interface
    container = todo container
    parent = place to put the scroller
    """
    def __init__(s, parent, view, settings, container):
        s.view = view
        s.settings = settings
        s.parent = parent
        s.attach = None
        s.refresh(container)

    def refresh(s, container):
        if s.attach:
            s.attach.delete()
        s.attach = s.view.ScrollField(
            parent=s.parent
        )
        s.structure = {} # Hold all info of our todos
        if container:
            for todo in container:
                grp = todo.metadata["group"]
                grp = grp if grp else ["none"]
                for g in grp:
                    s.structure[g] = s.structure.get(g, {})
                    s.structure[g][todo] = None
            for group in sorted(s.structure.keys()):
                if group != "none":
                    grp = s.view.CollapsableGroup(
                        attributes={
                            "label"     : group,
                            "position"  : ""
                        },
                        events={
                            "position"  : lambda x: x
                        },
                        parent=s.attach
                    )
                    for todo in sorted(s.structure[group].keys(), key=lambda x: x.label):
                        s.structure[group][todo] = s.addTodo(grp, todo)
            if s.structure.has_key("none"):
                for todo in sorted(s.structure["none"].keys(), key=lambda x: x.label):
                    s.structure["none"][todo] = s.addTodo(s.attach, todo)

    def addTodo(s, parent, todo):
        label = todo.label
        attributes = {
            "label"         : label,
            "annotation"    : "Click to check off and save.\nTODO: %s" % label
            }
        attributes["specialIcon"] = "openScript.png"
        attributes["specialAnn"] = "Press me to do something."
        layout = s.view.HorizontalLayout(
            parent=parent
        )
        todoView = s.view.Todo(
            attributes=attributes,
            events={
                "complete"  : s.todoComplete,
                "special"   : s.todoSpecial,
                "edit"      : s.todoEdit,
                "delete"    : s.todoDelete
            },
            parent=layout
        )
        todoEdit = s.view.TodoEdit(
            attributes={
                "text"  : todo.task
            },
            events={
                "edit"  : lambda x: x
            },
            parent=layout
        )
        return (layout, todoView, todoEdit)

    def todoComplete(s, todo):
        print "complete"
    def todoSpecial(s, todo):
        print "special"
    def todoEdit(s, todo):
        print "edit"
    def todoDelete(s, todo):
        print "delete"



Main("maya")
