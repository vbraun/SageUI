"""
Editor Window
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


from gi.repository import Gdk, Gtk, Pango
from gi.repository import GtkSource
 
from .window import Window
from .buildable import Buildable


import logging


class EditorWindowTab(object):
    
    def __init__(self, buffer_model_id):
        self.buffer_id = buffer_model_id
        self.scroll = scroll = Gtk.ScrolledWindow()
        self.sourceview = sourceview = GtkSource.View()
        scroll.add(sourceview)
        self.buffer = buffer = GtkSource.Buffer()
        sourceview.set_buffer(buffer)
        # bg = Gdk.RGBA(0.8, 0.8, 0.8, 1)
        # gutter = self.sourceview.get_gutter(Gtk.TextWindowType.LEFT)
        # TODO: set gutter background color
        fontdesc = Pango.FontDescription("monospace")
        sourceview.modify_font(fontdesc)
        self.set_language()

    def set_language(self):
        mgr = GtkSource.LanguageManager()
        lang = mgr.get_language('python')
        self.buffer.set_language(lang)
        


class EditorWindow(Buildable, Window):

    def __init__(self, presenter, glade_file):
        self.presenter = presenter
        Buildable.__init__(self, ['editor_window',
                                  'editor_tool_save',
                                  'edtior_help_about'])
        builder = self.get_builder(glade_file)
        Window.__init__(self, builder, 'editor_window')
        self.toolbar_save = builder.get_object('editor_tool_save')
        self.notebook = builder.get_object('editor_notebook')
        self.tabs = []
        builder.connect_signals(self)

    def add_tab(self, buf):
        tab = EditorWindowTab(buf.get_id())
        self.tabs.append(tab)
        label = Gtk.Label(buf.filename)
        self.notebook.append_page(tab.scroll, label)
        self.notebook.show_all()
        
    def get_content(self, buffer_id):
        for tab in self.tabs:
            if tab.buffer_id == buffer_id:
                buf = tab.buffer
                return buf.get_text(buf.get_start_iter(), buf.get_end_iter(), True)
        raise ValueError('invalid buffer id')

    def on_editor_menu_quit_activate(self, widget, data=None):
        logging.info('quit from menu clicked')
        self.presenter.hide_editor_window()

    def on_editor_menu_about_activate(self, widget, data=None):
        self.presenter.show_about_dialog()
    
    def on_editor_window_delete_event(self, widget, data=None):
        logging.debug('editor delete event')
        self.presenter.hide_editor_window()
        return False
    
    def on_editor_menu_save_activate(self, widget, data=None):
        logging.info('save from menu clicked')

    def on_editor_tool_save_clicked(self, widget, data=None):
        n = self.notebook.get_current_page()
        for tab in self.tabs:
            if n == self.notebook.page_num(tab.scroll):
                self.presenter.save_file(tab.buffer_id)
                return
        raise ValueError('did not find buffer to save')

    def on_editor_tool_find_clicked(self, widget, data=None):
        logging.info('find toolbar button clicked')

    def on_editor_tool_replace_clicked(self, widget, data=None):
        logging.info('replace toolbar button clicked')



    def on_editor_menu_undo_activate(self, widget, data=None):
        logging.info('undo from menu clicked')

    def on_editor_tool_undo_clicked(self, widget, data=None):
        logging.info('undo toolbar button clicked')

    def on_editor_menu_redo_activate(self, widget, data=None):
        logging.info('redo from menu clicked')

    def on_editor_tool_redo_clicked(self, widget, data=None):
        logging.info('redo toolbar button clicked')

