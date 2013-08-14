"""
Branches in the Local Git Repository

In fact, a particular commit on a branch.

EXAMPLES::

    >>> repo.local_branches()
    [Git branch master, Git branch my_branch, Git branch sageui/1000/u/user/description, Git branch sageui/1001/u/alice/work, Git branch sageui/1001/u/bob/work, Git branch sageui/1002/public/anything, Git branch sageui/none/u/user/description]


"""


    


class GitBranchABC(object):
    """
    Base class for git branches
    """

    def __init__(self, repository, branch_name, commit):
        self.repository = repository
        self.name = branch_name
        self.commit = commit

    @property 
    def ticket_string(self):
        raise NotImplementedError

    @property
    def full_branch_name(self):
        return self.name

    def __repr__(self):
        return 'Git branch '+self.full_branch_name


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

