# Default Todo Parsers

from urlparse import urlparse


# FILTERS
# Return text unless it is to be removed
# Return name of token if one is found, and corresponding info
temp = {} # Temp variable to hold info if needed

"""
Hashtag
"""
temp["hashtag"] = set()
def parseHashTag(token):
    if 1 < len(token) and token[:1] == "#":
        temp["hashtag"].add(token[1:])
        return "", ("Hashtag", temp["hashtag"])
    return token, None

"""
Website URL
"""
temp["url"] = set()
def parseUrl(token):
    url = urlparse(token)
    if url.scheme and url.netloc:
        temp["url"].add(token)
        return url.netloc, ("Url", temp["url"])
    return token, None

"""
Frame Range
"""
temp["framerange"] = []
rangeNames = ["to", "through", "-", ":", "and", "->"] # Names that create a range
def parseFrame(token):
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

def getAllParsers():
    return [
        parseHashTag,
        parseUrl,
        parseFrame
    ]
