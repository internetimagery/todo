# Pull all parsers together
# Created 01/10/15 Jason Dixon
# http://internetimagery.com

def parsers():
    import todo.parsers.generic as generic
    import _file
    return [
        _file.File
        ] + generic.parsers
parsers = parsers()
