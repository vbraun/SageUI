"""
Window With a Terminal and the Sage Command Line
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

import os
import gtk
from gtksourceview2 import View as GtkSourceView

from buildable import Buildable
from window import Window
from terminal_widget import TerminalWidget


class CommandlineWindow(Buildable, Window):

    def __init__(self, presenter, glade_file):
        self.presenter = presenter
        Buildable.__init__(self, ['cmdline_window', 'cmdline_menubar', 'statusbar', 
                                  'terminal', 'terminal_adjustment'])
        builder = self.get_builder(glade_file)
        Window.__init__(self, builder, 'cmdline_window')
        self.menu = builder.get_object('cmdline_menubar')
        self.status = builder.get_object('cmdline_statusbar')
        self.terminal = builder.get_object('terminal')
        self.terminal_adjustment = builder.get_object('terminal_adjustment')
        builder.connect_signals(self)
        
    def run(self, path, command):
        exe = os.path.join(path, command)
        self.terminal.reset(full=True, clear_history=False)
        self.terminal.fork_command(exe)

    def on_cmdline_window_delete_event(self, widget, data=None):
        self.presenter.hide_commandline_window()
        return False

    def on_cmdline_window_destroy(self, widget, data=None):
        print 'TODO: destroyed. autosave?'
        
    def on_cmdline_window_map(self, widget, data=None):
        self.terminal.configure()

    def on_cmdline_menu_about_activate(self, widget, data=None):
        self.presenter.show_about_dialog()

    def on_cmdline_menu_quit_activate(self, widget, data=None):
        self.presenter.hide_commandline_window()

    def on_cmdline_menu_new_activate(self, widget, data=None):
        self.presenter.show_notification(self, "todo: new attached file")
        
    def on_cmdline_menu_open_activate(self, widget, data=None):
        self.presenter.show_notification(self, "todo: open file and attach")

    def on_cmdline_menu_copy_activate(self, widget, data=None):
        self.presenter.show_notification(self, "todo: copy")
        
    def on_cmdline_menu_paste_activate(self, widget, data=None):
        self.presenter.show_notification(self, "todo: paste")
        
    def on_cmdline_menu_preferences_activate(self, widget, data=None):
        self.presenter.show_preferences_dialog()
        
    def on_cmdline_menu_trac_activate(self, widget, data=None):
        self.presenter.show_trac_window()
        
    def on_cmdline_menu_git_activate(self, widget, data=None):
        self.presenter.show_git_window()

