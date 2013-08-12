"""
Git Window
"""

 
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
        self.files_view = builder.get_object('git_files_view')
        self.files_store = builder.get_object('git_files_store')
        self.base_view = builder.get_object('git_base_view')
        self.base_store = builder.get_object('git_base_store')
        builder.connect_signals(self)


    def on_git_window_delete_event(self, widget, data=None):
        self.presenter.hide_git_window()
        return False
    
