# Filter todo for its possible parts

from os.path import dirname, realpath, join, isfile, basename
from urlparse import urlparse
import maya.cmds as cmds
from shlex import split

# FILTERS
# Return text unless it is to be removed
# Return name of token if one is found, and corresponding info
temp = {} # Temp variable to hold info if needed
temp["hashtag"] = set()
def parseHashTag(i, token, fileName):
    if 1 < len(token) and token[:1] == "#":
        temp["hashtag"].add(token[1:])
        return "", ("Hashtag", temp["hashtag"])
    return token, None

temp["url"] = set()
def parseUrl(i, token, fileName):
    url = urlparse(token)
    if url.scheme and url.netloc:
        temp["url"].add(token)
        return url.netloc, ("Url", temp["url"])
    return token, None

temp["file"] = set()
def parseFilePath(i, token, fileName):
    if "/" in token:
        root = dirname(fileName) if fileName else ""
        path = realpath(join(root, token))
        if isfile(path):
            temp["file"].add(path)
            return basename(token), ("File", temp["file"])
    return token, None

temp["framerange"] = []
rangeNames = ["to", "through", "-", ":", "and", "->"] # Names that create a range
def parseFrame(i, token, fileName):
    try:
        num = int(token)
    except ValueError:
        num = None
    size = len(temp["framerange"])
    if size == 0:
        if num is not None:
            temp["framerange"].append(num)
            return token, ("Frame", num)
    elif size == 1:
        if num is not None and temp["framerange"][0] is not num:
            r = sorted([temp["framerange"][0], num])
            temp["framerange"] = []
            return token, ("FrameRange", r)
        elif token in rangeNames:
            temp["framerange"].append(token)
        else:
            temp["framerange"] = []
    elif size == 2:
        if num is not None and temp["framerange"][0] is not num:
            r = sorted([temp["framerange"][0], num])
            temp["framerange"] = []
            return token, ("FrameRange", r)
        else:
            temp["framerange"] = []
    else:
        temp["framerange"] = []
    return token, None

temp["obj"] = []
def parseObjects(i, token, fileName):
    try:
        selection = cmds.ls(token, r=True)
        if selection:
            temp["obj"] += selection
            return token, ("Object", temp["obj"])
    except RuntimeError:
        pass
    return token, None

# A Single Todo
class Todo(object):
    """
    A single Todo
    """
    parsers = [ # Parsers
        parseHashTag, # Hashtag : "#hash"
        parseUrl, # urls : "http://thing.com"
        parseFilePath, # relative / absolute path : "./place"
        parseFrame, # grab numbers as possible frame numbers
        parseObjects # Check objects in maya scene
    ]
    def __init__(s, todoName, fileName):
        s.todoName = todoName.strip() # Original name of todo
        s.fileName = fileName # Name of current scene file
        s.label = "" # Name after parsing
        s.tokens = {} # Tokens if any
        s.parse()

    """
    Parse out the todo, and decide if there is anything special written inside it.
    """
    def parse(s):
        if s.todoName:
            tokens = split(s.todoName)
            filtered = []
            for i, token in enumerate(tokens):
                for parser in s.parsers:
                    if token:
                        token, extra = parser(i, token, s.fileName)
                        if extra:
                            tokenName, tokenArgs = extra
                            s.tokens[tokenName] = tokenArgs
                if token:
                    filtered.append(token)

            s.label = " ".join(filtered)
