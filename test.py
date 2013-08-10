#!/usr/bin/env python

import doctest
import sys
import os

sys.path.append('src')


def test_trac_model():
    import sageui.model.trac_ticket
    import sageui.model.trac_database
    import sageui.model.trac_interface
    doctest.testmod(sageui.model.trac_ticket)
    doctest.testmod(sageui.model.trac_database)
    doctest.testmod(sageui.model.trac_interface)
    


def run_doctests():
    test_trac_model()


if __name__ == '__main__':
    run_doctests()

