"""
The Data Model and Backend
"""

from config import Config
from trac_server import TracServer
from git_repository import GitRepository


class Model:
    
    def __init__(self, presenter):
        self.presenter = presenter
        c = Config()
        self.config = c
        self.trac = TracServer(c.trac_server_hostname,
                               c.trac_server_anonymous_xmlrpc)
        self.trac.database.load(c.sageui_directory)
        self.repo = GitRepository(c.sage_root)
    

    def terminate(self):
        self.trac.database.save(self.config.sageui_directory)

    def sage_installation(self, sage_root):
        from sage_installation import SageInstallation
        return SageInstallation(sage_root)

    def list_branches(self):
        return self.repo.local_branches()

    def current_branch(self):
        return self.repo.current_branch()
        
    def checkout_branch(self, branch_name, ticket_number=None):
        return self.repo.checkout_branch(branch_name, ticket_number)



    ###################################################################
    # Handle configuration change

    def config_sage_changed(self):
        self.repo = GitRepository(self.config.sage_root)
