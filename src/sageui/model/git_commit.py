"""
Git Commit
"""


class GitCommit(object):
    
    def __init__(self, repository, commit_sha1, title=None):
        self.repository = repository
        self._sha1 = commit_sha1.strip()
        assert len(self._sha1) == 40
        self._title = title

    def __repr__(self):
        return 'Commit '+self.short_sha1

    @property
    def sha1(self):
        return self._sha1

    @property
    def short_sha1(self):
        return self._sha1[0:6]

    @property
    def title(self):
        return str(self._title)

    def __str__(self):
        return self._sha1

    def __hash__(self):
        return hash(self._sha1)

    def __cmp__(self, other):
        """
        EXAMPLES::

            sage: repo = test.git_repo()
            sage: assert 0 == repo.head.__cmp__(repo.base_commit)
            sage: assert 0 == cmp(*[repo.head._sha1, repo.base_commit._sha1])
            sage: assert 0 == cmp(*[repo.head, repo.base_commit])
            sage: assert 0 == cmp(repo.head, repo.base_commit)
        """
        return cmp(self._sha1, other._sha1)

    def get_history(self, limit=20):
        """
        Return the list of (direct and indirect) parent commits
        """
        master = self.repository.master.commit    # TODO
        result = []
        rev_list = self.repository.git.rev_list(
            self.sha1, '^'+master.sha1, format='oneline', max_count=limit)
        for line in rev_list.splitlines():
            sha1 = line[0:40]
            title = line[40:].strip()
            result.append(GitCommit(self.repository, sha1, title))
        result.append(master)
        return result
    
        
        
