# Parse out files and return a function that opens thems.
# Created 01/10/15 Jason Dixon
# http://internetimagery.com

from todo.parsers.parser import Parser
import webbrowser
import subprocess
import os.path
import sys
import os

class File(Parser):
    def start(s):
        s.description = "No files to open."
        s.icon = "todo.file"
        s.name = "file"
        s.files = set()
        filename = s.model.File._FILE_Running()
        s.root = os.path.dirname(filename) if filename else ""
    def update(s, token):
        if "/" in token:
            path = os.path.realpath(os.path.join(s.root, token))
            if os.path.exists(path):
                s.files.add(path)
                if 1 < len(s.files):
                    s.description = "Open files:" + "\n- ".join(["\n* %s" % f for f in s.files])
                else:
                    s.description = "Open file: %s" % list(s.files)[0]
                s.priority += 2 # Higher priority if more files found
                return os.path.basename(path)
        return token
    def run(s):
        if s.files:
            for f in s.files:
                s.model.File.load(f)
