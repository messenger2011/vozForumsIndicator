import gi

gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
gi.require_version('Notify', '0.7')

from gi.repository import Gtk as gtk
from gi.repository import AppIndicator3 as appindicator
from gi.repository import Notify

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

import json
import signal
import webbrowser
import re
import urllib.request
from bs4 import BeautifulSoup

class Link(object):
    def __init__(self, url, title):
        self.url = url
        self.title = title

class VozForums:
    protocol = "https"
    domain = "vozforums.com"
    vozurl = protocol + "://" + domain + "/"
    forum = "forumdisplay.php?f="
    thead = "showthread.php?t="

    @classmethod
    def get(self, url):
        req = urllib.request.Request(url=url, method='GET')
        with urllib.request.urlopen(req) as f:
            return self.parseBody(f)

    @classmethod
    def forums(self, f):
        return vozurl + forum + str(f)

    @classmethod
    def threads(self, t):
        return vozurl + thread + str(t)

    @classmethod
    def parseBody(self, response):
        if (response):
            return response.read().decode('utf-8')
    
    def listForums(self):
        forums = []
        body = self.get(self.vozurl)
        soup = BeautifulSoup(body, 'html.parser')
        for td in soup.find_all('td', { "class": "alt1Active" }):
            if (td.div and td.div.a.strong and td.div.a.strong.string and td.div.a.get('href') != '#'):
                link = Link(self.vozurl + td.div.a.get('href'), td.div.a.strong.string)
                forums.append(link)
        return forums

APPINDICATOR_ID = 'vozIndicator'

def build_menu():
    menu = gtk.Menu()
    voz = VozForums()
    for f in voz.listForums():
        item = gtk.MenuItem(f.title)
        item.connect('activate', open, f.url)
        menu.append(item)
    ##
    item_quit = gtk.MenuItem("Exit")
    item_quit.connect('activate', quit)
    menu.append(item_quit)
    ##
    menu.show_all()
    ##
    return menu
 
def quit(self):
    gtk.main_quit()

def open(self, url):
    webbrowser.open_new_tab(url)

def main():
    Notify.init(APPINDICATOR_ID)
    indicator = appindicator.Indicator.new(APPINDICATOR_ID, gtk.STOCK_INFO, appindicator.IndicatorCategory.SYSTEM_SERVICES)
    indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
    indicator.set_menu(build_menu())
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    gtk.main()

if __name__ == "__main__":
    main()

