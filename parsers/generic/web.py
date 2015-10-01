# Parse out websites and open them in a browser
# Created 01/10/15 Jason Dixon
# http://internetimagery.com

from todo.parsers.parser import Parser
from urlparse import urlparse
import webbrowser

class Web(Parser):
    def start(s):
        s.description = "Nothing to open."
        s.icon = "todo.web"
        s.name = "web"
        s.priority = 0 # Set at 0 and replace if token found
        s.urls = set()
    def update(s, token):
        url = urlparse(token)
        if url.scheme and url.netloc:
            s.urls.add(token)
            s.priority += 10 # High priority for something so specific
            if 1 < len(s.urls):
                s.description = "Open urls:" + "\n- ".join(["\n* %s" % u for u in s.urls])
            else:
                s.description = "Open url: %s" % s.urls[0]
            return url.netloc
        return token
    def run(s):
        if s.urls:
            print "Opening: %s" % " & ".join(s.urls)
            for url in s.urls:
                webbrowser.open(url, new=2)
