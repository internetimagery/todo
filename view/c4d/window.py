# Main window
import c4d
from c4d import gui

class Window(gui.GeDialog):

    def __init__(s, requestSettingsPage, requestTodoPage):
        s.elements = {} # Keep track of elements and their associative functions
        s.requestSettingsPage = requestSettingsPage # Callback to get settings built
        s.requestTodoPage = requestTodoPage # Callback to get todos information
        s.todoIds = [] # Store the ids of Todos, to free them up
        s.lastDoc = None # Previous document, to detect scene change
        gui.GeDialog.__init__(s)

    def Open(s):
        gui.GeDialog.Open(
            s,
            dlgtype=c4d.DLG_TYPE_ASYNC,
            defaultw=500,
            defaulth=500
            )

    def CreateLayout(s):
        s.SetTitle("Todo window")
        s.TabGroupBegin(
            id=s.getId(),
            flags=c4d.BFH_SCALEFIT|c4d.BFV_SCALEFIT
            )
        s.buildTodoPage(**s.requestTodoPage())
        s.buildSettingsPage(**s.requestSettingsPage())
        s.GroupEnd()
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
                print "Scene Changed!"
                s.lastDoc = identifier
        return True

    def buildTodoPage(s, buttonName="Default", pageName="Default", newTodo=None, buildTodo=None):
        """
        Build the todo page
        newTodo = callback when new todo is requested
        buildTodo = call to build out todo list based on given information dict
        """
        s.GroupBegin( # Open Page
            id=s.getId(),
            flags=c4d.BFH_SCALEFIT|c4d.BFV_SCALEFIT,
            cols=1,
            title=pageName,
            groupflags=c4d.BFV_CMD_EQUALCOLUMNS
            )
        textfield = s.getId()
        s.AddEditText(
            id=textfield,
            flags=c4d.BFH_SCALEFIT,
        )
        button = s.getId()
        s.AddButton(
            id=button,
            flags=c4d.BFH_SCALEFIT,
            name=buttonName
            )
        s.AddSeparatorH(c4d.BFH_SCALEFIT)
        s.ScrollGroupBegin( # Open Scroll
            id=s.getId(),
            flags=c4d.BFH_SCALEFIT|c4d.BFV_SCALEFIT,
            scrollflags=c4d.SCROLLGROUP_VERT
            )
        s.todolist = s.getId()
        s.GroupBegin( # Open Dummy
            id=s.todolist,
            flags=c4d.BFH_FIT|c4d.BFV_TOP,
            cols=1
            )
        # EMPTY SPACE FOR TODOS TO BE PLACED
        s.GroupEnd() # Close Dummy
        s.GroupEnd() # Close Scroll
        s.GroupEnd() # Close Page
        def new(id):
            if newTodo:
                if newTodo(s.GetString(textfield)):
                    s.SetString(textfield, "") # Reset todo field if successful
            else:
                print "MISSING newTodo Callback!!"
        s.bind(button, new)
        s.buildTodos()

    def buildTodos(s):
        """
        Insert and refesh the todos
        """
        todos = range(10)
        if s.todoIds:
            for id in s.todoIds:
                s.unbind(id)
        s.LayoutFlushGroup(id=s.todolist) # Empty the todo list!!



        bmpbutton = c4d.BaseContainer()
        bmpbutton.SetBool(c4d.BITMAPBUTTON_BUTTON, True)
        bmpbutton.SetString(c4d.BITMAPBUTTON_TOOLTIP, "Remove this Task")
        bmpbutton.SetLong(c4d.BITMAPBUTTON_ICONID1, c4d.RESOURCEIMAGE_CLEARSELECTION)
        s.AddCustomGui(
            s.getId(),
            c4d.CUSTOMGUI_BITMAPBUTTON, name="", flags=0, minw=0,
            minh=0, customdata=bmpbutton)


        if todos:
            def add(todo):
                def completeFunc(id):
                    print "Completed Todo!"
                def editFunc(id):
                    print "Pressed edit"
                def deleteFunc(id):
                    print "Pressed Delete"
                group = s.getId()
                taskBtn = s.getId()
                editBtn = s.getId()
                delBtn = s.getId()
                s.GroupBegin( # Open Todo
                    id=group,
                    flags=c4d.BFH_SCALEFIT,
                    cols=3
                    )
                s.AddButton(
                    id=taskBtn,
                    flags=c4d.BFH_SCALEFIT,
                    name="Todo Number %s" % todo
                    )
                s.AddButton(
                    id=editBtn,
                    flags=0,
                    name="EDIT"
                    )
                s.AddButton(
                    id=delBtn,
                    flags=0,
                    name="DEL"
                    )
                s.GroupEnd() # Close todo
                s.todoIds.append(taskBtn)
                s.todoIds.append(editBtn)
                s.todoIds.append(delBtn)
                s.bind(taskBtn, completeFunc)
                s.bind(editBtn, editFunc)
                s.bind(delBtn, deleteFunc)
            for todo in todos:
                add(todo)
        s.GroupEnd() # Close Dummy
        s.LayoutChanged(id=s.todolist)

    def buildSettingsPage(s):
        """
        Build the todo page
        """
        s.GroupBegin( # Open Page
            id=s.getId(),
            flags=c4d.BFH_SCALEFIT|c4d.BFV_SCALEFIT,
            cols=1,
            title="Settings",
            groupflags=c4d.BFV_CMD_EQUALCOLUMNS
            )
        s.AddButton(1013, c4d.BFV_MASK, initw=145, name="INSERT SETTINGS IN HERE LATER")
        s.GroupEnd() # Close Page



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
    # TEST THE WINDOW
    def infoTodo(): # fill in the information and give it to the GUI
        return {
            "buttonName"  : "Create a new TODO",
            "pageName"    : "Tasks",
            "newTodo"     : newTodo # Callback
        }
    def buildTodo(): # Build out todos
        pass

    def newTodo(text):
        text = text.strip()
        if text:
            print "New Todo Text:", text
            return True

    w = Window(
        lambda: {},
        infoTodo
    )
    w.Open()
