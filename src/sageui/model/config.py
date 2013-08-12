

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
