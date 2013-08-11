"""
Notification Dialog

This is a lame modal dialog with text and a single "OK" button. Should 
only be used as placeholder for future functionality.
"""

 
from window import Window
from buildable import Buildable


class ErrorDialog(Buildable, Window):

    def __init__(self, presenter, glade_file, title, text):
        self.presenter = presenter
        Buildable.__init__(self, ['error_dialog'])
        builder = self.get_builder(glade_file)
        Window.__init__(self, builder, 'error_dialog')
        self.window.set_markup(title)
        self.window.format_secondary_text(text)
        builder.connect_signals(self)

    def on_error_dialog_response(self, widget, data=None):
        self.presenter.destroy_modal_dialog()
        
