# View items and event handler to be expanded upon.

class EventManager(object):
    """
    Trigger interraction events from the GUI.
    """
    def __init__(s):
        s.events = {}
    def add(s, event, handler):
        s.events[event] = s.events.get(event, set())
        s.events[event].add(handler)
    def remove(s, handler):
        for event in s.events:
            if handler in s.events[event]:
                s.events[event].remove(handler)
    def fire(s, event, *args, **kwargs):
        if event in s.events:
            if s.events[event]:
                for hander in s.events[event]:
                    hander(*args, **kwargs)

event = EventManager()

class Element(object):
    """
    Base class to build gui elements off for consistency.
    """
    def __init__(s, **kwargs):
        s.attributes = kwargs
        s.children = []
        if s.required():
            s.build()
            for at in s.attributes:
                s.update(at, s.attributes[at])
    def required(s):
        print "Check args match required args. Return true if so, else false."
    def build(s):
        print "Build the GUI element."
    def clear(s):
        print "Clear element of all children."
    def remove(s):
        print "Remove element entirely."
    def update(s, k, v):
        print "Update element attribute %s to %s." % (k, v)
