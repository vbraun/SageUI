"""
The drawing area widget for the page
"""

import gtk
import math
import vte

class TerminalWidget(vte.Terminal):
    __gtype_name__ = 'TerminalWidget'
    #__gsignals__ = {"expose_event": "override" }
 
    def __init__(self):
        vte.Terminal.__init__(self)
  
