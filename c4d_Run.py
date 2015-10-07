# Allow for imports
import sys
import os.path
sys.path.append(os.path.realpath(os.path.dirname(os.path.dirname(__file__))))

from todo.quotes import quotes

class Main(object):
    def __init__(s, view):
        s.view = view
        s.data = {}
        s.window = view.window(
            "TITLE OMG",
            s.sendSettingsPageInfo, # triggered on page creation
            s.sendTodoPageInfo, # triggered on page creation
            s.resetData # triggered on scene refresh
        )
        s.window.Open() # Display the window

    def sendSettingsPageInfo(s, recieved):
        return {}

    def sendTodoPageInfo(s, recieved):
        s.buildTodo = recieved["buildTodos"] # Recieve our controls
        return { # Send our info
            "sendNew"        : s.todoNew,
            "sendEdit"       : s.todoEdit,
            "sendDelete"     : s.todoDelete,
            "sendSpecial"    : s.todoSpecial,
            "sendComplete"   : s.todoComplete,
            "newBtnName"     : "Create a new TODO",
            "pageBtnName"    : "Settings ->",
            "requestBuild"   : s.refreshTodo
        }

    def resetData(s):
        """
        Gather all data from the scene
        """
        print "Reset requested"

    def refreshTodo(s):
        """
        Build the Todo List, or Refresh it when changes are made.
        """
        todos = {} # Build out todo structure
        s.buildTodo(todos)

    def todoNew(s, text):
        """
        New Todo requested.
        """
        text = text.strip()
        if text:
            print "Creating:", text
            s.refreshTodo()
            return True

    def todoEdit(s, text):
        """
        Todo edit requested
        """
        text = text.strip()
        if text:
            print "Editing todo", text
            s.refreshTodo()

    def todoDelete(s):
        """
        Todo deletion requested
        """
        print "Delete todo"
        s.refreshTodo()

    def todoSpecial(s):
        """
        Todo special requested
        """
        print "Trigger special todo function"

    def todoComplete(s):
        """
        Todo Completion requested.
        """
        print "Todo completed!"
        s.todoDelete()

if __name__ == '__main__':
    import todo.view.c4d as view
    Main(view)
