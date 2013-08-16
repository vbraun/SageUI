#!/usr/bin/env python

import doctest
import sys
import os 
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
    


def test_git_model():
    testmod('sageui.model.git_error')
    from sageui.test.test_builder import TestBuilder
    test = TestBuilder()
    testmod('sageui.model.git_commit', globs={'test':test})
    testmod('sageui.model.git_branch', globs={'test':test})
    testmod('sageui.model.git_repository', globs={'test':test})
    #repo = sageui.model.git_repository.GitRepository(repo_path, verbose=True)
    #repo.git._user_email_set = False
    #testmod('sageui.model.git_interface', globs={'git':repo.git})


def run_doctests():
    test_trac_model()
    test_git_model()

if __name__ == '__main__':
    run_doctests()

