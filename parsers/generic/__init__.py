# Pull all parsers together
# Created 01/10/15 Jason Dixon
# http://internetimagery.com

def parsers():
    import web
    import _file
    return [
        web.Web,
        _file.File
        ]
parsers = parsers()
