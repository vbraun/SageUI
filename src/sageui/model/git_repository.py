"""
Git repository

This is a easy-to use frontent for the necessary git 
operations. It generally returns more elaborate
Python objects.

The managed branches are all named `sageui/1234/u/user/description`.
"""

from git_error import GitError, DetachedHeadException
from git_branch import GitBranch, GitLocalBranch, GitManagedBranch
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
        return 'sageui/'

    @property
    def prefix_nonumber(self):
        """
        The prefix for managed local branches that have no ticket number
        """
        return 'sageui/none/'

    @cached_property
    def git(self):
        return GitInterface(self.repo_path, verbose=self._verbose)

    @property
    def master(self):
        return GitLocalBranch(self, 'master')

    def get_branch(self, branch_name):
        return GitBranch(self, branch_name)

    def untracked_files(self):
        r"""
        Return a list of file names for files that are not tracked by git and
        not ignored.

        EXAMPLES::

            sage: repo = test.git_repo()
            sage: repo.untracked_files()
            ['untracked']
        """
        return self.git.ls_files(other=True, exclude_standard=True).splitlines()

    def checkout_branch(self, branch_name, ticket_number=None):
        """
        Check out branch.

        This modifies the working directory.

        EXAMPLES::

            sage: repo = test.new_git_repo()
            sage: repo.current_branch()
            Git branch sageui/1002/public/anything
            sage: repo.checkout_branch('u/user/description')
            Git branch sageui/none/u/user/description
            sage: _ == repo.current_branch()
            True
        """
        if '/' in branch_name:
            branch = GitManagedBranch(self, branch_name, ticket_number)
        else:
            branch = GitLocalBranch(self, branch_name)
        assert branch is not None
        self.git.checkout(branch.full_branch_name)
        return branch

    def local_branches(self):
        """
        Return the list of local branches

        Output is in descending age of commits

        EXAMPLES::

            sage: repo = test.git_repo()
            sage: repo.local_branches()
            [Git branch master, Git branch my_branch, Git branch sageui/1000/u/user/description, Git branch sageui/1001/u/alice/work, Git branch sageui/1001/u/bob/work, Git branch sageui/1002/public/anything, Git branch sageui/none/u/user/description]
        """
        branches = self.git.for_each_ref(
            'refs/heads/', sort='committerdate', format="%(objectname) %(refname:short)")
        result = []
        for line in branches.splitlines():
            sha1 = line[0:40]
            name = line[41:]
            branch = GitBranch(self, name, sha1)
            if branch:
                result.append(branch)
        return result

    def current_branch(self):
        r"""
        Return the current branch

        EXAMPLES:

            sage: repo = test.new_git_repo()
            sage: repo.current_branch()
            Git branch sageui/1002/public/anything

        If ``HEAD`` is detached::

            sage: repo.git.silent.checkout('HEAD~')
            sage: repo.current_branch()
            Traceback (most recent call last):
            ...
            DetachedHeadException: unexpectedly, git is in a detached HEAD state
            sage: repo.git.silent.checkout('master')
        """
        try:
            branch_string = self.git.symbolic_ref('HEAD', short=True, quiet=True).strip()
        except GitError as e:
            if e.exit_code == 1:
               raise DetachedHeadException()
            raise
        return GitBranch(self, branch_string)

    def rename_branch(self, oldname, newname):
        r"""
        Rename ``oldname`` to ``newname``.

        EXAMPLES:

        Create some branches::

            sage: repo = test.new_git_repo()
            sage: repo.git.silent.branch('branch1')
            sage: repo.git.silent.branch('branch2')

        Rename some branches::

            sage: repo.rename_branch('branch1', 'branch3')
            sage: repo.rename_branch('branch2', 'branch3')
            Traceback (most recent call last):
            ...
            GitError: git returned with non-zero exit code (128) when executing "git branch --move branch2 branch3"
                STDOUT: 
                STDERR: fatal: A branch named 'branch3' already exists.
        """
        self.git.branch(oldname, newname, move=True)

    def diff(self, from_commit, to_commit):
        """
        List the changed files between the two commits

            sage: repo = test.git_repo()
            sage: branch = repo.current_branch()
            sage: history = branch.commit.get_parents()
            sage: history
            [Commit ..., Commit ..., Commit ...]
            sage: repo.diff(history[-1], history[0])
            ['1', '0', 'bar/foo6.txt']
            ['1', '0', 'foo2.txt']
            ['1', '0', 'foo3.txt']
            ['1', '0', 'foo4.txt']
            ['1', '0', 'foo5.txt']
        """
        log = self.git.diff(from_commit, to_commit, numstat=True, z=True)
        for line in log.split('\0'):
            if line == '':  # two nulls is the end marker
                break
            print line.split('\t')
        

    def changes_since(self, commit):
        """
        List all changes since (and including) commit
        """
        
