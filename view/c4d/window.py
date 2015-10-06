# Main window
import c4d
from c4d import gui

class Window(gui.GeDialog):

    def __init__(s, title, requestSettingsPage, requestTodoPage, requestReset):
        s.title = title
        s.elements = {} # Keep track of elements and their associative functions
        s.requestSettingsPage = requestSettingsPage # Callback to get settings built
        s.requestTodoPage = requestTodoPage # Callback to get todos information
        s.requestReset = requestReset # Callback when scene changes asking for a data reset
        s.todoIds = [] # Store the ids of Todos, to free them up
        s.panelIds = [] # Store ids for each panel
        s.lastDoc = None # Previous document, to detect scene change
        s.CoreMessage(c4d.EVMSG_DOCUMENTRECALCULATED, None) # Trigger first refresh
        gui.GeDialog.__init__(s)

    def Open(s):
        gui.GeDialog.Open(
            s,
            dlgtype=c4d.DLG_TYPE_ASYNC,
            defaultw=500,
            defaulth=500
            )

    def CreateLayout(s):
        s.SetTitle(s.title)
        s.wrapper = s.getId()
        s.GroupBegin( # Open Page
            id=s.wrapper,
            flags=c4d.BFH_SCALEFIT|c4d.BFV_SCALEFIT,
            cols=1
            )
        s.GroupEnd()
        s.buildTodoPage(s.requestTodoPage({"buildTodos" : s.buildTodos}))
        return True

    def Command(s, id, msg):
        if id in s.elements and s.elements[id]:
            s.elements[id](id)
        return True

    def CoreMessage(s, id, msg):
        if id == c4d.EVMSG_DOCUMENTRECALCULATED: # Scene redrawn
            current = c4d.documents.GetActiveDocument()
            currName = current.GetDocumentName()
            currPath = current.GetDocumentPath()
            identifier = "%s:%s" % (
                currName,
                currPath if currPath else ""
                )
            if s.lastDoc != identifier:
                s.lastDoc = identifier
                s.requestReset()
        return True

    def buildTodoPage(s, ctrls):
        """
        Build the todo page
        newTodo = callback when new todo is requested
        buildTodo = call to build out todo list based on given information dict
        """
        s.ctrls = ctrls # Store our latest controls
        if s.panelIds:
            for id in s.panelIds:
                s.unbind(id)
        s.LayoutFlushGroup(id=s.wrapper) # Empty the panel
        s.GroupBegin( # Open Page
            id=0,
            flags=c4d.BFH_SCALEFIT|c4d.BFV_SCALEFIT,
            cols=1,
            groupflags=c4d.BFV_CMD_EQUALCOLUMNS
            )
        pageBtn = s.getId()
        s.panelIds.append(pageBtn)
        s.AddButton(
            id=pageBtn,
            flags=c4d.BFH_RIGHT,
            name=ctrls["pageBtnName"]
            )
        s.bind(pageBtn, lambda x: s.buildSettingsPage(s.requestSettingsPage({})))
        textfield = s.getId()
        s.panelIds.append(textfield)
        s.AddEditText(
            id=textfield,
            flags=c4d.BFH_SCALEFIT,
        )
        button = s.getId()
        s.panelIds.append(button)
        s.AddButton(
            id=button,
            flags=c4d.BFH_SCALEFIT,
            name=ctrls["newBtnName"]
            )
        s.bind(button, lambda x: s.SetString(textfield, "") if ctrls["sendNew"](s.GetString(textfield)) else None)
        s.AddSeparatorH(c4d.BFH_SCALEFIT)
        s.ScrollGroupBegin( # Open Scroll
            id=0,
            flags=c4d.BFH_SCALEFIT|c4d.BFV_SCALEFIT,
            scrollflags=c4d.SCROLLGROUP_VERT
            )
        s.todolist = s.getId()
        s.panelIds.append(s.todolist)
        s.GroupBegin( # Open Dummy
            id=s.todolist,
            flags=c4d.BFH_FIT|c4d.BFV_TOP,
            cols=1
            )
        # EMPTY SPACE FOR TODOS TO BE PLACED
        s.GroupEnd() # Close Dummy
        s.GroupEnd() # Close Scroll
        s.GroupEnd() # Close Page
        s.LayoutChanged(id=s.wrapper)
        ctrls["requestBuild"]()

    def buildTodos(s, todos):
        """
        Insert and refesh the todos
        """
        todos = range(10)
        if s.todoIds:
            for id in s.todoIds:
                s.unbind(id)
        s.LayoutFlushGroup(id=s.todolist) # Empty the todo list!!
        if todos:
            def add(todo):
                def completeFunc(id):
                    s.ctrls["sendComplete"]()
                def specialFunc(id):
                    s.ctrls["sendSpecial"]()
                def editFunc(id):
                    s.LayoutFlushGroup(id=group)
                    textfield = s.getId()
                    s.panelIds.append(textfield)
                    s.AddEditText(
                        id=textfield,
                        flags=c4d.BFH_SCALEFIT,
                    )
                    editText = s.getId()
                    s.panelIds.append(editText)
                    s.AddButton(
                        id=editText,
                        flags=0,
                        name="Update"
                        )
                    s.LayoutChanged(id=group)
                    s.bind(editText, lambda x: s.ctrls["sendEdit"](s.GetString(textfield)))
                def deleteFunc(id):
                    s.ctrls["sendDelete"]()
                group = s.getId()
                s.GroupBegin( # Open Todo
                    id=group,
                    flags=c4d.BFH_SCALEFIT,
                    cols=4
                    )
                taskBtn = s.getId()
                s.todoIds.append(taskBtn)
                s.AddButton(
                    id=taskBtn,
                    flags=c4d.BFH_SCALEFIT,
                    name="Todo Number %s" % todo
                    )
                s.bind(taskBtn, completeFunc)
                if todo == 3:
                    specialBtn = s.buildImageButton(
                        c4d.RESOURCEIMAGE_OBJECTMANAGER_DISP2,
                        "Special Button"
                    )
                    s.todoIds.append(specialBtn)
                    s.bind(specialBtn, specialFunc)
                editBtn = s.buildImageButton(
                    c4d.RESOURCEIMAGE_BROWSER_CATALOG,
                    "Edit the task"
                )
                s.todoIds.append(editBtn)
                s.bind(editBtn, editFunc)
                delBtn = s.buildImageButton(
                    c4d.RESOURCEIMAGE_CLEARSELECTION,
                    "Remove the task without saving."
                )
                s.todoIds.append(delBtn)
                s.bind(delBtn, deleteFunc)
                s.GroupEnd() # Close todo
            for todo in todos:
                add(todo)
        s.GroupEnd() # Close Dummy
        s.LayoutChanged(id=s.todolist)

    def buildSettingsPage(s, ctrls):
        """
        Build the todo page
        """
        s.ctrls = ctrls # Store our latest controls
        if s.panelIds:
            for id in s.panelIds:
                s.unbind(id)
        s.LayoutFlushGroup(id=s.wrapper) # Empty the panel
        s.GroupBegin( # Open Page
            id=s.getId(),
            flags=c4d.BFH_SCALEFIT|c4d.BFV_SCALEFIT,
            cols=1,
            title="Settings",
            groupflags=c4d.BFV_CMD_EQUALCOLUMNS
            )
        pageBtn = s.getId()
        s.panelIds.append(pageBtn)
        s.AddButton(
            id=pageBtn,
            flags=c4d.BFH_LEFT,
            name="<- Tasks"
            )
        s.AddSeparatorH(c4d.BFH_SCALEFIT)
        s.AddStaticText(
            0,
            c4d.BFH_CENTER,
            name="Settings are Scene Independant."
        )
        s.AddSeparatorH(c4d.BFH_SCALEFIT)
        s.bind(pageBtn, lambda x: s.buildTodoPage(s.requestTodoPage({"buildTodos" : s.buildTodos})))
        s.AddButton(1013, c4d.BFV_MASK, initw=145, name="INSERT SETTINGS IN HERE LATER")
        s.GroupEnd() # Close Page
        s.LayoutChanged(id=s.wrapper)

    def buildImageButton(s, image, text):
        bmpbutton = c4d.BaseContainer()
        bmpbutton.SetBool(c4d.BITMAPBUTTON_BUTTON, True)
        bmpbutton.SetString(c4d.BITMAPBUTTON_TOOLTIP, text)
        bmpbutton.SetLong(c4d.BITMAPBUTTON_ICONID1, image)
        id = s.getId()
        s.AddCustomGui(
            id,
            c4d.CUSTOMGUI_BITMAPBUTTON,
            name="",
            flags=0,
            minw=0,
            minh=0,
            customdata=bmpbutton
            )
        return id

    def getId(s):
        start = 1050
        ids = s.elements.keys()
        while True:
            if start not in ids:
                s.elements[start] = None
                return start
            start += 1

    def bind(s, id, function):
        s.elements[id] = function

    def unbind(s, id):
        if id in s.elements:
            del s.elements[id]

if __name__ == '__main__':
    pass
    # TEST THE WINDOW
    # def resetScene():
    #     print "Scene changed. Need to load more info"
    # def infoTodo(): # fill in the information and give it to the GUI
    #     return {
    #         "newBtnName"  : "Create a new TODO",
    #         "pageBtnName"    : "Settings ->",
    #         "newTodo"     : newTodo # Callback
    #     }
    # def buildTodo(): # Build out todos
    #     pass
    #
    # def newTodo(text):
    #     text = text.strip()
    #     if text:
    #         print "New Todo Text:", text
    #         return True
    #
    # w = Window(
    #     "Todo window",
    #     lambda: {},
    #     infoTodo,
    #     resetScene
    # )
    # w.Open()
