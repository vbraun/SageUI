 
from window import Window
from buildable import Buildable


class AboutDialog(Buildable, Window):

    def __init__(self, presenter, glade_file):
        self.presenter = presenter
        Buildable.__init__(self, ['about_dialog'])
        builder = self.get_builder(glade_file)
        Window.__init__(self, builder, 'about_dialog')
        builder.connect_signals(self)

    def on_about_dialog_response(self, widget, data=None):
        self.presenter.hide_about()

