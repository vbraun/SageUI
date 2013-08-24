"""
Generic Error Dialog
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


class ErrorDialog(Buildable, DialogWindow):

    def __init__(self, presenter, glade_file, title, text):
        self.presenter = presenter
        Buildable.__init__(self, ['error_dialog'])
        builder = self.get_builder(glade_file)
        DialogWindow.__init__(self, builder, 'error_dialog')
        self.window.set_property('text', title)
        self.window.set_property('secondary_text', text)
        builder.connect_signals(self)

    def on_error_dialog_response(self, widget, data=None):
        self.presenter.destroy_modal_dialog()
        
