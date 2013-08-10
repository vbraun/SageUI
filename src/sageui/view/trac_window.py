

import gtk
import pango
from gtksourceview2 import View as GtkSourceView

from buildable import Buildable
from window import Window
from terminal_widget import TerminalWidget



class TracWindow(Buildable, Window):

    def __init__(self, presenter, glade_file):
        self.presenter = presenter
        Buildable.__init__(self, ['trac_window', 'trac_menubar', 'trac_toolbar',
                                  'trac_ticketlist_store', 'trac_ticketlist_view',
                                  'trac_comments',
                                  'trac_comment_text', 'trac_comment_buffer'])
        builder = self.get_builder(glade_file)
        Window.__init__(self, builder, 'trac_window')
        self.menu = builder.get_object('trac_menubar')
        self.toolbar = builder.get_object('trac_toolbar')
        self.ticketlist_store = builder.get_object('trac_ticketlist_store')
        self.ticketlist_view = builder.get_object('trac_ticketlist_view')
        self._init_ticketlist()
        # existing commetns
        self.comments = builder.get_object('trac_comments')
        #self.comments.modify_text(gtk.STATE_NORMAL, gtk.gdk.color_parse("red")) 
        font = 'serif'
        font_desc = pango.FontDescription(font)
        self.comments.modify_font(font_desc)
        color = gtk.gdk.color_parse('#F0EAD6')
        self.comments.modify_base(gtk.STATE_NORMAL, color)
        # new comment
        self.comment_text = builder.get_object('trac_comment_text')
        self.comment_buffer = builder.get_object('trac_comment_buffer')
        builder.connect_signals(self)

    def _init_ticketlist(self):
        sel = self.ticketlist_view.get_selection()
        sel.set_mode(gtk.SELECTION_BROWSE)

        # add two columns
        self.col_title = gtk.TreeViewColumn('Description')
        self.col_time = gtk.TreeViewColumn('Last seen')
        self.ticketlist_view.append_column(self.col_title)
        self.ticketlist_view.append_column(self.col_time)

        # create a CellRenderers to render the data
        self.cell_title = gtk.CellRendererText()
        self.cell_title.set_property('ellipsize', pango.ELLIPSIZE_END)

        self.cell_time = gtk.CellRendererText()
        
        # set background color property
        #self.cell_title.set_property('cell-background', 'yellow')
        #self.cell_text.set_property('cell-background', 'cyan')
        #self.cell_version.set_property('cell-background', 'pink')

        # add the cells to the columns - 2 in the first
        self.col_title.pack_start(self.cell_title, True)
        self.col_title.set_attributes(self.cell_title, markup=1)
        self.col_title.set_resizable(True)
        self.col_title.set_expand(True)

        self.col_time.pack_end(self.cell_time, True)
        self.col_time.set_attributes(self.cell_time, markup=2)
        #self.col_time.set_expand(True)

    def set_ticket_list(self, ticket_list):
        self._ticket_list = ticket_list
        self.ticketlist_store.clear()
        for ticket in ticket_list:
            n = ticket.get_number()
            row = [n,
                   '<b>#'+str(n)+'</b> '+ticket.get_title(), 
                   str(ticket.get_last_viewed_time())]
            print row
            self.ticketlist_store.append(row)
        sel = self.ticketlist_view.get_selection()
        sel.select_iter(self.ticketlist_store.get_iter_first())
        self.presenter.trac_ticket_selected(ticket_list[0])

    def on_trac_ticketlist_view_cursor_changed(self, widget, data=None):
        model, iter = self.ticketlist_view.get_selection().get_selected()
        if not iter: 
            return
        ticket_number = model.get_value(iter, 0)
        for ticket in self._ticket_list:
            if ticket.get_number() == ticket_number:
                self.presenter.trac_ticket_selected(ticket)
                return

    def display_ticket(self, ticket):
        buf = self.comments.get_buffer()
        buf.set_text(ticket.get_description())

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
        
