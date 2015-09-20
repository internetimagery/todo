# Controller for Maya
import maya.cmds as cmds
import maya.utils as utils
from re import compile
import todo.viewMaya as view
import todo.controller as ctrl
import todo.crudMaya as crud


# fileInfo "TODO_SETTINGS" "{\"FileArchive.active\": true, \"Todo.SectionState\": {\"animation\": false}, \"FileArchive.path\": \"/home/maczone/Desktop/backup\"}";
# fileInfo "TODO_144249523723" "#animation right dash 1 to 10";

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
                utils.executeDeferred(s.refreshTodo())
            return view.TodoSection(
                cat,
                todoContainerGrouped,
                open=s.todoSectionStates[cat],
                openCallback=openSection,
                closeCallback=closeSection
                )
        def addTodo(section, task):
            def done(todoElement):
                print "Ticked off", task.label
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
    Update window position
    """
    def moveUpdate(s, location):
        s.globalSettingsSet("location", location)

    """
    No real functionality
    """
    def closeUpdate(s):
        print "closed window"


"""
Todo with Maya specific parsers
"""
from os.path import dirname, realpath, join, isfile, basename

def Todo(task):
    temp = {}
    """
    File parser
    """
    temp["file"] = temp.get("file", set())
    def parseFilePath(token):
        fileName = cmds.file(q=True, sn=True)
        if "/" in token:
            root = dirname(fileName) if fileName else ""
            path = realpath(join(root, token))
            if isfile(path):
                temp["file"].add(path)
                return basename(token), ("File", temp["file"])
        return token, None

    """
    Object Lookup
    """
    temp["obj"] = temp.get("obj", set())
    def parseObject(token):
        obj = cmds.ls(token, r=True)
        if obj:
            temp["obj"] |= set(obj)
            return "", ("Object", temp["obj"])
        return token, None
    return td.Todo(task, [
        parseFilePath,
        parseObject
        ])

Start()
