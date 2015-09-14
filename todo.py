# Filter todo for its possible parts

from urlparse import urlparse
from os.path import dirname, realpath, join, isfile, basename
from shlex import split

# FILTERS
# Return text unless it is to be removed
# Return name of token if one is found, and corresponding info

def parseHashTag(i, token, fileName):
    if 1 < len(token) and token[:1] == "#":
        return "", ("Hashtag", [token[1:]])
    return token, None

def parseUrl(i, token, fileName):
    url = urlparse(token)
    if url.scheme and url.netloc:
        return url.netloc, ("Url", [token])
    return token, None

def parseFilePath(i, token, fileName):
    if "/" in token:
        root = dirname(fileName) if fileName else ""
        path = realpath(join(root, token))
        if isfile(path):
            return basename(token), ("File", [path])
    return token, None

# A Single Todo
class Todo(object):
    """
    A single Todo
    """
    parsers = [ # Parsers
        parseHashTag, # Hashtag : "#hash"
        parseUrl, # urls : "http://thing.com"
        parseFilePath # relative / absolute path : "./place"
    ]
    def __init__(s, todoName, fileName):
        s.todoName = todoName.strip() # Original name of todo
        s.fileName = fileName # Name of current scene file
        s.label = "" # Name after parsing
        s.tokens = {} # Tokens if any
        s.parse()
        print s.tokens
        print s.label

    """
    Parse out the todo, and decide if there is anything special written inside it.
    """
    def parse(s):
        if s.todoName:
            tokens = split(s.todoName)
            filtered = []
            for i, token in enumerate(tokens):
                for parser in s.parsers:
                    token, extra = parser(i, token, s.fileName)
                    if extra:
                        tokenName, tokenArgs = extra
                        s.tokens[tokenName] = tokenArgs
                if token:
                    filtered.append(token)

            s.label = " ".join(filtered)

import maya.cmds as cmds
f = cmds.file(q=True, sn=True)
Todo("#home ./test.ma /basename/place\ thing -stuff http://internetimagery.com/thing", f)

    # def _parseTodo(s, label, **kwargs):
    #     """
    #     Parse out metadata from Todo
    #     """
    #     def build_reg():

    #         frr = "(?:(?P<range1>\d+)\s*(?:[^\d\s]|to|and|through)\s*(?P<range2>\d+))"  # Frame range
    #         fr = "(?P<frame>\d+)"  # Frame
    #         reg += "(?:%s|%s)?" % (frr, fr)
    #         reg += "(?P<file>(?:[a-zA-Z]:|\\.{1,2})?[^\t\r\n:|]+\.\w+)?"  # Filename?
    #         return re.compile(reg)
    #
    #     s.regex["label"] = s.regex.get("label", build_reg())
    #     parse = s.regex["label"].finditer(label)
    #     result = kwargs  # Add extra additional custom arguments
    #     result["token"] = ""
    #     result["hashtag"] = []
    #     result["url"] = ""
    #     result["file"] = ""  # Default
    #     result["frame"] = None
    #     result["framerange"] = []
    #     replace = {}  # Make the output nicer by removing certain tags
    #     if parse:
    #         for p in parse:
    #             m = p.groupdict()
    #             if m["token"]:  # Match tokens
    #                 result["token"] = m["token"]
    #                 replace[m["token"] + ":"] = ""
    #             if m["hashtag"]:  # Grab all hashtags, avoiding duplicates
    #                 if m["hashtag"] not in result["hashtag"]:
    #                     result["hashtag"].append(m["hashtag"].strip())
    #                     replace["#" + m["hashtag"]] = ""
    #             if m["url"]:  # Looking for a website?
    #                 result["url"] = m["url"]
    #                 replace[m["url"]] = urlparse.urlparse(m["url"]).netloc
    #             if m["range1"] and m["range2"]:  # Frame range?
    #                 result["framerange"] = sorted([m["range1"], m["range2"]])
    #             if m["frame"]:
    #                 result["frame"] = m["frame"]
    #             if m["file"] and not result["file"]:
    #                 path = m["file"].split(" ")
    #                 scene = os.path.dirname(cmds.file(q=True, sn=True))
    #                 refPaths = dict((os.path.basename(f), f) for f in cmds.file(l=True, q=True)[1:])  # Listing of all files
    #                 refNames = refPaths.keys()
    #                 for i in range(len(path)):  # Try figure out if a path is being requested
    #                     p = " ".join(path[i:])
    #                     closeMatch = difflib.get_close_matches(p, refNames, 1, 0.9)  # Fuzzy search filenames
    #                     if closeMatch:  # Have we found a reference file?
    #                         rpath = os.path.realpath(refPaths[closeMatch[0]])
    #                     else:  # ... or perhaps another file somewhere else on the system?
    #                         rpath = os.path.realpath(os.path.join(scene, p))
    #                     if os.path.isfile(rpath):
    #                         result["file"] = rpath
    #                         replace[p] = os.path.basename(p)
    #     result["label"] = label.strip()
