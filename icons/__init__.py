# Images
import os.path
import os


def Icons():
    root = os.path.realpath(os.path.dirname(__file__))
    return dict((os.path.splitext(p)[0], os.path.join(root, p)) for p in os.listdir(root))
Icons = Icons()
