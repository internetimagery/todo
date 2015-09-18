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
# moveCallback(location) = run when docked or undocked
# closeCallback = run when window closed
# buildTodoCallback(parent) = run when switching to main todo window
# buildSettingsCallback(parent) = run when switching to settings window
# newTodoCallback(text) = run when creating a new todo
class MainWindow(GUIElement):
    """
    build window
    """
    def buildElement(s):
        window = cmds.window(title=s.options["title"], rtf=True)
        s.outerContainer = cmds.columnLayout(adj=True)
        s.window = cmds.dockControl(
            s.label,
            content=window,
            a="left",
            aa=["left", "right"],
            fl=True,
            l=s.options["title"],
            fcc=s.moveDock,
            vcc=s.closeDock
            )
        allowed = ["left", "right"]
        if s.options["location"] == 'float':
            cmds.dockControl(s.window, e=True, fl=True)
        elif s.options["location"] in allowed:
            cmds.dockControl(s.window, e=True, a=s.options["location"], fl=False)
        return s.buildTodo()

    """
    Build todo window
    """
    def buildTodo(s):
        s.removeUI()
        s.wrapper = cmds.columnLayout(adj=True)
        cmds.columnLayout(adj=True)
        cmds.iconTextButton(
            h=30,
            ann="Click to view the Todo scripts settings. Settings are saved with the Maya scene, so you will need to set them for each scene.",
            image="attributes.png",
            label="Settings ->",
            style="iconAndTextHorizontal",
            c=s.buildSettings
            )
        cmds.separator()
        s.todoText = cmds.textField(
            aie=True,
            ed=True,
            h=30,
            ann="Type a task into the box.",
            ec=lambda x: s.options["newTodoCallback"](cmds.textField(s.todoText, q=True, tx=True))
            )
        cmds.button(
            label="Create a new TODO",
            h=20,
            ann="Type a task into the box.",
            c=lambda x: s.options["newTodoCallback"](cmds.textField(s.todoText, q=True, tx=True))
            )
        cmds.setParent("..")
        s.options["buildTodoCallback"](s.wrapper)
        return s.wrapper

    """
    Build settings window
    """
    def buildSettings(s):
        s.removeUI()
        s.wrapper = cmds.columnLayout(adj=True, p=s.outerContainer)
        cmds.iconTextButton(
            h=30,
            ann="Click to return to your Todo list.",
            image="revealSelected.png",
            label="<- Todo",
            style="iconAndTextHorizontal",
            c=s.buildTodo
            )
        cmds.separator()
        cmds.text(label="Settings are unique to each Maya scene.", h=50)
        s.options["buildSettingsCallback"](s.wrapper)

    """
    Edit the todo input text
    """
    def editTodo(s, text):
        try:
            cmds.textField(s.todoText, e=True, tx=text)
        except RuntimeError:
            pass

    """
    Keep track of dock movement
    """
    def moveDock(s):  # Update dock location information
        if cmds.dockControl(s.window, q=True, fl=True):
            s.options["location"] = "float"
            s.options["moveCallback"]("float")
            print "Floating Dock."
        else:
            area = cmds.dockControl(s.window, q=True, a=True)
            s.options["location"] = area
            s.options["moveCallback"](area)
            print "Docking %s." % area

    """
    Close window
    """
    def closeDock(s, *loop):
        visible = cmds.dockControl(s.window, q=True, vis=True)
        if not visible and loop:
            cmds.scriptJob(ie=s.closeDock, p=s.window, ro=True)
        elif not visible:
            print "Window closed."
            cmds.deleteUI(s.window)
            s.options["closeCallback"]()

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
