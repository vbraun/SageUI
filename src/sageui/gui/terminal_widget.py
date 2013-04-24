"""
The drawing area widget for the page
"""

import gtk
import math
import vte

class TerminalWidget(vte.Terminal):
    __gtype_name__ = 'TerminalWidget'
    __gsignals__ = {
        #"expose_event": "override" 
        }
 
    def __init__(self):
        vte.Terminal.__init__(self)

    def configure(self):
        self.fork_command('sage')
        from gtk.gdk import Color
        self.set_color_background(Color('white'))
        self.set_color_foreground(Color('black'))
        #self.set_size(80, -1)
        print self.get_size_request()


