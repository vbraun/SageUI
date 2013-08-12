"""
The Data Model and Backend
"""

from config import Config
from trac_server import TracServer


class Model:
    
    def __init__(self, presenter):
        self.presenter = presenter
        c = Config()
        self.config = c
        self.trac = TracServer(c.trac_server_hostname,
                               c.trac_server_anonymous_xmlrpc)
        self.trac.database.load(c.sageui_directory)

    

    def terminate(self):
        self.trac.database.save(self.config.sageui_directory)


    def sage_installation(self, sage_root):
        from sage_installation import SageInstallation
        return SageInstallation(sage_root)

        
