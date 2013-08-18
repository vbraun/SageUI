"""
The Data Model and Backend
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


import logging


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
        logging.info('checking out {} {}'.format(str(branch_name), str(ticket_number)))
        return self.repo.checkout_branch(branch_name, ticket_number)


    ###################################################################
    # Handle configuration change

    def config_sage_changed(self):
        self.repo = GitRepository(self.config.sage_root)
