# Standard parser for pulling out groups
# Created 01/10/15 Jason Dixon
# http://internetimagery.com

import parser

class Group(parser.Parser):
    def start(s):
        s.description = "Todos Grouped. This is a special Parser."
        s.name = "group"
        s.icon = ""
        s.priority = 0
        s.tags = set() # Store groups
    def update(s, token):
        """
        Parse out groups from tasks. Also serves as an example parser...
        """
        if 1 < len(token) and token[:1] == "#":
            s.tags.add(token[1:])
        else:
            return token
