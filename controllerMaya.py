# Controller for Maya
import maya.cmds as cmds
import maya.utils as utils
from re import compile
import todo.viewMaya as view
import todo.controller as ctrl
import todo.crudMaya as crud
import todo.parsersMaya as parsers

# Begin Application
class Start(ctrl.Controller):
    """
    Application
    """
    def __init__(s, location=None):
        store = crud.CRUD()
        ctrl.Controller.__init__(
            s,
            store.create,
            store.read,
            store.update,
            store.delete
        )

        # Load settings
        s.todoSectionStates = s.settingsGet("groups", {})
        # Load Parsers
        for parser in parsers.export():
            s.addParser(parser)

        s.window = view.MainWindow(
            "Todo_Window",
            "",
            title                 = s.quote,
            location              = s.globalSettingsGet("location", "float"),
            moveCallback          = s.moveUpdate,
            closeCallback         = s.closeUpdate,
            buildTodoCallback     = s.buildTodoContainer,
            buildSettingsCallback = s.buildSettingsContainer,
            newTodoCallback       = s.newTodo
            )

    """
    Build out todo page
    """
    def buildTodoContainer(s, parent):
        # set up our container
        s.wrapper = parent
        # Insert Todos
        s.refreshTodo()

    """
    Refresh the todo list
    """
    def refreshTodo(s):
        # Build our Todo section
        clear = cmds.columnLayout(s.wrapper, q=True, ca=True)
        if clear:
            cmds.deleteUI(clear)
        todoContainer = cmds.scrollLayout(bgc=[0.2, 0.2, 0.2], cr=True, p=s.wrapper)
        todoContainerGrouped = cmds.columnLayout(adj=True, p=todoContainer)
        todoContainerUngrouped = cmds.columnLayout(adj=True, p=todoContainer)

        def addSection(cat):
            s.todoSectionStates[cat] = s.todoSectionStates.get(cat, True)
            def openSection():
                s.todoSectionStates[cat] = True
                s.settingsSet("groups", s.todoSectionStates)
                utils.executeDeferred(s.refreshTodo())
            def closeSection():
                s.todoSectionStates[cat] = False
                s.settingsSet("groups", s.todoSectionStates)
            return view.TodoSection(
                cat,
                todoContainerGrouped,
                open=s.todoSectionStates[cat],
                openCallback=openSection,
                closeCallback=closeSection
                )
        def addTodo(section, task):
            def done(todoElement):
                s.todoComplete(task)
                delete(todoElement)
            def delete(todoElement):
                s.todoRemove(task)
                todoElement.removeUI()
            def edit(todoElement, text):
                text = text.strip()
                if text:
                    task.parse(text)
                    todoElement.label = task.label
                    todoElement.buildElement()
            print task.meta
            return view.Todo(
                task.label,
                section,
                ID="STUFF",
                realLabel=task.task,
                doneCallback=done,
                editCallback=edit,
                deleteCallback=delete,
                special={}
                #     "description" : "what it does",
                #     "icon" : "fileOpen.png",
                #     "callback" : test
                # }
                )

        tree = s.todoGetTree()
        for cat in sorted(tree.keys()):
            if cat == "None":
                for task in tree[cat]:
                    addTodo(todoContainerUngrouped, task)
            else:
                section = addSection(cat)
                for task in tree[cat]:
                    addTodo(section.attach(), task)

    """
    Build out settings page
    """
    def buildSettingsContainer(s, parent):
        cmds.text(l="Todo: Insert settings stuff in here!\nLove, controller. :)", p=parent)

    """
    New todo requested
    """
    def newTodo(s, text):
        text = text.strip()
        if text:
            newTodo = s.todoCreate(text)
            if newTodo:
                s.window.editTodo("")
                s.refreshTodo()
        else:
            cmds.confirmDialog(title="Whoops...", message="You need to add some text for your Todo.")

    """
    Check off a todo and run archives
    """
    def todoComplete(s, task):
        print "Complete:", task.label
        s.todoArchive(task)

    """
    Update window position
    """
    def moveUpdate(s, location):
        s.globalSettingsSet("location", location)

    """
    No real functionality
    """
    def closeUpdate(s):
        print "closed window"

Start()
