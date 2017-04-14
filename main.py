from vozForums import VozForums
##
import gi

gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
gi.require_version('Notify', '0.7')

from gi.repository import Gtk as gtk
from gi.repository import AppIndicator3 as appindicator
from gi.repository import Notify

import signal
import webbrowser

APPINDICATOR_ID = 'vozIndicator'

def build_forums_menu(forums=[], main=True, showHidden=False):
    menu = gtk.Menu()
    for f in forums:
        item = gtk.MenuItem(f.title)
        if (len(f.subForums) > 0):
            item.set_submenu(build_forums_menu(forums=f.subForums, main=False))
        else:
            item.connect('activate', open, f.url)
        menu.append(item)
    ##
    if (main==True):
        if (showHidden):
            item_f33 = gtk.MenuItem('Điểm báo')
            item_f33.connect('activate', open, 'https://vozforums.com/forumdisplay.php?f=33')
            menu.append(item_f33)
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
    voz = VozForums()

    Notify.init(APPINDICATOR_ID)
    indicator = appindicator.Indicator.new(APPINDICATOR_ID, gtk.STOCK_INFO, appindicator.IndicatorCategory.SYSTEM_SERVICES)
    indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
    indicator.set_menu(build_forums_menu(forums=voz.Forums, main=True, showHidden=True))
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    gtk.main()

if __name__ == "__main__":
    main()

