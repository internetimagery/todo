# Todos layed out in a scroll field
# Created 30/09/15 Jason Dixon
# http://internetimagery.com

import _todo as cTodo

class TodoScroller(object):
    """
    Todos displayed in scroll field
    parent = layout to place scroller
    view = GUI interface
    settings = settings interface
    completeCallback = run with the Todo when the todo is checked off
    """
    def __init__(s, parent, view, model, data, parsers, checkCallback):
        s.parent = parent
        s.view = view
        s.model = model
        s.data = data
        s.parsers = parsers
        s.checkCallback = checkCallback
        s.attach = None
        s.todoStructure = {}
        s.container = []

    def refresh(s, container):
        if s.attach:
            s.attach.delete()
        s.attach = s.view.ScrollField(
            parent=s.parent
        )

        new = {} # New structure
        s.groupPos = {} # Track group open close state
        if container:
            for todo in container:
                grp = todo.groups
                grp = grp if grp else ["none"]
                for g in grp:
                    new[g] = new.get(g, {})
                    new[g][todo] = None
            # add, remove = s.diffStructure(new, s.todoStructure)
            # TODO: Add logic to deal with differences

            # Too many differences. Build em!
            s.todoStructure = new
            s.container = container
            pos = s.data.get("Todo.SectionState", {})
            for group in sorted(s.todoStructure.keys()):
                if group != "none":
                    s.groupPos[group] = pos.get(group, True)
                    grp = s.addGroup(group, s.attach)
                    for todo in sorted(s.todoStructure[group].keys(), key=lambda x: x.label):
                        s.todoStructure[group][todo] = s.addTodo(grp, todo)
            if s.todoStructure.has_key("none"):
                for todo in sorted(s.todoStructure["none"].keys(), key=lambda x: x.label):
                    s.todoStructure["none"][todo] = s.addTodo(s.attach, todo)

    def diffStructure(s, new, old):
        """
        Compare group differences between two structures to determine GUI updates.
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

    def addGroup(s, name, parent):
        def changePos(element):
            s.groupPos[name] = element.position
            s.data["Todo.SectionState"] = s.groupPos
        pos = s.groupPos.get(name, True)
        grp = s.view.CollapsableGroup(
            attributes={
                "label"     : name,
                "position"  : pos
            },
            events={
                "position"  : changePos
            },
            parent=parent
        )
        return grp

    def addTodo(s, parent, todo):
        """
        Add a Todo Element to the Scroller
        """
        layout = s.view.HorizontalLayout(
            parent=parent
        )
        label = todo.label
        todoAttributes={
            "label"         : label,
            "annotation"    : "Click to check off and save.\nTODO: %s" % label,
            "icon"          : s.model.Icon["todo.save"],
            "editIcon"      : s.model.Icon["todo.edit"],
            "editAnnotaion" : "Edit Task.",
            "delIcon"       : s.model.Icon["todo.delete"],
            "delAnnotation" : "Delete Todo without saving."
            }
        if todo.special:
            todoAttributes["specialIcon"] = s.model.Icon[todo.special.icon]
            todoAttributes["specialAnn"] = todo.special.description
        todoView = s.view.Todo(
            attributes=todoAttributes,
            events={
                "complete"  : lambda x: s.todoComplete(todo, todoView, todoEdit, layout),
                "special"   : lambda x: s.todoSpecial(todo, todoView, todoEdit, layout),
                "edit"      : lambda x: s.todoModeSwitch(todo, todoView, todoEdit, layout),
                "delete"    : lambda x: s.todoDelete(todo, todoView, todoEdit, layout),
            },
            parent=layout
        )
        todoEdit = s.view.TodoEdit(
            attributes={
                "text"  : todo.task,
                "label" : "Update"
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
                old = set(todo.groups)
                todo.task = task
                new = set(todo.groups)
                if old == new: # Groups haven't changed. Update in place
                    todoEdit.visible = False
                    todoView.visible = True
                    todoView.label = todo.label
                    if todo.special:
                        todoView.specialIcon = s.model.Icon[todo.special.icon]
                        todoView.specialAnn = todo.special.description
                else:
                    s.refresh(s.container)
            except AttributeError as e:
                s.view.Notice(
                    attributes={
                        "title"     : "Uh oh...",
                        "message"   : str(e)
                    }
                )

    def todoCreate(s, task):
        todo = cTodo.Todo(
            data=s.data,
            task=task,
            parsers=s.parsers
        )
        s.container.append(todo)
        s.refresh(s.container)

    def todoComplete(s, todo, todoView, todoEdit, layout):
        cacheTask = todo.task
        s.todoDelete(todo, todoView, todoEdit, layout)
        if s.checkCallback(todo):
            print "Task Complete %s: %s." % (todo.id, todo.task)
        else: # Save failed. Reinstate Todo
            s.todoCreate(cacheTask)

    def todoSpecial(s, todo, todoView, todoEdit, layout):
        if todo.special:
            todo.special.run()

    def todoDelete(s, todo, todoView, todoEdit, layout):
        print "Removing %s: %s." % (todo.id, todo.task)
        s.container.remove(todo)
        layout.delete()
        todo.delete()
