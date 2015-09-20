# Parsers for Maya

# Default Todo Parsers

from urlparse import urlparse
from os.path import dirname, realpath, join, basename
import maya.cmds as cmds


"""
Website URL
"""
def parseUrl(tokens):
    urls = []
    filteredToken = []
    for token in tokens:
        url = urlparse(token)
        if url.scheme and url.netloc:
            urls.append(token)
            filteredToken.append(url.netloc)
        else:
            filteredToken.append(token)
    return filteredToken, {"Url" : urls}

"""
Frame Range
"""
rangeNames = ["to", "through", "-", ":", "and", "->"] # Names that create a range
def parseRange(tokens):
    ranges = []
    for i, token in enumerate(tokens):
        if token in rangeNames:
            try:
                num1 = int(tokens[i-1])
                num2 = int(tokens[i+1])
                ranges.append(sorted([num1, num2]))
            except ValueError:
                print "Value Error"
    return tokens, {"Range" : ranges}

"""
Single Frame
"""
def parseFrame(tokens):
    frames = []
    for token in tokens:
        try:
            frames.append(int(token))
        except ValueError:
            pass
    return tokens, {"Frame" : frames}

"""
File
"""
def parseFile(tokens):
    files = []
    filteredToken = []
    filename = cmds.file(q=True, sn=True)
    for token in tokens:
        if "/" in token:
            root = dirname(filename) if filename else ""
            path = realpath(join(root, token))
            if isfile(path):
                files.append(path)
            filteredToken.append(basename(path))
        else:
            filteredToken.append(token)
    return filteredToken, {"File" : files}

"""
Object Parse
"""
def parseObject(tokens):
    objs = []
    for token in tokens:
        obj = cmds.ls(token, r=True)
        if obj:
            objs += obj
    return tokens, {"Object" : objs}

# Send back parsers
def export():
    return [
        parseFrame,
        parseRange,
        parseUrl,
        parseObject,
        parseFile
    ]
