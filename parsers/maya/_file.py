# Parse out a filename and return a function that opens it.
# Created 01/10/15 Jason Dixon
# http://internetimagery.com

from todo.parsers.parser import Parser
from todo.images import icon
import maya.cmds as cmds
import os.path

class File(Parser):
    def start(s):
        s.description = "No files to open."
        s.icon = icon.get("folder_16")
        s.name = "file"
        s.priority = 0 # Set at 0 and replace if token found
        s.files = set()
        filename = cmds.file(q=True, sn=True)
        s.root = os.path.dirname(filename) if filename else ""
    def update(s, token):
        if "/" in token:
            path = os.path.realpath(os.path.join(s.root, token))
            if os.path.isfile(path):
                s.files.add(path)
                s.description = "Open the files: %s" % ", ".join(s.files)
                s.priority += 2 # Higher priority if more files found
                return os.path.basename(path)
        return token
    def run(s):
        print "DO THE FILE THING"
