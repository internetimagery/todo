# Controller for Maya
import maya.cmds as cmds
import maya.utils as utils
from re import compile
from time import time, ctime
from random import choice
from os.path import join, dirname, isfile, realpath
from base64 import b64encode
from os import listdir
import webbrowser
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
                scene = realpath(cmds.fileInfo(q=True, sn=True))
                if isfile(scene): # If file exists then save
                    process = cmds.scriptJob(e=['SceneSaved', lambda: s.todoArchive(task, scene)], ro=True)
                    try:
                        message = """
                        <div>- This Scene was last saved on <em>%(time)s</em>.</div>
                        <div>- Completing the task: <code>%(todo)s</code></div>
                        <div>- The file <strong>has not been modified since.</strong></div><br>
                        """ % {"time": ctime(), "todo": task.label}
                        with Popup(message):
                            cmds.file(save=True)  # Save the scene
                            print "Complete:", task.label
                        s.todoRemove(task)
                        delete(todoElement)
                    except RuntimeError: # Save was canceled
                        if cmds.scriptJob(ex=process):
                            cmds.scriptJob(kill=process)
                else: # Untitled scene
                    s.todoRemove(task)
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
            return view.Todo(
                task.label,
                section,
                ID="STUFF",
                realLabel=task.task,
                doneCallback=done,
                editCallback=edit,
                deleteCallback=delete,
                special=s.pickMetadata(task)
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
    Pick a single metadata special button
    """
    def pickMetadata(task):
        if "File" in task.meta and task.meta["File"]:
            f = task.meta["File"][0]
            return {
                "description"   : "Open file: %s" % f,
                "icon"          : "openScript.png",
                "callback"      : lambda: fileOpen(f)
            }
        elif "Url" in task.meta and task.meta["Url"]:
            url = task.meta["Url"][0]
            return {
                "description"   : "Open url: %s" % url,
                "icon"          : "SP_ComputerIcon.png",
                "callback"      : lambda: webbrowser.open(url, new=2)
            }
        elif "Range" in task.meta and task.meta["Range"]:
            mini = task.meta["Range"][0][0]
            maxi = task.meta["Range"][0][1]
            return {
                "description"   : "Jump to frame range (%s, %s)." % (mini, maxi),
                "icon"          : "traxFrameRange.png",
                "callback"      : lambda: cmds.playbackOptions(e=True, min=mini,max=maxi)
            }
        elif "Frame" in task.meta and task.meta["Frame"]:
            frame = task.meta["Frame"][0]
            return {
                "description"   : "Go to Frame: %s" % frame,
                "icon"          : "centerCurrentTime.png",
                "callback"      : lambda: cmds.currentTime(frame)
            }
        else:
            return {}

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

class Popup(object):
    """
    Create a one time popup
    """
    def __init__(s, message):
        s.uid = "TODO_POPUP_%s" % int((time() * 100))  # Generate unique ID
        s.message = message

    def stringify(s, data):
        return "python(\"%s\");" % data.replace("\\", "\\\\").replace("\"", "\\\"").replace("\n", r"\n")

    def __enter__(s):
        s.job = cmds.scriptNode(n=s.uid, st=2, bs="")
        s.code = """
import maya.cmds as cmds
uid = "%(uid)s"
job = "%(job)s"
if cmds.fileInfo(uid, q=True) == ["ok"]:
    def makepopup():
        p = cmds.setParent(q=True)
        cmds.rowLayout(nc=2, ad2=2, p=p)
        cmds.columnLayout()
        %(image)s
        cmds.setParent("..")
        cmds.columnLayout(adj=True)
        cmds.text(al="left", hl=True, l=\"\"\"%(message)s\"\"\", h=70)
        cmds.button(l="Thanks", c="cmds.layoutDialog(dismiss=\\"gone\\")", h=30)
        cmds.setParent("..")
    cmds.layoutDialog(ui=makepopup, t="Welcome Back")
if cmds.objExists(job):
    cmds.delete(job)
cmds.fileInfo(rm=uid)
""" % {"uid": s.uid, "job": s.job, "image": embedImage(), "message": s.message}
        cmds.scriptNode(s.job, e=True, bs=s.stringify(s.code))
        cmds.fileInfo(s.uid, "ok")
        return s

    def __exit__(s, err, val, trace):
        """
        Remove those things from the scene
        """
        cmds.fileInfo(rm=s.uid)
        if cmds.objExists(s.job):
            cmds.delete(s.job)

def embedImage():
    """
    Grab a random image and embed it in the scene.
    """
    path = join(dirname(__file__), "images")
    images = [join(path, f) for f in listdir(path) if f.endswith(".png")]
    if images:
        image = choice(images)
        with open(image, "rb") as f:
            image = "<img src=\\\"data:image/png;base64,%s\\\">" % b64encode(f.read())
        return "cmds.text(hl=True, l=\"%s\", h=100, w=100)" % image
    else:
        return "cmds.iconTextStaticLabel(image=\"envChrome.svg\", h=100, w=100)  # file.svg looks nice too..."

def fileOpen(path):
    if os.path.isfile(path):
        if path[-3:] in [".ma", ".mb"]:  # Make a special exception for maya files.
            if cmds.file(mf=True, q=True):  # File is modified. Need to make some changes.
                def ask(answer):
                    if answer == "yes":
                        if not cmds.file(q=True, sn=True):
                            loc = saveAs()
                            if loc:
                                cmds.file(rn=loc[0])
                            else:
                                return
                        cmds.file(save=True)
                    elif answer == "no":
                        cmds.file(path, o=True, f=True)
                    else:
                        return
                view.PopupDialog(
                    "Excuse me one moment...",
                    "",
                    message="""
<h3>There are unsaved changes in your scene.</h3>
<div>Would you like to save before leaving?</div>
""",
                    image=eval(embedImage()),
                    responseCallback=ask
                    )
            else:
                cmds.file(path, o=True, f=True)
        else:
            universalOpen(path)

def saveAs():
    """
    Save prompt
    """
    return cmds.fileDialog2(ds=2, sff="Maya ASCII", ff="Maya Files (*.ma *.mb);;Maya ASCII (*.ma);;Maya Binary (*.mb);;")

def universalOpen(command):
    """
    Open file in different OS's
    """
    try:
        os.startfile(command)  # Open file on windows
    except AttributeError:  # Open file on anything else
        for com in [["open"], ["xdg-open"], ["gnome-open"], ["kde-open"], ["exo-open"]]:
            try:
                return subprocess.Popen(com + [command])
            except OSError:
                pass
            webbrowser.open(command)

Start()
