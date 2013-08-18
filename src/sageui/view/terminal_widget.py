"""
The drawing area widget for the page
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
        from gtk.gdk import Color
        self.set_color_background(Color('white'))
        self.set_color_foreground(Color('black'))
        #self.set_size(80, -1)


