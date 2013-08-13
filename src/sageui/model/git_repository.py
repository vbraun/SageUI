"""
Manage local git repository

The local branches are all named `sageui/1234/u/user/description`



"""

from git_error import GitError
from git_branch import GitLocalBranch, GitManagedBranch




class GitRepository(object):

    def __init__(self, repo_path):
        self.repo_path = repo_path

    @property
    def prefix(self):
        """
        The prefix for local branches
        """
        return 'sageui'

    def checkout_branch(self, branch_name, ticket_number=None):
        branch = GitManagedBranch(self, branch_name, ticket_number)
        return branch

    def list_branches(self):
        """
        Return the list of local branches
        """
        
