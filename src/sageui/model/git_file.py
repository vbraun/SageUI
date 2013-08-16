"""
Diffs for Files in the Git Working Tree

"""


class GitFileABC(object):

    def __init__(self, repository, filename):
        self.repository = repository
        self._filename = filename

    @property
    def type(self):
        """
        Return a short string to destribe the type of GitFile.
        """
        raise NotImplementedError

    @property
    def name(self):
        """
        The file name and path relative to the repository root
        """
        return self._filename

    def __repr__(self):
        return self.type + ':' + self.name

    


class GitFileCommitted(GitFileABC):
    """
    Diff for a file with committed changes.

    Obviously, this is only possible if the file is
    under version control already.
    """
    
    def __init__(self, repository, lines_added, lines_subtracted, filename, commit):
        self.commit = commit
        self.added = lines_added
        self.subed = lines_subtracted
        super(GitFileCommitted, self).__init__(repository, filename)
        
    @property
    def type(self):
        return 'diff'
    
    def __repr__(self):
        return self.type + ':+' + str(self.added) + '-' + str(self.subed) + ':' + self.name


class GitFileDiff(GitFileCommitted):
    """
    Diff from/to for a file.
    """
    
    def __init__(self, repository, lines_added, lines_subtracted, filename, from_commit, to_commit):
        self.added = lines_added
        self.subed = lines_subtracted
        self.from_commit = from_commit
        self.to_commit = to_commit
        super(GitFileDiff, self).__init__(repository, lines_added, lines_subtracted, filename, from_commit)
        
    @property
    def type(self):
        return 'diff_index'


class GitFileUntracked(GitFileABC):
    
    @property
    def type(self):
        return 'untracked'
    

class GitFileUnstaged(GitFileCommitted):
    
    @property
    def type(self):
        return 'unstaged'
    

class GitFileStaged(GitFileCommitted):
    
    @property
    def type(self):
        return 'staged'
    

