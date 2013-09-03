"""
Editor

The editor model manages a list of buffers.
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
import tempfile

from sageui.misc.cached_property import cached_property

from .editor_buffer import EditorBuffer

class Editor(object):
    
    def __init__(self, sageui_directory):
        self.buffers = []
        self._temp_dir = os.path.join(sageui_directory, 'attached_files')
        if not os.path.exists(self._temp_dir):
            os.mkdir(self._temp_dir)

    def buffer_from_id(self, buf_id):
        for buf in self.buffers:
            if id(buf)==buf_id:
                return buf
        raise ValueError('buffer not in the editor')

    def new_buffer(self, suffix='.py'):
        fd, filename = tempfile.mkstemp(dir=self._temp_dir, suffix=suffix)
        os.close(fd)
        buf = EditorBuffer(filename, True)
        self.buffers.append(buf)
        return buf

    def load_buffer(self, filename):
        buf = EditorBuffer(filename, False)
        self.buffers.append(buf)
        return buf        
        
    def close_buffer(self, buf):
        if not isinstance(buf, EditorBuffer):
            buf = self.buffer_from_id(buf)
        self.buffers.remove(buf)

    
