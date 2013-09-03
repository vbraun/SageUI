"""
The Presenter (Controller) for the Editor

This is a mixin class for the presenter
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



class EditorPresenter(object):

    def show_editor_window(self, buf):
        return self.view.show_editor_window(buf)

    def hide_editor_window(self):
        self.view.hide_editor_window()
        if not self.view.have_open_window():
            self.terminate()

    def new_attached_file(self):
        buf = self.model.new_attached_buffer()
        attach = "attach('{0}')\n".format(buf.full_qualified_name)
        print(attach)
        self.paste_into_terminal(attach)
        self.show_editor_window(buf)

    def save_file(self, buffer_id):
        content = self.view.get_editor_content(buffer_id)
        buf = self.model.editor.buffer_from_id(buffer_id)
        buf.set_content(content)
        buf.save_content()
