# Lets do it!!
# Created 04/10/15 Jason Dixon
# http://internetimagery.com

import todo.controller.main as main

software = ""
try:
    import maya
    software = "maya"
except ImportError:
    raise Exception, "Software not supported"

def Start():
    if software:
        main.Main(software)
