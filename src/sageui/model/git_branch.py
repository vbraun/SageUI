
class GitBranchABC(object):

    def __init__(self, repository, branch_name):
        self.repository = repository
        self.name = branch_name

    @property 
    def ticket_string(self):
        raise NotImplementedError

    @property
    def full_branch_name(self):
        return self.name

    @property
    def commit(self):
        return '72f6b86f1afc47b6a94ee5aa621839ec390fdc3c'


class GitLocalBranch(GitBranchABC):
    
    def __init__(self, repository, branch_name):
        GitBranchABC.__init__(self, repository, branch_name)

    @property 
    def ticket_string(self):
        return 'local'


class GitManagedBranch(GitBranchABC):
    
    def __init__(self, repository, branch_name, ticket_number):
        GitBranchABC.__init__(self, repository, branch_name)
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

