# TODO!!
# jason.dixon.email@gmail.com
from functools import wraps
import maya.cmds as cmds
import collections
import json
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
            print "ERR: %s" % e
            return u

    def _key(s, k):
        if k in ["application", "product", "version", "cutIdentifier", "osv", "license"]:
            return "%s_" % k
        return k

    def __init__(s):
        s.data = dict()
        init = cmds.fileInfo(q=True)
        if init:
            s.data = dict((k, s._decode(v)) for k, v in (lambda x: zip(x[::2], x[1::2]))(cmds.fileInfo(q=True)))
        s.update(s.data)

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


class Scene(object):
    """
    Maya scene
    """
    def __init__(s):
        s.path = s._getPath()

    def _getPath(s):
        return cmds.file(q=True, sn=True)

    def save(s):
        print "Saving scene."
        s.path = cmds.file(save=s._getPath())


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
        s.data["todo_location"] = s.data["todo_location"] if "todo_location" in s.data.keys() else "float"
        s.basename = "TODO"  # Name for all todo's to derive from

        title = "TODO:"

        window = cmds.window(title=title)
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
        cmds.iconTextButton(h=30, image="attributes.png", label="Settings ->", style="iconAndTextHorizontal", c=s._buildSettings)
        cmds.separator()
        text = cmds.textField()
        cmds.button(label="Create a new TODO", h=40, c=lambda x: s.createTodo(cmds.textField(text, q=True, tx=True)))
        s.todowrap = cmds.scrollLayout(bgc=[0.2, 0.2, 0.2], cr=True)
        regex = re.compile("^TODO_\d+")
        for k in sorted([k for k in s.data.keys() if k and regex.match(k)], key=lambda x: s.data[x]["label"]):
            s.addTodo(k)
        cmds.setParent("..")
        cmds.setParent(s.wrapper)

    def _buildSettings(s, *args):
        """
        Load the settings page
        """
        s.page = "settings"
        data = s.data["todo_settings"] if "todo_settings" in s.data.keys() else {}

        def colour(val):
            return [0.5, 0.5, 0.5] if val else [0.2, 0.2, 0.2]

        def update(k, v):
            data[k] = v
            s.data["todo_settings"] = data
            s._buildSettings()
            print data

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
        # cmds.file(save="PATH", compress=True)
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
        wrapper = cmds.rowLayout(nc=3, ad3=1)
        cmds.iconTextButton(
            image="Bookmark.png",
            h=30,
            style="iconAndTextHorizontal",
            label=s.data[uid]["label"],
            fn="fixedWidthFont",
            c=Call(s.activateTodo, uid, wrapper))
        cmds.iconTextButton(image="editBookmark.png", style="iconOnly", w=30, c=Call(s.editTodo, uid, wrapper))
        cmds.iconTextButton(image="removeRenderable.png", style="iconOnly", w=30, c=Call(s.removeTodo, uid, wrapper))
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

        [cmds.deleteUI(ui) for ui in cmds.rowLayout(gui, q=True, ca=True)]
        cmds.rowLayout(gui, e=True, nc=2)
        text = cmds.textField(p=gui, ec=Call(s._buildTodo))
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
            s.data[n] = {"label": txt}
            s._buildTodo()
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
        [cmds.deleteUI(ui) for ui in cmds.rowLayout(gui, q=True, ca=True)]
        prog = cmds.progressBar(p=gui, pr=0)
        import time
        for i in range(10):
            cmds.progressBar(prog, e=True, pr=i*10)
            time.sleep(0.1)
            cmds.refresh(cr=True)
        s.removeTodo(uid, gui)

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

MainWindow()
