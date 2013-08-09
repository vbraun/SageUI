"""
Abstract base for (gtk-)buildable things
"""

import gtk


class Buildable(object):

    def __init__(self, object_ids):
        self._object_ids = object_ids

    def get_builder(self, glade_file):
        builder = gtk.Builder()
        builder.add_objects_from_file(glade_file, self._object_ids)
        return builder
    
