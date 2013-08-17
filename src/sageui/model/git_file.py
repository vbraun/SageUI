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
    
    def __init__(self, repository, lines_added, lines_subtracted, filename, commit, binary=False):
        self.binary = binary
        self.commit = commit
        self.added = lines_added
        self.subed = lines_subtracted
        super(GitFileCommitted, self).__init__(repository, filename)
        
    @property
    def type(self):
        return 'diff'
    
    def __repr__(self):
        if self.binary:
            return self.type + ':' + self.name
        else:
            return self.type + ':+' + str(self.added) + '-' + str(self.subed) + ':' + self.name
            
    def _diff_commits(self):
        return [self.commit]

    def diff(self, algorithm='minimal'):
        """
        Return the diff from `self.commit`

        INPUT:

        - ``algorithm`` -- string, one of ``patience``, ``minimal``, ``histogram``, 
          and ``myers``. The diff algorithm, see ``git help diff`` for details.

        OUTPUT:

        String

        EXAMPLES::

            sage: repo = test.new_git_repo() 
            sage: repo.base_commit = repo.head.get_history()[-1]
            sage: git_file = repo.changes()[3]
            sage: print git_file.diff()
            diff --git a/foo4.txt b/foo4.txt
            new file mode 100644
            index 0000000..a53e390
            --- /dev/null
            +++ b/foo4.txt
            @@ -0,0 +1,2 @@
            +456
            +another line
            <BLANKLINE>
        """
        if self.binary:
            raise ValueError('cannot diff binary files')
        args = self._diff_commits() + ['--diff-algorithm='+algorithm, '--', self.name]
        return self.repository.git.diff(*args)

    def word_diff(self):
        """
        Return the word from ``self.commit``

        OUTPUT:

        String.

        EXAMPLES::

            sage: repo = test.new_git_repo() 
            sage: repo.base_commit = repo.head.get_history()[-1]
            sage: git_file = repo.changes()[3]
            sage: print git_file.word_diff()
            diff --git a/foo4.txt b/foo4.txt
            new file mode 100644
            index 0000000..a53e390
            --- /dev/null
            +++ b/foo4.txt
            @@ -0,0 +1,2 @@
            +456
            ~
            +another line
            ~
            <BLANKLINE>
        """
        if self.binary:
            raise ValueError('cannot diff binary files')
        args = self._diff_commits() + ['--word-diff=porcelain', '--', self.name]
        return self.repository.git.diff(*args)

    def commit_log(self, format='fuller'):
        """
        Return the log entry for ``self.commit``
        
        EXAMPLES::

            sage: repo = test.new_git_repo() 
            sage: repo.base_commit = repo.head.get_history()[-1]
            sage: git_file = repo.changes()[3]
            sage: print git_file.commit_log()
            commit ...
            Author:     ...
            AuthorDate: ...
            Commit:     ...
            CommitDate: ...
            <BLANKLINE>
                initial commit
            <BLANKLINE>
        """
        return self.repository.git.log(self.commit, format=format, max_count=1)


class GitFileDiff(GitFileCommitted):
    """
    Diff from/to for a file.
    """
    
    def __init__(self, repository, lines_added, lines_subtracted, filename, from_commit, to_commit, binary=False):
        self.added = lines_added
        self.subed = lines_subtracted
        self.from_commit = from_commit
        self.to_commit = to_commit
        super(GitFileDiff, self).__init__(repository, lines_added, lines_subtracted, filename, 
                                          from_commit, binary=binary)
        
    def _diff_commits(self):
        return [self.from_commit, self.to_commit]

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
    



