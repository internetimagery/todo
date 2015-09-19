# Controller for Maya
import maya.cmds as cmds
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

        s.window = view.MainWindow(
            "Todo_Window",
            "",
            title                 = "grab from file",
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
        # set up some containers
        s.todoContainerSections = cmds.columnLayout(adj=True, p=parent)
        s.todoContainerUnsectioned = cmds.columnLayout(adj=True, p=parent)
        s.todoSections = {}
        # insert todos
        for cat in s.getCategories():
            if cat == "None":
                print s.todoGetCategory(cat)
                print "here"
            else:
                print s.todoGetCategory(cat)
                print "there"

        # # TESTING:::
        # cmds.text(l="Added in controller")
        # cmds.text(l="Also added in controller")
        # cmds.text(l="Comes from in controller")
        # def test(*args):
        #     print "test", args
        # def edit(ID, text):
        #     viewdo.label = text
        #     viewdo.buildElement()
        # viewdo = view.Todo(
        #     "one",
        #     parent,
        #     ID="STUFF",
        #     realLabel="thing",
        #     doneCallback=test,
        #     editCallback=edit,
        #     deleteCallback=test,
        #     special={
        #         "description" : "what it does",
        #         "icon" : "fileOpen.png",
        #         "callback" : test
        #     })

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
