"""
Setup Assistant

Assistant/wizzard/droid to guide you through setting up SAGE_ROOT
"""

 
from window import Window
from buildable import Buildable


class SetupAssistant(Buildable, Window):

    def __init__(self, presenter, glade_file, sage_root, callback):
        self.presenter = presenter
        self.callback = callback
        Buildable.__init__(self, ['setup_assistant', 'setup_sage_root',
                                  'setup_confirmation', 'setup_content'])
        builder = self.get_builder(glade_file)
        Window.__init__(self, builder, 'setup_assistant')
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
        print 'apply'
        self.callback(self.sage)

    def on_setup_assistant_close(self, widget, data=None):
        print 'close'
        self.presenter.destroy_modal_dialog()

    def on_setup_assistant_cancel(self, widget, data=None):
        print 'cancel'
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


    
