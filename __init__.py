# coding: utf-8
# Todo script for Maya
# Created by Jason Dixon.
# 02.05.15

import maya.utils as utils
import maya.cmds as cmds
import collections
import threading
import traceback
import random
import addons
import json
import time
import math
import sys
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


class Popup(object):
    """
    Create a one time popup
    """
    def __init__(s, message):
        s.uid = "shot_unique_id_%s" % int((time.time() * 100))  # Generate unique ID
        s.message = message

    def stringify(s, data):
        return "python(\"%s\");" % data.replace("\\", "\\\\").replace("\"", "\\\"").replace("\n", r"\n")

    def __enter__(s):
        """
        Add things to the scene
        """
        s.job = cmds.scriptNode(n=s.uid, st=2, bs="")
        s.code = """
import maya.cmds as cmds
uid = "%s"
job = "%s"
load = cmds.fileInfo(uid, q=True)
load = load[0] if load else ""
if load == "ok":
    def makepopup():
        p = cmds.setParent(q=True)
        cmds.rowLayout(nc=2, ad2=2, p=p)
        cmds.columnLayout()
        cmds.iconTextStaticLabel(image="defaultCustomLayout.png", h=30, w=30)
        cmds.setParent("..")
        cmds.columnLayout(adj=True)
        cmds.text(al="left", hl=True, l=\"\"\"%s\"\"\")
        cmds.button(l="Thanks", c="cmds.layoutDialog(dismiss=\\"gone\\")")
        cmds.setParent("..")
    cmds.layoutDialog(ui=makepopup, t="A Quick Update")
if cmds.objExists(job):
    cmds.delete(job)
cmds.fileInfo(rm=uid)
""" % (s.uid, s.job, s.message)
        cmds.scriptNode(s.job, e=True, bs=s.stringify(s.code))
        cmds.fileInfo(s.uid, "ok")
        return s

    def __exit__(s, err, val, trace):
        """
        Remove those things from the scene
        """
        cmds.fileInfo(rm=s.uid)
        cmds.delete(s.job)


class Module(object):
    """
    Keep modules running smoothly. Make them threadsafe.
    """
    def __init__(s, name):
        if name in addons.modules:
            s.mod = addons.modules[name]
            s.mod.cmds = dummyCMD()
        else:
            raise Exception
        s.oldOut = sys.stdout
        sys.stdout = s

    def write(s, *t):
        t = "".join(t)
        if len(t.rstrip()):
            utils.executeDeferred(lambda: s.oldOut.write("%s\n" % t))

    def __enter__(s):
        return s.mod

    def __exit__(s, errType, errVal, trace):
        sys.stdout = s.oldOut
        s.mod.cmds = cmds
        if errType and hasattr(s.mod, "debug") and s.mod.debug:
            s.write("Uh oh... there was a problem. :(")
            s.write("%s :: %s" % (errType.__name__, errVal))
            for t in traceback.format_tb(trace):
                s.write(t)
        try:
            s.mod.cleanup()
        except Exception as e:
            if hasattr(s.mod, "debug") and s.mod.debug:
                s.write("Cleanup Error", e)
        return True


class dummyCMD(object):
    """
    Allow usage of cmds in threads.
    """
    def __getattr__(s, n):
        if hasattr(cmds, n):
            at = getattr(cmds, n)
            return lambda *a, **kw: utils.executeInMainThreadWithResult(lambda: at(*a, **kw))


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


def unique(item):
    """
    Only keep one window open at a time
    """
    items = {}

    def UniqueItem(*args, **kwargs):
        if (item in items and sys.getrefcount(items[item]) < 3) or item not in items:
            items[item] = item(*args, **kwargs)
        return items[item]
    return UniqueItem


@unique
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
            "Todo:", "Tasks:", "Doing well.", "Keep it up!", "You can do it.",
            "Good stuff.", "Make it happen!", ":D", "Nicely done.",
            "Things to do...", "Plan it. Do it. Succeed.", "Forward momentum.",
            "Making progress.", "I am a todo window?! How did I get in this strange place?",
            "Slow and steady.",
            "The secret of joy in work is contained in one word – excellence. To know how to do something well is to enjoy it.",
            "Knowing trees, I understand the meaning of patience. Knowing grass, I can appreciate persistence.",
            "Success consists of going from failure to failure without loss of enthusiasm.",
            "Successful and unsuccessful people do not vary greatly in their abilities. They vary in their desires to reach their potential.",
            "If you can imagine it, you can achieve it; if you can dream it, you can become it.",
            "Change your thoughts and you change your world.",
            "Out of clutter, find Simplicity. From discord, find Harmony. In the middle of difficulty lies Opportunity.",
            "You miss 100% of the shots you don’t take.",
            "If you don’t pay appropriate attention to what has your attention, it will take more of your attention than it deserves.",
            "The miracle is not that we do this work, but that we are happy to do it.",
            "Talent is cheaper than table salt. What separates the talented individual from the successful one is a lot of hard work.",
            "Big jobs usually go to the men who prove their ability to outgrow small ones.",
            "Never give up, for that is just the place and time that the tide will turn.",
            "You will never win if you never begin.",
            "Let's roll.",
            "I think, therefore, I am.",
            "What's done is done.",
            "Attack in all directions!",
            "No day but today.",
            "Attitude is everything.",
            "Whatever happens, take responsibility.",
            "Know thyself.",
            "Do it now!",
            "The buck stops here.",
            "Never, never, never give up.",
            "The most important thing is not to stop questioning.",
            "Only those who dare to fail greatly can ever achieve greatly.",
            "Thinking will not overcome fear but action will.",
            "Facts do not cease to exist because they are ignored.",
            "A creative man is motivated by the desire to achieve, not by the desire to beat others.",
            "If you aren't fired with enthusiasm, you will be fired with enthusiasm.",
            "Would you be shocked if I put on something more comfortable?",
            "Frankly, my dear, I don't give a damn!",
            "We don't see things as they are, we see things as we are.",
            "If you don't know where you are going you will probably end up somewhere else.",
            "I am a great believer in luck, and I find the harder I work, the more I have of it.",
            "The greatest revenge is to accomplish what others say you cannot do.",
            "All glory comes from daring to begin.",
            "If you change nothing, nothing changes.",
            "You might as well remember that nothing can bring you success but yourself.",
            "A goal is a dream with a deadline.",
            "Nothing is particularly hard if you divide it into small jobs.",
            "Once you have a clear picture of your priorities - organize around them.",
            "High achievement always takes place in the framework of high expectation.",
            "This one step, choosing a goal and sticking to it, changes everything.",
            "A good plan today is better than a great plan tomorrow.",
            "Knowing what to do is very, very different than actually doing it.",
            "First, say to yourself what you would be; and then do what you have to do.",
            "A mistake is only a mistake if you don't learn from it.",
            "It is amazing what you can accomplish if you do not care who gets the credit.",
            "A person who graduated yesterday and stops studying today is uneducated tomorrow.",
            "Don't let yesterday take up too much of today.",
            "Strive for excellence, not perfection.",
            "Failing to plan is planning to fail.",
            "Plan you work and work your plan.",
            "The discipline of writing something down is the first step toward making it happen.",
            "The best way to predict the future is to create it.",
            "I'll always cherish the original misconception I had of you.",
            "It is not necesssary to understand things in order to argue about them.",
            "In the middle of every difficulty lies opportunity",
            "If you change nothing, nothing changes",
            "You miss every shot you don't take.",
            "Stop thinking of what could go wrong and start thinking of what could go right",
            "If you waste time, time will waste you!",
            "Yes I Can!",
            "Do it Now!",
            "No day but today"])

        window = cmds.window(title=title, rtf=True)
        s.container = cmds.columnLayout(adjustableColumn=True)
        s.wrapper = ""

        allowed_areas = ['right', 'left']
        s.dock = cmds.dockControl(a='left', content=window, aa=allowed_areas, fl=True, l=title, fcc=s.moveDock, vcc=s.closeDock)

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
                        state[h] = s.sections[h] if h in s.sections else False
                        s.addTodo(v, section(h, state[h]))
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
            name = "%s_%s" % (s.basename, int(time.time() * 100))
            s.data[name] = txt
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
            """
            Update the progress bar
            """
            if cmds.progressBar(prog, ex=True):
                val = cmds.progressBar(prog, q=True, pr=True) + p
                if val < 100:
                    cmds.progressBar(prog, e=True, pr=val)
                    cmds.refresh()
                else:
                    cmds.progressBar(prog, e=True, pr=100)
                    cmds.refresh()
                    time.sleep(0.3)  # Pause on 100 for dramatic effect!
                    s._buidTodoTasks()

        scene = os.path.realpath(cmds.file(q=True, sn=True))  # Scene name
        temp = s.data[uid]  # hold onto todo data
        del s.data[uid]  # Remove todo from memory
        if os.path.splitext(os.path.basename(scene))[0] and os.path.isfile(scene):  # Check the scene is not untitled and still exists
            process = cmds.scriptJob(e=['SceneSaved', lambda: s.performArchive(scene, temp, update)], ro=True)
            try:
                message = """
<div>- This Scene was last saved on <em>%s</em>.</div>
<div>- Completing the task: <code>%s</code></div>
<div>- The file has <strong>not</strong> been modified since.</div><br>
""" % (time.ctime(), s._parseTodo(temp)["label"])
                with Popup(message):
                    cmds.file(save=True)  # Save the scene
            except RuntimeError:  # If scene save was canceled or failed. Reset everything
                if cmds.scriptJob(ex=process):
                    cmds.scriptJob(kill=process)
                s.data[uid] = temp
                s._buidTodoTasks()
        else:
            for i in range(25):  # The scene is untitled. Run a dummy progress bar to look nice
                time.sleep(0.01)
                update(4)
            s._buidTodoTasks()

    def performArchive(s, mayaFile, todo, callback):
        """
        Process the archving of the scene.
        """

        def getter(k, default):
            """
            Grab setting entry
            """
            return data.get(k, default)

        def archive(m):
            """
            Run archives
            """
            with Module(m) as mod:
                mod.archive(mayaFile, s._parseTodo(todo), getter)
            utils.executeDeferred(lambda: callback(step))

        data = s.data["todo_settings"]  # settings information
        step = int(math.ceil(100.0 / (len(addons.modules) + 1)))
        callback(step)  # One for the scene save!
        if addons.modules:
            for m in addons.modules:
                th = threading.Thread(target=archive, args=(m,))
                th.daemon = True
                th.start()

    def moveDock(s):  # Update dock location information
        if cmds.dockControl(s.dock, q=True, fl=True):
            s.location = "float"
            print "Floating Dock."
        else:
            area = cmds.dockControl(s.dock, q=True, a=True)
            s.location = area
            print "Docking %s." % area

    def closeDock(s, *loop):
        visible = cmds.dockControl(s.dock, q=True, vis=True)
        if not visible and loop:
            cmds.scriptJob(ie=s.closeDock, p=s.dock, ro=True)
        elif not visible:
            cmds.deleteUI(s.dock, ctl=True)
            print "Window closed."

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
