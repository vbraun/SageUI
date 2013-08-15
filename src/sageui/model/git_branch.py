"""
Branches in the Local Git Repository

In fact, a particular commit on a branch.

EXAMPLES::

    >>> repo.local_branches()
    [Git branch master, Git branch my_branch, Git branch sageui/1000/u/user/description, Git branch sageui/1001/u/alice/work, Git branch sageui/1001/u/bob/work, Git branch sageui/1002/public/anything, Git branch sageui/none/u/user/description]


"""


def GitBranch(git_repository, name, commit=None):
    """
    Construct a branch object given the name as a string
    """
    prefix = git_repository.prefix
    prefix_nonumber = git_repository.prefix_nonumber
    if '/' not in name:
        return GitLocalBranch(git_repository, name, commit)
    elif name.startswith(prefix_nonumber+'/'):
        description = name[len(prefix_nonumber)+1:]
        return GitManagedBranch(git_repository, description, commit, None)
    elif name.startswith(prefix+'/'):
        start = len(prefix) + 1
        end = name.find('/', start)
        number = name[start:end]
        description = name[end+1:]
        try:
            number = int(number)
            return GitManagedBranch(git_repository, description, commit, number)
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
    def full_branch_name(self):
        return self.name

    def __repr__(self):
        return 'Git branch '+self.full_branch_name

    @property
    def commit(self):
        """
        Return the commit SHA-1

        EXAMPLES::

            sage: b = repo.current_branch()
            sage: b.commit    # random output
            '087e1fdd0fe6f4c596f5db22bc54567b032f5d2b'
        """
        if self._commit is None:
            self._commit = self.repository.git.show_ref(
                'refs/heads/'+self.full_branch_name, verify=True, hash=True)
        return self._commit


class GitLocalBranch(GitBranchABC):
    """
    An ordinary local branch

    Not associated to a ticket or any trac ticket. Does 
    not start with ``sageui/``.
    """
    
    def __init__(self, repository, branch_name, commit):
        GitBranchABC.__init__(self, repository, branch_name, commit)

    @property 
    def ticket_string(self):
        return 'local'


class GitManagedBranch(GitBranchABC):
    """
    A branch that SageUI created for its own private use
    """
    
    def __init__(self, repository, branch_name, commit, ticket_number):
        GitBranchABC.__init__(self, repository, branch_name, commit)
        self.ticket_number = ticket_number

    @property 
    def ticket_string(self):
        if self.ticket_number is None:
            return 'none'
        else:
            return str(self.ticket_number)

    @property
    def full_branch_name(self):
        prefix = self.repository.prefix
        number = self.ticket_string
        return '{0}/{1}/{2}'.format(prefix, number, self.name)

