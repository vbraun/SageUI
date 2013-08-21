#!/usr/bin/env python3

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


import doctest
import sys
import os 
import logging
import importlib

sys.path.append(os.path.join(os.getcwd(), 'src'))

from sageui.test.doctest_parser import SageDocTestParser, SageOutputChecker

def testmod(module, verbose=False, globs={}):
    if isinstance(module, str):
        module = importlib.import_module(module)
    parser = SageDocTestParser(long=True, optional_tags=('sage',))
    finder = doctest.DocTestFinder(parser=parser)
    checker = SageOutputChecker()
    opts = doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS
    runner = doctest.DocTestRunner(checker=checker, optionflags=opts, verbose=verbose)
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
    testmod('sageui.model.git_interface', globs={'test':test, 'git':test.new_git_repo(verbose=True).git})
    testmod('sageui.model.git_file', globs={'test':test})
    testmod('sageui.model.git_commit', globs={'test':test})
    testmod('sageui.model.git_branch', globs={'test':test})
    testmod('sageui.model.git_repository', globs={'test':test})
    #repo = sageui.model.git_repository.GitRepository(repo_path, verbose=True)
    #repo.git._user_email_set = False
    #testmod('sageui.model.git_interface', globs={'git':repo.git})


def run_doctests():
    testmod('sageui.test.doctest_parser')    
    test_trac_model()
    test_git_model()

if __name__ == '__main__':
    run_doctests()

