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

icons = dict((os.path.splitext(p)[0], os.path.join(root, "icons", p)) for p in os.listdir(os.path.join(root, "icons")))
