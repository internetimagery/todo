# Controller for Maya
import maya.cmds as cmds
from re import compile
import todo.viewMaya as view
import todo.todoElement as td
import todo.controller as ctrl
import todo.crudMaya as crud


# fileInfo "TODO_SETTINGS" "{\"FileArchive.active\": true, \"Todo.SectionState\": {\"animation\": false}, \"FileArchive.path\": \"/home/maczone/Desktop/backup\"}";
# fileInfo "TODO_144249523723" "#animation right dash 1 to 10";

class Controller(ctrl.Controller):
    """
    Controller for Maya
    """
    def __init__(s):
        store = crud.CRUD()
        ctrl.Controller.__init__(
            s,
            store.create,
            store.read,
            store.update,
            store.delete
        )
        print s.todoTree

Controller()
# Begin Application
class Start(object):
    """
    Application
    """
    def __init__(s, location=None):
        s.controller = Controller()
        s.settings = s.store.get("TODO_SETTINGS", {}) # Saved settings

        # Get our Todos
        reg = compile(r"Task_[\w\\-]+")
        s.todos = {} # Todos
        for task in s.store.cache:
            if reg.match(task):
                newTodo = Todo(s.store.get(task, ""))
                newTodo.id = task
                s.todos[task] = newTodo

        s.window = view.MainWindow(
            "Todo_Window",
            "",
            title                 = "grab from file",
            location              = s.settings["location"] if "location" in s.settings else "float",
            moveCallback          = s.moveUpdate,
            closeCallback         = s.closeUpdate,
            buildTodoCallback     = s.buildTodo,
            buildSettingsCallback = s.buildSettings,
            newTodoCallback       = s.newTodo
            )

        def test(*args):
            print args
        parent = s.window.buildTodo()
        view.Todo(
            "one",
            parent,
            realLabel="thing",
            doneCallback=test,
            editCallback=test,
            deleteCallback=test,
            special={
                "description" : "what it does",
                "icon" : "flowers.png",
                "callback" : test
            })


        # options:
        # realLabel = label that includes hashtags etc etc
        # doneCallback = ticked off todo
        # editCallback = changed todo name
        # deleteCallback = deleted todo
        # special = button
        #   description = describe button
        #   icon = button icon
        #   callback = run when pressed

    """
    Build out todo page
    """
    def buildTodo(s, parent):
        s.todoContainer = cmds.scrollLayout(bgc=[0.2, 0.2, 0.2], cr=True, p=parent)
        cmds.text(l="Added in controller")
        cmds.text(l="Also added in controller")
        cmds.text(l="Comes from in controller")
        s.todoContainerSections = cmds.columnLayout(adj=True, p=s.todoContainer)
        s.todoContainerUnsectioned = cmds.columnLayout(adj=True, p=s.todoContainer)

    """
    Build out settings page
    """
    def buildSettings(s, parent):
        cmds.text(l="Todo: Insert settings stuff in here!", p=parent)

    """
    New todo requested
    """
    def newTodo(s, text):
        text = text.strip()
        if text:
            s.window.editTodo("")
            newTodo = Todo(text)
            s.todos[newTodo.id] = newTodo
            s.store.set(newTodo.id, text)
        else:
            cmds.confirmDialog(title="Whoops...", message="You need to add some text for your Todo.")

    """
    Update window position
    """
    def moveUpdate(s, location):
        print "moved", location
        s.settings["location"] = location
        s.store.set("TODO_SETTINGS", s.settings)

    """
    No real functionality
    """
    def closeUpdate(s):
        print "closed"


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
