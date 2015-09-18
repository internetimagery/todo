# Maya UI Elements
import maya.cmds as cmds

class GUIElement(object):
    """
    Base gui class
    """
    def __init__(s, label, parent, **kwargs):
        s.label = label
        s.parent = parent
        s.options = kwargs
        s.wrapper = ""
        s.buildElement()

    """
    Clear UI for refreshing
    """
    def removeUI(s):
        try:
            cmds.deleteUI(s.wrapper)
        except RuntimeError:
            pass

    """
    dummy build function
    """
    def buildElement(s):
        print "Need to override the build element function"

# options:
# title = window title
# location = "float" or "left" or "right"
# moveCallback = run when docked or undocked
# closeCallback = run when window closed
class MainWindow(GUIElement):
    """
    build window
    """
    def buildElement(s):
        s.removeUI()
        window = cmds.window(title=title, rtf=True)
        s.outerContainer = cmds.columnLayout(adj=True)
        s.wrapper = cmds.dockControl(
            s.label,
            a="float",
            content=window,
            aa=["left", "right"],
            fl=True,
            l=s.options["title"],
            fcc=s.moveDock,
            vcc=s.closeDock
            )
        if s.options["location"] in ["left", "right"]:
            cmds.dockControl(s.wrapper, e=True, a=s.options["location"], fl=False)


# options:
# realLabel = label that includes hashtags etc etc
# doneCallback = ticked off todo
# editCallback = changed todo name
# deleteCallback = deleted todo
# special = button
#   description = describe button
#   icon = button icon
#   callback = run when pressed
class Todo(GUIElement):
    """
    Build the todo
    """
    def buildElement(s):
        s.removeUI()
        s.wrapper = cmds.rowLayout(nc=4, ad4=1, p=s.parent)
        cmds.iconTextButton(
            image="fileSave.png",
            h=30,
            style="iconAndTextHorizontal",
            label=s.label,
            fn="fixedWidthFont",
            ann="Click to check off and save.\nTODO: %s" % s.label,
            c=lambda: s.options["doneCallback"]()
            )
        if s.options["special"]:
            cmds.iconTextButton(
                image=s.options["special"]["icon"],
                style="iconOnly",
                w=30,
                ann=s.options["special"]["description"],
                c=lambda: s.options["special"]["callback"]
                )
        cmds.iconTextButton(
            image="setEdEditMode.png",
            style="iconOnly",
            w=30,
            ann="Edit Todo.",
            c=lambda: s.editTodo()
            )
        cmds.iconTextButton(
            image="removeRenderable.png",
            style="iconOnly",
            w=30,
            ann="Delete Todo without saving.",
            c=lambda: s.deleteTodo()
            )
        return s.wrapper

    """
    edit todo
    """
    def editTodo(s):
        s.removeUI()
        s.wrapper = cmds.rowLayout(nc=2, ad4=0, p=s.parent)
        text = cmds.textField(tx=s.options["realLabel"])
        cmds.button(l="Ok", c=lambda x: s.options["editCallback"](cmds.textField(text, q=True, tx=True)))

    """
    delete the todo
    """
    def deleteTodo(s):
        s.options["deleteCallback"]()
        s.removeUI()

# options:
# openCallback = run when opening
# closeCallback = run when closing
class TodoSection(GUIElement):
    """
    build section
    """
    def buildElement(s):
        s.removeUI()
        s.wrapper = cmds.frameLayout(
            l=s.label,
            p=s.parent,
            cll=True,
            cl=False,
            cc=lambda: s.options["closeCallback"](),
            ec=lambda: s.options["openCallback"]()
        )
        return s.wrapper

    def open(s):
        cmds.frameLayout(s.wrapper, e=True, cl=False)

    def close(s):
        cmds.frameLayout(s.wrapper, e=True, cl=True)


# options:
# [
#
# ]
class setting(GUIElement):
    """
    Build Elements
    """
    def buildElement(s):
        pass
