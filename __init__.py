# coding: utf-8
# TODO!!
# jason.dixon.email@gmail.com
import maya.cmds as cmds
import collections
import traceback
import random
import addons
import json
import time
import os
import re


class FileInfo(collections.MutableMapping):
    """
    Dictionary style interface for fileInfo
    """
    def _encode(s, txt):
        return json.dumps(txt)

    def _decode(s, u):
        u = u.decode("unicode_escape")
        try:
            return json.loads(u)
        except ValueError as e:
            print "ERR: %s" % e, u
            return u

    def _key(s, k):
        if k in s.blacklist:
            return "%s_" % k
        return k

    def __init__(s):
        s.blacklist = ["application", "product", "version", "cutIdentifier", "osv", "license"]
        s.data = dict()
        init = cmds.fileInfo(q=True)
        if init:
            s.data = dict((k, s._decode(v)) for k, v in (lambda x: zip(x[::2], x[1::2]))(cmds.fileInfo(q=True)) if k not in s.blacklist)
        s.update(dict())

    def __getitem__(s, k):
        k = s._key(k)
        i = cmds.fileInfo(k, q=True)
        s.data[k] = s._decode(i[0] if i else '""')
        return s.data[k]

    def __setitem__(s, k, v):
        k = s._key(k)
        cmds.fileInfo(k, s._encode(v))
        s.data[k] = v

    def __delitem__(s, k):
        k = s._key(k)
        cmds.fileInfo(rm=k)
        del s.data[k]

    def __iter__(s):
        return iter(s.data)

    def __len__(s):
        return len(s.data)


class Module(object):
    """
    Keep modules running smoothly
    """
    def __init__(s, name):
        if name in addons.modules:
            s.mod = addons.modules[name]
        else:
            s.mod = False

    def __enter__(s):
        return s.mod

    def __exit__(s, errType, errVal, trace):
        if errType and hasattr(s.mod, "debug") and s.mod.debug:
            print "Uh oh... there was a problem. :("
            print "%s :: %s" % (errType.__name__, errVal)
            for t in traceback.format_tb(trace):
                print t
        try:
            s.mod.cleanup()
        except Exception as e:
            if hasattr(s.mod, "debug") and s.mod.debug:
                print "Cleanup Error", e
        return True


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


class MainWindow(object):
    """
    Main GUI Window
    """
    def __init__(s):
        s.page = ""  # Page we are on.
        s.data = FileInfo()  # Scene stored data
        s.basename = "TODO"  # Name for all todo's to derive from
        s.regex = {}  # Compiled regexes
        s.sections = {}  # Closed / Open state of todo sections

        title = random.choice([
            "Todo:",
            "Going well.",
            "Keep it up!",
            "You can do it.",
            "Good stuff.",
            "Things to do...",
            "Making progress.",
            "Slow and steady."])

        window = cmds.window(title=title, rtf=True)
        s.container = cmds.columnLayout(adjustableColumn=True)
        s.wrapper = ""

        allowed_areas = ['right', 'left']
        s.dock = cmds.dockControl("todo_window", a='left', content=window, aa=allowed_areas, fl=True, l=title, fcc=s.moveDock, vcc=s.closeDock)

        s._buildTodo()

        if s.data["todo_location"] == 'float':
            cmds.dockControl(s.dock, e=True, fl=True)
        elif s.data["todo_location"] in allowed_areas:
            cmds.dockControl(s.dock, e=True, a=s.data["todo_location"], fl=False)
        else:
            s.data["todo_location"] = "float"

        cmds.scriptJob(e=["PostSceneRead", s._refresh], p=s.dock)
        cmds.scriptJob(e=["NewSceneOpened", s._refresh], p=s.dock)

    def _clear(s):
        """
        Clear the layout ready to be refreshed
        """
        if cmds.layout(s.wrapper, ex=True):
            cmds.deleteUI(s.wrapper)
        s.wrapper = cmds.columnLayout(adjustableColumn=True, p=s.container)

    def _refresh(s):
        """
        Refresh the data
        """
        s.data = FileInfo()
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
        cmds.columnLayout(adjustableColumn=True)
        cmds.columnLayout(adjustableColumn=True)
        cmds.iconTextButton(h=30, image="attributes.png", label="Settings ->", style="iconAndTextHorizontal", c=s._buildSettings)
        cmds.separator()
        text = cmds.textField(
            aie=True,
            ed=True,
            h=30,
            ec=lambda x: not s.createTodo(x) or clear())
        cmds.button(
            label="Create a new TODO",
            h=20,
            c=lambda x: not s.createTodo(cmds.textField(text, q=True, tx=True)) or clear())
        cmds.setParent("..")

        def clear():  # Clear the text field
            cmds.textField(text, e=True, tx="")

        s.todowrap = cmds.columnLayout(adjustableColumn=True)
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
        s.regex["uid"] = s.regex.get("uid", re.compile("^%s_\d+" % s.basename))
        s.todoContainer = cmds.scrollLayout(bgc=[0.2, 0.2, 0.2], cr=True, p=s.todowrap)
        sorter = cmds.columnLayout(adj=True, p=s.todoContainer)
        unsort = cmds.columnLayout(adj=True, p=s.todoContainer)
        sort_data = {}

        def stateChange(section, state):  # Save state of sections
            s.sections[section] = state

        def section(title, state):  # Build a section for each piece
            title = title.strip()
            if title in sort_data:
                return sort_data[title]
            else:
                sort_data[title] = cmds.frameLayout(l=title, p=sorter, cll=True, cl=state, cc=lambda: stateChange(title, True), ec=lambda: stateChange(title, False))
                return sort_data[title]

        state = {}
        for v in sorted([dict({"uid": k}, **s._parseTodo(s.data[k])) for k in s.data.keys() if k and s.regex["uid"].match(k)], key=lambda x: x["label"]):
            if v["token"] or v["hashtag"]:
                if v["token"]:
                    state[v["token"]] = s.sections[v["token"]] if v["token"] in s.sections else False
                    s.addTodo(v, section(v["token"], state[v["token"]]))
                if v["hashtag"]:
                    for h in v["hashtag"]:
                        state[v["hashtag"]] = s.sections[v["hashtag"]] if v["hashtag"] in s.sections else False
                        s.addTodo(v, section(h, state[v["hashtag"]]))
            else:  # Unsorted todos
                s.addTodo(v, unsort)
        s.sections = state

    def _buildSettings(s, *args):
        """
        Load the settings page
        """
        ready = False  # Bug fix. Trigger updates when page is built
        s.page = "settings"
        data = s.data["todo_settings"] if s.data["todo_settings"] else {}

        def colour(val):
            return [0.5, 0.5, 0.5] if val else [0.2, 0.2, 0.2]

        def update(k, v):  # Allow module to set value
            if ready:
                data[k] = v
                s.data["todo_settings"] = data
                s._buildSettings()

        def get(k, default=None):  # Allow module to get value
            return data.get(k, default)

        s._clear()
        cmds.columnLayout(adjustableColumn=True, p=s.wrapper)
        cmds.iconTextButton(h=30, image="revealSelected.png", label="<- Todo", style="iconAndTextHorizontal", c=s._buildTodo)
        cmds.separator()
        cmds.text(label="Settings are unique to each Maya scene.", h=50)
        cmds.frameLayout(l="Archive options:")
        # Settings module
        for m in addons.modules:
            with Module(m) as mod:
                mod.settings_archive(get, update)
        cmds.setParent("..")
        ready = True

    def _parseTodo(s, label):
        """
        Parse out metadata from Todo
        """
        def build_reg():
            reg = "(\A\w+(?=:))?"  # Token
            reg += "((?<=#)\s?\w+)?"  # Hashtag
            frr = "(?:(\d+)\s*(?:[^\d\s]|to|and)\s*(\d+))"  # Frame range
            fr = "(\d+)"  # Frame
            reg += "(?:%s|%s)?" % (frr, fr)
            return re.compile(reg)

        s.regex["label"] = s.regex.get("label", build_reg())
        parse = s.regex["label"].finditer(label)
        result = {}
        result["token"] = ""
        result["hashtag"] = []
        result["frame"] = None
        result["framerange"] = []
        if parse:
            for p in parse:
                m = p.groups()
                if m[0]:  # Match tokens
                    result["token"] = m[0]
                if m[1]:
                    if m[1] not in result["hashtag"]:
                        result["hashtag"].append(m[1].strip())
                if m[2] and m[3]:
                    result["framerange"] = sorted([m[2], m[3]])
                if m[4]:
                    result["frame"] = m[4]
        # Clean out hashtags and tokens for nicer looking todos
        s.regex["label_clean"] = s.regex.get("label_clean", re.compile("(\A\w+:)?" + "(#\s?\w+,?)?"))
        result["label"] = s.regex["label_clean"].sub("", label).strip()
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
        if todo["frame"] or todo["frame"] is 0:
            cmds.iconTextButton(
                image="centerCurrentTime.png",
                style="iconOnly",
                w=30,
                ann="Go to frame %s." % todo["frame"],
                c=lambda: TimeSlider().frame(todo["frame"]))
        elif todo["framerange"]:
            cmds.iconTextButton(
                image="traxFrameRange.png",
                style="iconOnly",
                w=30,
                ann="Jump to frame range (%s to %s)." % (todo["framerange"][0], todo["framerange"][1]),
                c=lambda: TimeSlider().range(todo["framerange"][0], todo["framerange"][1]))
        cmds.iconTextButton(
            image="editBookmark.png",
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
            meta = s._parseTodo(label)
            if meta["label"]:
                s.data[uid] = label
                print "Updated Todo."
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
        meta = s._parseTodo(txt)
        if meta["label"]:
            def name(i):
                return "%s_%s" % (s.basename, i)

            i = 0
            n = name(i)
            while n in s.data.keys():
                i += 1
                n = name(i)
            s.data[n] = txt
            s._buidTodoTasks()
            return True  # Return True to retain input
        else:
            cmds.confirmDialog(title="Whoops...", message="You need to add some text for your Todo.")
            return False

    def removeTodo(s, uid):
        """
        Remove a Todo
        """
        del s.data[uid]
        s._buidTodoTasks()

    def activateTodo(s, uid, gui):
        """
        Trigger the todo archive process
        """
        for ui in cmds.rowLayout(gui, q=True, ca=True):
            cmds.deleteUI(ui)
        prog = cmds.progressBar(p=gui, pr=0)

        def update(p):
            cmds.progressBar(prog, e=True, pr=p)
            cmds.refresh(cv=True)

        temp = s.data[uid]
        del s.data[uid]
        try:
            s.performArchive(temp, update)
        except RuntimeError as e:
            print "Warning:", e
            s.data[uid] = temp  # Rebuild todo
        s._buidTodoTasks()

    def performArchive(s, todo, callback):
        """
        Do the archive process
        """
        data = s.data["todo_settings"]
        progress = 10
        callback(progress)

        def getter(k, default):
            return data.get(k, default)

        scene = cmds.file(q=True, sn=True)
        base = os.path.splitext(os.path.basename(scene))
        if os.path.isfile(scene) and base[0]:  # Check if the savepath exists (ie if we are not an untitled scene)
            cmds.file(save=True)  # Save the file regardless
            if addons.modules:
                steps = len(addons.modules)  # Number of archives
                for m in addons.modules:
                    with Module(m) as mod:
                        mod.archive(scene, s._parseTodo(todo), getter)
                        progress += 50 / steps  # Progress bar up to halfway with real progress. Rest of the way fake. :P
                        callback(progress)

        for i in range(20):  # Make marking off a todo look fancy
            progress += i*5
            if progress <= 100:
                callback(progress)
                time.sleep(0.05)

    def moveDock(s):  # Update dock location information
        if cmds.dockControl(s.dock, q=True, fl=True):
            s.data["todo_location"] = "float"
            print "Floating Dock."
        else:
            area = cmds.dockControl(s.dock, q=True, a=True)
            s.data["todo_location"] = area
            print "Docking %s." % area

    def closeDock(s, *loop):
        visible = cmds.dockControl(s.dock, q=True, vis=True)
        if not visible and loop:
            cmds.scriptJob(ie=s.closeDock, p=s.dock, ro=True)
        elif not visible:
            cmds.deleteUI(s.dock, ctl=True)
            print "Window closed."


def go():  # Run the main window
    try:
        MainWindow()
    except RuntimeError:
        print "Window exists already."
