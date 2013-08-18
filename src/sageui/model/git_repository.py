"""
Git repository

This is a easy-to use frontent for the necessary git 
operations. It generally returns more elaborate
Python objects.

The managed branches are all named `sageui/1234/u/user/description`.
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

from sageui.misc.cached_property import cached_property

from .git_commit import GitCommit
from .git_error import GitError, DetachedHeadException
from .git_branch import GitBranch, GitLocalBranch, GitManagedBranch
from .git_interface import GitInterface
from .git_file import GitFileDiff, GitFileCommitted, GitFileStaged, GitFileUnstaged, GitFileUntracked



class GitRepository(object):

    def __init__(self, repo_path, verbose=False):
        self.repo_path = repo_path
        self._verbose = verbose
        self._base_commit = None

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
    
    @property
    def build_system(self):
        return GitLocalBranch(self, 'build_system')
    
    @property
    def head(self):
        head = self.git.show_ref('HEAD', head=True)
        return GitCommit(self, head[0:40])

    @property
    def base_commit(self):
        """
        A commit relative to which changes are displayed.

        See :meth:`changes`
        
        EXAMPLES::

            sage: repo = test.git_repo()
            sage: repo.base_commit
            Commit ...
            sage: repo.base_commit == repo.head
            True 
        """
        if self._base_commit is None:
            self._base_commit = self.head
        return self._base_commit

    @base_commit.setter
    def base_commit(self, commit):
        if isinstance(commit, GitCommit):
            assert commit.repository is self
            self._base_commit = commit
        else:
            self._base_commit = GitCommit(self, commit)

    def get_branch(self, branch_name):
        return GitBranch(self, branch_name)

    def untracked_files(self):
        r"""
        Return a list of file names for files that are not tracked by git and
        not ignored.

        EXAMPLES::

            sage: repo = test.git_repo()
            sage: repo.untracked_files()
            [untracked:untracked_file]
        """
        log = self.git.ls_files(others=True, exclude_standard=True, z=True)
        result = []
        for line in log.split('\0'):
            if line == '':  # two nulls is the end marker
                break
            result.append(GitFileUntracked(self, line))
        return result

    def checkout_branch(self, branch_name, ticket_number=None):
        """
        Check out branch.

        This modifies the git working tree.

        EXAMPLES::

            sage: repo = test.new_git_repo();  repo.git.silent.stash()
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
        name = branch.full_branch_name
        if self.git.exit_code.show_ref(name) != 0:
            logging.debug('downloading branch %s', name)
            self.git.fetch('trac', branch_name)
            self.git.branch(name, 'FETCH_HEAD')
        self.git.checkout(name)
        self._base_commit = None
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

            sage: repo.git.silent.stash(); repo.git.silent.checkout('HEAD~')
            sage: repo.current_branch()
            Traceback (most recent call last):
            ...
            sageui.model.git_error.DetachedHeadException: unexpectedly, 
            git is in a detached HEAD state
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
            sageui.model.git_error.GitError: git returned with 
            non-zero exit code (128) when executing "git branch --move branch2 branch3"
                STDERR: fatal: A branch named 'branch3' already exists.
        """
        self.git.branch(oldname, newname, move=True)

    def diff_index(self, from_commit, to_commit):
        """
        List the changed files between the two commits

            sage: repo = test.git_repo()
            sage: branch = repo.current_branch()
            sage: history = branch.commit.get_history()
            sage: history
            [Commit ..., Commit ..., Commit ...]
            sage: repo.diff_index(history[-1], history[0])
            [diff_index:+1-0:bar/foo6.txt, diff_index:+1-0:foo2_moved.txt, diff_index:+1-0:foo3.txt, diff_index:+1-0:foo4.txt, diff_index:+1-0:foo5.txt]
        """
        log = self.git.diff(from_commit, to_commit, numstat=True, z=True)
        result = []
        for line in log.split('\0'):
            if line == '':  # two nulls is the end marker
                break
            line = line.split('\t')
            f = GitFileDiff(self, int(line[0]), int(line[1]), line[-1], from_commit, to_commit)
            result.append(f)
        return result

    def changes(self):
        """
        List all changes since (and including) :meth:`base_commit`
        
        Note that a file can be both changed in git history and 
        staged/unstaged. The latter takes precedence.

        EXAMPLES::
        
            sage: repo = test.git_repo() 
            sage: repo.base_commit = repo.head.get_history()[-1]
            sage: repo.changes()
            [diff:+1-0:bar/foo6.txt, 
             diff:+1-0:foo2_moved.txt, 
             diff:+1-0:foo3.txt, 
             unstaged:+2-0:foo4.txt,  
             diff:+1-0:foo5.txt, 
             staged:+0-0:staged_file, 
             untracked:untracked_file]
        """
        files = dict()
        log = self.git.diff(self.base_commit, numstat=True, z=True)
        for line in log.split('\0'):
            if line == '':  # two nulls is the end marker
                break
            line = line.split('\t')
            name = line[-1]
            if line[0] == line[1] == '-':
                f = GitFileCommitted(self, 0, 0, name, self.base_commit, binary=True) 
            else:
                f = GitFileCommitted(self, int(line[0]), int(line[1]), name, self.base_commit, binary=False) 
            files[name] = f
        log = self.git.status(z=True)
        for line in log.split('\0'):
            if line == '':  # two nulls is the end marker
                break
            status = line[0:2]
            status_unstaged = line[1]
            status_staged = line[0]
            name = line[3:]
            blank = ' '
            if status == '??':
                files[name] = GitFileUntracked(self, name)
            elif status_unstaged != blank:
                f = files[name]
                files[name] = GitFileUnstaged(self, f.added, f.subed, f.name, f.commit, binary=f.binary)
            elif status_staged != blank:
                f = files[name]
                files[name] = GitFileStaged(self, f.added, f.subed, f.name, f.commit, binary=f.binary)
            else:
                raise ValueError('unknown status '+status)
        return [files[name] for name in sorted(files.keys())]

