import os
import sys
import gtk
# https://bugs.launchpad.net/bugs/480398
gtk.gdk.threads_init()
import webkit

class Webless(object):
    def __init__(self, url=''):
        self.view = webkit.WebView()
        self.open(url)

    def inject_file(self, path):
        '''run a script in a file'''
        if os.path.isfile(path) and os.access(path, os.R_OK):
            self.inject_script(file(path).read())
            return True

        return False

    def inject_script(self, script):
        '''run a script'''
        self.view.execute_script(script)

    def get_code(self):
        '''return the text of the widget'''
        self.view.execute_script('oldtitle=document.title;document.title=document.documentElement.innerHTML;')
        html = self.view.get_main_frame().get_title()
        self.view.execute_script('document.title=oldtitle;')
        return html

    def open(self, url):
        if not url.startswith('http://') and not url.startswith('https://'):
            self.url = 'http://' + url
        else:
            self.url = url

        self.view.open(self.url)

class Browserless(gtk.Window, Webless):
    def __init__(self, url=''):
        gtk.Window.__init__(self)
        Webless.__init__(self, url)
        self.add(self.view)

class Browser(gtk.Window, Webless):
    def __init__(self, url=''):
        gtk.Window.__init__(self)
        Webless.__init__(self, url)
        self.set_title('Browser')
        self.set_default_size(640, 480)

        scroll = gtk.ScrolledWindow()
        scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scroll.set_shadow_type(gtk.SHADOW_IN)

        scroll.add(self.view)

        vbox = gtk.VBox()
        hbox = gtk.HBox()

        entry = gtk.Entry()
        entry.connect('activate', self._on_url_changed)

        if self.url:
            entry.set_text(self.url)

        code = gtk.Entry()
        code.connect('activate', self._on_run_code)

        getcode = gtk.Button("html to clipboard")
        getcode.connect('clicked', self._on_get_code)

        hbox.pack_start(code, True, True)
        hbox.pack_start(getcode, False)

        vbox.pack_start(entry, False)
        vbox.pack_start(scroll, True, True)
        vbox.pack_start(hbox, False)
        vbox.show_all()

        self.add(vbox)

        self.connect('delete-event', lambda *args: sys.exit(0))

    def _on_get_code(self, button):
        '''copy the content of the html window to the clipboard'''
        code = self.get_code()
        gtk.clipboard_get().set_text(code)

    def _on_url_changed(self, entry):
        '''called when the url changes'''
        url = entry.get_text()
        self.open(url)

    def _on_run_code(self, entry):
        '''called when the url changes'''
        code = entry.get_text()
        self.inject_script(code)

def process_events():
    while gtk.events_pending():
        gtk.main_iteration(True)

if __name__ == '__main__':
    browser = Browser('www.google.com/search?q=emesene')

    def inject_fun(view, frame):
        browser.inject_file('js/jquery.js')
        browser.inject_file('js/json2.js')

    browser.view.connect('load-finished', inject_fun)

    browser.show()

    gtk.main()
