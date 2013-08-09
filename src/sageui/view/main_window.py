

import gtk
from gtksourceview2 import View as GtkSourceView

from buildable import Buildable
from terminal_widget import TerminalWidget


class MainWindow(Buildable):

    def __init__(self, glade_file):
        Buildable.__init__(self, ['main_window', 'statusbar', 'terminal'])
        builder = self.get_builder(glade_file)
        self.window = builder.get_object('main_window')
        self.status = builder.get_object('statusbar')
        self.terminal = builder.get_object('terminal')
        builder.connect_signals(self)

    def show(self):
        self.window.show()

    def on_main_window_destroy(self, widget, data=None):
        gtk.main_quit()
     
