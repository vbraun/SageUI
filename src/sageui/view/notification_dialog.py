"""
Notification Dialog

This is a lame modal dialog with text and a single "OK" button. Should 
only be used as placeholder for future functionality.
"""

 
from window import Window
from buildable import Buildable


class NotificationDialog(Buildable, Window):

    def __init__(self, presenter, glade_file, text):
        self.presenter = presenter
        Buildable.__init__(self, ['notification_dialog'])
        builder = self.get_builder(glade_file)
        Window.__init__(self, builder, 'notification_dialog')
        self.label = builder.get_object('notification_label')
        self.label.set_text(text)
        builder.connect_signals(self)

    def on_notification_ok_clicked(self, widget, data=None):
        self.presenter.hide_notification()

    def on_notification_dialog_close(self, widget, data=None):
        self.presenter.hide_notification()

