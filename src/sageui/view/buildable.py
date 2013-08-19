"""
Abstract base for (gtk-)buildable things
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


from gi.repository import Gtk


class Buildable(object):

    def __init__(self, object_ids):
        self._object_ids = object_ids

    def get_builder(self, glade_file):
        builder = Gtk.Builder()
        builder.add_objects_from_file(glade_file, self._object_ids)
        return builder
    
