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
        self._notification_dialogs = []
        
    @cached_property
    def resource_dir(self):
        return os.path.dirname(sys.modules['sageui'].__file__)

    @cached_property
    def glade_file(self):
        return os.path.join(self.resource_dir, 'res', 'SageUI.xml')
        
    @cached_property
    def main_window(self):
        from main_window import MainWindow
        return MainWindow(self.presenter, self.glade_file)

    @cached_property
    def trac_window(self):
        from trac_window import TracWindow
        return TracWindow(self.presenter, self.glade_file)

    @cached_property
    def about_dialog(self):
        from about_dialog import AboutDialog
        return AboutDialog(self.presenter, self.glade_file)

    def terminate(self):
        self.main_window.destroy()
        gtk.main_quit()

    def new_notification_dialog(self, text):
        from notification_dialog import NotificationDialog
        dlg = NotificationDialog(self.presenter, self.glade_file, text)
        self._notification_dialogs.append(dlg)
        return dlg

    def hide_notification_dialogs(self):
        for dlg in self._notification_dialogs:
            dlg.window.destroy()
        self._notification_dialogs = []
