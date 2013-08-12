

import os


class Config(object):

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
    def sage_root(self):
        return 'env $SAGE_ROOT'
