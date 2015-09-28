# Todo / Settings Panel
from todo.view import Element

class TodoPanel(Element):
    """
    Todo panel
    Attributes:
        newtodo     : new todo text box
        scrollbox   : area to place todos
    Events:
        new         : Triggered when a new todo is being requested.
    """
    def _buildGUI(s):
        s.newtext = s.attributes["newtodo"](
            attributes={
                "label"     : "Create a new TODO",
                "annotation": "Type a task into the box."
                },
            events={
                "trigger"   : s.validate
                },
            parent=s.parent
            )
        s.scroll = s.attributes["scrollbox"](
            parent=s.parent
        )
    def validate(s, text):
        print "validate todo"
