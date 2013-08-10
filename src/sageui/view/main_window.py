

import gtk
from gtksourceview2 import View as GtkSourceView

from buildable import Buildable
from window import Window
from terminal_widget import TerminalWidget


class MainWindow(Buildable, Window):

    def __init__(self, presenter, glade_file):
        self.presenter = presenter
        Buildable.__init__(self, ['main_window', 'main_menubar', 'statusbar', 
                                  'terminal', 'terminal_adjustment'])
        builder = self.get_builder(glade_file)
        Window.__init__(self, builder, 'main_window')
        self.menu = builder.get_object('main_menubar')
        self.status = builder.get_object('main_statusbar')
        self.terminal = builder.get_object('terminal')
        self.terminal_adjustment = builder.get_object('terminal_adjustment')
        builder.connect_signals(self)

    def on_main_window_delete_event(self, widget, data=None):
        print 'main window delete (todo: want to quit y/n if unsaved data)'
        return False

    def on_main_window_destroy(self, widget, data=None):
        self.presenter.terminate()

    def on_main_window_map(self, widget, data=None):
        self.terminal.configure()

    def on_main_menu_about_activate(self, widget, data=None):
        self.presenter.show_about()

    def on_main_menu_quit_activate(self, widget, data=None):
        self.presenter.terminate()

    def on_main_menu_new_activate(self, widget, data=None):
        self.presenter.show_notification("todo: new attached file")
        
    def on_main_menu_open_activate(self, widget, data=None):
        self.presenter.show_notification("todo: open file and attach")

    def on_main_menu_copy_activate(self, widget, data=None):
        self.presenter.show_notification("todo: copy")
        
    def on_main_menu_paste_activate(self, widget, data=None):
        self.presenter.show_notification("todo: paste")
        
    def on_main_menu_trac_activate(self, widget, data=None):
        self.presenter.show_trac()
        
    def on_main_menu_git_activate(self, widget, data=None):
        self.presenter.show_notification("todo: git browser")

