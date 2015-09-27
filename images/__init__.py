# Images
from os.path import dirname, realpath, join, isdir
from random import choice
from os import listdir

root = realpath(dirname(__file__))

def randomImage():
    """
    Grab a random image
    """
    path = join(root, "random")
    return choice([join(root, p) for p in listdir(path)])

class IconStore(object):
    """
    All images in the icons folder
    """
    def __init__(s):
        path = join(root, "icons")
        s.icons = dict((i[:-4], join(path, i)) for i in listdir(path))# if i[:-3] in ["png"])
    def get(s, key):
        return s.icons.get(key, s.icons["error"])

icon = IconStore()
