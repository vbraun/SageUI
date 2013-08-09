"""
The main application window
"""

import os
import sys
import gtk
import pango
import gtk.glade
import pkgutil

from about import AboutDialog
from terminal_widget import TerminalWidget
#from gtksourceview2 import GtkSourceView
from gtksourceview2 import View as GtkSourceView


class Application:
    """
    The SageUI main window
    """
    
    def __init__(self, filename=None):
        self._home_dir = d = os.path.dirname(sys.modules['sageui'].__file__)
        gladefile = os.path.join(self._home_dir, 'res', 'SageUI.xml')
        builder = gtk.Builder()
        builder.add_from_file(gladefile)
        self.window = builder.get_object('main_window')
        self.status = builder.get_object('statusbar')
        self.terminal = builder.get_object('terminal')
        self.editor = builder.get_object('editor')
        self.dlg_about = builder.get_object('about_dialog')
        builder.connect_signals(self)
        self.window.show()
        

    def log(self, msg):
        print 'Log:', msg

    def set_status(self, msg, context='default'):
        context = self.status.get_context_id(context)
        self.status.pop(context)
        self.status.push(context, msg)

    def on_main_destroy(self, widget, data=None):
        gtk.main_quit()
     
    def on_menu_help_about_activate(self, widget, data=None):
        self.dlg_about.run()

    def on_about_dialog_response(self, widget, data=None):
        self.dlg_about.hide()

    def on_main_window_destroy(self, widget, data=None):
        gtk.main_quit()

    def on_main_window_map(self, widget, data=None):
        print 'map main'
        self.terminal.configure()
        
     
