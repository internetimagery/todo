# TODO!!
# jason.dixon.email@gmail.com
from functools import wraps
import maya.cmds as cmds
import collections
import traceback
import datetime
import shutil
import json
import time
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


class SafetyNet(object):
    """
    Keep archives running smoothly
    """
    def delete(s, path):
        try:
            if os.path.isfile(path):
                os.remove(path)
                print "Deleting file %s" % path
            elif os.path.isdir(path):
                shutil.rmtree(path)
                print "Removing folder %s" % path
        except OSError as e:
            print e

    def __enter__(s):
        s.cleanup = []
        return s

    def __exit__(s, errType, errVal, trace):
        if errType:
            print "Uh oh... there was a problem. :("
            print "%s :: %s" % (errType.__name__, errVal)
            print "\n".join(traceback.format_tb(trace))
        if s.cleanup:
            for clean in s.cleanup:
                s.delete(clean)


class Scene(object):
    """
    Maya scene
    """
    def __init__(s):
        s.path = s._getPath()

    def _getPath(s):
        """
        Get scene location
        """
        path = re.findall("^((.+?)(\w*)(\.ma|\.mb))$", cmds.file(q=True, sn=True))
        if path:
            return path[0]  # (0 source, 1 path, 2 name, 3 extension)

    def save(s):
        """
        Save the scene
        """
        print "Saving scene."
        path = s._getPath()
        if path and path[2]:
            cmds.file(rename=path[0])
            cmds.file(save=True)
            s.path = path

    def archive(s, path, comment=""):
        """
        Save scene compressed with explicit name
        """
        if s.path and s.path[2]:
            name = "%s_%s_%s.ma" % (s.path[2], int(time.time()*100), comment)
            cmds.file(rename=os.path.join(path, name))
            cmds.file(save=True, compress=True)
            cmds.file(rename=s.path[0])


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


class Call(object):
    """
    Generic callback
    """
    def __init__(self, func, *args, **kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def __call__(self, *args):
        return self.func(*self.args, **self.kwargs)


def unique(item):
    """
    Only allow one window
    """
    items = {}

    @wraps(item)
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
        s.data = FileInfo()
        s.data["todo_location"] = s.data["todo_location"] if s.data["todo_location"] else "float"
        s.basename = "TODO"  # Name for all todo's to derive from

        title = "TODO:"

        window = cmds.window(title=title, rtf=True)
        s.container = cmds.columnLayout(adjustableColumn=True)
        s.wrapper = ""

        allowed_areas = ['right', 'left']
        s.dock = cmds.dockControl(a='left', content=window, aa=allowed_areas, fl=True, l=title, fcc=s.moveDock, vcc=s.closeDock)

        s._buildTodo()

        if s.data["todo_location"] == 'float':
            cmds.dockControl(s.dock, e=True, fl=True)
        elif s.data["todo_location"] in allowed_areas:
            cmds.dockControl(s.dock, e=True, a=s.data["todo_location"], fl=False)

        cmds.scriptJob(e=["PostSceneRead", Call(s._refresh)], p=s.dock)
        cmds.scriptJob(e=["NewSceneOpened", Call(s._refresh)], p=s.dock)

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
            ec=lambda x: (s.createTodo(x), clear()))
        cmds.button(
            label="Create a new TODO",
            h=40,
            c=lambda x: (s.createTodo(cmds.textField(text, q=True, tx=True)), clear()))
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
        regex = re.compile("^TODO_\d+")
        s.todoContainer = cmds.scrollLayout(bgc=[0.2, 0.2, 0.2], cr=True, p=s.todowrap)
        for k in sorted([k for k in s.data.keys() if k and regex.match(k)], key=lambda x: s.data[x]["label"]):
            s.addTodo(k)

    def _buildSettings(s, *args):
        """
        Load the settings page
        """
        s.page = "settings"
        data = s.data["todo_settings"] if s.data["todo_settings"] else {}

        def colour(val):
            return [0.5, 0.5, 0.5] if val else [0.2, 0.2, 0.2]

        def update(k, v):
            data[k] = v
            s.data["todo_settings"] = data
            s._buildSettings()

        s._clear()
        cmds.columnLayout(adjustableColumn=True)
        cmds.iconTextButton(h=30, image="revealSelected.png", label="<- Todo", style="iconAndTextHorizontal", c=s._buildTodo)
        cmds.separator()
        cmds.text(label="Settings are scene independent.", h=50)
        # Use File Archiving
        data["archive"] = data.get("archive", False)
        cmds.columnLayout(
            adjustableColumn=True,
            bgc=colour(data["archive"]))
        cmds.checkBox(
            l="Use File Archive",
            v=data["archive"],
            cc=lambda x: update("archive", x))
        # File archive path
        data["archive_path"] = data.get("archive_path", "")
        cmds.iconTextButton(
            en=data["archive"],
            image="fileOpen.png",
            l=data["archive_path"] if data["archive_path"] else "Pick archive folder.",
            style="iconAndTextHorizontal",
            c=lambda: update("archive_path", cmds.fileDialog2(ds=2, cap="Select a Folder.", fm=3, okc="Select")[0]))
        cmds.setParent("..")
        # Use AMP
        data["amp"] = data.get("amp", False)
        cmds.columnLayout(
            adjustableColumn=True,
            bgc=colour(data["amp"]))
        cmds.checkBox(
            l="Use AMP archive",
            v=data["amp"],
            cc=lambda x: update("amp", x))
        cmds.setParent(s.wrapper)

    def addTodo(s, uid):
        """
        Insert a todo
        """
        label = s.data[uid] # fileSave.png 
        parse = re.match("^[^\d]*?[^#](\d+)(\s*(-|,|to|and)\s*(\d+))?", label)  # Test for frame ranges
        range1 = parse.group(1) if parse else False
        range2 = parse.group(4) if parse else False

        wrapper = cmds.rowLayout(nc=4, ad4=1)  # if range1 else cmds.rowLayout(nc=3, ad3=1)
        cmds.iconTextButton(
            image="fileSave.png",  #"Bookmark.png", 
            h=30,
            style="iconAndTextHorizontal",
            label=label,
            fn="fixedWidthFont",
            ann="Click to check off and save.",
            c=Call(s.activateTodo, uid, wrapper))
        if range1 or range1 is 0:
            if range2 or range2 is 0:
                r = sorted([range1, range2])
                cmds.iconTextButton(
                    image="traxFrameRange.png",
                    style="iconOnly",
                    w=30,
                    ann="Jump to frame range (%s to %s)." % (r[0], r[1]),
                    c=lambda: TimeSlider().range(r[0], r[1]))
            else:
                cmds.iconTextButton(
                    image="centerCurrentTime.png",
                    style="iconOnly",
                    w=30,
                    ann="Go to frame %s." % range1,
                    c=lambda: TimeSlider().frame(range1))
        cmds.iconTextButton(
            image="editBookmark.png",
            style="iconOnly",
            w=30,
            ann="Edit Todo.",
            c=Call(s.editTodo, uid, wrapper))
        cmds.iconTextButton(
            image="removeRenderable.png",
            style="iconOnly",
            w=30,
            ann="Delete Todo without saving.",
            c=Call(s.removeTodo, uid, wrapper))
        cmds.setParent("..")

    def editTodo(s, uid, gui):
        """
        Change a todos information
        """
        def update(uid, label):
            data = s.data[uid]
            data["label"] = label
            s.data[uid] = data
            print "Updated Todo."
            s._buildTodo()

        for ui in cmds.rowLayout(gui, q=True, ca=True):
            cmds.deleteUI(ui)
        cmds.rowLayout(gui, e=True, nc=2)
        text = cmds.textField(p=gui, tx=s.data[uid])
        cmds.button(l="Ok", p=gui, c=lambda x: update(uid, cmds.textField(text, q=True, tx=True)))

    def createTodo(s, txt):
        """
        Create a new Todo
        """
        if txt:
            def name(i):
                return "%s_%s" % (s.basename, i)

            i = 0
            n = name(i)
            while n in s.data.keys():
                i += 1
                n = name(i)
            s.data[n] = txt
            s._buidTodoTasks()
            #s._buildTodo("debug")
        else:
            cmds.confirmDialog(title="Whoops...", message="You need to add some text for your Todo.")

    def removeTodo(s, uid, gui):
        """
        Remove a Todo
        """
        if cmds.rowLayout(gui, ex=True):
            cmds.deleteUI(gui)
        del s.data[uid]

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

        try:
            s.performArchive(uid, update)
            s.removeTodo(uid, gui)
        except RuntimeError as e:
            print "Warning:", e
            s._buidTodoTasks()

    def performArchive(s, uid, callback):
        """
        Do the archive process
        """
        data = s.data["todo_settings"]
        scene = cmds.file(q=True, sn=True)
        base = os.path.splitext(os.path.basename(scene))
        if base[0] and os.path.isfile(scene):  # Check if the savepath exists (ie if we are not an untitled scene)
            cmds.file(save=True)  # Save the file regardless
            if "archive" in data and data["archive"]:
                if "archive_path" in data and data["archive_path"] and os.path.isdir(data["archive_path"]):
                    with SafetyNet():
                        print "Archiving to folder: %s" % data["archive_path"]
                        FileArchive().archive(scene, data["archive_path"], s.data[uid])
                else:
                    cmds.confirmDialog(title="Uh oh...", message="Can't save file archive. You need to provide a folder.")
            if "amp" in data and data["amp"]:
                with SafetyNet():
                    print "Archiving to AMP"
                    AMPArchive().archive(scene, s.data[uid])
        for i in range(10):  # Make todo look fancy
            callback(i*10)
            time.sleep(0.03)

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


####### ARCHIVE METHODS
class FileArchive(object):
    """
    Archive using zipfile
    """
    def __init__(s):
        s.zip = __import__("zipfile")

    def archive(s, src, dest, comment=""):
        basename = os.path.basename(src)
        name = "%s_%s_%s.zip" % (os.path.splitext(basename)[0], int(time.time() * 100), comment)
        dest = os.path.join(dest, name)
        z = s.zip.ZipFile(dest, "w")
        z.write(src, basename)
        z.close()


class AMPArchive(object):
    """
    Archive using AMP
    """
    def __init__(s):
        try:
            am = __import__("am")
            s.config = am.cmclient.config.Configurator()
            s.manager = am.cmclient.manager.getShotManager(s.config)
            s.root = s.manager.contentRoot
            s.working = s._walk(s.root, [], "working")
        except ImportError:
            s.manager = False

    def archive(s, path, comment):
        """
        Save off file.
        """
        if s.manager and os.path.isfile(path) and s.root in path:
            if s._status(path):
                s._checkIn(path, comment)
                s._checkOut(path)
                return True
            elif "Confirm" == cmds.confirmDialog(title="Hold up...", message="You need to check out the file first.\nWould you like to do that now?"):
                s._checkOut(path)
                s._checkIn(path, comment)
                s._checkOut(path)
                return True
        return False

    def _walk(s, path, paths, stop):
        """
        Search files for working dir
        """
        for d in os.listdir(path):
            p = os.path.join(path, d)
            if os.path.isdir(p):
                if d == stop:
                    paths.append(p)
                else:
                    s._walk(p, paths, stop)
        return paths

    def _checkIn(s, path, comment):
        """
        Check in the file to lock in changes.
        """
        s.manager.checkinViewItemByPath(path, comment=comment)

    def _checkOut(s, path):
        """
        Check out file for editing.
        """
        s.manager.checkoutViewItemByPath(path)

    def _revert(s, path):
        """
        Revert file back to the most recent state.
        """
        s.manager.revertViewItemByPath(path)

    def _status(s, path):
        """
        Check the locked status of a file.
        """
        return os.access(path, os.W_OK)  # True = Checked out. False = Checked in.

MainWindow()
