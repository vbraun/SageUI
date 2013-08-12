"""
The View
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
        
    def have_open_window(self):
        return len(self._open_windows) != 0

    @cached_property
    def resource_dir(self):
        return os.path.dirname(sys.modules['sageui'].__file__)

    @cached_property
    def glade_file(self):
        return os.path.join(self.resource_dir, 'res', 'SageUI.xml')
        
    @cached_property
    def commandline_window(self):
        from commandline_window import CommandlineWindow
        return CommandlineWindow(self.presenter, self.glade_file)

    def show_commandline_window(self):
        self._open_windows.add(self.commandline_window)
        self.commandline_window.show()

    def hide_commandline_window(self):
        self.commandline_window.hide()
        self._open_windows.remove(self.commandline_window)

    @cached_property
    def trac_window(self):
        from trac_window import TracWindow
        return TracWindow(self.presenter, self.glade_file)
        
    def show_trac_window(self):
        self._open_windows.add(self.trac_window)
        self.trac_window.show()

    def hide_trac_window(self):
        self.trac_window.hide()
        self._open_windows.remove(self.trac_window)

    @cached_property
    def about_dialog(self):
        from about_dialog import AboutDialog
        return AboutDialog(self.presenter, self.glade_file)

    def terminate(self):
        gtk.main_quit()

    def new_notification_dialog(self, text):
        from notification_dialog import NotificationDialog
        dlg = NotificationDialog(self.presenter, self.glade_file, text)
        assert self._modal_dialog is None
        self._modal_dialog = dlg
        return dlg

    def new_error_dialog(self, title, text):
        from error_dialog import ErrorDialog
        dlg = ErrorDialog(self.presenter, self.glade_file, title, text)
        assert self._modal_dialog is None
        self._modal_dialog = dlg
        return dlg

    def destroy_modal_dialog(self):
        assert self._modal_dialog is not None
        self._modal_dialog.window.destroy()
        self._modal_dialog = None
        
    def xdg_open(self, file_or_uri):
        from xdg_open import xdg_open
        xdg_open(file_or_uri, self.presenter)
