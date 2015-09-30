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
        s.container = []
        keys = s.model.CRUD.read() # Initialize our Todos
        if keys:
            for key in keys:
                if re.match(r"^TODO_[\d\.]+", key):
                    try:
                        s.container.append(cTodo.Todo(
                            CRUD=s.model.CRUD,
                            id=key,
                            parsers=[]
                            )
                        )
                    except AttributeError as e:
                        print "Error loading %s: %s" % (key, e)

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
        s.todoStructure = {}
        s.refresh(container)

    def refresh(s, container):
        if s.attach:
            s.attach.delete()
        s.attach = s.view.ScrollField(
            parent=s.parent
        )

        new = {} # New structure
        if container:
            for todo in container:
                grp = todo.metadata["group"]
                grp = grp if grp else ["none"]
                for g in grp:
                    new[g] = new.get(g, {})
                    new[g][todo] = None
        add, remove = s.diffStructure(new, s.todoStructure)

        if container:
            # Compare differences to see if we need to update
            oldContainer = set(s.container)
            newContainer = set(container)
            addedTodo = oldContainer.difference(newContainer)
            removedTodo = newContainer.difference(oldContainer)
            # Compare differences to groups





        s.todoStructure = {} # Hold all info of our todos
        if container:
            for todo in container:
                grp = todo.metadata["group"]
                grp = grp if grp else ["none"]
                for g in grp:
                    s.todoStructure[g] = s.todoStructure.get(g, {})
                    s.todoStructure[g][todo] = None
            for group in sorted(s.todoStructure.keys()):
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
                    for todo in sorted(s.todoStructure[group].keys(), key=lambda x: x.label):
                        s.todoStructure[group][todo] = s.addTodo(grp, todo)
            if s.todoStructure.has_key("none"):
                for todo in sorted(s.todoStructure["none"].keys(), key=lambda x: x.label):
                    s.todoStructure["none"][todo] = s.addTodo(s.attach, todo)

    def diffStructure(s, new, old):
        """
        Compare differences between two structures to determine GUI updates.
        """
        add = {}
        remove = {}
        # Get difference between groups
        newGrp = set(new.keys())
        oldGrp = set(old.keys())
        addGrp = newGrp.difference(oldGrp)
        delGrp = oldGrp.difference(newGrp)
        for grp in newGrp.union(oldGrp):
            if grp in addGrp: # New group
                add[grp] = set(new[grp].keys())
            elif grp in delGrp: # Whole group removed
                remove[grp] = set(old[grp].keys())
            else: # Test intergroup for changes
                chk1 = set(new[grp].keys())
                chk2 = set(old[grp].keys())
                addChk = chk1.difference(chk2)
                delChk = chk2.difference(chk1)
                if addChk:
                    add[grp] = addChk
                if delChk:
                    remove[grp] = delChk
        return add, remove


    def addTodo(s, parent, todo):
        """
        Add a Todo Element to the Scroller
        """
        layout = s.view.HorizontalLayout(
            parent=parent
        )
        label = todo.label
        todoView = s.view.Todo(
            attributes={
                "label"      : label,
                "annotation" : "Click to check off and save.\nTODO: %s" % label
                },
            events={
                "complete"  : s.todoComplete,
                "special"   : s.todoSpecial,
                "edit"      : lambda x: s.todoModeSwitch(todo, todoView, todoEdit, layout),
                "delete"    : s.todoDelete
            },
            parent=layout
        )
        todoEdit = s.view.TodoEdit(
            attributes={
                "text"  : todo.task
            },
            events={
                "edit"  : lambda x: s.todoModeSwitch(todo, todoView, todoEdit, layout)
            },
            parent=layout,
            visible=False
        )
        return (layout, todoView, todoEdit)

    def todoModeSwitch(s, todo, todoView, todoEdit, layout):
        view = todoView.visible
        edit = todoEdit.visible
        if view: # Switching off the viewer
            task = todo.task
            todoView.visible = False
            todoEdit.visible = True
            todoEdit.text = task
        else: # Switching from edit mode back to viewer
            task = todoEdit.text
            try:
                groupsOld = todo.metadata["group"].copy() # Store groups
                todo.task = task
                todoEdit.visible = False
                todoView.visible = True
                todoView.label = todo.label
                groupsNew = todo.metadata["group"]
                # Check for changes to do minimum ammount of refreshing
                removed = groupsOld.difference(groupsNew)
                added = groupsNew.difference(groupsOld)
                if added: # Some new groups were added. Need to refresh.
                    print "Damn need to refresh..."
                elif removed:
                    for remove in removed: # Remove Todos directly
                        if len(s.todoStructure[remove]) < 2: # Removing this todo will empty the group
                            print "group:", s.todoStructure[remove][todo][0].parent
                        else: # Remove just the Todo
                            pass

            except AttributeError as e:
                s.view.Notice(
                    attributes={
                        "title"     : "Uh oh...",
                        "message"   : str(e)
                    }
                )



    def todoComplete(s, todo):
        print "complete"
    def todoSpecial(s, todo):
        print "special"
    def todoEdit(s, todo):
        print "edit"
    def todoDelete(s, todo):
        print "delete"



Main("maya")
