# Pull all parsers together
# Created 01/10/15 Jason Dixon
# http://internetimagery.com

def parsers():
    import todo.parsers.generic as generic
    import frame
    import frameRange
    import _object
    return [
        frame.Frame,
        frameRange.Range,
        _object.Object
        ] + generic.parsers
parsers = parsers()
