"""
The drawing area widget for the page
"""

import gtk
import pango


class DiffViewerWidget(gtk.TextView):
    __gtype_name__ = 'DiffViewerWidget'
 
    def __init__(self, *args, **kwds):
        super(DiffViewerWidget, self).__init__(*args, **kwds)
        self.set_editable(False)
        self.set_cursor_visible(False)
        self.color_plus = gtk.gdk.color_parse('#ddffdd')
        self.color_minus = gtk.gdk.color_parse('#ffdddd')
        self._init_tag_table()

    def _init_tag_table(self):
        tag_table = self.get_buffer().get_tag_table()
        tag = gtk.TextTag('default')
        tag.set_property('family', 'monospace')
        tag_table.add(tag)
        tag = gtk.TextTag('plus')
        tag.set_property('family', 'monospace')
        tag.set_property('background-gdk', self.color_plus)
        tag_table.add(tag)
        tag = gtk.TextTag('minus')
        tag.set_property('family', 'monospace')
        tag.set_property('background-gdk', self.color_minus)
        tag_table.add(tag)

    def set_diff(self, diff_string):
        buf = self.get_buffer()
        tag_table = buf.get_tag_table()
        plus_tag = tag_table.lookup('plus')
        minus_tag = tag_table.lookup('minus')
        default_tag = tag_table.lookup('default')
        buf.set_text('')
        tag_from_char = {'+':plus_tag, '-':minus_tag}
        for line in diff_string.splitlines():
            tag = default_tag if line=='' else tag_from_char.get(line[0], default_tag)
            end = buf.get_end_iter()
            buf.insert_with_tags(end, line+'\n', tag)

    def set_error_diff(self):
        """
        Show an error message that the file cannot be diffed
        """
        buf = self.get_buffer()
        buf.set_text('')
        warning = self.render_icon(gtk.STOCK_DIALOG_ERROR, gtk.ICON_SIZE_DIALOG);
        buf.insert_pixbuf(buf.get_start_iter(), warning)
        buf.insert(buf.get_end_iter(), '    No diff available, file is binary or untracked.')

    def set_commit_message(self, message):
        buf = self.get_buffer()
        buf.set_text(message)
