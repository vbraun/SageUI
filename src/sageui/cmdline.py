"""
Handle Command Line Options and Launch the Sage UI
"""

import sys
import os
import importlib

def check_gui_prerequisites():
    try:
        import gtk
    except ImportError:
        print 'Fatal: You need the Python GTK interface!'
        sys.exit(1)
    try:
        import pygtk
        pygtk.require('2.0')
    except ImportError:
        print 'Fatal: You need PyGTK version 2 or higher!'
        sys.exit(1)
    try:
        import gtk.glade
    except ImportError:
        print 'Fatal: You need the Python Glade interface!'
        sys.exit(1)
    try:
        import cairo
    except ImportError:
        print 'Fatal: You need the Python Cairo interface!'
        sys.exit(1)
    try: 
        import vte
    except ImportError:
        print 'Fatal: You need VTE!'
        sys.exit(1)


def debug_shell(app):
    from IPython.lib.inputhook import enable_gtk
    enable_gtk()
    from IPython.frontend.terminal.ipapp import TerminalIPythonApp
    ip = TerminalIPythonApp.instance()
    ip.initialize(argv=[])
    ip.shell.enable_gui('gtk')
    ip.shell.user_global_ns['app'] = app
    ip.shell.user_global_ns['repo'] = app.model.repo
    ip.shell.user_global_ns['git'] = app.model.repo.git
    def ipy_import(module_name, identifier):
        module = importlib.import_module(module_name)
        ip.shell.user_global_ns[identifier] = getattr(module, identifier) 
    ipy_import('sageui.model.git_interface', 'GitInterface')
    ipy_import('sageui.model.git_repository', 'GitRepository')
    ip.start()


def launch_gui(debug=False):
    check_gui_prerequisites()
    from sageui.app import Application
    app = Application()
    if debug:
        debug_shell(app)
    else:
        import gtk
        gtk.main()



description = """
    The Sage UI ..."""


def run_doctests(args):
    from sage.doctest.control import DocTestController
    DC = DocTestController(*args)
    err = DC.run()
    sys.exit(err)


def launch():
    from argparse import ArgumentParser
    parser = ArgumentParser(description=description)
    parser.add_argument('--debug', dest='debug', action='store_true',
                        default=False, 
                        help='debug')
    parser.add_argument('--doctest', dest='doctest', action='store_true',
                        default=False, 
                        help='doctest')
    args = parser.parse_args()
    if args.doctest:
        run_doctests(args)
    else:
        launch_gui(debug=args.debug)
