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
    def _diff_commits(self):
        return [self.from_commit, self.to_commit]
