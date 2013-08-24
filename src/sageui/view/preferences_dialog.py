"""
Preferences
"""

##############################################################################
#  SageUI: A graphical user interface to Sage, Trac, and Git.
#  Copyright (C) 2013  Volker Braun <vbraun.name@gmail.com>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
##############################################################################


from .window import DialogWindow
from .buildable import Buildable


class PreferencesDialog(Buildable, DialogWindow):

    def __init__(self, presenter, glade_file):
        self.presenter = presenter
        Buildable.__init__(self, ['prefs_dialog',
                                  'prefs_ok', 'prefs_cancel',
                                  'prefs_root_value', 'prefs_version_value'])
        builder = self.get_builder(glade_file)
        DialogWindow.__init__(self, builder, 'prefs_dialog')
        self.ok_button = builder.get_object('prefs_ok')
        self.cancel_button = builder.get_object('prefs_cancel')
        self.sage_root = builder.get_object('prefs_root_value')
        self.sage_version = builder.get_object('prefs_version_value')
        builder.connect_signals(self)

    def update(self, config):
        self.sage_root.set_text(config.sage_root)
        self.sage_version.set_text(config.sage_version)

    def apply(self, config):
        changed = False
        sage_root = self.sage_root.get_text()
        if sage_root != config.sage_root:
            config.sage_root = sage_root
            changed = True
        sage_version = self.sage_version.get_text()
        if sage_version != config.sage_version:
            config.sage_version = sage_version
            changed = True
        if changed:
            self.presenter.config_sage_changed()

    def on_prefs_dialog_close(self, widget, data=None):
        self.presenter.hide_preferences_dialog()

    def on_prefs_ok_clicked(self, widget, data=None):
        self.presenter.apply_preferences_dialog()
        self.presenter.hide_preferences_dialog()

    def on_prefs_cancel_clicked(self, widget, data=None):
        self.presenter.hide_preferences_dialog()
        
    def on_prefs_root_change_clicked(self, widget, data=None):
        self.presenter.show_setup_assistant(self,
            self.sage_root.get_text(),
            self.setup_assistant_callback)
        
    def setup_assistant_callback(self, sage_install):
        self.sage_root.set_text(sage_install.sage_root)
        self.sage_version.set_text(sage_install.version)
        
        
