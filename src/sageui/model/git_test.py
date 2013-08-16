"""
Build a new git repo for doctests
"""

POPULATE_GIT_REPO = """
git init .
echo '123' > foo1.txt && git add . && git commit -m 'initial commit'
git checkout -q -b 'my_branch'
echo '234' > foo2.txt && git add . && git commit -m 'second commit'
git checkout -q -b 'sageui/none/u/user/description'
echo '345' > foo3.txt
mv foo2.txt foo2_moved.txt 
git add --all
git commit -m 'third commit'
git checkout -q -b 'sageui/1000/u/user/description'
echo '456' > foo4.txt && git add . && git commit -m 'fourth commit'
git checkout -q -b 'sageui/1001/u/bob/work'
echo '567' > foo5.txt && git add . && git commit -m 'fifth commit'
git checkout -q -b 'sageui/1001/u/alice/work'
mkdir 'bar' && echo '678' > bar/foo6.txt && git add bar && git commit -m 'sixth commit'
git checkout -q -b 'sageui/1002/public/anything'
touch staged_file && git add staged_file
echo 'another line' >> foo4.txt
touch untracked_file
"""

import os
import tempfile
import shutil
import atexit
import subprocess

temp_dirs = []

@atexit.register
def delete_temp_dirs():
    global temp_dirs
    for temp_dir in temp_dirs:
        # print 'deleting '+temp_dir
        shutil.rmtree(temp_dir)


class TestBuilderGit(object):
    
    def new_git_repo(self, verbose=False, user_email_set=True):
        """
        Return a newly populated git repository
        """
        temp_dir = tempfile.mkdtemp()
        global temp_dirs
        temp_dirs.append(temp_dir)
        repo_path = os.path.join(temp_dir, 'git_repo')
        try:
            cwd = os.getcwd()
            os.mkdir(repo_path)
            os.chdir(repo_path)
            for line in POPULATE_GIT_REPO.splitlines():
                # print 'Executing', line
                subprocess.check_output(line, shell=True)
        finally:
            os.chdir(cwd)
        from git_repository import GitRepository
        repo = GitRepository(repo_path, verbose=verbose)
        repo.git._user_email_set = user_email_set
        return repo

    def git_repo(self):
        """
        Return a cached git repository.

        For doctests that modify the git repo you shoud use :meth:`new_git_repo`.
        """
        try:
            return self._git_repo
        except AttributeError:
            self._git_repo = self.new_git_repo()
            return self._git_repo
    
