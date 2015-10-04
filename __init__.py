# Lets do it!!
# Created 04/10/15 Jason Dixon
# http://internetimagery.com

import todo.controller.main as main

def Start():
    software = ""
    try:
        import maya
        software = "maya"
    except ImportError:
        print "Software not supported"
    if software:
        main.Main(software)
