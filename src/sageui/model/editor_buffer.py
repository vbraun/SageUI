"""
Buffer in the Editor

A buffer represents what goes into a single source file. It is always an existing 
file, possibly empty and a temporary file whose name is not supposed to be shown to
the end user. It must be updated (via :meth:`set_content`) from the GUI or loaded 
from storage (via :meth:`load_content`) before it knows anything about the actual 
document content. 
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


import os
import logging

from sageui.misc.cached_property import cached_property


class EditorBuffer(object):
    
    def __init__(self, full_qualified_name, anonymous):
        self.anonymous = anonymous
        self.full_qualified_name = os.path.abspath(full_qualified_name)
        self._data = None
        self._attached = False
    
    def get_id(self):
        return id(self);

    def is_attached():
        """
        Whether the file is attached to the current Sage session
        """
        return self._attached

    def attach(self):
        self._attached = True
        
    def detach(self):
        self._attached = False

    @property
    def language(self):
        return 'python'

    @property
    def path(self):
        return os.path.split(self.full_qualified_name)[0]

    @property
    def filename(self):
        """
        The Human-readable file name
        """
        if self.anonymous:
            return '<unnamed>'
        return os.path.split(self.full_qualified_name)[1]

    def file_exists(self):
        if sef.full_qualified_name is None:
            return False
        return os.path.exists(self.full_qualified_name)

    def load_content(self, content):
        if not self.file_exists():
            raise ValueError('file does not exists')
        with open(self.full_qualified_name, 'r', encoding='utf-8') as f:
            self._data = f.read()

    def save_content(self):
        with open(self.full_qualified_name, 'w', encoding='utf-8') as f:
            f.write(self._data)

    def set_content(self, content):
        self._data = content

    def get_content(self):
        return self._data
    
