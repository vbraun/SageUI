"""
Setup Assistant

Assistant/wizzard/droid to guide you through setting up SAGE_ROOT
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

import logging
 
from .window import DialogWindow
from .buildable import Buildable


class SetupAssistant(Buildable, DialogWindow):

    def __init__(self, presenter, glade_file, sage_root, callback):
        self.presenter = presenter
        self.callback = callback
        Buildable.__init__(self, ['setup_assistant', 'setup_sage_root',
                                  'setup_confirmation', 'setup_content'])
        builder = self.get_builder(glade_file)
        DialogWindow.__init__(self, builder, 'setup_assistant')
        self.sage_root = builder.get_object('setup_sage_root')
        self.content = builder.get_object('setup_content')
        if sage_root is None:
            sage = self.presenter.sage_installation(None)
            if sage.is_usable:
                sage_root = sage.sage_root
        if sage_root is not None:
            self.sage_root.set_text(sage_root)
        self.confirmation = builder.get_object('setup_confirmation')
        builder.connect_signals(self)

    def on_setup_assistant_apply(self, widget, data=None):
        logging.info('setup assistant apply')
        self.callback(self.sage)

    def on_setup_assistant_close(self, widget, data=None):
        logging.info('setup assistant close')
        self.presenter.destroy_modal_dialog()

    def on_setup_assistant_cancel(self, widget, data=None):
        logging.info('setup assistant cancel')
        self.presenter.destroy_modal_dialog()

    def on_setup_assistant_prepare(self, widget, data=None):
        if data is self.content:
            self.sage_root.select_region(0, -1)
        if data is self.confirmation:
            path = self.sage_root.get_text()
            self.sage = self.presenter.sage_installation(path)
            s = '<i>Directory:</i>\n'
            s += '   ' + path + '\n\n'
            if self.sage.is_usable:
                s += '<i>Version:</i>\n'
                s += '   ' + self.sage.version + '\n\n'
                s += '<b>Found Sage installation</b>\n'
                if self.sage.has_git:
                    s += '<b>Uses Git</b>\n'
                else:
                    s += '<b>Too old to use Git</b>\n'
            else:
                s += '<b>Error: no usable Sage installation</b>\n'
            self.confirmation.set_markup(s)
            self.window.set_page_complete(self.confirmation, self.sage.is_usable)


    
