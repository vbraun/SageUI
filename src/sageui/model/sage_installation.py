"""
Query data about an existing Sage install
"""

import os
import subprocess
from sageui.misc.cached_property import cached_property

class SageInstallation(object):
    
    def __init__(self, sage_root=None):
        if sage_root is None:
            sage_root = self._sage_from_path()
        self.sage_root = sage_root
        
    def _sage_from_path(self):
        try:
            sage_root = subprocess.check_output([
                'sage',
                '-python', '-c',
                'import os; print os.environ["SAGE_ROOT"]'])
        except subprocess.CalledProcessError as err:
            return None
        return sage_root.strip()

    @cached_property
    def is_usable(self):
        if self.sage_root is None:
            return False
        if not os.path.isfile(os.path.join(self.sage_root, 'sage')):
            return False
        return True
        
    @cached_property
    def has_git(self):
        assert self.is_usable
        return os.path.isdir(os.path.join(self.sage_root, '.git'))

    @cached_property
    def version(self):
        assert self.is_usable
        try:
            version = subprocess.check_output([
                os.path.join(self.sage_root, 'sage'), '--version'])
        except CalledProcessError as err:
            return str(err)
        return version

        
