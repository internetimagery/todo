# Git archive. Store file in git and commit with the option to push
# Created 02/10/15 Jason Dixon
# http://internetimagery.com

import subprocess as sub
import maya.cmds as cmds
import archive
import os.path
import os

class Git(archive.Archive):
    def start(s):
        s.settingName = "setting.git"
        s.settingPushName = "setting.git.push"
        s.settingPushUrlName = "setting.git.push.url"
    def set(s, key, val):
        s.data[key] = val
    def buildSettings(s, parent):
        # Check if git is loaded.
        if not _version_[1]:
            s.section = s.view.CheckSection(
                attributes={
                    "checked"   : s.data.get(s.settingName, False),
                    "label"     : "Git Archive (experimental)",
                    "annotation": "Commit the Maya file into Git (if the file is located in a valid repo) upon each Todo task completion."
                },
                events={
                    "change"    : lambda x: s.set(s.settingName, x.checked)
                },
                parent=parent
            )
            s.view.Text(
                attributes={
                    "text"  : "%s found." % _version_[0].capitalize().replace("\n", ""),
                    "align" : "left"
                },
                parent=s.section
            )
            push = s.view.CheckSection(
                attributes={
                    "checked"   : s.data.get(s.settingPushName, False),
                    "label"     : "Automatically PUSH commits.",
                    "annotation": "Commit the Maya file into Git (if the file is located in a valid repo) upon each Todo task completion."
                },
                events={
                    "change"    : lambda x: s.set(s.settingPushName, x.checked)
                },
                parent=s.section
            )
            s.view.Text(
                attributes={
                    "text"      : "Enter remote branch name:",
                    "align"     : "left"
                },
                parent=push
            )
            btn1 = s.view.Button(
                attributes={
                    "label"     : s.data.get(s.settingPushUrlName, "Click to enter a Branch Name"),
                    "annotation": "Click to enter a Branch name.",
                    "image"     : s.model.Icon["settings.git.push"]
                },
                events={
                    "pressed"   : lambda x: s.switchButtons(btn1, btn2)
                },
                parent=push
            )
            btn2 = s.view.TodoEdit(
                attributes={
                    "text"      : s.data.get(s.settingPushUrlName, ""),
                    "label"     : "Update"
                },
                events={
                    "edit"      : lambda x: s.switchButtons(btn1, btn2)
                },
                parent=push
            )
            btn2.visible = False
    def switchButtons(s, btn1, btn2):
        vis1 = btn1.visible
        vis2 = btn2.visible
        if vis1:
            btn1.visible = False
            btn2.visible = True
            btn2.text = s.data.get(s.settingPushUrlName, "")
        else:
            btn1.visible = True
            btn2.visible = False
            text = btn2.text
            s.set(s.settingPushUrlName, text)
            btn1.label = text if text else "Click to enter a Branch Name"

    def runArchive(s, todo, filename):
        path = os.path.realpath(filename)
        if s.data.get(s.settingName, False) and os.path.isfile(path):
            check = GitInterface().status(path)
            if check[1]:
                print "Cannot commit file: %s." % check[1]
            else:
                if GitInterface().commit(path, todo.label) and s.data.get(s.settingPushName, ""):
                    print "Pushing update"
                    push = s.data.get(s.settingPushUrlName, "")
                    pushed = GitInterface().push(path, push)
                    print pushed[1] if pushed[1] else pushed[0]

class GitInterface(object):
    """
    Control Git
    """
    def __init__(s, *args, **kwargs):
        if args or kwargs:
            return s._git(*args, **kwargs)

    def _git(s, *args, **kwargs):
        """
        git command line function
        """
        try:
            return sub.Popen(["git"] + list(args), stdout=sub.PIPE, stderr=sub.PIPE, **kwargs).communicate()
        except OSError as e:
            return ("", e.__str__())

    def push(s, path, dest):
        return s._git("push", dest, cwd=os.path.dirname(path))

    def commit(s, path, comment):
        if not s._git("add", os.path.basename(path), cwd=os.path.dirname(path))[1]:
            if not s._git("commit", "--quiet", "--message", comment, "--only", os.path.basename(path), cwd=os.path.dirname(path))[1]:
                print "File committed"
                return True

    def status(s, path):
        return s._git("status", "--porcelain", os.path.basename(path), cwd=os.path.dirname(path))

    def version(s):
        return s._git("--version")

# Check for Git
_version_ = GitInterface().version()
if _version_[1]:
    print "Git not found. Skipping."
