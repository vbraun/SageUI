#!/usr/bin/env python

import doctest
import sys
import os
import tempfile
import shutil
import subprocess
import logging
import importlib

sys.path.append(os.path.join(os.getcwd(), 'src'))

from sageui.test.doctest_parser import SageDocTestParser, SageOutputChecker

def testmod(module, globs={}):
    if isinstance(module, basestring):
        module = importlib.import_module(module)
    parser = SageDocTestParser(long=True, optional_tags=('sage',))
    finder = doctest.DocTestFinder(parser=parser)
    checker = SageOutputChecker()
    opts = doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS
    runner = doctest.DocTestRunner(checker=checker, optionflags=opts)
    for test in finder.find(module):
        test.globs.update(globs)
        runner.run(test)

testmod('sageui.test.doctest_parser')
 

def test_trac_model():
    testmod('sageui.model.trac_ticket')
    testmod('sageui.model.trac_database')
    testmod('sageui.model.trac_server')
    

POPULATE_GIT_REPO = """
git init .
echo '123' > foo1.txt && git add . && git commit -m 'initial commit'
git checkout -q -b 'my_branch'
echo '234' > foo2.txt && git add . && git commit -m 'second commit'
git checkout -q -b 'sageui/none/u/user/description'
echo '345' > foo3.txt && git add . && git commit -m 'third commit'
git checkout -q -b 'sageui/1000/u/user/description'
echo '456' > foo4.txt && git add . && git commit -m 'fourth commit'
git checkout -q -b 'sageui/1001/u/bob/work'
echo '567' > foo5.txt && git add . && git commit -m 'fifth commit'
git checkout -q -b 'sageui/1001/u/alice/work'
echo '678' > foo6.txt && git add . && git commit -m 'sixth commit'
git checkout -q -b 'sageui/1002/public/anything'
touch untracked
"""

def make_test_git_repo(temp_dir):
    try:
        cwd = os.getcwd()
        os.mkdir(temp_dir)
        os.chdir(temp_dir)
        for line in POPULATE_GIT_REPO.splitlines():
            # print 'Executing', line
            subprocess.check_output(line, shell=True)
    finally:
        os.chdir(cwd)

def test_git_model():
    testmod('sageui.model.git_error')
    import sageui.model.git_repository
    temp_dir = tempfile.mkdtemp()
    repo_path = os.path.join(temp_dir, 'git_repo')
    try:
        make_test_git_repo(repo_path)
        repo = sageui.model.git_repository.GitRepository(repo_path)
        repo.git._user_email_set = True
        testmod('sageui.model.git_branch', globs={'repo':repo})
        testmod('sageui.model.git_repository', globs={'repo':repo})
        repo = sageui.model.git_repository.GitRepository(repo_path, verbose=True)
        repo.git._user_email_set = False
        #testmod('sageui.model.git_interface', globs={'git':repo.git})
    finally:
        shutil.rmtree(temp_dir)


def run_doctests():
    test_trac_model()
    test_git_model()

if __name__ == '__main__':
    run_doctests()

