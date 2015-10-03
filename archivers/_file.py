# File archive. Store off info into a folder
# Created 02/10/15 Jason Dixon
# http://internetimagery.com

import archive
import os.path
import zipfile
import time
import os

class File(archive.Archive):
    def start(s):
        s.settingName = "setting.file"
        s.settingFileName = "setting.file.files"
    def set(s, k, v):
        s.data[k] = v
    def buildSettings(s, parent):
        s.files = set(s.data.get(s.settingFileName, []))
        s.section = s.view.CheckSection(
            attributes={
                "checked"   : s.data.get(s.settingName, False),
                "label"     : "File Archive",
                "annotation": "Store a backup of the current scene into the provided folder upon each Todo completion."
            },
            events={
                "change"    : lambda x: s.set(s.settingName, x.checked)
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
            project = s.model.File.project()
            path = s.relativePath(path, project)
            s.files.add(path)
            s.data[s.settingFileName] = list(s.files)
            s.buildFiles()

    def removeFile(s, path, element):
        if path in s.files:
            s.files.remove(path)
            s.data = [s.settingFileName] = list(s.files)
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

    def absolutePath(s, path, root):
        """
        Taken relative path return a workable absolute path
        """
        root = s.model.File.project()
        return os.path.realpath(os.path.join(root, path))

    def relativePath(s, path, root):
        """
        Take an absolute path, return a relative path if in project
        """
        try:
            rPath = os.path.relpath(path, root)
        except ValueError: # On windows, the path is on another drive?
            rPath = path
        return s.absolutePath(path).replace("\\", "/") if rPath[:2] == ".." else rPath.replace("\\", "/")

    def runArchive(s, todo, filename):
        active = s.data.get(s.settingName, False)
        target = os.path.realpath(filename)
        if active and os.path.isfile(target):
            paths = s.data.get(s.settingFileName, [])
            if paths:
                basename = os.path.basename(target)
                whitelist = [" ", ".", "_", "@"]  # Strip invalid characters
                label = "".join(ch for ch in todo.label if ch.isalnum() or ch in whitelist).rstrip()
                name = "%s_%s_%s.zip" % (os.path.splitext(basename)[0], int(time.time() * 100), label)
                project = s.model.File.project()
                for path in paths:
                    folder = s.absolutePath(path, project)
                    if os.path.isdir(folder):
                        dest = os.path.join(path, name)
                        z = zipfile.ZipFile(dest, "w")
                        z.write(target, basename)
                        z.close()
