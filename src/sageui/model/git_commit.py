"""
Git Commit
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

from functools import total_ordering

@total_ordering
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

    def __eq__(self, other):
        """
        EXAMPLES::

            sage: repo = test.git_repo()
            sage: assert repo.head.__eq__(repo.base_commit)
        """
        return (self._sha1 == other._sha1)

    def __lt__(self, other):
        """
        EXAMPLES::

            sage: repo = test.git_repo()
            sage: assert not repo.head.__lt__(repo.base_commit)
        """
        return (self._sha1 < other._sha1)
       
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
        
    def get_message(self, format='fuller'):
        """
        Return the log entry for the commit
        
        EXAMPLES::

            sage: repo = test.git_repo() 
            sage: commit = repo.head.get_history()[-1]
            sage: print(commit.get_message())
            commit ...
            Author:     ...
            AuthorDate: ...
            Commit:     ...
            CommitDate: ...
            <BLANKLINE>
                initial commit
            <BLANKLINE>
        """
        return self.repository.git.log(self.sha1, format=format, max_count=1)

        
