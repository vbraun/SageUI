"""
Git Window

.. note::

    ComboBoxes activate the "change" callback when calling
    :meth:`set_active`.  To work around this, we have the
    `self._branch_entry_ignore_next_change` and
    `self._base_view_ignore_next_change` attributes.

"""

import gtk
import pango
 
from window import Window
from buildable import Buildable

import logging


class GitWindow(Buildable, Window):

    def __init__(self, presenter, glade_file):
        self.presenter = presenter
        Buildable.__init__(self, ['git_window',
                                  'git_tool_remote', 'git_tool_refresh', 
                                  'git_tool_branch', 'git_tool_ticket',
                                  'git_branch_entry', 'git_branch_store',
                                  'git_files_view', 'git_files_store',
                                  'git_base_view', 'git_base_store',
                                  'git_diff'])
        builder = self.get_builder(glade_file)
        Window.__init__(self, builder, 'git_window')
        self.toolbar_remote = builder.get_object('git_tool_remote')
        self.toolbar_branch = builder.get_object('git_tool_branch')
        self.toolbar_ticket = builder.get_object('git_tool_ticket')
        self.toolbar_refresh = builder.get_object('git_tool_refresh')
        self.branch_entry = builder.get_object('git_branch_entry')
        self.branch_store = builder.get_object('git_branch_store')
        self._init_branch(self.branch_entry, self.branch_store)
        self.files_view = builder.get_object('git_files_view')
        self.files_store = builder.get_object('git_files_store')
        self._init_files(self.files_view, self.files_store)
        self.base_view = builder.get_object('git_base_view')
        self.base_store = builder.get_object('git_base_store')
        self._init_base(self.base_view, self.base_store)
        self.diff = builder.get_object('git_diff')
        builder.connect_signals(self)
        self.repo_path = None
        self._branch_entry_ignore_next_change = False
        self._base_view_ignore_next_change = False
        self.set_ticket_number(None)

    def _init_branch(self, view, store):
        branch = view.get_cells()[0]
        #branch = gtk.CellRendererText()
        #view.pack_start(branch, expand=True)
        view.add_attribute(branch, 'text', 1)  
        ticket = gtk.CellRendererText()
        ticket.set_property('xalign', 0)
        view.pack_end(ticket, expand=False)
        view.add_attribute(ticket, 'text', 2)  
        view.set_entry_text_column(1)

    def _init_base(self, view, store):
        name = gtk.CellRendererText()
        view.pack_start(name, expand=True)
        view.add_attribute(name, 'text', 0)  

    def _init_files(self, view, store):
        view.get_selection().set_mode(gtk.SELECTION_BROWSE)
        col = gtk.TreeViewColumn('Changed files')
        view.append_column(col)
        name = gtk.CellRendererText()
        name.set_property('ellipsize', pango.ELLIPSIZE_START)
        col.pack_start(name, expand=True)
        col.add_attribute(name, 'text', 0)  
        col.add_attribute(name, 'cell_background', 1)  
        col.add_attribute(name, 'strikethrough', 2)  
        view.set_has_tooltip(True)
        view.connect("query-tooltip", self._files_tooltip_query)
             
    def _files_tooltip_query(self, treeview, x, y, mode, tooltip):
        context = treeview.get_tooltip_context(x, y, mode)
        if context:
            model, path, iter = context
            name, git_file = model.get(iter, 0, 3)
            tooltip.set_icon_from_stock(gtk.STOCK_FILE, gtk.ICON_SIZE_MENU)
            tooltip.set_text(str(git_file))
            return True
        return False

    @property
    def prefix(self):
        return 'sageui/'

    def set_repo(self, repo_path):
        if self.repo_path == repo_path:
            return
        self.repo_path = repo_path
        self.branch_store.clear()
        self.base_store.clear()
        self.diff.get_buffer().set_text('')

    def set_branches(self, local_branches, current_branch=None):
        self.branch_entry.set_model(None)
        self.branch_store.clear()
        active = None
        for i, branch in enumerate(local_branches):
            n = branch.ticket_number
            number_string = 'Trac #{0}'.format(n)
            self.branch_store.append([i, branch.name, number_string, n])
            if branch == current_branch:
                active = i
        self.branch_entry.set_model(self.branch_store)
        if current_branch is not None:
            self._branch_entry_ignore_next_change = True
            self.branch_entry.set_active(active)

    def set_ticket_number(self, ticket_number=None):
        self.ticket_number = ticket_number
        number = self.toolbar_ticket.get_child()
        if ticket_number is None:
            number.set_label('No ticket')
            self.toolbar_ticket.set_sensitive(False)
        else:
            number_string = 'Trac #{0}'.format(ticket_number)
            number.set_label(number_string)
            self.toolbar_ticket.set_sensitive(True)

    def set_bases_list(self, git_commit_list=None):
        self.base_view.set_model(None)
        self.base_store.clear()
        if git_commit_list is None:
            return
        for c in git_commit_list:
            #print c, c.title, c.sha1
            self.base_store.append([c.title, c.short_sha1, c])
        self.base_view.set_model(self.base_store)
        self._base_view_ignore_next_change = True
        self.base_view.set_active(0)

    def set_base(self, git_commit):
        pass

    def set_changed_files(self, git_file_status_list):
        self.files_view.set_model(None)
        self.files_store.clear()
        for git_file in git_file_status_list:
            name = git_file.name
            strikethrough = False
            background = None
            if git_file.type == 'staged':
                background = 'Pale Green'
            if git_file.type == 'unstaged':
                background = 'Orange Red'
            if git_file.type == 'untracked':
                strikethrough = True
            self.files_store.append([name, background, strikethrough, git_file])
        self.files_view.set_model(self.files_store)
            
    def set_diff(self, git_file):
        self.diff.get_buffer().set_text(str(git_file))

    def on_git_branch_entry_changed(self, widget, data=None):
        n = self.branch_entry.get_active()
        if self._branch_entry_ignore_next_change:
            self._branch_entry_ignore_next_change=False
            return
        logging.info('git branch_entry changed %s', n)
        index, name, number_str, number = self.branch_store[n]
        self.presenter.checkout_branch(name, number)

    def on_git_base_view_changed(self, widget, data=None):
        if self._base_view_ignore_next_change:
            self._base_view_ignore_next_change = False
            return
        n = self.base_view.get_active()
        logging.info('git base_view changed %s', n)
        commit = self.base_store[n][2]
        self.presenter.base_commit_selected(commit)
    
    def on_git_files_view_cursor_changed(self, widget, data=None):
        sel = self.files_view.get_selection()
        logging.info('git files_view changed')
        _, iter = sel.get_selected()
        git_file = self.files_store.get_value(iter, 3)
        self.presenter.git_file_selected(git_file)
        

    def on_git_window_realize(self, widget, data=None):
        self.presenter.show_current_branch()

    def on_git_menu_preferences_activate(self, widget, data=None):
        self.presenter.show_preferences_dialog()

    def on_git_menu_about_activate(self, widget, data=None):
        self.presenter.show_about_dialog()

    def on_git_window_delete_event(self, widget, data=None):
        self.presenter.hide_git_window()
        return False
    
    def on_git_ticket_button_clicked(self, widget, data=None):
        assert self.ticket_number is not None   # button should be disabled 
        self.presenter.load_ticket(self.ticket_number, use_cache=True)
        self.presenter.show_trac_window()

    def on_git_tool_refresh_clicked(self, widget, data=None):
        n = self.base_view.get_active()
        if n == -1: 
            return
        commit = self.base_store[n][2]
        self.presenter.base_commit_selected(commit)
