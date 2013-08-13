#!/usr/bin/env python

import doctest
import sys
import os
import tempfile
import shutil
import subprocess
import logging

sys.path.append(os.path.join(os.getcwd(), 'src'))


def test_trac_model():
    import sageui.model.trac_ticket
    import sageui.model.trac_database
    import sageui.model.trac_server
    doctest.testmod(sageui.model.trac_ticket)
    doctest.testmod(sageui.model.trac_database)
    doctest.testmod(sageui.model.trac_server)
    

POPULATE_GIT_REPO = """
git init .
echo '123' > foo.txt
git add .
git commit -m 'initial commit'
git checkout -q -b 'my_branch'
git checkout -q -b 'sageui/none/u/user/description'
git checkout -q -b 'sageui/1000/u/user/description'
git checkout -q -b 'sageui/1001/u/bob/work'
git checkout -q -b 'sageui/1001/u/alice/work'
git checkout -q -b 'sageui/1002/public/anything'
touch untracked
"""

def make_test_git_repo(temp_dir):
    try:
        cwd = os.getcwd()
        os.chdir(temp_dir)
        for line in POPULATE_GIT_REPO.splitlines():
            # print 'Executing', line
            subprocess.check_output(line, shell=True)
    finally:
        os.chdir(cwd)

class MultiLineFormatter(logging.Formatter):
    def format(self, record):
        str = logging.Formatter.format(self, record)
        header, footer = str.split(record.message)
        str = str.replace('\n', '\n' + ' '*len(header))
        return str
        
def test_git_model():
    import sageui.model.git_branch
    import sageui.model.git_repository
    import sageui.model.git_interface
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(MultiLineFormatter('%(name)s:%(levelname)s %(message)s'))
    sageui.model.git_interface.log.addHandler(handler)
    sageui.model.git_interface.log.setLevel(logging.DEBUG)
    try:
        temp_dir = tempfile.mkdtemp()
        make_test_git_repo(temp_dir)
        git_repo = sageui.model.git_repository.GitRepository(temp_dir)
        doctest.testmod(sageui.model.git_branch, globs={'git':git_repo})
        doctest.testmod(sageui.model.git_repository, globs={'git':git_repo})
        doctest.testmod(sageui.model.git_interface, globs={'git':git_repo.git})
    finally:
        shutil.rmtree(temp_dir)


def run_doctests():
    test_trac_model()
    test_git_model()

if __name__ == '__main__':
    run_doctests()

