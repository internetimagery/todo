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
        print "Reset requested"

    def refreshTodo(s):
        s.buildTodo()

    def todoNew(s, text):
        text = text.strip()
        if text:
            print "Creating:", text
            return True

    def todoEdit(s, text):
        print "Editing todo", text
    def todoDelete(s):
        print "Delete todo"
    def todoSpecial(s):
        print "Trigger special todo function"
    def todoComplete(s):
        print "Todo completed!"

if __name__ == '__main__':
    import todo.view.c4d as view
    Main(view)
