# coding: utf-8
# Todo script for Maya
# Created by Jason Dixon.
# 02.05.15
# https://github.com/internetimagery/todo

import maya.utils as utils
import maya.cmds as cmds
import webbrowser
import subprocess
import threading
import traceback
import urlparse
import difflib
import random
import addons
import base64
import json
import time
import sys
import os
import re


def unique(item):
    """
    Only keep one instance open at a time
    """
    items = {}

    def UniqueItem(*args, **kwargs):
        if (item in items and sys.getrefcount(items[item]) < 3) or item not in items:
            items[item] = item(*args, **kwargs)
        return items[item]
    return UniqueItem


def embedImage():
    """
    Grab a random image and embed it in the scene.
    """
    path = os.path.join(os.path.dirname(__file__), "images")
    images = [os.path.join(path, f) for f in os.listdir(path) if f.endswith(".png")]
    if images:
        image = random.choice(images)
        with open(image, "rb") as f:
            image = "<img src=\\\"data:image/png;base64,%s\\\">" % base64.b64encode(f.read())
        return "cmds.text(hl=True, l=\"%s\", h=100, w=100)" % image
    else:
        return "cmds.iconTextStaticLabel(image=\"envChrome.svg\", h=100, w=100)  # file.svg looks nice too..."


def SaveAs():
    """
    Save prompt
    """
    return cmds.fileDialog2(ds=2, sff="Maya ASCII", ff="Maya Files (*.ma *.mb);;Maya ASCII (*.ma);;Maya Binary (*.mb);;")


class FileInfo(dict):
    """
    Fileinfo interface
    """
    def __init__(s):
        s.update(dict((k, v.decode("unicode_escape")) for k, v in (lambda x: zip(x[::2], x[1::2]))(cmds.fileInfo(q=True))))

    def __setitem__(s, k, v):
        utils.executeDeferred(lambda: cmds.fileInfo(k, v))
        super(FileInfo, s).__setitem__(k, v)

    def __delitem__(s, k):
        cmds.fileInfo(rm=k)
        super(FileInfo, s).__delitem__(k)


def FileOpen(path):
    """
    Open a file
    """
    def savePrompt():
        p = cmds.setParent(q=True)
        cmds.columnLayout(adj=True, p=p)
        cmds.rowLayout(nc=2)
        cmds.columnLayout()
        eval(embedImage())
        cmds.setParent("..")
        cmds.columnLayout(adj=True)
        cmds.text(al="left", hl=True, l="""
<h3>There are unsaved changes in your scene.</h3>
<div>Would you like to save before leaving?</div>""", h=70)
        cmds.rowLayout(nc=3, h=30)
        cmds.button(l="Yes please!".center(20), c="cmds.layoutDialog(dismiss=\"yes\")")
        cmds.button(l="No Thanks".center(20), c="cmds.layoutDialog(dismiss=\"no\")")
        cmds.button(l="Cancel".center(20), c="cmds.layoutDialog(dismiss=\"cancel\")")
        cmds.setParent("..")
        cmds.setParent("..")

    if os.path.isfile(path):
        if path[-3:] in [".ma", ".mb"]:  # Make a special exception for maya files.
            if cmds.file(mf=True, q=True):  # File is modified. Need to make some changes.
                answer = cmds.layoutDialog(ui=savePrompt, t="Excuse me one moment...")
                if answer == "yes":
                    if not cmds.file(q=True, sn=True):
                        loc = SaveAs()
                        if loc:
                            cmds.file(rn=loc[0])
                        else:
                            return
                    cmds.file(save=True)
                elif answer == "no":
                    pass
                else:
                    return
            cmds.file(path, o=True, f=True)
        else:
            universalOpen(path)


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


class Settings(object):
    """
    Settings interface
    """
    data = {}
    info = FileInfo()

    def __init__(s):
        try:
            s.data = json.loads(s.info["TODO_SETTINGS"])
        except (ValueError, KeyError):
            pass

    def __getattr__(s, k):
        print "KEY:", k
        return s.data.get(k, None)

    def __setattr__(s, k, v):
        s.data[k] = v
        s.info["TODO_SETTINGS"] = json.dumps(s.data)


class Popup(object):
    """
    Create a one time popup
    """
    def __init__(s, message):
        s.uid = "TODO_POPUP_%s" % int((time.time() * 100))  # Generate unique ID
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


class safeOut(object):
    """
    Protect output during threads
    """
    def __init__(s):
        s.oldOut = sys.stdout
        sys.stdout = s

    def write(s, *t):
        t = "".join(t)
        if len(t.rstrip()):
            utils.executeDeferred(lambda: s.oldOut.write("%s\n" % t))

    def __enter__(s):
        return s

    def __exit__(s, errType, errVal, trace):
        sys.stdout = s.oldOut
        if errType:
            s.write("Uh oh... there was a problem. :(")
            s.write("%s :: %s" % (errType.__name__, errVal))
            for t in traceback.format_tb(trace):
                s.write(t)
        return True


class safeCMDS(object):
    """
    Protect usage of cmds in threads.
    """
    def __getattr__(s, n):
        if hasattr(cmds, n):
            at = getattr(cmds, n)
            return lambda *a, **kw: utils.executeInMainThreadWithResult(lambda: at(*a, **kw))
        raise AttributeError


class TimeSlider(object):
    """
    Timeslider functionality
    """
    def frame(s, frame):
        cmds.currentTime(frame)

    def range(s, start, end):
        """
        Set frame range
        """
        cmds.playbackOptions(e=True, min=start, max=end)


#@unique
class MainWindow(object):
    """
    Main GUI Window
    """
    def __init__(s):
        s.registerHooks()  # Load our hooks
        if cmds.dockControl("TODO_WINDOW", ex=True):
            cmds.deleteUI("TODO_WINDOW")
            s.fireHook("app.end")
            print "Window exists. Closing and opening a new window."
        s.page = ""  # Page we are on.
        s._refresh()  # Initialize saved data
        s.fireHook("app.start")
        s.regex = {}  # Compiled regexes
        title = "Todo"
        try:
            with open(os.path.join(os.path.dirname(__file__), "quotes.json"), "r") as f:  # Motivation!
                title = random.choice(json.load(f))
        except (IOError, ValueError):
            print "No inspirational quotes loaded."

        window = cmds.window(title=title, rtf=True)
        s.container = cmds.columnLayout(adj=True)
        s.wrapper = ""

        allowed_areas = ['right', 'left']
        s.dock = cmds.dockControl("TODO_WINDOW", a='left', content=window, aa=allowed_areas, fl=True, l=title, fcc=s.moveDock, vcc=s.closeDock)

        s._buildTodo()

        if s.location == 'float':
            cmds.dockControl(s.dock, e=True, fl=True)
        elif s.location in allowed_areas:
            cmds.dockControl(s.dock, e=True, a=s.location, fl=False)

        cmds.scriptJob(e=["PostSceneRead", s._refresh], p=s.dock)
        cmds.scriptJob(e=["NewSceneOpened", s._refresh], p=s.dock)

    def _clear(s):
        """
        Clear the layout ready to be refreshed
        """
        if cmds.layout(s.wrapper, ex=True):
            cmds.deleteUI(s.wrapper)
        s.wrapper = cmds.columnLayout(adj=True, p=s.container)

    def _refresh(s):
        """
        Refresh the data
        """
        s.data = FileInfo()  # scene stored data
        s.settings = Settings()  # Settings wrapper for data
        if s.page == "todo":
            s._buildTodo()
        if s.page == "settings":
            s._buildSettings()

    def _buildTodo(s, *args):
        """
        Load up the TODO layout
        """
        s.page = "todo"
        s._clear()
        cmds.columnLayout(adj=True)
        cmds.columnLayout(adj=True)
        cmds.iconTextButton(
            h=30,
            ann="Click to view the Todo scripts settings. Settings are saved with the Maya scene, so you will need to set them for each scene.",
            image="attributes.png",
            label="Settings ->",
            style="iconAndTextHorizontal",
            c=s._buildSettings)
        cmds.separator()
        text = cmds.textField(
            aie=True,
            ed=True,
            h=30,
            ann="Type a task into the box.",
            ec=lambda x: not s.createTodo(x) or clear())
        cmds.button(
            label="Create a new TODO",
            h=20,
            ann="Type a task into the box.",
            c=lambda x: not s.createTodo(cmds.textField(text, q=True, tx=True)) or clear())
        cmds.setParent("..")

        def clear():  # Clear the text field
            cmds.textField(text, e=True, tx="")

        s.todowrap = cmds.columnLayout(adj=True)
        # Todo items in here!
        s.todoContainer = ""
        cmds.setParent("..")
        cmds.setParent(s.wrapper)

        s._buidTodoTasks()

    def _buidTodoTasks(s):
        """
        Refresh the todo task section of the window (fixes bug with lambda never returning)
        """
        if cmds.scrollLayout(s.todoContainer, ex=True):
            cmds.deleteUI(s.todoContainer)
        s.regex["uid"] = s.regex.get("uid", re.compile("^TODO_\d+"))
        s.todoContainer = cmds.scrollLayout(bgc=[0.2, 0.2, 0.2], cr=True, p=s.todowrap)
        sorter = cmds.columnLayout(adj=True, p=s.todoContainer)
        unsort = cmds.columnLayout(adj=True, p=s.todoContainer)
        sort_data = {}

        def stateChange(section, state):  # Save state of sections
            s.fireHook("app.changeSection")  # , settings=s._buidTodoTasks)
            data = s.settings.TodoSection if s.settings.TodoSection else {}
            data[section] = state
            s.settings.TodoSection = data
            utils.executeDeferred(s._buidTodoTasks)

        def section(title, state):  # Build a section for each piece
            title = title.strip()
            if title in sort_data:
                return sort_data[title]
            else:
                sort_data[title] = cmds.frameLayout(l=title, p=sorter, cll=True, cl=state, cc=lambda: stateChange(title, True), ec=lambda: stateChange(title, False))
                return sort_data[title]

        s.fireHook("app.buildList")
        currState = s.settings.TodoSection if s.settings.TodoSection else {}
        state = {}
        for v in sorted([s._parseTodo(s.data[k], uid=k) for k in s.data.keys() if k and s.regex["uid"].match(k)], key=lambda x: x["label"]):
            if v["token"] or v["hashtag"]:
                if v["token"]:
                    state[v["token"]] = currState[v["token"]] if v["token"] in currState else False
                    s.addTodo(v, section(v["token"], state[v["token"]]))
                if v["hashtag"]:
                    for h in v["hashtag"]:
                        state[h] = currState[h] if h in currState else False
                        s.addTodo(v, section(h, state[h]))
            else:  # Unsorted todos
                s.addTodo(v, unsort)
        s.settings.TodoSection = state

    def _buildSettings(s, *args):
        """
        Load the settings page
        """
        s.page = "settings"

        s._clear()
        cmds.columnLayout(adj=True, p=s.wrapper)
        cmds.iconTextButton(
            h=30,
            ann="Click to return to your Todo list.",
            image="revealSelected.png",
            label="<- Todo",
            style="iconAndTextHorizontal",
            c=s._buildTodo)
        cmds.separator()
        cmds.text(label="Settings are unique to each Maya scene.", h=50)
        frame = cmds.frameLayout(l="Archive options:")
        # Settings module
        s.fireHook("settings.archive", callback=lambda x: cmds.setParent(frame))  # , settings=s._buildSettings)
        cmds.setParent("..")
        cmds.frameLayout(l="Feedback:")
        cmds.iconTextButton(
            image="party.png",
            ann="Have any feedback? Good or bad. Love to hear it! :)",
            l="Leave Feedback...",
            style="iconAndTextHorizontal",
            c=lambda: universalOpen("mailto:jason.dixon.email@gmail.com?subject=Todo Feedback"))  # TODO errors when no folder is chosen because of 0 index

    def _parseTodo(s, label, **kwargs):
        """
        Parse out metadata from Todo
        """
        def build_reg():
            reg = "(?P<token>\A\w+(?=:\s))?"  # Token
            reg += "(?P<hashtag>(?<=#)\s?\w+)?"  # Hashtag
            reg += "(?P<url>https?://[^\s]+)?"  # Url
            frr = "(?:(?P<range1>\d+)\s*(?:[^\d\s]|to|and)\s*(?P<range2>\d+))"  # Frame range
            fr = "(?P<frame>\d+)"  # Frame
            reg += "(?:%s|%s)?" % (frr, fr)
            reg += "(?P<file>(?:[a-zA-Z]:|\\.{1,2})?[^\t\r\n:|]+\.\w+)?"  # Filename?
            return re.compile(reg)

        s.regex["label"] = s.regex.get("label", build_reg())
        parse = s.regex["label"].finditer(label)
        result = kwargs  # Add extra additional custom arguments
        result["token"] = ""
        result["hashtag"] = []
        result["url"] = ""
        result["file"] = ""  # Default
        result["frame"] = None
        result["framerange"] = []
        replace = {}  # Make the output nicer by removing certain tags
        if parse:
            for p in parse:
                m = p.groupdict()
                if m["token"]:  # Match tokens
                    result["token"] = m["token"]
                    replace[m["token"] + ":"] = ""
                if m["hashtag"]:  # Grab all hashtags, avoiding duplicates
                    if m["hashtag"] not in result["hashtag"]:
                        result["hashtag"].append(m["hashtag"].strip())
                        replace["#" + m["hashtag"]] = ""
                if m["url"]:  # Looking for a website?
                    result["url"] = m["url"]
                    replace[m["url"]] = urlparse.urlparse(m["url"]).netloc
                if m["range1"] and m["range2"]:  # Frame range?
                    result["framerange"] = sorted([m["range1"], m["range2"]])
                if m["frame"]:
                    result["frame"] = m["frame"]
                if m["file"] and not result["file"]:
                    path = m["file"].split(" ")
                    scene = os.path.dirname(cmds.file(q=True, sn=True))
                    refPaths = dict((os.path.basename(f), f) for f in cmds.file(l=True, q=True))  # Listing of all files
                    refNames = refPaths.keys()
                    for i in range(len(path)):  # Try figure out if a path is being requested
                        p = " ".join(path[i:])
                        closeMatch = difflib.get_close_matches(p, refNames, 1)  # Fuzzy search filenames
                        if closeMatch:  # Have we found a reference file?
                            rpath = os.path.realpath(refPaths[closeMatch[0]])
                        else:  # ... or perhaps another file somewhere else on the system?
                            rpath = os.path.realpath(os.path.join(scene, p))
                        if os.path.isfile(rpath):
                            result["file"] = rpath
                            replace[p] = os.path.basename(p)
        result["label"] = label.strip()
        if replace:
            for r in replace:
                result["label"] = result["label"].replace(r, replace[r])
        return result

    def addTodo(s, todo, parent):
        """
        Insert a todo
        """
        wrapper = cmds.rowLayout(nc=4, ad4=1, p=parent)
        cmds.iconTextButton(
            image="fileSave.png",
            h=30,
            style="iconAndTextHorizontal",
            label=todo["label"],
            fn="fixedWidthFont",
            ann="Click to check off and save.\nTODO: %s" % todo["label"],
            c=lambda: s.activateTodo(todo["uid"], wrapper))
        if todo["file"]:
            cmds.iconTextButton(
                image="openScript.png",
                style="iconOnly",
                w=30,
                ann="Open file: %s" % todo["file"],
                c=lambda: FileOpen(todo["file"]))
        elif todo["url"]:
            cmds.iconTextButton(
                image="SP_ComputerIcon.png",
                style="iconOnly",
                w=30,
                ann="Open url: %s" % todo["url"],
                c=lambda: webbrowser.open(todo["url"], new=2))
        elif todo["framerange"]:
            cmds.iconTextButton(
                image="traxFrameRange.png",
                style="iconOnly",
                w=30,
                ann="Jump to frame range (%s to %s)." % (todo["framerange"][0], todo["framerange"][1]),
                c=lambda: TimeSlider().range(todo["framerange"][0], todo["framerange"][1]))
        elif todo["frame"] or todo["frame"] is 0:  # Extra convenience button
            cmds.iconTextButton(
                image="centerCurrentTime.png",
                style="iconOnly",
                w=30,
                ann="Go to frame %s." % todo["frame"],
                c=lambda: TimeSlider().frame(todo["frame"]))
        cmds.iconTextButton(
            image="setEdEditMode.png",
            style="iconOnly",
            w=30,
            ann="Edit Todo.",
            c=lambda: s.editTodo(todo["uid"], wrapper))
        cmds.iconTextButton(
            image="removeRenderable.png",
            style="iconOnly",
            w=30,
            ann="Delete Todo without saving.",
            c=lambda: s.removeTodo(todo["uid"]))
        cmds.setParent("..")

    def editTodo(s, uid, gui):
        """
        Change a todos information
        """
        def update(uid, label):
            meta = s._parseTodo(label, uid=uid)
            if meta["label"]:
                s.data[uid] = label
                s.fireHook("todo.edit", meta, faf=True)
                s._buidTodoTasks()
            else:
                cmds.confirmDialog(title="Whoops...", message="You need to add some text for your Todo.")

        for ui in cmds.rowLayout(gui, q=True, ca=True):
            cmds.deleteUI(ui)
        cmds.rowLayout(gui, e=True, nc=2)
        text = cmds.textField(p=gui, tx=s.data[uid])
        cmds.button(l="Ok", p=gui, c=lambda x: update(uid, cmds.textField(text, q=True, tx=True)))

    def createTodo(s, txt):
        """
        Create a new Todo
        """
        name = "%(name)s_%(stamp)s" % {"name": "TODO", "stamp": int(time.time() * 100)}
        meta = s._parseTodo(txt, uid=name)
        if meta["label"]:
            s.data[name] = txt
            s.fireHook("todo.create", meta, faf=True)
            s._buidTodoTasks()
            return True  # Return True to retain input
        else:
            cmds.confirmDialog(title="Whoops...", message="You need to add some text for your Todo.")
            return False

    def removeTodo(s, uid):
        """
        Remove a Todo
        """
        meta = s._parseTodo(s.data[uid], uid=uid)
        s.fireHook("todo.delete", meta, faf=True)
        del s.data[uid]
        s._buidTodoTasks()

    def activateTodo(s, uid, gui):
        """
        Trigger the todo archive process
        """
        cmds.rowLayout(gui, e=True, en=False)

        def performArchive():
            s.fireHook("todo.complete", todo=tempmeta, faf=True)
            closeTodo()

        def closeTodo():  # Animate todo closed. Fancy.
            if cmds.layout(gui, ex=True):
                height = cmds.layout(gui, q=True, h=True)
                for i in range(20):
                    i = (100 - i*5) / 100.0
                    cmds.layout(gui, e=True, h=height * i)
                    cmds.refresh()
                    time.sleep(0.01)
            s._buidTodoTasks()

        temp = s.data[uid]  # hold onto todo data
        tempmeta = s._parseTodo(temp, uid=uid)
        del s.data[uid]  # Remove todo from memory
        if os.path.isfile(cmds.file(q=True, sn=True)):  # Check the scene is not untitled and still exists
            process = cmds.scriptJob(e=['SceneSaved', performArchive], ro=True)
            try:
                message = """
<div>- This Scene was last saved on <em>%(time)s</em>.</div>
<div>- Completing the task: <code>%(todo)s</code></div>
<div>- The file <strong>has not been modified since.</strong></div><br>
""" % {"time": time.ctime(), "todo": tempmeta["label"]}
                with Popup(message):
                    cmds.file(save=True)  # Save the scene
            except RuntimeError:  # If scene save was canceled or failed. Reset everything
                if cmds.scriptJob(ex=process):
                    cmds.scriptJob(kill=process)
                s.data[uid] = temp
                s._buidTodoTasks()
        else:
            performArchive()

    def moveDock(s):  # Update dock location information
        """
        Track dock movement
        """
        if cmds.dockControl(s.dock, q=True, fl=True):
            s.location = "float"
            print "Floating Dock."
        else:
            area = cmds.dockControl(s.dock, q=True, a=True)
            s.location = area
            print "Docking %s." % area

    def closeDock(s, *loop):
        """
        Gracefully close window
        """
        visible = cmds.dockControl(s.dock, q=True, vis=True)
        if not visible and loop:
            cmds.scriptJob(ie=s.closeDock, p=s.dock, ro=True)
        elif not visible:
            cmds.deleteUI(s.dock, ctl=True)
            s.fireHook("app.end")
            print "Window closed."

    def registerHooks(s):
        """
        Grab any hooks
        """
        s.hooks = {}
        if addons.modules:
            for name in addons.modules:
                mod = addons.modules[name]
                mod.cmds = safeCMDS()
                try:
                    hooks = mod.hooks()
                    for hook in hooks:
                        s.hooks[hook] = s.hooks.get(hook, []) + [hooks[hook]]
                except (AttributeError, TypeError):
                    print "Module %s is misisng a \"hooks\" function." % name

    def fireHook(s, hook, todo=None, faf=False, callback=None):
        """
        Use a hook
        hook = hookname, todo = todo meta data, faf = fire and forget the tasks, callback = run after each task has completed.
        """
        def fire(func):
            result = None
            with safeOut():
                result = func(mayaFile, todo, s.settings)
            if callback:
                callback(result)
            return result

        result = []
        threads = []
        if hook in s.hooks:
            path = os.path.realpath(cmds.file(q=True, sn=True))  # Scene name
            mayaFile = os.path.realpath(path) if os.path.isfile(path) else None
            for h in s.hooks[hook]:
                if faf:
                    th = threading.Thread(
                        target=lambda x: result.append(fire(x)),
                        args=(h,))
                    th.daemon = True
                    th.start()
                    threads.append(th)
                else:
                    result.append(fire(h))
        if threads and False:  # Block threads? TODO: stop maya from crashing...
            for th in threads:
                th.join()
        return result

    def location():
        """
        Window location
        """
        def fget(s):
            if cmds.optionVar(ex="todo_window_location"):
                return cmds.optionVar(q="todo_window_location")
            else:
                return "float"

        def fset(s, value):
            cmds.optionVar(sv=["todo_window_location", value])

        def fdel(s):
            if cmds.optionVar(ex="todo_window_location"):
                cmds.optionVar(rm="todo_window_location")
        return locals()
    location = property(**location())
