# Parse out websites and open them in a browser
# Created 01/10/15 Jason Dixon
# http://internetimagery.com

from todo.parsers.parser import Parser
from urlparse import urlparse
import webbrowser

class Web(Parser):
    def start(s):
        s.description = "Nothing to open."
        s.icon = icon.get("web_16")
        s.name = "web"
        s.priority = 0 # Set at 0 and replace if token found
        s.urls = set()
    def update(s, token):
        url = urlparse(token)
        if url.scheme and url.netloc:
            s.urls.add(token)
            s.priority += 10 # High priority for something so specific
            s.description = "Open Urls: %s" % ", ".join(s.urls)
            return url.netloc
        return token
    def run(s):
        if s.urls:
            print "Opening: %s" % " & ".join(s.urls)
            for url in s.urls:
                webbrowser.open(url, new=2)
