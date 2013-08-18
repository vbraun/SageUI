"""
The View

Holds a number of persistent windows/dialogs as well as modal 
dialogs. They are treated slighty differently:

* An ordinary window is only constructed once when it is 
  required. When the user closes it, it is only hidden and ready
  to be shown again as needed.

* Modal dialogs are continuously re-constructed. There can only 
  be one modal dialog at any one time. When the user closes it,
  it must call :meth:`View.destroy_modal_dialog`. Modal dialogs 
  have their parent window as argument so they can display 
  in front of it.
"""

import os
import sys
import gtk

from sageui.misc.cached_property import cached_property



class View(object):

    def __init__(self, presenter):
        self.presenter = presenter
        self._modal_dialog = None
        self._open_windows = set()
        self.commandline_window_constructed = False
        self.trac_window_constructed = False
        self.git_window_constructed = False
        self.about_dialog_constructed = False
        self.preferences_window_constructed = False
        
    def have_open_window(self):
        return len(self._open_windows) != 0

    @cached_property
    def resource_dir(self):
        return os.path.dirname(sys.modules['sageui'].__file__)

    @cached_property
    def glade_file(self):
        return os.path.join(self.resource_dir, 'res', 'SageUI.xml')
        
    def terminate(self):
        gtk.main_quit()

    def xdg_open(self, file_or_uri):
        from xdg_open import xdg_open
        xdg_open(file_or_uri, self.presenter)

    ##################################################################
    # The commandline window

    @cached_property
    def commandline_window(self):
        self.commandline_window_constructed = True
        from commandline_window import CommandlineWindow
        return CommandlineWindow(self.presenter, self.glade_file)

    def show_commandline_window(self, path, command):
        self._open_windows.add(self.commandline_window)
        self.commandline_window.run(path, command)
        self.commandline_window.present()

    def hide_commandline_window(self):
        self.commandline_window.hide()
        self._open_windows.remove(self.commandline_window)

    ###################################################################
    # The trac window

    @cached_property
    def trac_window(self):
        self.trac_window_constructed = True
        from trac_window import TracWindow
        return TracWindow(self.presenter, self.glade_file)
        
    def show_trac_window(self):
        self._open_windows.add(self.trac_window)
        self.trac_window.present()

    def hide_trac_window(self):
        self.trac_window.hide()
        self._open_windows.remove(self.trac_window)

    ###################################################################
    # The git window

    @cached_property
    def git_window(self):
        self.git_window_constructed = True
        from git_window import GitWindow
        return GitWindow(self.presenter, self.glade_file)
        
    def show_git_window(self, repo_path):
        self._open_windows.add(self.git_window)
        self.git_window.set_repo(repo_path)
        self.git_window.present()

    def hide_git_window(self):
        self.git_window.hide()
        self._open_windows.remove(self.git_window)

    def set_git_branches(self, local_branches, current_branch=None):
        assert (current_branch) is None or (current_branch in local_branches)
        self.git_window.set_branches(local_branches, current_branch)
        if current_branch is None:
            self.git_window.set_bases_list(None)
            self.git_window.set_ticket_number(None)
            self.git_window.set_diff(None)
        else:
            self.git_window.set_bases_list(current_branch.commit.get_history())
            self.git_window.set_ticket_number(current_branch.ticket_number)
            self.presenter.base_commit_selected(current_branch.commit)

    def set_git_base_commit(self, base_commit, changed_files):
        self.git_window.set_base(base_commit)
        self.git_window.set_changed_files(changed_files)
        self.git_window.set_commit_message(base_commit)
        
    def set_git_file(self, git_file):
        self.git_window.set_diff(git_file)

    ###################################################################
    # The about dialog

    @cached_property
    def about_dialog(self):
        self.about_dialog_constructed = True
        from about_dialog import AboutDialog
        return AboutDialog(self.presenter, self.glade_file)

    def show_about_dialog(self):
        self._open_windows.add(self.about_dialog)
        self.about_dialog.show()

    def hide_about_dialog(self):
        self.about_dialog.hide()
        self._open_windows.remove(self.about_dialog)

    ###################################################################
    # The preferences dialog

    @cached_property
    def preferences_dialog(self):
        self.preferences_window_constructed = True
        from preferences_dialog import PreferencesDialog
        return PreferencesDialog(self.presenter, self.glade_file)

    def show_preferences_dialog(self, config):
        self._open_windows.add(self.preferences_dialog)
        self.preferences_dialog.update(config)
        self.preferences_dialog.show()

    def hide_preferences_dialog(self):
        self.preferences_dialog.hide()
        self._open_windows.remove(self.preferences_dialog)

    def apply_preferences_dialog(self, config):
        self.preferences_dialog.apply(config)

    ###################################################################
    # Modal dialogs

    def new_notification_dialog(self, parent, text):
        from notification_dialog import NotificationDialog
        dlg = NotificationDialog(self.presenter, self.glade_file, text)
        dlg.window.set_transient_for(parent.window)
        assert self._modal_dialog is None
        self._modal_dialog = dlg
        return dlg

    def new_error_dialog(self, parent, title, text):
        from error_dialog import ErrorDialog
        dlg = ErrorDialog(self.presenter, self.glade_file, title, text)
        dlg.window.set_transient_for(parent.window)
        assert self._modal_dialog is None
        self._modal_dialog = dlg
        return dlg
        
    def new_setup_assistant(self, parent, sage_root, callback):
        from setup_assistant import SetupAssistant
        dlg = SetupAssistant(self.presenter, self.glade_file, sage_root, callback)
        if parent is not None:
            # parent is allowed to be none if running at the first start
            dlg.window.set_transient_for(parent.window)
        assert self._modal_dialog is None
        self._modal_dialog = dlg
        return dlg

    def destroy_modal_dialog(self):
        assert self._modal_dialog is not None
        self._modal_dialog.window.destroy()
        self._modal_dialog = None
        
    ###################################################################
    # Handle configuration change

    def config_sage_changed(self, config):
        if self.preferences_dialog_constructed:
            self.preferences_dialog.update(config)
        if self.commandline_window_constructed:
            self.commandline_window.run(config.sage_root, 'sage')
        if self.git_window_constructed:
            self.git_window.set_repo(config.sage_root)
