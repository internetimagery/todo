# Images
import os.path
import random
import os

root = os.path.realpath(os.path.dirname(__file__))

def randomImage():
    """
    Grab a random image
    """
    path = os.path.join(root, "random")
    return random.choice([os.path.join(root, p) for p in os.listdir(path)])

class icon(object):
    """
    All images in the icons folder
    """
    def __init__(s):
        path = os.path.join(root, "icons")
        s.icons = dict((i[:-4], os.path.join(path, i)) for i in os.listdir(path))# if i[:-3] in ["png"])
    def get(s, key):
        return s.icons.get(key, s.icons["error"])

icon = icon()
