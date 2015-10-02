# File archive. Store off info into a folder
# Created 02/10/15 Jason Dixon
# http://internetimagery.com

import archive
import os.path

class File(archive.Archive):
    def start(s):
        s.settingName = "setting.file"
        s.settingFileName = "setting.file.files"
    def buildSettings(s, parent):
        s.files = set(s.settings.get(s.settingFileName, []))
        s.section = s.view.CheckSection(
            attributes={
                "checked"   : s.settings.get(s.settingName, False),
                "label"     : "File Archive",
                "annotation": "Store a backup of the current scene into the provided folder upon each Todo completion."
            },
            events={
                "change"    : lambda x: s.settings.set(s.settingName, x.checked)
            },
            parent=parent
        )
        s.view.Button(
            attributes={
                "label"     : "Pick archive folder.",
                "image"     : s.model.Icon["settings.file"],
                "annotation": "Pick archive folder."
            },
            events={
                "pressed"   : s.setFile
            },
            parent=s.section
        )
        s.wrapperOuter = s.view.HorizontalLayout(
            parent=s.section
        )
        s.wrapperInner = None
        s.buildFiles()

    def setFile(s, element):
        path = s.model.File.dialog(True)
        if path:
            path = s.relativePath(path)
            s.files.add(path)
            s.settings.set(s.settingFileName, list(s.files))
            s.buildFiles()

    def removeFile(s, path, element):
        if path in s.files:
            s.files.remove(path)
            s.settings.set(s.settingFileName, list(s.files))
            element.delete()

    def buildFiles(s):
        if s.wrapperInner:
            s.wrapperInner.delete()
        s.wrapperInner = s.view.HorizontalLayout(
            parent=s.wrapperOuter
        )
        def addFile(f):
            s.view.Button(
                attributes={
                    "label"     : f,# s.absolutePath(f),
                    "annotation": "Click to remove",
                    "image"     : s.model.Icon["settings.filepath"]
                },
                events={
                    "pressed"   : lambda x: s.removeFile(f, x)
                },
                parent=s.wrapperInner
            )
        for f in s.files:
            addFile(f)

    def absolutePath(s, path):
        """
        Taken relative path return a workable absolute path
        """
        root = s.model.File.project()
        return os.path.realpath(os.path.join(root, path))

    def relativePath(s, path):
        """
        Take an absolute path, return a relative path if in project
        """
        root = s.model.File.project()
        try:
            rPath = os.path.relpath(path, root)
        except ValueError: # On windows, the path is on another drive?
            rPath = path
        return s.absolutePath(path).replace("\\", "/") if rPath[:2] == ".." else rPath.replace("\\", "/")
