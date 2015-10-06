# Allow for imports
import sys
import os.path
sys.path.append(os.path.realpath(os.path.dirname(__file__)))


class Main(object):
    def __init__(s, view):
        s.view = view
        s.data = {}
        s.window = view.window(
            s.sendSettingsPageInfo, # triggered on page creation
            s.sendTodoPageInfo, # triggered on page creation
            s.resetData # triggered on scene refresh
        )
        s.window.Open() # Display the window

    def sendSettingsPageInfo():
        return {}
    def sendTodoPageInfo():
        return {
            "newBtn"  : "Create a new TODO",
            "pageBtn"    : "Settings ->",
            "newTodo"     : s.createTodo # Callback
        }
    def resetData():
        print "Reset requested"

    def createTodo(text):
        text = text.strip()
        if text:
            print "Creating:", text
            return True

if __name__ == '__main__':
    import view.c4d as view
    main(view)
