# Interface for images to be overridden
# Created 01/10/15 Jason Dixon
# http://internetimagery.com

import todo.images as img

# Replace with software specific icons if desired.
Icon = {
    # Top Button, panel switcher
    "panel.settings"  : img.icons["settings_22"],
    "panel.todo"      : img.icons["todo_22"],
    # Todo entry
    "todo.save"       : img.icons["save_16"],
    "todo.edit"       : img.icons["todo_16"],
    "todo.delete"     : img.icons["brush_16"],
    # Todo special entires
    "todo.web"        : img.icons["web_16"],
    "todo.file"       : img.icons["folder_16"]
}
