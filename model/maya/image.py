# Interface for maya specific images
# Created 01/10/15 Jason Dixon
# http://internetimagery.com

from todo.model.image import Icon

# Override Icons
# Top Button, panel switcher
Icon["panel.settings"] = "attributes.png"
Icon["panel.todo"] = "revealSelected.png"
# Todo entry
Icon["todo.save"] = "fileSave.png"
Icon["todo.edit"] = "setEdEditMode.png"
Icon["todo.delete"] = "removeRenderable.png"
# Todo special entires
Icon["todo.web"] = "SP_ComputerIcon.png"
Icon["todo.file"] = "openScript.png"
# Maya specfic parsers!
Icon["todo.object"] = "selectByObject.png"
Icon["todo.frame"] = "centerCurrentTime.png"
Icon["todo.range"] = "traxFrameRange.png"
