"""
Branches in the Local Git Repository

In fact, a particular commit on a branch.

EXAMPLES::

    sage: repo = test.git_repo()
    sage: repo.local_branches()
    [Git branch master, Git branch my_branch, Git branch sageui/1000/u/user/description, Git branch sageui/1001/u/alice/work, Git branch sageui/1001/u/bob/work, Git branch sageui/1002/public/anything, Git branch sageui/none/u/user/description]


"""

from git_commit import GitCommit


def GitBranch(git_repository, name, commit=None):
    """
    Construct a branch object given the name as a string
    """
    if commit is not None:
        commit = GitCommit(git_repository, commit)
    prefix = git_repository.prefix
    prefix_nonumber = git_repository.prefix_nonumber
    if '/' not in name:
        return GitLocalBranch(git_repository, name, commit)
    elif name.startswith(prefix_nonumber):
        description = name[len(prefix_nonumber):]
        return GitManagedBranch(git_repository, description, None, commit)
    elif name.startswith(prefix):
        start = len(prefix)
        end = name.find('/', start+1)
        number = name[start:end]
        description = name[end+1:]
        try:
            number = int(number)
            return GitManagedBranch(git_repository, description, number, commit)
        except ValueError:
            pass
    


class GitBranchABC(object):
    """
    Base class for git branches
    """

    def __init__(self, repository, branch_name, commit):
        self.repository = repository
        self.name = branch_name
        self._commit = commit

    @property 
    def ticket_string(self):
        raise NotImplementedError

    @property 
    def ticket_number(self):
        return None

    @property
    def full_branch_name(self):
        """
        The branch name in the git repository
        """
        return self.name

    def __repr__(self):
        return 'Git branch '+self.full_branch_name

    @property
    def commit(self):
        """
        Return the commit SHA-1

        EXAMPLES::

            sage: b = test.git_repo().current_branch()
            sage: b.commit    # random output
            '087e1fdd0fe6f4c596f5db22bc54567b032f5d2b'
        """
        if self._commit is None:
            sha1 = self.repository.git.show_ref(
                'refs/heads/'+self.full_branch_name, verify=True, hash=True)
            self._commit = GitCommit(self.repository, sha1)
        return self._commit

    def __hash__(self):
        key = (self.full_branch_name, self.commit.sha1)
        return hash(key)

    def __cmp__(self, other):
        c = cmp(type(self), type(other))
        if c != 0:
            return c
        self_key = (self.full_branch_name, self.commit.sha1)
        other_key = (other.full_branch_name, other.commit.sha1)
        return cmp(self_key, other_key)
        

class GitLocalBranch(GitBranchABC):
    """
    An ordinary local branch

    Not associated to a ticket or any trac ticket. Does 
    not start with ``sageui/``.
    """
    
    def __init__(self, repository, branch_name, commit=None):
        GitBranchABC.__init__(self, repository, branch_name, commit)

    @property 
    def ticket_string(self):
        return 'local'


class GitManagedBranch(GitBranchABC):
    """
    A branch that SageUI created for its own private use
    """
    
    def __init__(self, repository, branch_name, ticket_number, commit=None):
        GitBranchABC.__init__(self, repository, branch_name, commit)
        self._ticket_number = ticket_number

    @property 
    def ticket_string(self):
        if self.ticket_number is None:
            return 'none'
        else:
            return str(self.ticket_number)

    @property
    def ticket_number(self):
        return self._ticket_number

    @property
    def full_branch_name(self):
        prefix = self.repository.prefix
        number = self.ticket_string
        return '{0}{1}/{2}'.format(prefix, number, self.name)

