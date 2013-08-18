"""
Container for Configuration Data
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
import json


class Config(object):

    def __init__(self):
        self._load()

    def _save(self):
        data_json = json.JSONEncoder(indent=2).encode(self._data)
        with open(self.settings_file, 'wb') as f:
            f.write(data_json)

    def _load(self):
        try:        
            with open(self.settings_file, 'rb') as f:
                self._data = json.JSONDecoder().decode(f.read())
        except (IOError, OSError, ValueError):
            self._data = dict()
        
    @property
    def version(self):
        return 1

    @property
    def trac_server_hostname(self):
        return 'http://trac.sagemath.org'

    @property
    def trac_server_anonymous_xmlrpc(self):
        return 'xmlrpc'

    @property
    def trac_server_authenticated_xmlrpc(self):
        return 'login/xmlrpc'

    @property
    def dot_sage_directory(self):
        return os.path.join(os.path.expanduser('~'), '.sage')

    @property
    def sageui_directory(self):
        path = os.path.join(self.dot_sage_directory, 'sageui')
        if not os.path.exists(path):
            os.mkdir(path)
        return path

    @property 
    def settings_file(self):
        return os.path.join(self.sageui_directory, 'settings.json')

    ###########################################################3
    # read/write properties follow

    @property
    def sage_root(self):
        return self._data.get('sage_root', None)

    @sage_root.setter
    def sage_root(self, value):
        self._data['sage_root'] = value
        self._save()

    @property
    def sage_version(self):
        return self._data.get('sage_version', 'Unknown version')
    
    @sage_version.setter
    def sage_version(self, value):
        self._data['sage_version'] = value
        self._save()
