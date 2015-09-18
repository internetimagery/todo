# Maya UI Elements
import maya.cmds as cmds

# kwargs:
# realLabel = label that includes hashtags etc etc
# doneCallback = ticked off todo
# editCallback = changed todo name
# deleteCallback = deleted todo
# special = button
#   description = describe button
#   icon = button icon
#   callback = run when pressed
class Todo(object):
    """
    Single Todo UI element
    """
    def __init__(s, label, parent, **kwargs):
        s.label = label
        s.parent = parent
        s.options = kwargs
        s.wrapper = ""

    """
    Clear todo
    """
    def clearTodo(s):
        if cmds.rowLayout(s.wrapper, ex=True):
            cmds.deleteUI(s.wrapper)

    """
    Build the todo
    """
    def buildTodo(s):
        s.clearTodo()
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

    """
    edit todo
    """
    def editTodo(s):
        s.clearTodo()
        s.wrapper = cmds.rowLayout(nc=2, ad4=0, p=s.parent)
        text = cmds.textField(tx=s.options["realLabel"])
        cmds.button(l="Ok", c=lambda x: s.options["editCallback"](cmds.textField(text, q=True, tx=True)))

    """
    delete the todo
    """
    def deleteTodo(s):
        s.options["deleteCallback"]()
        s.clearTodo()

# kwargs:
# openCallback = run when opening
# closeCallback = run when closing
class TodoSection(object):
    """
    section to place todos
    """
    def __init__(s, label, parent, **kwargs):
        s.label = label
        s.parent = parent
        s.options = kwargs
        s.element = ""

    """
    remove section
    """
    def removeSection(s):
        if cmds.frameLayout(s.element, ex=True):
            cmds.deleteUI(s.element)

    """
    build section
    """
    def buildSection(s, open):
        s.removeSection()
        s.element = cmds.frameLayout(
            l=s.label,
            p=s.parent,
            cll=True,
            cl=open,
            cc=lambda: s.options["closeCallback"](),
            ec=lambda: s.options["openCallback"]()
        )
