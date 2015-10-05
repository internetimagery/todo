# Interface for maya specific images
# Created 01/10/15 Jason Dixon
# http://internetimagery.com

from todo.model.image import icon

# Override Icons
# Top Button, panel switcher
icon["panel.settings"] = "attributes.png"
icon["panel.todo"] = "revealSelected.png"
# Todo entry
icon["todo.save"] = "fileSave.png"
icon["todo.edit"] = "setEdEditMode.png"
icon["todo.delete"] = "removeRenderable.png"
# Todo special entires
icon["todo.web"] = "SP_ComputerIcon.png"
icon["todo.file"] = "openScript.png"
# Settings
icon["settings.file"] = "fileOpen.png"
icon["settings.filepath"] = "removeRenderable.png"
icon["settings.git.push"] = "createContainer.png"
# Maya specfic parsers!
icon["todo.object"] = "selectByObject.png"
icon["todo.frame"] = "centerCurrentTime.png"
icon["todo.range"] = "traxFrameRange.png"

Image = icon
