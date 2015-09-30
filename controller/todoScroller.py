# Todos layed out in a scroll field
# Created 30/09/15 Jason Dixon
# http://internetimagery.com

from todo.images import icon

class TodoScroller(object):
    """
    Todos displayed in scroll field
    parent = layout to place scroller
    view = GUI interface
    settings = settings interface
    completeCallback = run with the Todo when the todo is checked off
    """
    def __init__(s, parent, view, settings, completeCallback):
        s.parent = parent
        s.view = view
        s.settings = settings
        s.completeCallback = completeCallback
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
                grp = todo.metadata["group"]
                grp = grp if grp else ["none"]
                for g in grp:
                    new[g] = new.get(g, {})
                    new[g][todo] = None
            # add, remove = s.diffStructure(new, s.todoStructure)
            # TODO: Add logic to deal with differences

            # Too many differences. Build em!
            s.todoStructure = new
            s.container = container
            pos = s.settings.get("Todo.SectionState", {})
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
            s.settings.set("Todo.SectionState", s.groupPos)
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
        todoView = s.view.Todo(
            attributes={
                "label"         : label,
                "annotation"    : "Click to check off and save.\nTODO: %s" % label,
                "icon"          : icon.get("save_16"), #"fileSave.png",
                "editIcon"      : icon.get("todo_16"), #"setEdEditMode.png",
                "editAnnotaion" : "Edit Task.",
                "delIcon"       : icon.get("brush_16"), #"removeRenderable.png",
                "delAnnotation" : "Delete Todo without saving."
                },
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
                todo.task = task
                s.refresh(s.container)
            except AttributeError as e:
                s.view.Notice(
                    attributes={
                        "title"     : "Uh oh...",
                        "message"   : str(e)
                    }
                )

    def todoComplete(s, todo, todoView, todoEdit, layout):
        print "Task Complete %s: %s." % (todo.id, todo.task)
        if s.completeCallback(todo):
            s.todoDelete(todo, todoView, todoEdit, layout)

    def todoSpecial(s, todo, todoView, todoEdit, layout):
        print "Special Function not defined yet!"

    def todoDelete(s, todo, todoView, todoEdit, layout):
        print "Removing %s: %s." % (todo.id, todo.task)
        s.container.remove(todo)
        layout.delete()
        todo.delete()
