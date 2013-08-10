

import gtk
from gtksourceview2 import View as GtkSourceView

from buildable import Buildable
from window import Window
from terminal_widget import TerminalWidget


class TracWindow(Buildable, Window):

    def __init__(self, presenter, glade_file):
        self.presenter = presenter
        Buildable.__init__(self, ['trac_window', 'trac_menubar', 'trac_toolbar',
                                  'trac_ticketlist_store', 'trac_ticketlist_view',
                                  'trac_comments'])
        builder = self.get_builder(glade_file)
        Window.__init__(self, builder, 'trac_window')
        self.menu = builder.get_object('trac_menubar')
        self.toolbar = builder.get_object('trac_toolbar')
        self.ticketlist_store = builder.get_object('trac_ticketlist_store')
        self.ticketlist_view = builder.get_object('trac_ticketlist_view')
        self.comments = builder.get_object('trac_comments')
        builder.connect_signals(self)

    def set_ticket_list(self, ticket_list):
        self._ticket_list = ticket_list
        

 
    def on_trac_window_delete_event(self, widget, data=None):
        self.presenter.hide_trac()
        return True
     
    def on_trac_menu_close_activate(self, widget, data=None):
         self.presenter.hide_trac()

    def on_trac_window_map(self, widget, data=None):
        print 'trac window map'

    def on_trac_menu_new_activate(self, widget, data=None):
        self.presenter.show_notification("todo: trac new ticket")

    def on_trac_menu_open_activate(self, widget, data=None):
        self.presenter.show_notification("todo: trac open ticket")

    def on_trac_menu_about_activate(self, widget, data=None):
         self.presenter.show_about()

    def on_trac_menu_cut_activate(self, widget, data=None):
        self.presenter.show_notification("todo: trac cut")
        
    def on_trac_menu_copy_activate(self, widget, data=None):
        self.presenter.show_notification("todo: trac copy")
        
    def on_trac_menu_paste_activate(self, widget, data=None):
        self.presenter.show_notification("todo: trac paste")

    def on_trac_menu_delete_activate(self, widget, data=None):
        self.presenter.show_notification("todo: trac delete")

    def on_trac_tool_new_clicked(self, widget, data=None):
        self.presenter.show_notification("todo: trac new ticket")
        
    def on_trac_tool_refresh_clicked(self, widget, data=None):
        self.presenter.show_notification("todo: trac refresh")
        
    def on_trac_tool_search_clicked(self, widget, data=None):
        self.presenter.show_notification("todo: trac search")
        
