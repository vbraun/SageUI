"""
Git repository

This is a easy-to use frontent for the necessary git 
operations. It generally returns more elaborate
Python objects.

The managed branches are all named `sageui/1234/u/user/description`.
"""

from git_error import GitError
from git_branch import GitLocalBranch, GitManagedBranch
from git_interface import GitInterface

from sageui.misc.cached_property import cached_property



class GitRepository(object):

    def __init__(self, repo_path, verbose=False):
        self.repo_path = repo_path
        self._verbose = verbose

    @property
    def prefix(self):
        """
        The prefix for managed local branches
        """
        return 'sageui'

    @property
    def prefix_nonumber(self):
        """
        The prefix for managed local branches that have no ticket number
        """
        return 'sageui/none'

    @cached_property
    def git(self):
        return GitInterface(self.repo_path, verbose=self._verbose)

    def checkout_branch(self, branch_name, ticket_number=None):
        branch = GitManagedBranch(self, branch_name, ticket_number)
        return branch

    def local_branches(self):
        """
        Return the list of local branches

        EXAMPLES::

            >>> repo.local_branches()
            [Git branch master, Git branch my_branch, Git branch sageui/1000/u/user/description, Git branch sageui/1001/u/alice/work, Git branch sageui/1001/u/bob/work, Git branch sageui/1002/public/anything, Git branch sageui/none/u/user/description]
        """
        branches = self.git.for_each_ref(
            'refs/heads/', sort='committerdate', format="%(objectname)%(refname:short)")
        result = []
        for line in branches.splitlines():
            commit = line[0:40]
            name = line[40:]
            if '/' not in name:
                branch = GitLocalBranch(self, name, commit)
                result.append(branch)
            elif name.startswith(self.prefix_nonumber+'/'):
                description = name[len(self.prefix_nonumber)+1:]
                branch = GitManagedBranch(self, description, commit, None)
                result.append(branch)
            elif name.startswith(self.prefix+'/'):
                start = len(self.prefix) + 1
                end = name.find('/', start)
                number = name[start:end]
                description = name[end+1:]
                try:
                    number = int(number)
                    branch = GitManagedBranch(self, description, commit, number)
                    result.append(branch)
                except ValueError:
                    pass
        return result

    def current_branch(self):
        r"""
        Return the current branch

        EXAMPLES:

        Create a :class:`GitInterface` for doctesting::

            sage: import os
            sage: from sage.dev.git_interface import GitInterface, SILENT, SUPER_SILENT
            sage: from sage.dev.test.config import DoctestConfig
            sage: from sage.dev.test.user_interface import DoctestUserInterface
            sage: config = DoctestConfig()
            sage: git = GitInterface(config["git"], DoctestUserInterface(config["UI"]))

        Create some branches::

            sage: os.chdir(config['git']['src'])
            sage: git.commit(SILENT, '-m','initial commit','--allow-empty')
            sage: git.commit(SILENT, '-m','second commit','--allow-empty')
            sage: git.branch('branch1')
            sage: git.branch('branch2')

            sage: git.current_branch()
            'master'
            sage: git.checkout(SUPER_SILENT, 'branch1')
            sage: git.current_branch()
            'branch1'

        If ``HEAD`` is detached::

            sage: git.checkout(SUPER_SILENT, 'master~')
            sage: git.current_branch()
            Traceback (most recent call last):
            ...
            DetachedHeadError: unexpectedly, git is in a detached HEAD state

        """
        try:
            return self.symbolic_ref('HEAD', short=True, quiet=True).strip()
        except GitError as e:
            if e.exit_code == 1:
               raise DetachedHeadError()
            raise


