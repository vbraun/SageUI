

import gtk 
import gobject
import pango
from gtksourceview2 import View as GtkSourceView

from buildable import Buildable
from window import Window
from terminal_widget import TerminalWidget




class TracWindowUpdater(object):
    
    def __init__(self, trac_window, timeout=1):
        self.trac_window = trac_window
        self.counter = 0
        gobject.timeout_add_seconds(timeout, self.callback)

    def callback(self):
        self.counter += 1
        #print 'updating trac window', str(self.counter)
        if not self.trac_window.window.get_visible():
            return False
        self.trac_window.update_ticket_age()
        return True


class TracWindow(Buildable, Window):

    def __init__(self, presenter, glade_file):
        self.presenter = presenter
        Buildable.__init__(self, ['trac_window', 'trac_menubar', 'trac_toolbar',
                                  'trac_ticketlist_store', 'trac_ticketlist_view',
                                  'trac_search_entry',
                                  'trac_comments',
                                  'trac_comment_text', 'trac_comment_buffer'])
        builder = self.get_builder(glade_file)
        Window.__init__(self, builder, 'trac_window')
        self.menu = builder.get_object('trac_menubar')
        self.toolbar = builder.get_object('trac_toolbar')
        self.search_entry = builder.get_object('trac_search_entry')
        self.ticketlist_store = builder.get_object('trac_ticketlist_store')
        self.ticketlist_view = builder.get_object('trac_ticketlist_view')
        self._init_ticketlist(self.ticketlist_view)
        self.comments = builder.get_object('trac_comments')
        self._init_comments(self.comments)
        self.comment_text = builder.get_object('trac_comment_text')
        self.comment_buffer = builder.get_object('trac_comment_buffer')
        builder.connect_signals(self)
        self.ticket_list = None
        self.current_ticket = None

    def _init_ticketlist(self, listview):
        listview.get_selection().set_mode(gtk.SELECTION_BROWSE)

        # add two columns
        self.col_title = gtk.TreeViewColumn('Description')
        self.col_time = gtk.TreeViewColumn('Last seen')
        listview.append_column(self.col_title)
        listview.append_column(self.col_time)

        # create a CellRenderers to render the data
        self.cell_title = gtk.CellRendererText()
        self.cell_title.set_property('ellipsize', pango.ELLIPSIZE_END)
        self.cell_time = gtk.CellRendererText()
        
        # add the cells to the columns - 2 in the first
        self.col_title.pack_start(self.cell_title, True)
        self.col_title.set_attributes(self.cell_title, markup=1)
        self.col_title.set_resizable(True)
        self.col_title.set_expand(True)

        self.col_time.pack_end(self.cell_time, True)
        self.col_time.set_attributes(self.cell_time, markup=2)
        #self.col_time.set_expand(True)

    def _init_comments(self, comments):
        color = gtk.gdk.color_parse('#F0EAD6')
        comments.modify_base(gtk.STATE_NORMAL, color)
        tag_table = comments.get_buffer().get_tag_table()
        tag = gtk.TextTag('warning')
        tag.set_property('foreground', 'red')
        tag_table.add(tag)
        tag = gtk.TextTag('label')
        tag.set_property('foreground', 'blue')
        tag.set_property('style', pango.STYLE_ITALIC)
        tag_table.add(tag)
        tag = gtk.TextTag('description')
        tag.set_property('foreground', 'black')
        tag.set_property('family', 'monospace')
        tag.set_property('wrap-mode', gtk.WRAP_WORD)
        tag_table.add(tag)
        tag = gtk.TextTag('trac_field')
        tag.set_property('foreground', 'black')
        tag.set_property('family', 'monospace')
        tag.set_property('weight', pango.WEIGHT_SEMIBOLD)
        tag_table.add(tag)
        tag = gtk.TextTag('comment')
        tag.set_property('foreground', 'black')
        tag.set_property('family', 'monospace')
        tag.set_property('wrap-mode', gtk.WRAP_WORD)
        tag_table.add(tag)
        tag = gtk.TextTag('title')
        tag.set_property('foreground', 'black')
        tag.set_property('weight', pango.WEIGHT_BOLD)
        tag.set_property('scale', pango.SCALE_X_LARGE)
        tag_table.add(tag)
        tag = gtk.TextTag('debug')
        tag.set_property('wrap-mode', gtk.WRAP_WORD)
        tag_table.add(tag)

    def show(self):
        super(TracWindow, self).show()
        TracWindowUpdater(self)
        
    def set_ticket_list(self, ticket_list, current_ticket=None): 
        assert (current_ticket is None) or (current_ticket in ticket_list)
        self.ticket_list = ticket_list
        self.ticketlist_store.clear()
        for ticket in ticket_list:
            n = ticket.get_number()
            row = [n,
                   '<b>#'+str(n)+'</b> '+ticket.get_title(), 
                   str(ticket.get_pretty_last_viewed_time())]
            self.ticketlist_store.append(row)
        self.set_current_ticket(current_ticket)

    def get_ticket_numbers(self):
        result = []
        store = self.ticketlist_store
        iter = store.get_iter_first()
        while iter is not None:
            result.append(store.get_value(iter, 0))
        return tuple(result)

    def set_current_ticket(self, ticket):
        """
        Select ``ticket`` in the ticket list.
    
        Also, updates the "Last seen" field since it probably changed to right now.
        """
        self.current_ticket = ticket
        sel = self.ticketlist_view.get_selection()
        if ticket is None:
            sel.unselect_all()
            return
        assert ticket in self.ticket_list
        ticket_number = ticket.get_number()
        store = self.ticketlist_store
        iter = store.get_iter_first()
        while (iter is not None) and (store.get_value(iter, 0) != ticket_number):
            iter = store.iter_next(iter)
        assert iter != None
        sel.select_iter(iter)
        self.update_ticket_age([ticket])

    def update_ticket_age(self, tickets=None):
        if tickets is None:
            tickets = self.ticket_list
        if tickets is None:
            return
        ticket_by_number = dict()
        for ticket in self.ticket_list:
            ticket_by_number[ticket.get_number()] = ticket
        store = self.ticketlist_store
        iter = store.get_iter_first()
        while iter is not None:
            n = store.get_value(iter, 0)
            ticket = ticket_by_number[n]
            store.set(iter, 2, str(ticket.get_pretty_last_viewed_time()))
            iter = store.iter_next(iter)

    def on_trac_ticketlist_view_cursor_changed(self, widget, data=None):
        model, iter = self.ticketlist_view.get_selection().get_selected()
        if not iter: 
            return
        ticket_number = model.get_value(iter, 0)
        print 'cursor changed to ticket #'+str(ticket_number)
        self.presenter.ticket_selected(ticket_number)

    def display_ticket(self, ticket):
        buf = self.comments.get_buffer()
        buf.set_text('')
        if ticket is None:
            return
        def append(*args):
            buf.insert_with_tags(buf.get_end_iter(), *args)
        tag_table = buf.get_tag_table()
        warn_tag = tag_table.lookup('warning')
        title_tag = tag_table.lookup('title')
        label_tag = tag_table.lookup('label')
        trac_field_tag = tag_table.lookup('trac_field')
        description_tag = tag_table.lookup('description')
        comment_tag = tag_table.lookup('comment')
        debug_tag = tag_table.lookup('debug')
        append('Trac #'+str(ticket.get_number())+': '+ticket.get_title(), title_tag)
        append('\n\n')
        branch = ticket.get_branch()
        if branch is not None:
            append('Branch:  ', label_tag)
            append(branch, trac_field_tag)
            append('\n')
        deps = ticket.get_dependencies()
        if deps is not None:
            append('Dependencies:  ', label_tag)
            append(deps, trac_field_tag)
            append('\n')
        append('Description:\n', label_tag)
        append(ticket.get_description().strip(), description_tag)
        for comment in ticket.comment_iter():
            append('\n\n')
            author = comment.get_author()
            time = str(comment.get_ctime())
            append('Comment (by {0} on {1}):\n'.format(author, time), label_tag)
            append(comment.get_comment().strip(), comment_tag)
        append('\n\n')
        append(str(ticket._data), debug_tag)

    def on_trac_window_delete_event(self, widget, data=None):
        self.presenter.hide_trac_window()
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
         self.presenter.show_about_dialog()

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
        
    def on_trac_search_entry_activate(self, widget, data=None):
        entry = self.search_entry.get_buffer().get_text()
        entry = entry.strip('# ')
        try:
            ticket_number = int(entry)
            self.presenter.load_ticket(ticket_number)
        except ValueError:
            self.presenter.show_error('Invalid ticket number', 'Expected integer, got: '+entry)

        
