"""
Preferences
"""


from window import Window
from buildable import Buildable


class PreferencesDialog(Buildable, Window):

    def __init__(self, presenter, glade_file, config):
        self.presenter = presenter
        self.config = config
        Buildable.__init__(self, ['prefs_dialog',
                                  'prefs_ok', 'prefs_cancel',
                                  'prefs_root_value', 'prefs_version_value'])
        builder = self.get_builder(glade_file)
        Window.__init__(self, builder, 'prefs_dialog')
        self.ok_button = builder.get_object('prefs_ok')
        self.cancel_button = builder.get_object('prefs_cancel')
        self.sage_root = builder.get_object('prefs_root_value')
        self.sage_root.set_text(config.sage_root)
        self.sage_version = builder.get_object('prefs_version_value')
        builder.connect_signals(self)

    def on_prefs_dialog_close(self, widget, data=None):
        self.presenter.destroy_modal_dialog()

    def on_prefs_ok_clicked(self, widget, data=None):
        self.presenter.destroy_modal_dialog()
        
    def on_prefs_cancel_clicked(self, widget, data=None):
        self.presenter.destroy_modal_dialog()
        
    def on_prefs_root_change_clicked(self, widget, data=None):
        self.presenter.destroy_modal_dialog()
        

        
