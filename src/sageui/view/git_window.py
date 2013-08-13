"""
Git Window
"""

import gtk
import pango
 
from window import Window
from buildable import Buildable


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
        self.base_view = builder.get_object('git_base_view')
        self.base_store = builder.get_object('git_base_store')
        self._init_base(self.base_view, self.base_store)
        self.diff = builder.get_object('git_diff')
        builder.connect_signals(self)
        self.repo_path = None
        self._set_ticket_number(None)

    def _init_branch(self, view, store):
        branch = view.get_cells()[0]
        #branch = gtk.CellRendererText()
        #view.pack_start(branch, expand=True)
        view.add_attribute(branch, 'text', 1)  
        ticket = gtk.CellRendererText()
        view.pack_end(ticket, expand=False)
        view.add_attribute(ticket, 'text', 2)  
        view.set_entry_text_column(1)

    def _init_base(self, view, store):
        name = gtk.CellRendererText()
        view.pack_start(name, expand=True)
        view.add_attribute(name, 'text', 0)  

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

    def set_branch(self, git_branch):
        self.branch_store.clear()
        number_string = 'Trac #{0}'.format(git_branch.ticket_number)
        self.branch_store.append([0, git_branch.name, number_string])
        text = self.branch_entry.get_child()
        text.set_text(git_branch.name)
        self._set_ticket_number(git_branch.ticket_number)

    def _set_ticket_number(self, ticket_number=None):
        self.ticket_number = ticket_number
        number = self.toolbar_ticket.get_child()
        if ticket_number is None:
            number.set_label('No ticket')
            self.toolbar_ticket.set_sensitive(False)
        else:
            number_string = 'Trac #{0}'.format(ticket_number)
            number.set_label(number_string)
            self.toolbar_ticket.set_sensitive(True)

    def set_bases(self, git_commit_list):
        self.base_store.clear()
        self.base_store.append(['HEAD', '9adadeb329a7a0cade90daa6c85353a037f660bb'])
        self.base_view.set_active(0)

    def set_change_files(self, git_file_status_list):
        pass

    def set_diff(self, diff):
        pass

    def on_git_branch_entry_changed(self, widget, data=None):
        print 'changed', widget, data
        return False

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

