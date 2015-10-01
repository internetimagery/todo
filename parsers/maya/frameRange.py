# Pull out frame ranges
# Created 01/10/15 Jason Dixon
# http://internetimagery.com

from todo.parsers.parser import Parser
import maya.cmds as cmds

class Range(Parser):
    def start(s):
        s.icon = "todo.range"
        s.name = "range"
        s.ranges = []
        s.buffer = []
        s.keywords = ["to", "through", "-", ":", "and", "->"] # Names that create a range
    def update(s, token):
        s.buffer.append(token)
        if 3 <= len(s.buffer): # Buffer some tokens
            num1 = s.buffer.pop(0)
            word = s.buffer[0]
            num2 = s.buffer[1]
            if word in s.keywords: # first check for keyword
                try:
                    num1 = int(num1)
                    num2 = int(num2)
                    # We have succeeded in getting a range
                    s.ranges.append(sorted([num1, num2]))
                    s.priority = 3
                    s.description = "Go to frame range: %s" % "".join(["\n* %s - %s" % (r[0], r[1]) for r in s.ranges])
                    s.buffer = [] # flush the buffer
                except ValueError:
                    pass
        return token
    def run(s):
        if s.ranges:
            def setRange(r):
                cmds.playbackOptions(e=True, min=r[0], max=r[1])
            if 1 < len(s.ranges):
                rangeQuery(s.ranges, setRange)
            else:
                setRange(s.ranges[0])

def rangeQuery(ranges, callback):
    """
    Ask user to pick desired range
    """
    def rangePick(r):
        print "Moving timeslider to %s, %s" % (r[0], r[1])
        cmds.deleteUI(window)
        callback(r)
    def addPicker(r):
        cmds.button(
            l="Move timeslider between frames %s and %s." % (r[0], r[1]),
            c=lambda x: rangePick(r)
            )
    window = cmds.window(t="Which range would you like?", rtf=True)
    cmds.columnLayout(adj=True)
    for r in ranges:
        addPicker(r)
    cmds.showWindow(window)
